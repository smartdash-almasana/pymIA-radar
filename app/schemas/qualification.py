from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field, model_validator


class IdentityProfile(StrEnum):
    INVESTOR = "INVERSOR"
    RESIDENT = "RESIDENTE"
    ARTISAN = "ARTIFICE"
    UNDEFINED = "NO_DEFINIDO"


class ParticipationPath(StrEnum):
    PATRIMONIAL_SOWER = "SEMBRADOR_PATRIMONIAL"
    ESSENTIAL_FOUNDER = "FUNDADOR_CIMENTACION_ESENCIAL"
    INTEGRAL_FOUNDER = "FUNDADOR_CIMENTACION_INTEGRAL"
    ANCHOR_ARTISAN = "ARTIFICE_ANCLAJE"
    UNDEFINED = "NO_DEFINIDO"


class CapitalBand(StrEnum):
    BELOW_50K = "MENOS_DE_USD_50000"
    FROM_50K_TO_150K = "USD_50000_A_150000"
    ABOVE_150K = "MAS_DE_USD_150000"
    UNDECLARED = "NO_DECLARADO"


class TimeHorizon(StrEnum):
    THIS_MONTH = "ESTE_MES"
    THREE_TO_SIX_MONTHS = "TRES_A_SEIS_MESES"
    SIX_TO_TWELVE_MONTHS = "SEIS_A_DOCE_MESES"
    ONLY_LOOKING = "SOLO_MIRANDO"
    UNDEFINED = "SIN_DEFINIR"


class ArtisanAnchorType(StrEnum):
    LAND = "TIERRA"
    CAPITAL = "CAPITAL"
    TALENT = "TALENTO"


class TrafficLight(StrEnum):
    RED = "ROJO"
    YELLOW = "AMARILLO"
    GREEN = "VERDE"


class QualificationStatus(StrEnum):
    NOT_QUALIFIED = "NO_CALIFICADO"
    NURTURING = "EN_MADURACION"
    QUALIFIED = "CALIFICADO"
    PRIORITY = "PRIORITARIO"


class QualificationAction(StrEnum):
    EDUCATION_NO_CALENDAR = "EDUCACION_SIN_CALENDARIO"
    NURTURE = "MADURACION"
    AGENDA_ACCESS = "ACCESO_A_AGENDA"


class RadarCommercialState(StrEnum):
    DETECTED = "DETECTED"
    REVIEW_PENDING = "REVIEW_PENDING"
    OBSERVING = "OBSERVING"
    APPROACH_APPROVED = "APPROACH_APPROVED"
    CONTACTED = "CONTACTED"
    REPLIED = "REPLIED"
    QUALIFICATION_STARTED = "QUALIFICATION_STARTED"
    NURTURING = "NURTURING"
    QUALIFIED = "QUALIFIED"
    PRIORITY_QUALIFIED = "PRIORITY_QUALIFIED"
    TRANSFERRED_TO_CRM = "TRANSFERRED_TO_CRM"
    OPPORTUNITY_OPEN = "OPPORTUNITY_OPEN"
    DISCARDED = "DISCARDED"
    DO_NOT_CONTACT = "DO_NOT_CONTACT"


class QualificationInput(BaseModel):
    identity_profile: IdentityProfile = IdentityProfile.UNDEFINED
    declared_path_interest: ParticipationPath = ParticipationPath.UNDEFINED
    capital_band: CapitalBand = CapitalBand.UNDECLARED
    time_horizon: TimeHorizon = TimeHorizon.UNDEFINED
    motivation_text: str | None = Field(default=None, max_length=1000)
    motivation_coherent: bool | None = None
    artisan_anchor_type: ArtisanAnchorType | None = None
    artisan_anchor_evidence: str | None = Field(default=None, max_length=1000)
    consent_to_continue: bool = False
    requests_next_step: bool = False
    minimum_information_complete: bool = False
    objections: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_artisan_fields(self) -> "QualificationInput":
        if self.identity_profile != IdentityProfile.ARTISAN:
            if self.artisan_anchor_type is not None or self.artisan_anchor_evidence is not None:
                raise ValueError("artisan anchor fields are only valid for ARTIFICE")
        return self


class QualificationResult(BaseModel):
    traffic_light: TrafficLight
    status: QualificationStatus
    action: QualificationAction
    radar_state: RadarCommercialState
    recommended_path: ParticipationPath
    path_requires_human_confirmation: bool = True
    crm_transfer_allowed: bool
    calendar_access_allowed: bool
    reasons: list[str] = Field(min_length=1)
    missing_information: list[str] = Field(default_factory=list)
    source_contract: str = "docs/specs/005_qualification.md"
    deterministic: bool = True
