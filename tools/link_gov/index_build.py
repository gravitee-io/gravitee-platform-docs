from __future__ import annotations

from pathlib import Path

from .utils import CACHE_DIR, load_config


def build_indexes(config_path: Path) -> None:
    _cfg = load_config(config_path)
    # Placeholder artifacts we’ll replace in Step 1
    (CACHE_DIR / "files_index.json").write_text("{}", encoding="utf-8")
    (CACHE_DIR / "headings_index.json").write_text("{}", encoding="utf-8")
