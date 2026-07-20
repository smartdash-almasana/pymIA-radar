from datetime import UTC, datetime
from uuid import uuid4

from fastapi.testclient import TestClient

from app.db.session import SessionLocal, init_db
from app.main import app
from app.models.conversation import Conversation


def _seed_real_like_conversation() -> int:
    init_db()
    with SessionLocal() as db:
        row = Conversation(
            source='reddit',
            external_id=f'real-htmx-{uuid4()}',
            conversation_url='https://www.reddit.com/r/MexicoFinanciero/example',
            author_name='autor_publico_real',
            title='Consulta real persistida para RADAR',
            text='Conversación pública persistida en la base local de RADAR.',
            context='Dato de prueba focal, separado de producción por la base de pytest.',
            published_at=datetime(2026, 7, 20, tzinfo=UTC),
            query_origin='consulta real RADAR',
            status='detected',
        )
        db.add(row)
        db.commit()
        return row.id


def test_htmx_home_uses_real_backend_and_no_mock_copy() -> None:
    _seed_real_like_conversation()
    with TestClient(app) as client:
        page = client.get('/')
        assert page.status_code == 200
        assert 'Mapa visual por señal' in page.text
        assert 'Conversaciones reales agrupadas' in page.text
        assert 'Consulta real persistida para RADAR' in page.text
        assert 'Busco una comunidad regenerativa en Yucatán' not in page.text
        assert '¿Esto garantiza rentabilidad rápida?' not in page.text
        css = client.get('/static/radar-ui.css')
        assert css.status_code == 200
        assert css.headers['content-type'].startswith('text/css')


def test_htmx_fragments_are_partial_and_open_real_conversation() -> None:
    conversation_id = _seed_real_like_conversation()
    with TestClient(app) as client:
        fragment = client.get('/htmx/results?status=todos')
        assert fragment.status_code == 200
        assert '<html' not in fragment.text.lower()
        assert 'Mapa visual por señal' in fragment.text
        assert 'Consulta real persistida para RADAR' in fragment.text
        modal = client.get(f'/htmx/conversations/{conversation_id}/modal')
        assert modal.status_code == 200
        assert 'role="dialog"' in modal.text
        assert 'Ver fuente original' in modal.text
        analysis = client.get(f'/analysis/{conversation_id}')
        assert analysis.status_code == 200
        assert 'ANÁLISIS DE CONVERSACIÓN' in analysis.text
        assert 'RADAR no contactará' in analysis.text


def test_htmx_excludes_test_source_and_example_urls() -> None:
    init_db()
    with SessionLocal() as db:
        row = Conversation(
            source='test_source',
            external_id=f'test-{uuid4()}',
            conversation_url='https://example.com/conversations/test-ui',
            author_name='fixture',
            title='Inversión regenerativa falsa de prueba',
            text='Este registro no debe aparecer como conversación verdadera.',
            query_origin='fixture',
            status='REVIEW_PENDING',
        )
        db.add(row)
        db.commit()
        conversation_id = row.id
    with TestClient(app) as client:
        page = client.get('/')
        assert page.status_code == 200
        assert 'Inversión regenerativa falsa de prueba' not in page.text
        assert 'example.com/conversations/test-ui' not in page.text
        modal = client.get(f'/htmx/conversations/{conversation_id}/modal')
        assert modal.status_code == 404


def test_modal_markup_does_not_block_close_button() -> None:
    conversation_id = _seed_real_like_conversation()
    with TestClient(app) as client:
        modal = client.get(f'/htmx/conversations/{conversation_id}/modal')
    assert modal.status_code == 200
    assert 'data-modal-close' in modal.text
    assert 'data-modal-backdrop' in modal.text
    assert 'stopPropagation' not in modal.text


def test_ui_trace_uses_human_labels_not_provider_names() -> None:
    conversation_id = _seed_real_like_conversation()
    with TestClient(app) as client:
        modal = client.get(f'/htmx/conversations/{conversation_id}/modal')
        analysis = client.get(f'/analysis/{conversation_id}')
    combined = modal.text + analysis.text
    assert 'Evaluación semántica con IA' in combined
    assert 'Revisión adicional no requerida' in combined
    assert 'Agnes' not in combined
    assert 'Gemma' not in combined


def test_discarded_conversations_are_not_visible_or_filterable() -> None:
    init_db()
    with SessionLocal() as db:
        row = Conversation(
            source='reddit',
            external_id=f'real-discarded-{uuid4()}',
            conversation_url='https://www.reddit.com/r/MexicoFinanciero/discarded-visible-test',
            author_name='autor_publico_real',
            title='Conversación descartada que no debe volver',
            text='Este registro representa una conversación real ya descartada.',
            query_origin='prueba descartada',
            status='DISCARDED',
        )
        db.add(row)
        db.commit()
    with TestClient(app) as client:
        page = client.get('/')
        all_fragment = client.get('/htmx/results?status=todos')
        forced_fragment = client.get('/htmx/results?status=descartado')
    combined = page.text + all_fragment.text + forced_fragment.text
    assert 'Conversación descartada que no debe volver' not in combined
    assert 'Descartadas' not in page.text
    assert 'value="descartado"' not in page.text


def test_analysis_decision_form_allows_candidate_publication_draft_or_discard() -> None:
    conversation_id = _seed_real_like_conversation()
    with TestClient(app) as client:
        analysis = client.get(f'/analysis/{conversation_id}')
    assert analysis.status_code == 200
    html = analysis.text
    assert 'Identificar persona candidata' in html
    assert 'value="classify_candidate"' in html
    assert 'Preparar mensaje para la publicación' in html
    assert 'value="prepare_public_reply"' in html
    assert 'Descartar' in html
    assert 'value="discard"' in html
    assert 'Notas opcionales' in html
    assert 'Identificación pública de la persona' in html
    assert 'Borrador para dejar en la publicación' in html
    assert 'publication_reply' in html
    assert 'Mensaje propuesto' not in html
    assert 'proposed_message' not in html
    assert 'Aprobar acercamiento humano' not in html
    assert 'Mantener en observación' not in html
    assert 'value="do_not_contact"' not in html


def test_classifying_candidate_requires_public_identity_and_sends_no_contact() -> None:
    conversation_id = _seed_real_like_conversation()
    with TestClient(app) as client:
        missing = client.post(
            f'/htmx/conversations/{conversation_id}/decision',
            data={'decision': 'classify_candidate', 'internal_note': 'nota'},
        )
        assert missing.status_code == 200
        assert 'identidad pública' in missing.text

        response = client.post(
            f'/htmx/conversations/{conversation_id}/decision',
            data={
                'decision': 'classify_candidate',
                'lead_identity': 'usuario_publico_relevante',
                'internal_note': 'Nota opcional de revisión.',
            },
        )
        assert response.status_code == 200
        assert 'Persona candidata identificada' in response.text
        assert 'No se envió ningún contacto automático' in response.text

    from app.models.discovery import DiscoveryCandidate
    from app.models.engagement import EngagementEvent
    from app.models.review import ReviewDecision

    with SessionLocal() as db:
        candidate = db.query(DiscoveryCandidate).filter_by(origin_conversation_id=conversation_id).one()
        reviews = db.query(ReviewDecision).filter_by(conversation_id=conversation_id).all()
        contacts = db.query(EngagementEvent).filter_by(conversation_id=conversation_id, event_type='CONTACTED').all()
    assert candidate.public_name == 'usuario_publico_relevante'
    assert candidate.discovery_state == 'DISCOVERY_CANDIDATE'
    assert any(item.decision == 'IDENTIFY_DISCOVERY_CANDIDATE' for item in reviews)
    assert contacts == []


def test_prepare_public_reply_requires_draft_and_sends_no_contact() -> None:
    conversation_id = _seed_real_like_conversation()
    draft = 'Gracias por compartir esto. ¿Podrías contar un poco más sobre el contexto?'
    with TestClient(app) as client:
        missing = client.post(
            f'/htmx/conversations/{conversation_id}/decision',
            data={'decision': 'prepare_public_reply', 'internal_note': 'nota'},
        )
        assert missing.status_code == 200
        assert 'borrador para la publicación' in missing.text
        assert 'No se envió ningún contacto automático' in missing.text

        response = client.post(
            f'/htmx/conversations/{conversation_id}/decision',
            data={
                'decision': 'prepare_public_reply',
                'publication_reply': draft,
                'internal_note': 'Nota opcional de revisión.',
            },
        )
        assert response.status_code == 200
        assert 'Borrador para publicación preparado' in response.text
        assert 'No se envió ningún contacto automático' in response.text

    from app.models.engagement import EngagementEvent
    from app.models.review import ReviewDecision

    with SessionLocal() as db:
        reviews = db.query(ReviewDecision).filter_by(conversation_id=conversation_id).all()
        contacts = db.query(EngagementEvent).filter_by(conversation_id=conversation_id, event_type='CONTACTED').all()
    assert any(item.decision == 'PREPARE_PUBLICATION_REPLY' and item.edited_response == draft for item in reviews)
    assert contacts == []
