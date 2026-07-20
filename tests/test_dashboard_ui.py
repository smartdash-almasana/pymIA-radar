from fastapi.testclient import TestClient

from app.main import app


def test_dashboard_loads_real_htmx_signal_board() -> None:
    with TestClient(app) as client:
        dashboard = client.get('/')
        assert dashboard.status_code == 200
        assert dashboard.headers['content-type'].startswith('text/html')
        html = dashboard.text
        assert 'RADAR DE CONVERSACIONES' in html
        assert 'RADAR encuentra y analiza. La persona revisa y decide.' in html
        assert 'Mapa visual por señal' in html or 'No hay conversaciones reales' in html
        assert 'Encontradas reales' in html
        assert 'hx-get="/htmx/results"' in html
        assert 'Busco una comunidad regenerativa en Yucatán' not in html
        assert 'example.com/conversations/test' not in html


def test_dashboard_assets_support_signal_board_and_modal_close() -> None:
    with TestClient(app) as client:
        stylesheet = client.get('/static/radar-ui.css')
        script = client.get('/static/radar-ui.js')

    assert stylesheet.status_code == 200
    assert stylesheet.headers['content-type'].startswith('text/css')
    assert '.signal-board' in stylesheet.text
    assert '.signal-lane' in stylesheet.text
    assert '.signal-card' in stylesheet.text

    assert script.status_code == 200
    assert script.headers['content-type'].startswith('application/javascript')
    javascript = script.text
    assert 'function closeModal()' in javascript
    assert 'data-modal-close' in javascript
    assert 'data-modal-backdrop' in javascript
    assert 'replaceChildren' in javascript
