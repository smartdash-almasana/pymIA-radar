from fastapi.testclient import TestClient

from app.main import app


def test_dashboard_and_assets_are_served() -> None:
    with TestClient(app) as client:
        dashboard = client.get("/")
        assert dashboard.status_code == 200
        assert dashboard.headers["content-type"].startswith("text/html")
        assert "RADAR · Revisión humana" in dashboard.text
        assert "conversationList" in dashboard.text
        assert "qualificationForm" in dashboard.text

        stylesheet = client.get("/static/radar.css")
        assert stylesheet.status_code == 200
        assert stylesheet.headers["content-type"].startswith("text/css")
        assert ".conversation-list" in stylesheet.text

        script = client.get("/static/radar.js")
        assert script.status_code == 200
        assert "loadConversations" in script.text
        assert "APPROVE_APPROACH" not in script.text
        assert "/engagement-events" in script.text
        assert "/qualifications" in script.text
