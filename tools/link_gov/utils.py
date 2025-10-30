from __future__ import annotations

from pathlib import Path

import yaml


def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


CACHE_DIR = Path("tools/.cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)
