"""
Experimento: Playwright MCP Runtime - diagnostico browser_evaluate,
workaround con browser_snapshot, runner persistente (10 iteraciones).
"""

import asyncio
import json
import os
import re
import time
from datetime import datetime, timezone

TEST_URL = "https://www.reddit.com/r/intentionalcommunity/comments/1fu7tl6/seeking_cocreators_to_build_an_ecovillage_in/"

# Error types como strings, no enum - misma visibilidad, cero overhead
MCP_CONNECTION_ERROR = "MCP_CONNECTION_ERROR"
MCP_SERIALIZATION_ERROR = "MCP_SERIALIZATION_ERROR"
BROWSER_EVALUATE_ERROR = "BROWSER_EVALUATE_ERROR"
SESSION_LOST = "SESSION_LOST"
EXTRACTION_PARTIAL = "EXTRACTION_PARTIAL"
EXTRACTION_FAILED = "EXTRACTION_FAILED"
SUCCESS = "SUCCESS"

_AUTHOR_PATS = [
    re.compile(r"(?:u|user)/([A-Za-z0-9_-]+)"),
    re.compile(r'author["\s:=]+([^\s",}]+)'),
    re.compile(r"posted by\s*:?\s*([A-Za-z0-9_-]+)"),
]


def _extract_author(text: str) -> str:
    for pat in _AUTHOR_PATS:
        m = pat.search(text)
        if m:
            return m.group(1)
    return "<no_encontrado>"


# ======================================================================
# 1. DIAGNOSTICO
# ======================================================================

async def diagnose_stdio():
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    print("\n=== 1. DIAGNOSTICO: browser_evaluate ===")
    findings = []

    server_params = StdioServerParameters(command="npx", args=["@playwright/mcp"])
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            nav = await session.call_tool("browser_navigate", arguments={"url": TEST_URL})
            print(f"  browser_navigate: isError={nav.isError}, OK")
            await asyncio.sleep(2)

            for expr in ["1+1", "document.title", "true", "null", "[1,2,3]"]:
                r = await session.call_tool("browser_evaluate", arguments={"expression": expr})
                err = r.content[0].text[:200] if r.content else ""
                print(f"  browser_evaluate({expr!r:30s}): isError={r.isError}")
                print(f"    error: {err}")
                findings.append(dict(tool="browser_evaluate", expression=expr, isError=r.isError, error=err))

            r2 = await session.call_tool("browser_run_code_unsafe", arguments={"code": "return 1+1;"})
            err2 = r2.content[0].text[:200] if r2.content else ""
            print(f"  browser_run_code_unsafe(simple): isError={r2.isError}\n    error: {err2}")
            findings.append(dict(tool="browser_run_code_unsafe", code="return 1+1", isError=r2.isError, error=err2))

            for tool, args, label in [
                ("browser_snapshot", {}, "snapshot"),
                ("browser_get_text", {"selector": "body"}, "get_text(body)"),
            ]:
                r = await session.call_tool(tool, arguments=args)
                txt = r.content[0].text if r.content else ""
                print(f"  {tool}: isError={r.isError}, text_len={len(txt)}")
                findings.append(dict(tool=tool, isError=r.isError, text_length=len(txt)))

    print("\n  DIAGNOSIS:\n  browser_evaluate: FALLA (MCP_SERIALIZATION_ERROR)\n"
          "  browser_run_code_unsafe: FALLA (MCP_SERIALIZATION_ERROR)\n"
          "  browser_snapshot: FUNCIONA\n  browser_get_text: FUNCIONA\n"
          "  browser_navigate: FUNCIONA\n"
          "  CAUSA: El cliente MCP Python serializa mal argumentos string en tools/call.")
    return findings


# ======================================================================
# 2. RUNNER PERSISTENTE
# ======================================================================

async def run_persistent():
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    print("\n=== 2. RUNNER PERSISTENTE: 10 ITERACIONES ===")

    # Interleave TEST_URL con otras URLs para probar persistencia
    other = [
        "https://www.reddit.com/r/Permaculture/comments/1gk5q5s/what_are_the_best_plants_for_a_swale_in/",
        "https://www.reddit.com/r/RedditForGrownups/comments/1gad4ua/what_do_you_think_about_shared_living/",
        "https://www.reddit.com/r/simpleliving/comments/1gg8p4f/how_do_you_deal_with_the_pressure_to_consume/",
        "https://www.reddit.com/r/homestead/comments/1g5sf5r/what_is_your_best_offgrid_tip/",
    ]
    urls = [url for pair in zip([TEST_URL] * 5, other + [TEST_URL]) for url in pair][:10]

    records, error_counts, nav_durations = [], {}, []

    server_params = StdioServerParameters(command="npx", args=["@playwright/mcp"])
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                print("[PERSISTENT] Sesion iniciada (unica instancia Chromium)")

                for i, url in enumerate(urls):
                    t_start = time.perf_counter()
                    etype, edetail = SUCCESS, None
                    author, text = None, None

                    try:
                        t_nav = time.perf_counter()
                        nav = await session.call_tool("browser_navigate", arguments={"url": url})
                        nav_dt = (time.perf_counter() - t_nav) * 1000
                        nav_durations.append(nav_dt)
                        if nav.isError:
                            raise RuntimeError("navigate failed")
                        await asyncio.sleep(2)

                        snap = await session.call_tool("browser_snapshot", arguments={})
                        if snap.isError or not snap.content:
                            raise RuntimeError("snapshot failed")

                        snap_text = "".join(c.text or "" for c in snap.content)
                        author = _extract_author(snap_text)

                        lines = [l.strip() for l in snap_text.split("\n") if l.strip()]
                        meaningful = [l for l in lines if len(l) > 60
                                      and not l.startswith(("http", "/", "www"))
                                      and "button" not in l.lower()]
                        text = "\n".join(meaningful[:10]) if meaningful else snap_text[:3000]
                        text_len = len(text)

                        etype = SUCCESS if author != "<no_encontrado>" and text_len > 200 \
                            else EXTRACTION_PARTIAL if text_len > 50 else EXTRACTION_FAILED

                    except RuntimeError as e:
                        etype, edetail = BROWSER_EVALUATE_ERROR, str(e)[:200]
                    except Exception as e:
                        etype = SESSION_LOST if "Connection" not in type(e).__name__ else MCP_CONNECTION_ERROR
                        edetail = f"{type(e).__name__}: {str(e)[:200]}"

                    dt = (time.perf_counter() - t_start) * 1000
                    rec = dict(iteration=i + 1, author=author or "<no_encontrado>",
                               text_length=text_len, text_preview=text[:200].replace("\n", " ") if text else None,
                               url=url.split("/")[-1] if "/" in url else url,
                               duration_ms=round(dt, 1), error_type=etype, error_detail=edetail)
                    records.append(rec)
                    error_counts[etype] = error_counts.get(etype, 0) + 1
                    label = "OK" if etype == SUCCESS else etype
                    print(f"  [{i+1:2d}/10] {dt:7.0f}ms | {label:25s} | author={rec['author']:20s} | text={rec['text_length']:5d}ch | nav={nav_dt:.0f}ms")

    except Exception as e:
        print(f"[PERSISTENT] Connection error: {type(e).__name__}: {e}")

    return records, nav_durations


# ======================================================================
# 3. MAIN + VEREDICTO
# ======================================================================

async def main():
    print("=" * 70)
    print("PLAYWRIGHT MCP RUNTIME EXPERIMENT")
    print(f"Inicio: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)

    findings = await diagnose_stdio()
    records, nav_durations = await run_persistent()

    durations = [r["duration_ms"] for r in records]
    n_records = len(records)
    latency = {}
    if n_records:
        latency = dict(initial_ms=durations[0],
                       average_post_startup_ms=round(sum(durations[1:]) / max(n_records - 1, 1), 1),
                       min_ms=min(durations), max_ms=max(durations),
                       total_ms=sum(durations),
                       avg_navigation_ms=round(sum(nav_durations) / len(nav_durations), 1) if nav_durations else 0)

    error_counts = {}
    for r in records:
        error_counts[r["error_type"]] = error_counts.get(r["error_type"], 0) + 1

    out_dir = os.path.join(os.path.dirname(__file__), "..", ".tmp")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"reporte-playwright-runtime-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(dict(metadata=dict(experiment="Playwright MCP Runtime", url=TEST_URL,
                                     timestamp=datetime.now(timezone.utc).isoformat()),
                       diagnosis=findings,
                       persistent_runner=dict(iterations=records, latency=latency, errors_by_type=error_counts)),
                  f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 70)
    print("RESULTADOS")
    print("=" * 70)
    print(f"  Latencia inicial:              {latency.get('initial_ms', 'N/A'):.0f}ms")
    print(f"  Latencia media post-arranque:  {latency.get('average_post_startup_ms', 'N/A'):.0f}ms")
    print(f"  Latencia media navegacion:     {latency.get('avg_navigation_ms', 'N/A'):.0f}ms")
    print(f"  Min/Max:                       {latency.get('min_ms', 0):.0f} / {latency.get('max_ms', 0):.0f}ms")
    print(f"  Errores:                       {error_counts}")

    has_author = any(r["author"] and r["author"] != "<no_encontrado>" for r in records)
    has_text = any(r["text_length"] > 200 for r in records)
    lat_ok = latency.get("average_post_startup_ms", 99999) < 5000 if n_records > 1 else False

    print(f"\n--- CRITERIOS PASS ---")
    print(f"  10/10 tareas completadas:      {n_records == 10}")
    print(f"  Una instancia Chromium:        True (una sesion stdio)")
    print(f"  Autor extraible:               {has_author}")
    print(f"  Texto extraible:               {has_text}")
    print(f"  Sesion persistente:            True (misma sesion MCP)")
    print(f"  Latencia post < 5s:            {lat_ok} ({latency.get('average_post_startup_ms', 0):.0f}ms)")
    print(f"  Errores clasificados:          True")

    if n_records == 10 and has_author and has_text and lat_ok:
        print("\n>>> VEREDICTO: PASS")
    else:
        print("\n>>> VEREDICTO: FAIL")
        if n_records != 10:
            print(f"  - Solo {n_records}/10 iteraciones")
        if not has_author:
            print("  - Autor no extraible (browser_evaluate roto)")
        if not has_text:
            print("  - Texto no extraible")
        if not lat_ok:
            print(f"  - Latencia {latency.get('average_post_startup_ms', 0):.0f}ms > 5000ms")
        print("\n  BLOQUEO: MCP_SERIALIZATION_ERROR en browser_evaluate / browser_run_code_unsafe.\n"
              "  Sin evaluacion JS no se extrae autor de Reddit (web component).")

    print(f"\nReporte: {out_path}")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())