from __future__ import annotations

import csv
import json
from collections.abc import Iterable, Iterator
from pathlib import Path

from .utils import CACHE_DIR

_FIELDS = [
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


def _rows_from_csv(path: Path) -> Iterator[dict]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        yield from reader


def _rows_from_json(path: Path) -> Iterator[dict]:
    """
    Expect shape like:
      {
        "safe": [ { ..., "suggestion": {"path": "...", "anchor": "...", "heading": "...", "score": 0.xx, "confidence": "high"} }, ... ],
        "needs_review": [ { ..., "suggestion": {... or null}, "confidence": "medium"/"low" }, ... ]
      }
    We normalize each item to the CSV field schema.
    """
    data = json.loads(path.read_text(encoding="utf-8"))

    def _emit(items: Iterable[dict], default_conf: str | None) -> Iterator[dict]:
        for it in items or []:
            sug = it.get("suggestion") or {}
            conf = (sug.get("confidence") or it.get("confidence") or default_conf or "").lower()

            yield {
                "src": it.get("src", ""),
                "text": it.get("text", ""),
                "reason": it.get("reason", ""),
                "raw_url": it.get("raw_url", ""),
                "normalized_path": it.get("normalized_path", ""),
                "normalized_anchor": it.get("normalized_anchor", ""),
                "suggest_path": sug.get("path", "") or "",
                "suggest_anchor": sug.get("anchor", "") or "",
                "suggest_heading": sug.get("heading", "") or "",
                "suggest_score": str(sug.get("score", "")),
                "confidence": conf,
            }

    # 'safe' are our highs
    for row in _emit(data.get("safe", []), default_conf="high"):
        yield row

    # 'needs_review' include mediums/lows
    for row in _emit(data.get("needs_review", []), default_conf="medium"):
        yield row


def split_confidence(
    in_path: Path | None = None, write_combined_csv: bool = True
) -> dict[str, int]:
    """
    Split suggestions into:
      - high_confidence_autofix.csv (only 'high' w/ suggestion)
      - needs_review.csv (only 'medium' w/ suggestion)
    Lows are ignored. Input can be JSON or CSV.
    """
    src = in_path or (CACHE_DIR / "suggestions_scored.json")
    if not src.exists():
        # fallback to CSV if user already has it
        alt = CACHE_DIR / "suggestions_scored.csv"
        if alt.exists():
            src = alt
        else:
            raise FileNotFoundError(f"No suggestions_scored input found at {src} or {alt}")

    is_json = src.suffix.lower() == ".json"

    # outputs
    high_csv = CACHE_DIR / "high_confidence_autofix.csv"
    review_csv = CACHE_DIR / "needs_review.csv"
    combined_csv = CACHE_DIR / "suggestions_scored.csv"

    # read rows
    rows = list(_rows_from_json(src) if is_json else _rows_from_csv(src))

    totals = {"high": 0, "medium": 0, "low": 0}
    for r in rows:
        c = (r.get("confidence") or "").lower()
        if c not in totals:
            totals[c] = 0
        totals[c] += 1

    # writers
    with (
        high_csv.open("w", encoding="utf-8", newline="") as fh,
        review_csv.open("w", encoding="utf-8", newline="") as fm,
    ):
        wh = csv.DictWriter(fh, fieldnames=_FIELDS)
        wm = csv.DictWriter(fm, fieldnames=_FIELDS)
        wh.writeheader()
        wm.writeheader()

        for r in rows:
            conf = (r.get("confidence") or "").lower()
            has_suggestion = (r.get("suggest_path") or r.get("suggest_anchor")) != ""
            if conf == "high" and has_suggestion:
                wh.writerow(r)
            elif conf == "medium" and has_suggestion:
                wm.writerow(r)
            # lows or items with null suggestion: ignore for autofix

    # optionally write a normalized combined CSV (useful for ad-hoc tooling)
    if write_combined_csv:
        with combined_csv.open("w", encoding="utf-8", newline="") as fc:
            wc = csv.DictWriter(fc, fieldnames=_FIELDS)
            wc.writeheader()
            for r in rows:
                wc.writerow(r)

    print(
        f"Split complete: high={totals.get('high',0)}, medium={totals.get('medium',0)}, low={totals.get('low',0)}"
    )
    print(f"→ {high_csv}\n→ {review_csv}")
    return totals


# --- simple CLI ---
if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(description="Split suggestions by confidence")
    p.add_argument(
        "-i",
        "--input",
        type=Path,
        default=None,
        help="Path to suggestions_scored.json or suggestions_scored.csv (default: tools/.cache/...)",
    )
    p.add_argument(
        "--no-combined",
        action="store_true",
        help="Do not write the normalized combined CSV",
    )
    args = p.parse_args()
    split_confidence(args.input, write_combined_csv=not args.no_combined)
