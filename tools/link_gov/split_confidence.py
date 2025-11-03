from __future__ import annotations

import csv
from pathlib import Path

from .utils import CACHE_DIR


def split_confidence(in_csv: Path | None = None) -> dict[str, int]:
    """Split suggestions_scored.csv into high_confidence_autofix.csv and needs_review.csv"""
    src_csv = in_csv or (CACHE_DIR / "suggestions_scored.csv")
    high_csv = CACHE_DIR / "high_confidence_autofix.csv"
    review_csv = CACHE_DIR / "needs_review.csv"

    fields = [
        "src",
        "text",
        "reason",
        "raw_url",
        "normalized_path",
        "normalized_anchor",
        "suggest_path",
        "suggest_anchor",
        "suggest_heading",
        "suggest_score",
        "confidence",
    ]

    totals = {"high": 0, "medium": 0, "low": 0}

    with (
        src_csv.open("r", encoding="utf-8") as fin,
        high_csv.open("w", encoding="utf-8", newline="") as fh,
        review_csv.open("w", encoding="utf-8", newline="") as fm,
    ):

        reader = csv.DictReader(fin)
        wh = csv.DictWriter(fh, fieldnames=fields)
        wm = csv.DictWriter(fm, fieldnames=fields)
        wh.writeheader()
        wm.writeheader()

        for row in reader:
            conf = row.get("confidence", "").lower()
            totals[conf] = totals.get(conf, 0) + 1
            if conf == "high":
                wh.writerow(row)
            elif conf == "medium":
                wm.writerow(row)
            # ignore lows

    print(f"Split complete: {totals['high']} high, {totals['medium']} medium, {totals['low']} low")
    print(f"→ {high_csv}\n→ {review_csv}")
    return totals
