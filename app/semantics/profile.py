from pathlib import Path
import yaml

PROFILE_PATH = Path("config/inlakech_profile.yaml")

def load_profile() -> dict:
    return yaml.safe_load(PROFILE_PATH.read_text(encoding="utf-8"))
