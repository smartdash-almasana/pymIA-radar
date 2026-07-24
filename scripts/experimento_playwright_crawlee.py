"""
Experimento v2 final: Playwright MCP vs Crawlee Python
Extraccion de fuente publica (Reddit) - 3 iteraciones cada enfoque
"""

import asyncio
import json
import os
import re
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Optional

TEST_URL = "https://www.reddit.com/r/intentionalcommunity/comments/1fu7tl6/seeking_cocreators_to_build_an_ecovillage_in/"
ITERATIONS = 3


@dataclass
class ExtractionResult:
    approach: str
    iteration: int
    success: bool
    duration_ms: float
    author: Optional[str] = None
    text_length: Optional[int] = None
    text_preview: Optional[str] = None
    url: Optional[str] = None
    error: Optional[str] = None
    error_type: Optional[str] = None
    extraction_quality: Optional[str] = None

    def to_dict(self):
        return asdict(self)


def _extract_author_re(text: str) -> Optional[str]:
    for pat in [r'(?:u|user)/([A-Za-z0-9_-]+)', r'author["\s:=]+([^\s",}]+)']:
        m = re.search(pat, text)
        if m:
            return m.group(1)
    return None


# ===========================================================================
# ENFOQUE A: Playwright MCP
# ===========================================================================

async def run_playwright_mcp(url: str, iteration: int) -> ExtractionResult:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    result = ExtractionResult(
        approach="playwright-mcp", iteration=iteration,
        success=False, duration_ms=0.0,
    )
    start = time.perf_counter()

    try:
        server_params = StdioServerParameters(command="npx", args=["@playwright/mcp"])
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                nav = await session.call_tool("browser_navigate", arguments={"url": url})
                if not nav or nav.isError:
                    raise RuntimeError("browser_navigate failed")
                await asyncio.sleep(3)

                # texto desde snapshot (browser_evaluate no funciona con mcp Python client)
                snap = await session.call_tool("browser_snapshot", arguments={})
                snap_text = ""
                if snap and not snap.isError and snap.content:
                    for c in snap.content:
                        if hasattr(c, "text") and c.text:
                            snap_text += c.text

                author = _extract_author_re(snap_text) or "<no_encontrado>"
                text_length = len(snap_text)
                text_preview = snap_text[:200].replace("\n", " ") if snap_text else None

                result.success = True
                result.author = author
                result.text_length = text_length
                result.text_preview = text_preview
                result.url = url
                result.extraction_quality = "COMPLETE" if author != "<no_encontrado>" and text_length > 100 else "PARTIAL" if text_length > 0 else "FAILED"

    except Exception as e:
        result.success = False
        result.error = str(e)
        result.error_type = type(e).__name__
        result.extraction_quality = "FAILED"

    result.duration_ms = (time.perf_counter() - start) * 1000
    return result


# ===========================================================================
# ENFOQUE B: Crawlee Python (PlaywrightCrawler - ejecuta JS)
# ===========================================================================

async def run_crawlee(url: str, iteration: int) -> ExtractionResult:
    from crawlee.crawlers import PlaywrightCrawler
    from crawlee.router import Router

    result = ExtractionResult(
        approach="crawlee", iteration=iteration,
        success=False, duration_ms=0.0,
    )
    start = time.perf_counter()

    try:
        extracted = {"author": None, "text": None}

        router = Router[PlaywrightCrawler]()

        @router.default_handler
        async def handler(context):
            page = context.page
            await page.wait_for_load_state("networkidle")

            # author via JS
            author = await page.evaluate("""
                (() => {
                    try {
                        let a = document.querySelector('shreddit-post');
                        if (a) return a.getAttribute('author');
                        let b = document.querySelector('a[data-testid="post_author_link"]');
                        if (b) {
                            let m = b.href.match(/\\/user\\/([^/]+)/);
                            return m ? m[1] : b.href;
                        }
                        return document.body.innerText.match(/(?:u|user)\\/([A-Za-z0-9_-]+)/)?.[1] || '';
                    } catch(e) { return ''; }
                })()
            """)
            extracted["author"] = (author or "").strip()

            # text
            text = await page.evaluate("""
                (() => {
                    try {
                        let s = document.querySelector('shreddit-post');
                        if (s) {
                            let c = s.querySelector('[slot="post-content"]');
                            if (c) return c.innerText;
                            return s.innerText;
                        }
                        return document.body.innerText || '';
                    } catch(e) { return ''; }
                })()
            """)
            extracted["text"] = (text or "").strip()

        crawler = PlaywrightCrawler(
            request_handler=router,
            max_requests_per_crawl=1,
            headless=True,
        )

        await crawler.run([url])

        author = extracted.get("author") or "<no_encontrado>"
        text = extracted.get("text") or ""
        text_length = len(text)
        text_preview = text[:200].replace("\n", " ") if text else None

        result.success = True
        result.author = author
        result.text_length = text_length
        result.text_preview = text_preview
        result.url = url
        result.extraction_quality = "COMPLETE" if author != "<no_encontrado>" and text_length > 100 else "PARTIAL" if text_length > 0 else "FAILED"

    except Exception as e:
        result.success = False
        result.error = str(e)
        result.error_type = type(e).__name__
        result.extraction_quality = "FAILED"

    result.duration_ms = (time.perf_counter() - start) * 1000
    return result


# ===========================================================================
# REPORTE
# ===========================================================================

def summarize(name: str, results: list[ExtractionResult]) -> dict:
    successes = [r for r in results if r.success]
    failures = [r for r in results if not r.success]
    quality = [r.extraction_quality or "FAILED" for r in results]
    durations = [r.duration_ms for r in results]

    return {
        "approach": name,
        "total": len(results),
        "successes": len(successes),
        "failures": len(failures),
        "success_rate": f"{len(successes)}/{len(results)}",
        "quality_distribution": {q: quality.count(q) for q in sorted(set(quality))},
        "duration_ms": {
            "mean": round(sum(durations) / len(durations), 1) if durations else 0,
            "min": round(min(durations), 1) if durations else 0,
            "max": round(max(durations), 1) if durations else 0,
            "total": round(sum(durations), 1),
            "all": [round(d, 1) for d in durations],
        },
        "errors": [
            {"iteration": r.iteration, "error_type": r.error_type, "error": (r.error or "")[:200]}
            for r in failures
        ],
        "extractions": [
            {
                "iteration": r.iteration, "success": r.success,
                "author": r.author, "text_length": r.text_length,
                "text_preview": r.text_preview, "quality": r.extraction_quality,
            }
            for r in results
        ],
    }


async def main():
    print("=" * 70)
    print("EXPERIMENTO v2: Playwright MCP vs Crawlee Python")
    print(f"URL: {TEST_URL}")
    print(f"Iteraciones: {ITERATIONS}")
    print(f"Inicio: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)

    all_results = []

    for i in range(1, ITERATIONS + 1):
        print(f"\n>> Playwright MCP - iteracion {i}/{ITERATIONS}")
        r = await run_playwright_mcp(TEST_URL, i)
        status = "OK" if r.success else "FAIL"
        print(f"  {status} {r.duration_ms:.0f}ms | autor={r.author} | text_len={r.text_length} | quality={r.extraction_quality}")
        if r.error:
            print(f"  error: {r.error[:120]}")
        all_results.append(r)

    for i in range(1, ITERATIONS + 1):
        print(f"\n>> Crawlee Python - iteracion {i}/{ITERATIONS}")
        r = await run_crawlee(TEST_URL, i)
        status = "OK" if r.success else "FAIL"
        print(f"  {status} {r.duration_ms:.0f}ms | autor={r.author} | text_len={r.text_length} | quality={r.extraction_quality}")
        if r.error:
            print(f"  error: {r.error[:120]}")
        all_results.append(r)

    pw = [r for r in all_results if r.approach == "playwright-mcp"]
    cr = [r for r in all_results if r.approach == "crawlee"]
    s_pw = summarize("playwright-mcp", pw)
    s_cr = summarize("crawlee", cr)

    print("\n\n" + "=" * 70)
    print("RESUMEN COMPARATIVO")
    print("=" * 70)
    for s in [s_pw, s_cr]:
        print(f"\n--- {s['approach']} ---")
        print(f"  Tasa de exito:     {s['success_rate']}")
        print(f"  Calidad:           {s['quality_distribution']}")
        print(f"  Duracion media:    {s['duration_ms']['mean']:.0f}ms")
        print(f"  Duracion total:    {s['duration_ms']['total']:.0f}ms")
        print(f"  Errores:           {len(s['errors'])}")
        for e in s["errors"]:
            print(f"    #{e['iteration']}: [{e['error_type']}] {e['error'][:100]}")

    out_dir = os.path.join(os.path.dirname(__file__), "..", ".tmp")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"reporte-playwright-vs-crawlee-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({
            "metadata": {
                "experiment": "Playwright MCP vs Crawlee Python",
                "url": TEST_URL,
                "iterations_per_approach": ITERATIONS,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "python_version": sys.version,
            },
            "playwright_mcp": s_pw,
            "crawlee": s_cr,
        }, f, indent=2, ensure_ascii=False)
    print(f"\nReporte JSON: {out_path}")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())