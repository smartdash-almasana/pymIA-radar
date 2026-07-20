from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
LAB_SOURCE_PATHS = [
    ROOT / "app" / "templates" / "lab.txt",
    ROOT / "app" / "static" / "lab.js.txt",
    ROOT / "app" / "lab_service.py",
    ROOT / "app" / "api" / "routes.py",
]
LAB_CORPUS_PATH = ROOT / "lab" / "corpus" / "semantic_lab_corpus.v1.json"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_lab_screen_and_assets_are_available() -> None:
    from fastapi.testclient import TestClient

    from app.main import app

    with TestClient(app) as client:
        page = client.get("/lab")
        assert page.status_code == 200
        assert "Laboratorio experimental neutral" in page.text
        assert "Ejecutar smoke reducido" in page.text
        assert "Ejecuta 10 conversaciones" not in page.text
        assert "60 evaluaciones" not in page.text

        stylesheet = client.get("/static/lab.css")
        assert stylesheet.status_code == 200
        assert stylesheet.headers["content-type"].startswith("text/css")

        script = client.get("/static/lab.js")
        assert script.status_code == 200
        assert "/api/lab/cases" in script.text
        assert "/api/lab/experiments" in script.text
        assert "Guardado:" in script.text


def test_lab_case_api_exposes_only_neutral_ids() -> None:
    from fastapi.testclient import TestClient

    from app.main import app

    corpus = json.loads(LAB_CORPUS_PATH.read_text(encoding="utf-8"))
    corpus_texts = [item["text"] for item in corpus["cases"]]

    with TestClient(app) as client:
        response = client.get("/api/lab/cases")

    assert response.status_code == 200
    assert response.json()
    assert all(sorted(item) == ["case_id"] for item in response.json())
    assert all(item["case_id"].startswith("CASE_") for item in response.json())
    serialized = response.text
    for phrase in corpus_texts:
        assert phrase not in serialized


def test_lab_sources_do_not_embed_corpus_phrases() -> None:
    corpus = json.loads(LAB_CORPUS_PATH.read_text(encoding="utf-8"))
    forbidden_phrases = {item["text"] for item in corpus["cases"]}
    for path in LAB_SOURCE_PATHS:
        content = _read(path)
        for phrase in forbidden_phrases:
            assert phrase not in content, f"{path} embeds corpus phrase: {phrase}"


def test_lab_service_does_not_pull_operational_conversations() -> None:
    forbidden = [
        "select(Conversation)",
        "conversation_limit",
        "order_by(Conversation.id",
        "Ejecuta 10 conversaciones",
        "60 evaluaciones",
    ]
    content = _read(ROOT / "app" / "lab_service.py")
    for fragment in forbidden:
        assert fragment not in content, f"lab_service.py contains forbidden fragment: {fragment}"


def test_lab_routes_require_explicit_payload() -> None:
    content = _read(ROOT / "app" / "api" / "routes.py")
    assert "payload: LabExperimentRequest" in content
    assert "run_comparison_experiment(db)" not in content
