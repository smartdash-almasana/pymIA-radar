from __future__ import annotations

from pydantic import BaseModel, Field

from app.schemas.qualification import QualificationInput, QualificationResult


class CRMTransferPayload(BaseModel):
    identity: str = Field(min_length=1)
    authorized_contact: str = Field(min_length=1)
    source: str = Field(min_length=1)
    source_url: str = Field(min_length=1)
    participation_path: str
    identity_profile: str
    capital_band: str
    time_horizon: str
    motivation_text: str | None = None
    artisan_anchor_type: str | None = None
    objections: list[str] = Field(default_factory=list)
    qualification_status: str
    radar_state: str
    next_action: str


def build_crm_transfer_payload(
    *,
    identity: str,
    authorized_contact: str,
    source: str,
    source_url: str,
    qualification_input: QualificationInput,
    qualification_result: QualificationResult,
) -> CRMTransferPayload:
    if not qualification_input.consent_to_continue:
        raise ValueError("explicit consent is required for CRM transfer")
    if not qualification_result.crm_transfer_allowed:
        raise ValueError("only qualified contacts can be transferred to CRM")

    return CRMTransferPayload(
        identity=identity,
        authorized_contact=authorized_contact,
        source=source,
        source_url=source_url,
        participation_path=qualification_result.recommended_path.value,
        identity_profile=qualification_input.identity_profile.value,
        capital_band=qualification_input.capital_band.value,
        time_horizon=qualification_input.time_horizon.value,
        motivation_text=qualification_input.motivation_text,
        artisan_anchor_type=(
            qualification_input.artisan_anchor_type.value
            if qualification_input.artisan_anchor_type
            else None
        ),
        objections=qualification_input.objections,
        qualification_status=qualification_result.status.value,
        radar_state=qualification_result.radar_state.value,
        next_action=qualification_result.action.value,
    )
