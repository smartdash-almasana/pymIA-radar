from __future__ import annotations

from app.schemas.qualification import (
    CapitalBand,
    IdentityProfile,
    ParticipationPath,
    QualificationAction,
    QualificationInput,
    QualificationResult,
    QualificationStatus,
    RadarCommercialState,
    TimeHorizon,
    TrafficLight,
)


def qualify_contact(data: QualificationInput) -> QualificationResult:
    """Apply the resolved deterministic Inlak'ech precalification rules."""
    red_reasons: list[str] = []

    if data.identity_profile == IdentityProfile.UNDEFINED:
        red_reasons.append("identity_profile_undefined")
    if data.capital_band == CapitalBand.BELOW_50K:
        red_reasons.append("capital_below_documented_threshold")
    if data.time_horizon == TimeHorizon.ONLY_LOOKING:
        red_reasons.append("only_looking")
    if data.identity_profile == IdentityProfile.ARTISAN and data.artisan_anchor_type is None:
        red_reasons.append("artisan_anchor_type_missing")

    recommended_path = _recommend_path(data)

    if red_reasons:
        return QualificationResult(
            traffic_light=TrafficLight.RED,
            status=QualificationStatus.NOT_QUALIFIED,
            action=QualificationAction.EDUCATION_NO_CALENDAR,
            radar_state=(
                RadarCommercialState.OBSERVING
                if data.consent_to_continue
                else RadarCommercialState.DO_NOT_CONTACT
            ),
            recommended_path=recommended_path,
            crm_transfer_allowed=False,
            calendar_access_allowed=False,
            reasons=red_reasons,
            missing_information=_missing_information(data),
        )

    missing = _missing_information(data)
    distant_horizon = data.time_horizon in {
        TimeHorizon.THREE_TO_SIX_MONTHS,
        TimeHorizon.SIX_TO_TWELVE_MONTHS,
    }
    artisan_anchor_unproven = (
        data.identity_profile == IdentityProfile.ARTISAN
        and data.artisan_anchor_type is not None
        and not _has_substantive_text(data.artisan_anchor_evidence)
    )

    green_ready = (
        data.capital_band in {CapitalBand.FROM_50K_TO_150K, CapitalBand.ABOVE_150K}
        and data.time_horizon == TimeHorizon.THIS_MONTH
        and data.motivation_coherent is True
        and data.minimum_information_complete
        and not artisan_anchor_unproven
    )

    if not green_ready:
        reasons = ["interest_present_but_not_ready_for_agenda"]
        if distant_horizon:
            reasons.append("time_horizon_requires_maturation")
        if artisan_anchor_unproven:
            reasons.append("artisan_anchor_requires_concrete_evidence")
        reasons.extend(missing)
        return QualificationResult(
            traffic_light=TrafficLight.YELLOW,
            status=QualificationStatus.NURTURING,
            action=QualificationAction.NURTURE,
            radar_state=(
                RadarCommercialState.NURTURING
                if data.consent_to_continue
                else RadarCommercialState.DO_NOT_CONTACT
            ),
            recommended_path=recommended_path,
            crm_transfer_allowed=False,
            calendar_access_allowed=False,
            reasons=list(dict.fromkeys(reasons)),
            missing_information=missing,
        )

    priority = data.requests_next_step
    status = QualificationStatus.PRIORITY if priority else QualificationStatus.QUALIFIED
    radar_state = (
        RadarCommercialState.PRIORITY_QUALIFIED
        if priority and data.consent_to_continue
        else RadarCommercialState.QUALIFIED
        if data.consent_to_continue
        else RadarCommercialState.DO_NOT_CONTACT
    )
    reasons = [
        "capital_within_documented_band",
        "time_horizon_this_month",
        "motivation_confirmed_coherent",
        "minimum_information_complete",
    ]
    if priority:
        reasons.append("concrete_request_to_advance")
    if not data.consent_to_continue:
        reasons.append("commercial_fit_without_contact_consent")

    return QualificationResult(
        traffic_light=TrafficLight.GREEN,
        status=status,
        action=(
            QualificationAction.AGENDA_ACCESS
            if data.consent_to_continue
            else QualificationAction.EDUCATION_NO_CALENDAR
        ),
        radar_state=radar_state,
        recommended_path=recommended_path,
        crm_transfer_allowed=data.consent_to_continue,
        calendar_access_allowed=data.consent_to_continue,
        reasons=reasons,
        missing_information=[],
    )


def _recommend_path(data: QualificationInput) -> ParticipationPath:
    if data.identity_profile == IdentityProfile.ARTISAN and data.artisan_anchor_type is not None:
        return ParticipationPath.ANCHOR_ARTISAN

    if data.declared_path_interest == ParticipationPath.PATRIMONIAL_SOWER:
        return ParticipationPath.PATRIMONIAL_SOWER

    if data.identity_profile == IdentityProfile.RESIDENT and data.capital_band == CapitalBand.ABOVE_150K:
        return ParticipationPath.INTEGRAL_FOUNDER

    if data.capital_band == CapitalBand.FROM_50K_TO_150K:
        return ParticipationPath.ESSENTIAL_FOUNDER
    if data.capital_band == CapitalBand.ABOVE_150K:
        return ParticipationPath.INTEGRAL_FOUNDER

    return ParticipationPath.UNDEFINED


def _missing_information(data: QualificationInput) -> list[str]:
    missing: list[str] = []
    if data.identity_profile == IdentityProfile.UNDEFINED:
        missing.append("identity_profile")
    if data.capital_band == CapitalBand.UNDECLARED:
        missing.append("capital_band")
    if data.time_horizon == TimeHorizon.UNDEFINED:
        missing.append("time_horizon")
    if not _has_substantive_text(data.motivation_text):
        missing.append("motivation_text")
    if data.motivation_coherent is None:
        missing.append("motivation_coherence")
    if data.identity_profile == IdentityProfile.ARTISAN:
        if data.artisan_anchor_type is None:
            missing.append("artisan_anchor_type")
        elif not _has_substantive_text(data.artisan_anchor_evidence):
            missing.append("artisan_anchor_evidence")
    if not data.minimum_information_complete:
        missing.append("minimum_information")
    return list(dict.fromkeys(missing))


def _has_substantive_text(value: str | None) -> bool:
    return bool(value and len(value.strip()) >= 8)
