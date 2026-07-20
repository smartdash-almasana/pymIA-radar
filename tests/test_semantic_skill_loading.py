from pathlib import Path

import yaml

from app.schemas.assessment_v3 import AffinityDomain

SKILL_PATH = Path("config/semantic_skills/inlakech_affinity_v1.yaml")
DOC_PATH = Path("docs/SEMANTIC_SKILL_CONTRACT_V1.md")

REQUIRED_TOP_LEVEL_KEYS = {
    "schema_version",
    "skill_id",
    "version",
    "status",
    "principle",
    "providers",
    "identity",
    "affinity_definition",
    "apparent_intention",
    "affinity_domains",
    "evidence",
    "interpretation_guidance",
    "false_positive_risk",
    "review_priority",
    "recommended_review_action",
    "inferences",
    "contract",
    "calibration_cases",
    "prompt_version",
}


def load_skill() -> dict:
    with SKILL_PATH.open(encoding="utf-8") as file:
        return yaml.safe_load(file)


def test_semantic_skill_yaml_loads_and_has_required_identity() -> None:
    data = load_skill()

    assert REQUIRED_TOP_LEVEL_KEYS.issubset(data.keys())
    assert data["schema_version"] == "radar-semantic-skill/v1"
    assert data["skill_id"] == "inlakech_affinity_v1"
    assert data["version"] == "1.0.0"
    assert data["status"] == "APPROVED"
    assert "El LLM interpreta el sentido." in data["principle"]
    assert "RADAR valida, registra y gobierna." in data["principle"]
    assert "La persona decide." in data["principle"]


def test_yaml_domains_match_python_affinity_domain_enum_exactly() -> None:
    data = load_skill()

    assert data["affinity_domains"] == [item.value for item in AffinityDomain]


def test_active_providers_are_mimo_and_nemotron_via_opencode_zen() -> None:
    data = load_skill()
    providers = data["providers"]

    assert providers["api"] == "OpenCode Zen"
    assert providers["primary"]["model"] == "MiMo 2.5 Free"
    assert providers["conditional_reviewer"]["model"] == "Nemotron 3 Ultra Free"
    assert providers["failover"]["primary_failure"]["resolution"] == "EXPLICIT_PROVIDER_FAILOVER"
    assert providers["failover"]["primary_failure"]["retries"] == 0
    assert providers["failover"]["primary_failure"]["human_review_required"] is True
    assert providers["failover"]["all_failed"]["resolution"] == "ALL_PROVIDERS_UNAVAILABLE"
    assert providers["failover"]["all_failed"]["retries"] == 0


def test_no_legacy_provider_references_are_active_in_contract_files() -> None:
    legacy_names = ["Ag" + "nes", "Gem" + "ma", "Gem" + "ini"]
    combined = SKILL_PATH.read_text(encoding="utf-8") + DOC_PATH.read_text(encoding="utf-8")

    for name in legacy_names:
        assert name not in combined


def test_review_priority_has_no_weighted_formula() -> None:
    data = load_skill()
    priority = data["review_priority"]

    assert "source" in priority
    assert "full contextual interpretation" in priority["source"]
    assert "formula" not in priority
    assert "weights" not in priority
    assert "scoring" not in priority
    assert "No weighted formula" in priority["prohibited"]
    assert "keyword scoring" in priority["prohibited"]
    assert "regex scoring" in priority["prohibited"]
