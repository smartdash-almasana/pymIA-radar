from pathlib import Path

import yaml

SKILL_PATH = Path("config/semantic_skills/inlakech_affinity_v1.yaml")

FORBIDDEN_INFERENCES = {
    "probable_archetype",
    "declared_capacity",
    "capital_band",
    "participation_path",
    "qualification_status",
    "commercial_lead_score",
    "contact_authorization",
    "consent_inference",
    "psychological_diagnosis",
    "financial_capacity_from_public_profile",
}


def load_skill() -> dict:
    with SKILL_PATH.open(encoding="utf-8") as file:
        return yaml.safe_load(file)


def test_forbidden_inferences_are_declared_but_absent_from_json_v3_fields() -> None:
    data = load_skill()

    assert set(data["inferences"]["prohibited"]) == FORBIDDEN_INFERENCES
    json_v3_fields = set(data["contract"]["json_v3"]["fields"])

    assert json_v3_fields.isdisjoint(FORBIDDEN_INFERENCES)


def test_json_v3_contract_uses_stable_python_enum_source() -> None:
    data = load_skill()
    json_v3 = data["contract"]["json_v3"]

    assert json_v3["enum_source"] == "app.schemas.assessment_v3"
    assert json_v3["dynamic_enums_allowed"] is False


def test_football_negative_case_is_defined_with_expected_semantic_result() -> None:
    data = load_skill()
    negative_cases = data["calibration_cases"]["negative"]
    football = next(
        item for item in negative_cases if item["id"] == "football_argentina_france_spain_messi"
    )

    assert football["expected"] == {
        "real_topic": "fútbol internacional",
        "apparent_affinity": "NONE",
        "apparent_intention": "NONE",
        "false_positive_risk": "HIGH",
        "recommended_review_action": "DISCARD",
    }
    assert "complete meaning" in football["interpretation_basis"]
