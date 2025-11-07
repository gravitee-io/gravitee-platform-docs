from __future__ import annotations

import csv
import json
from collections.abc import Iterable, Iterator
from pathlib import Path

from .utils import CACHE_DIR

BROKEN_CSV = CACHE_DIR / "broken_links.csv"

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


def _load_broken_lookups() -> tuple[dict, dict]:
    """Build quick lookups from broken_links.csv.
    anchor_by_key[(src, original_anchor_lower)] -> {normalized_path, raw_url}
    page_by_key[(src, original_path)] -> {normalized_path, raw_url}
    """
    anchor_by_key, page_by_key = {}, {}
    with BROKEN_CSV.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            src = row.get("src", "")
            reason = row.get("reason", "")
            if reason == "missing_anchor":
                orig = (row.get("normalized_anchor", "") or "").strip().lower()
                if orig:
                    anchor_by_key[(src, orig)] = {
                        "normalized_path": row.get("normalized_path", ""),
                        "raw_url": row.get("raw_url", ""),
                    }
            elif reason == "missing_file":
                orig_path = (row.get("normalized_path", "") or "").strip()
                if orig_path:
                    page_by_key[(src, orig_path)] = {
                        "normalized_path": orig_path,
                        "raw_url": row.get("raw_url", ""),
                    }
    return anchor_by_key, page_by_key


def _rows_from_csv(path: Path) -> Iterator[dict]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        yield from reader


def _rows_from_json(path: Path) -> Iterator[dict]:
    """
    Expect shape:
      {
        "safe": [ { "src", "kind": "anchor"|"page", "original", "suggestion", "score", "reason" }, ... ],
        "needs_review": [ ...same shape... ]
      }
    We enrich with data from broken_links.csv and map to the CSV field schema.
    """
    data = json.loads(path.read_text(encoding="utf-8"))
    anchor_by_key, page_by_key = _load_broken_lookups()

    def _emit(items: Iterable[dict], default_conf: str) -> Iterator[dict]:
        for it in items or []:
            src = it.get("src", "")
            kind = (it.get("kind") or "").strip().lower()
            original = (it.get("original") or "").strip()
            suggestion = (it.get("suggestion") or "").strip()

            # Defaults
            normalized_path = ""
            normalized_anchor = ""
            raw_url = ""
            suggest_path = ""
            suggest_anchor = ""

            if kind == "anchor":
                # locate the broken row by (src, original_anchor)
                ctx = anchor_by_key.get((src, original.lower()), {})
                normalized_path = ctx.get("normalized_path", "")
                raw_url = ctx.get("raw_url", "")

                # suggestion could be just a slug or "path#slug"
                if "#" in suggestion:
                    p, a = suggestion.split("#", 1)
                    suggest_path = p.strip()
                    suggest_anchor = a.strip()
                else:
                    # same-page anchor fix
                    suggest_path = ""  # keep empty so apply_autofix emits "#anchor"
                    suggest_anchor = suggestion

                reason = "missing_anchor"

            elif kind == "page":
                # locate by (src, wanted_path) — in broken CSV this equals normalized_path
                ctx = page_by_key.get((src, original), {})
                normalized_path = ctx.get("normalized_path", "") or original
                raw_url = ctx.get("raw_url", "")
                suggest_path = suggestion  # full path
                suggest_anchor = ""
                reason = "missing_file"

            else:
                # unknown kind — skip
                continue

            yield {
                "src": src,
                "text": "",  # not required by autofix
                "reason": reason,
                "raw_url": raw_url,
                "normalized_path": normalized_path,
                "normalized_anchor": normalized_anchor,
                "suggest_path": suggest_path,
                "suggest_anchor": suggest_anchor,
                "suggest_heading": "",
                "suggest_score": str(it.get("score", "")),
                "confidence": default_conf.lower(),
            }

    # 'safe' -> high, 'needs_review' -> medium (we only write highs/mediums w/ suggestions)
    for row in _emit(data.get("safe", []), default_conf="high"):
        yield row

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


# NEW: build_autofix_csv_from_scored(...) – only keep "fuzzy_same_page" anchors
def build_autofix_csv_from_scored(
    config: Path | None = None,
    scored_path: Path | None = None,
    reasons: tuple[str, ...] = ("fuzzy_same_page",),
    out_path: Path | None = None,
) -> Path:
    """
    Build a CSV (apply_autofix-compatible) directly from suggestions_scored.json,
    filtered to 'anchor' items whose suggestion 'reason' is in `reasons` and
    suggestion is not null. This is purpose-built for same-page anchor fixes.
    """
    # inputs / outputs
    scored = scored_path or (CACHE_DIR / "suggestions_scored.json")
    if not scored.exists():
        raise FileNotFoundError(f"{scored} not found; run `python -m tools.cli suggest` first")

    out_csv = out_path or (CACHE_DIR / "autofix_fuzzy_same_page.csv")

    # needed to enrich with raw_url / normalized_path
    anchor_by_key, page_by_key = _load_broken_lookups()

    payload = json.loads(scored.read_text(encoding="utf-8"))
    rows_out: list[dict] = []

    def _emit(items: Iterable[dict]) -> None:
        for it in items or []:
            if (it.get("kind") or "").strip().lower() != "anchor":
                continue
            if (it.get("reason") or "") not in reasons:
                continue
            suggestion = it.get("suggestion")
            if not suggestion:
                continue  # nothing to apply

            src = it.get("src", "")
            original_anchor = (it.get("original") or "").strip().lower()
            # find the broken row (gives us raw_url + normalized_path)
            ctx = anchor_by_key.get((src, original_anchor), {})
            normalized_path = ctx.get("normalized_path", "")
            raw_url = ctx.get("raw_url", "")

            # suggestion could be "#slug" implied or "path#slug"; for fuzzy_same_page we expect same page
            suggest_path = ""
            suggest_anchor = ""
            if "#" in suggestion:
                p, a = suggestion.split("#", 1)
                suggest_path = p.strip()
                suggest_anchor = a.strip().lower()
            else:
                suggest_anchor = (suggestion or "").strip().lower()

            rows_out.append(
                {
                    "src": src,
                    "text": "",
                    "reason": "missing_anchor",
                    "raw_url": raw_url,
                    "normalized_path": normalized_path or src,
                    "normalized_anchor": "",  # not needed by apply
                    "suggest_path": suggest_path,  # keep empty for same-page; if present, apply_autofix will still work
                    "suggest_anchor": suggest_anchor,  # the fixed anchor
                    "suggest_heading": "",
                    "suggest_score": str(it.get("score", "")),
                    "confidence": "high",  # treat these as high so they’re applied
                }
            )

    _emit(payload.get("safe", []))
    _emit(payload.get("needs_review", []))

    # write CSV
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=_FIELDS)
        w.writeheader()
        for r in rows_out:
            w.writerow(r)

    return out_csv


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
