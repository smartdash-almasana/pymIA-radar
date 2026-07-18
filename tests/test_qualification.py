import pytest

from app.crm_transfer import build_crm_transfer_payload
from app.qualification import qualify_contact
from app.schemas.qualification import (
    ArtisanAnchorType,
    CapitalBand,
    IdentityProfile,
    ParticipationPath,
    QualificationAction,
    QualificationInput,
    QualificationStatus,
    RadarCommercialState,
    TimeHorizon,
    TrafficLight,
)


def _base_input(**overrides) -> QualificationInput:
    data = {
        "identity_profile": IdentityProfile.INVESTOR,
        "declared_path_interest": ParticipationPath.UNDEFINED,
        "capital_band": CapitalBand.FROM_50K_TO_150K,
        "time_horizon": TimeHorizon.THIS_MONTH,
        "motivation_text": "Quiero construir un legado coherente y participar responsablemente.",
        "motivation_coherent": True,
        "consent_to_continue": True,
        "requests_next_step": False,
        "minimum_information_complete": True,
    }
    data.update(overrides)
    return QualificationInput(**data)


def test_green_without_consent_preserves_fit_but_blocks_contact_and_crm() -> None:
    result = qualify_contact(_base_input(consent_to_continue=False))
    assert result.traffic_light == TrafficLight.GREEN
    assert result.status == QualificationStatus.QUALIFIED
    assert result.radar_state == RadarCommercialState.DO_NOT_CONTACT
    assert result.calendar_access_allowed is False
    assert result.crm_transfer_allowed is False


def test_red_for_capital_below_documented_threshold() -> None:
    result = qualify_contact(_base_input(capital_band=CapitalBand.BELOW_50K))
    assert result.traffic_light == TrafficLight.RED
    assert "capital_below_documented_threshold" in result.reasons


def test_red_for_only_looking() -> None:
    result = qualify_contact(_base_input(time_horizon=TimeHorizon.ONLY_LOOKING))
    assert result.traffic_light == TrafficLight.RED
    assert "only_looking" in result.reasons


def test_yellow_for_three_to_six_month_horizon() -> None:
    result = qualify_contact(_base_input(time_horizon=TimeHorizon.THREE_TO_SIX_MONTHS))
    assert result.traffic_light == TrafficLight.YELLOW
    assert result.status == QualificationStatus.NURTURING
    assert result.action == QualificationAction.NURTURE
    assert result.crm_transfer_allowed is False


def test_green_for_compatible_this_month_and_coherent() -> None:
    result = qualify_contact(_base_input())
    assert result.traffic_light == TrafficLight.GREEN
    assert result.status == QualificationStatus.QUALIFIED
    assert result.radar_state == RadarCommercialState.QUALIFIED
    assert result.crm_transfer_allowed is True
    assert result.recommended_path == ParticipationPath.ESSENTIAL_FOUNDER


def test_priority_requires_concrete_next_step() -> None:
    result = qualify_contact(_base_input(requests_next_step=True))
    assert result.status == QualificationStatus.PRIORITY
    assert result.radar_state == RadarCommercialState.PRIORITY_QUALIFIED


def test_artisan_without_anchor_type_is_red() -> None:
    result = qualify_contact(
        _base_input(
            identity_profile=IdentityProfile.ARTISAN,
            capital_band=CapitalBand.ABOVE_150K,
        )
    )
    assert result.traffic_light == TrafficLight.RED
    assert "artisan_anchor_type_missing" in result.reasons


def test_artisan_with_anchor_but_without_evidence_is_yellow() -> None:
    result = qualify_contact(
        _base_input(
            identity_profile=IdentityProfile.ARTISAN,
            capital_band=CapitalBand.ABOVE_150K,
            artisan_anchor_type=ArtisanAnchorType.TALENT,
        )
    )
    assert result.traffic_light == TrafficLight.YELLOW
    assert "artisan_anchor_requires_concrete_evidence" in result.reasons


def test_artisan_with_concrete_anchor_can_be_green() -> None:
    result = qualify_contact(
        _base_input(
            identity_profile=IdentityProfile.ARTISAN,
            capital_band=CapitalBand.ABOVE_150K,
            artisan_anchor_type=ArtisanAnchorType.TALENT,
            artisan_anchor_evidence="Taller permanente de bioconstrucción con equipo y plan operativo.",
        )
    )
    assert result.traffic_light == TrafficLight.GREEN
    assert result.recommended_path == ParticipationPath.ANCHOR_ARTISAN


def test_sembler_path_can_be_preserved_when_explicitly_declared() -> None:
    result = qualify_contact(
        _base_input(declared_path_interest=ParticipationPath.PATRIMONIAL_SOWER)
    )
    assert result.recommended_path == ParticipationPath.PATRIMONIAL_SOWER
    assert result.path_requires_human_confirmation is True


def test_resident_above_150k_recommends_integral_founder() -> None:
    result = qualify_contact(
        _base_input(
            identity_profile=IdentityProfile.RESIDENT,
            capital_band=CapitalBand.ABOVE_150K,
        )
    )
    assert result.recommended_path == ParticipationPath.INTEGRAL_FOUNDER


def test_non_artisan_cannot_send_artisan_anchor_fields() -> None:
    with pytest.raises(ValueError, match="only valid for ARTIFICE"):
        _base_input(artisan_anchor_type=ArtisanAnchorType.CAPITAL)


def test_crm_payload_only_for_qualified_with_consent() -> None:
    qualification_input = _base_input()
    qualification_result = qualify_contact(qualification_input)
    payload = build_crm_transfer_payload(
        identity="Persona pública",
        authorized_contact="persona@example.com",
        source="public_forum",
        source_url="https://example.com/thread/1",
        qualification_input=qualification_input,
        qualification_result=qualification_result,
    )
    assert payload.qualification_status == "CALIFICADO"
    assert payload.participation_path == "FUNDADOR_CIMENTACION_ESENCIAL"


def test_crm_payload_rejects_nurturing_contact() -> None:
    qualification_input = _base_input(time_horizon=TimeHorizon.THREE_TO_SIX_MONTHS)
    qualification_result = qualify_contact(qualification_input)
    with pytest.raises(ValueError, match="only qualified"):
        build_crm_transfer_payload(
            identity="Persona pública",
            authorized_contact="persona@example.com",
            source="public_forum",
            source_url="https://example.com/thread/1",
            qualification_input=qualification_input,
            qualification_result=qualification_result,
        )


def test_relaticle_client_is_blocked_until_real_contract_is_audited() -> None:
    import asyncio

    from app.integrations.relaticle import (
        RelaticleClient,
        RelaticleIntegrationNotAudited,
    )

    qualification_input = _base_input()
    qualification_result = qualify_contact(qualification_input)
    payload = build_crm_transfer_payload(
        identity="Persona pública",
        authorized_contact="persona@example.com",
        source="public_forum",
        source_url="https://example.com/thread/1",
        qualification_input=qualification_input,
        qualification_result=qualification_result,
    )

    with pytest.raises(RelaticleIntegrationNotAudited, match="contract is audited"):
        asyncio.run(RelaticleClient().transfer_qualified_lead(payload))
