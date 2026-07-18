import json
from pathlib import Path

import pytest

from app.discovery.last30days_adapter import (
    Last30DaysAdapter,
    Last30DaysOutputError,
)


@pytest.fixture
def adapter(tmp_path: Path) -> Last30DaysAdapter:
    return Last30DaysAdapter(
        repo_path=tmp_path,
        python_executable="python312",
        timeout_seconds=12,
    )


@pytest.fixture
def valid_payload() -> dict:
    return {
        "schema_version": "1.2",
        "query": "inversion regenerativa",
        "generated_at": "2026-07-18T12:00:00Z",
        "window_days": 30,
        "source_status": {"reddit": "ok"},
        "freshness_verdicts": [],
        "clusters": [
            {
                "title": "Inversion de largo plazo",
                "summary": "Conversaciones sobre patrimonio y comunidad.",
                "sources": ["reddit"],
                "engagement_total": 42,
            }
        ],
        "results": [
            {
                "candidate_id": "reddit:abc123",
                "title": "Busco proyectos regenerativos",
                "source": "reddit",
                "url": "https://reddit.com/r/example/comments/abc123",
                "published_at": "2026-07-17T10:00:00Z",
                "summary": "Busco una inversion de largo plazo con impacto comunitario.",
                "engagement": {"score": 42},
                "relevance_score": 0.91,
                "cluster": 0,
            }
        ],
    }


def test_build_command_is_argument_list_without_shell(adapter: Last30DaysAdapter, tmp_path: Path):
    command = adapter.build_command(
        " inversion regenerativa ",
        save_dir=tmp_path / "run",
        search_sources=["reddit", "hackernews"],
        quick=True,
    )

    assert command[0] == "python312"
    assert command[2] == "inversion regenerativa"
    assert "--emit=json" in command
    assert "--json-profile=agent" in command
    assert "--search=reddit,hackernews" in command
    assert "--quick" in command


def test_parse_and_normalize_agent_export(
    adapter: Last30DaysAdapter,
    valid_payload: dict,
):
    export = adapter.parse_output(
        json.dumps(valid_payload),
        requested_query="inversion regenerativa",
    )
    results = adapter.normalize(export)

    assert len(results) == 1
    result = results[0]
    assert result.source == "reddit"
    assert result.external_id == "reddit:abc123"
    assert str(result.conversation_url).startswith("https://reddit.com/")
    assert result.author_name is None
    assert result.text.startswith("Busco una inversion")
    assert result.context == "Conversaciones sobre patrimonio y comunidad."
    assert result.query_origin == "inversion regenerativa"
    assert result.engagement == {"score": 42}


def test_normalize_deduplicates_same_source_and_candidate(
    adapter: Last30DaysAdapter,
    valid_payload: dict,
):
    valid_payload["results"].append(dict(valid_payload["results"][0]))
    export = adapter.parse_output(
        json.dumps(valid_payload),
        requested_query="inversion regenerativa",
    )

    assert len(adapter.normalize(export)) == 1


def test_empty_results_are_valid(adapter: Last30DaysAdapter, valid_payload: dict):
    valid_payload["results"] = []
    export = adapter.parse_output(
        json.dumps(valid_payload),
        requested_query="inversion regenerativa",
    )

    assert adapter.normalize(export) == []
    assert export.source_status == {"reddit": "ok"}


@pytest.mark.parametrize(
    "mutation",
    [
        lambda payload: payload.update(schema_version="2.0"),
        lambda payload: payload["results"][0].update(url="not-a-url"),
        lambda payload: payload["results"][0].update(summary=""),
    ],
)
def test_invalid_contract_is_rejected(
    adapter: Last30DaysAdapter,
    valid_payload: dict,
    mutation,
):
    mutation(valid_payload)

    with pytest.raises(Last30DaysOutputError):
        adapter.parse_output(
            json.dumps(valid_payload),
            requested_query="inversion regenerativa",
        )


def test_query_mismatch_is_rejected(adapter: Last30DaysAdapter, valid_payload: dict):
    with pytest.raises(Last30DaysOutputError, match="query mismatch"):
        adapter.parse_output(
            json.dumps(valid_payload),
            requested_query="otra consulta",
        )


def test_invalid_json_is_rejected(adapter: Last30DaysAdapter):
    with pytest.raises(Last30DaysOutputError, match="not valid JSON"):
        adapter.parse_output("not json", requested_query="consulta")


def test_search_returns_trace_and_source_status(
    adapter: Last30DaysAdapter,
    valid_payload: dict,
    tmp_path: Path,
    monkeypatch,
):
    adapter.entrypoint.parent.mkdir(parents=True, exist_ok=True)
    adapter.entrypoint.write_text("# fixture entrypoint", encoding="utf-8")

    class Completed:
        returncode = 0
        stdout = json.dumps(valid_payload)
        stderr = "source warning"

    monkeypatch.setattr("subprocess.run", lambda *args, **kwargs: Completed())

    result = adapter.search(
        "inversion regenerativa",
        save_dir=tmp_path / "run",
        search_sources=["reddit"],
        quick=True,
    )

    assert len(result.conversations) == 1
    assert result.export.source_status == {"reddit": "ok"}
    assert result.trace.return_code == 0
    assert result.trace.stderr == "source warning"
    assert result.trace.duration_seconds >= 0
    assert "--emit=json" in result.trace.command
