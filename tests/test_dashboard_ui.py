import shutil
import subprocess

import pytest
from fastapi.testclient import TestClient

from app.main import app


def test_dashboard_is_a_single_conversation_review_screen() -> None:
    with TestClient(app) as client:
        dashboard = client.get("/")
        assert dashboard.status_code == 200
        assert dashboard.headers["content-type"].startswith("text/html")

        html = dashboard.text
        assert "Conversaciones encontradas" in html
        assert "conversationView" in html
        assert "conversationText" in html
        assert "originalLink" in html
        assert "progressText" in html
        assert "previousButton" in html
        assert "nextButton" in html

        assert html.count('class="decision-button ') == 3
        assert "No corresponde" in html
        assert "Dejar para más adelante" in html
        assert "Vale la pena acercarnos" in html

        assert "scanQuery" not in html
        assert "scanButton" not in html
        assert "conversationList" not in html
        assert "statusFilter" not in html
        assert "searchInput" not in html
        assert "languageSelector" not in html
        assert "assessmentView" not in html
        assert "discoveryPanel" not in html
        assert "outcomeForm" not in html
        assert "qualificationForm" not in html

        assert "Evaluación V3" not in html
        assert "afinidad aparente" not in html.lower()
        assert "precalificación" not in html.lower()
        assert "candidato" not in html.lower()


def test_dashboard_assets_use_the_verified_backend_without_exposing_it() -> None:
    with TestClient(app) as client:
        stylesheet = client.get("/static/radar.css")
        assert stylesheet.status_code == 200
        assert stylesheet.headers["content-type"].startswith("text/css")
        assert ".conversation-card" in stylesheet.text
        assert ".decision-buttons" in stylesheet.text
        assert ".reviewer-dialog" in stylesheet.text

        script = client.get("/static/radar.js")
        assert script.status_code == 200
        assert script.headers["content-type"].startswith("application/javascript")
        javascript = script.text

        assert "selectNextPendingAfter" in javascript
        assert "APPROVE_DISCOVERY_CONTACT" in javascript
        assert "/assessments/v3" in javascript
        assert "/api/discovery-candidates" in javascript
        assert "KEEP_OBSERVING" in javascript
        assert "DISCARD" in javascript

        assert "APPROVE_APPROACH" not in javascript
        assert "/api/discovery/search-queries" not in javascript
        assert "/api/discovery/scan" not in javascript
        assert "prequalification-invitation" not in javascript
        assert "prequalification-acceptance" not in javascript
        assert "/engagement-events" not in javascript
        assert "/qualifications" not in javascript


def test_dashboard_javascript_has_valid_syntax(tmp_path) -> None:
    node = shutil.which("node")
    if node is None:
        pytest.skip("Node.js is not installed")

    with TestClient(app) as client:
        script_text = client.get("/static/radar.js").text

    script_path = tmp_path / "radar.js"
    script_path.write_text(script_text, encoding="utf-8")
    result = subprocess.run(
        [node, "--check", str(script_path)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
