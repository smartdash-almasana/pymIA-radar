import json
from pathlib import Path

from app.schemas.assessment_v3 import SCHEMA_VERSION_V3


def test_lab_experiment_records_traceability_without_external_calls(monkeypatch, tmp_path) -> None:
    import httpx

    import app.lab_service as lab_service

    root = tmp_path
    lab_dir = root / "lab"
    corpus_path = lab_dir / "corpus" / "semantic_lab_corpus.v1.json"
    corpus_path.parent.mkdir(parents=True)
    corpus_path.write_text(
        json.dumps(
            {
                "schema_version": "radar-lab-corpus/v1",
                "cases": [
                    {"case_id": "CASE_001", "text": "External corpus sentence one."},
                    {"case_id": "CASE_002", "text": "External corpus sentence two."},
                ],
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(lab_service, "ROOT_DIR", root)
    monkeypatch.setattr(lab_service, "LAB_DIR", lab_dir)
    monkeypatch.setattr(lab_service, "LAB_CORPUS_PATH", corpus_path)
    monkeypatch.setattr(lab_service.settings, "semantic_llm_model", "agnes-test")
    monkeypatch.setattr(lab_service.settings, "semantic_llm_base_url", "https://agnes.example/v1")
    monkeypatch.setattr(lab_service.settings, "semantic_llm_api_key", "secret")
    monkeypatch.setattr(lab_service.settings, "gemini_model", "gemma-test")
    monkeypatch.setattr(lab_service.settings, "gemini_base_url", "https://gemma.example/v1")
    monkeypatch.setattr(lab_service.settings, "gemini_api_key", "secret")

    class FakeResponse:
        status_code = 200
        text = "ok"

        def __init__(self, body: dict):
            self._body = body

        def json(self):
            return self._body

    def fake_post(url, *, headers, json, timeout):
        user_content = json["messages"][1]["content"]
        text = user_content.split("[TEXT]\n", 1)[1].split("\n\n", 1)[0]
        draft = {
            "schema_version": SCHEMA_VERSION_V3,
            "real_topic": "Test topic",
            "contextual_meaning": "Test meaning",
            "apparent_affinity": "NONE",
            "apparent_affinity_domains": [],
            "apparent_intention": "NONE",
            "intention_summary": "No apparent intention.",
            "evidence_fragments": [text],
            "contradictions": [],
            "missing_context": [],
            "false_positive_risk": "LOW",
            "uncertainty": "LOW",
            "human_review_reason": "Human review remains required.",
        }
        return FakeResponse({"choices": [{"message": {"content": json_module.dumps(draft)}}]})

    json_module = json
    monkeypatch.setattr(httpx, "post", fake_post)

    result = lab_service.run_comparison_experiment(
        source="corpus",
        case_ids=["CASE_001", "CASE_002"],
        providers=["agnes", "gemma"],
        repetitions=1,
        experiment_id="experimento1",
    )

    assert result["total_calls"] == 4
    assert (lab_dir / "experimento1.md").exists()
    required = {
        "experiment_id",
        "case_id",
        "input_text",
        "provider",
        "model",
        "repetition",
        "prompt_version",
        "started_at",
        "finished_at",
        "latency_ms",
        "raw_output",
        "parsed_output",
        "error",
        "fallback_used",
        "status",
    }
    for record in result["records"]:
        assert required <= set(record)
        assert record["fallback_used"] is False
        assert record["input_text"].startswith("External corpus sentence")
        assert record["parsed_output"]


def test_lab_experiment_captures_provider_errors_without_fallback(monkeypatch, tmp_path) -> None:
    import httpx

    import app.lab_service as lab_service

    root = tmp_path
    lab_dir = root / "lab"
    corpus_path = lab_dir / "corpus" / "semantic_lab_corpus.v1.json"
    corpus_path.parent.mkdir(parents=True)
    corpus_path.write_text(
        json.dumps(
            {
                "schema_version": "radar-lab-corpus/v1",
                "cases": [{"case_id": "CASE_001", "text": "External corpus sentence."}],
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(lab_service, "ROOT_DIR", root)
    monkeypatch.setattr(lab_service, "LAB_DIR", lab_dir)
    monkeypatch.setattr(lab_service, "LAB_CORPUS_PATH", corpus_path)
    monkeypatch.setattr(lab_service.settings, "semantic_llm_model", "agnes-test")
    monkeypatch.setattr(lab_service.settings, "semantic_llm_base_url", "https://agnes.example/v1")
    monkeypatch.setattr(lab_service.settings, "semantic_llm_api_key", "secret")

    def fake_post(*args, **kwargs):
        raise httpx.ConnectError("boom")

    monkeypatch.setattr(httpx, "post", fake_post)

    result = lab_service.run_comparison_experiment(
        source="corpus",
        case_ids=["CASE_001"],
        providers=["agnes"],
        repetitions=1,
        experiment_id="experimento1",
    )

    [record] = result["records"]
    assert record["error"] == "SEMANTIC_PROVIDER_UNAVAILABLE"
    assert record["fallback_used"] is False
    assert record["status"] == "SEMANTIC_ASSESSMENT_UNAVAILABLE"
    assert record["raw_output"]
