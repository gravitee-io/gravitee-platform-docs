# tools/link_gov/suggest_corrections.py
from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path

from .utils import CACHE_DIR, load_config

BROKEN_CSV = CACHE_DIR / "broken_links.csv"
FILES_INDEX = CACHE_DIR / "files_index.json"
HEADINGS_INDEX = CACHE_DIR / "headings_index.json"

# ---------- Helpers ----------


def _read_csv_dicts(p: Path) -> list[dict]:
    rows = []
    with p.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append(row)
    return rows


def _load_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def _slug_norm(s: str) -> str:
    s = (s or "").strip().lower()
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"[^a-z0-9_.\-]+", "-", s)
    s = s.strip("-")
    return s


def _version_bucket(path: str) -> str:
    # e.g., docs/gko/4.9/... -> ("docs/gko/4.9")
    m = re.match(r"^(.+?/\d+(?:\.\d+)*)/", path.replace("\\", "/"))
    return m.group(1) if m else ""


def _dir_of(path: str) -> str:
    p = Path(path)
    return str(p.parent).replace("\\", "/")


def _sim(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def _nearest_paths(candidates: list[str], target_dir: str) -> list[str]:
    # prefer same directory, then siblings
    scored = []
    for c in candidates:
        d = _dir_of(c)
        score = 1.0 if d == target_dir else (0.8 if Path(d).parent == Path(target_dir) else 0.0)
        scored.append((score, c))
    scored.sort(reverse=True)
    return [c for _, c in scored]


# GitBook-ish numbered variants we may see (already indexed in your indexer)
def _anchor_variants(raw_anchor: str) -> list[str]:
    # try id-<n>.-<slug>, id-<n>-<slug>, user-content-<slug> etc.
    out = []
    s = raw_anchor
    if s.startswith("user-content-"):
        base = s[len("user-content-") :]
        out.append(base)
    else:
        out.append(f"user-content-{s}")
    m = re.match(r"^(\d+)-(.+)$", s) or re.match(r"^(\d+)\.\-(.+)$", s)
    if m:
        n, tail = m.group(1), m.group(2)
        out += [f"id-{n}.-{tail}", f"id-{n}-{tail}", f"{n}.-{tail}", f"{n}-{tail}"]
    return list(dict.fromkeys(out))  # dedupe, keep order


@dataclass
class Suggestion:
    src: str
    kind: str  # 'anchor' or 'page'
    original: str
    suggestion: str | None
    score: float
    reason: str


# ---------- Core ----------


def _build_anchor_suggestions(
    broken_rows: list[dict], files_index: dict, headings_index: dict, anchor_threshold: float = 0.92
) -> list[Suggestion]:
    by_file_slugs: dict[str, set[str]] = defaultdict(set)
    for k in headings_index.keys():
        # k looks like: path#slug
        if "#" in k:
            path, slug = k.split("#", 1)
            by_file_slugs[path].add(slug)

    out: list[Suggestion] = []
    for r in broken_rows:
        if r.get("reason") != "missing_anchor":
            continue
        path = r.get("normalized_path") or ""
        want = (r.get("normalized_anchor") or "").strip().lower()
        # 1) if the page doesn’t exist in index, we can’t help here
        slugs = by_file_slugs.get(path)
        if not slugs:
            out.append(Suggestion(r["src"], "anchor", want, None, 0.0, "target_file_not_indexed"))
            continue

        want_norm = _slug_norm(want)
        # 2) exact match after normalization
        if want_norm in slugs:
            out.append(Suggestion(r["src"], "anchor", want, want_norm, 1.0, "exact_slug_found"))
            continue

        # 3) check common numbered/user-content variants
        for v in _anchor_variants(want_norm):
            if v in slugs:
                out.append(Suggestion(r["src"], "anchor", want, v, 0.99, "variant_slug_found"))
                break
        else:
            # 4) fuzzy match against this page’s slugs
            best = None
            best_score = 0.0
            for s in slugs:
                score = _sim(want_norm, s)
                if score > best_score:
                    best_score, best = score, s

            if best and best_score >= anchor_threshold:
                out.append(
                    Suggestion(r["src"], "anchor", want, best, best_score, "fuzzy_same_page")
                )
                continue

            # 5) fallback: look in nearby pages within same version bucket
            bucket = _version_bucket(path)
            candidates = [p for p in files_index.keys() if p.startswith(bucket)]
            nearby = _nearest_paths(candidates, _dir_of(path))[:30]
            best2, best2_score = None, 0.0
            for p2 in nearby:
                for s in by_file_slugs.get(p2, ()):
                    score = _sim(want_norm, s)
                    if score > best2_score:
                        best2_score, best2 = score, f"{p2}#{s}"
            if best2 and best2_score >= anchor_threshold:
                out.append(
                    Suggestion(r["src"], "anchor", want, best2, best2_score, "fuzzy_nearby_page")
                )
            else:
                out.append(
                    Suggestion(r["src"], "anchor", want, None, best2_score, "no_good_anchor_found")
                )

    return out


def _build_page_suggestions(
    broken_rows: list[dict], files_index: dict, page_threshold: float = 0.88
) -> list[Suggestion]:
    paths = set(files_index.keys())
    out: list[Suggestion] = []
    for r in broken_rows:
        if r.get("reason") != "missing_file":
            continue
        want_path = r.get("normalized_path") or ""
        want_dir = _dir_of(want_path)
        bucket = _version_bucket(want_path)
        # 1) exact basename match within bucket
        base = Path(want_path).name.lower()
        bucket_paths = [p for p in paths if p.startswith(bucket)]
        same_name = [p for p in bucket_paths if Path(p).name.lower() == base]
        if same_name:
            # prefer nearest dir
            best = _nearest_paths(same_name, want_dir)[0]
            out.append(
                Suggestion(r["src"], "page", want_path, best, 0.98, "same_name_same_version")
            )
            continue

        # 2) fuzzy path match in bucket
        want_norm = want_path.lower()
        best, best_score = None, 0.0
        for p in bucket_paths:
            score = _sim(want_norm, p.lower())
            # proximity bump
            if _dir_of(p) == want_dir:
                score += 0.05
            elif Path(_dir_of(p)).parent == Path(want_dir):
                score += 0.02
            if score > best_score:
                best_score, best = score, p

        if best and best_score >= page_threshold:
            out.append(
                Suggestion(r["src"], "page", want_path, best, best_score, "fuzzy_same_version")
            )
        else:
            out.append(
                Suggestion(r["src"], "page", want_path, None, best_score, "no_good_page_found")
            )
    return out


# ---------- Public API used by CLI ----------


def build_suggestions_preview(config_path: Path) -> Path:
    _ = load_config(config_path)
    broken = _read_csv_dicts(BROKEN_CSV)
    files_index = _load_json(FILES_INDEX)
    headings_index = _load_json(HEADINGS_INDEX)

    anchor_sugs = _build_anchor_suggestions(broken, files_index, headings_index)
    page_sugs = _build_page_suggestions(broken, files_index)

    # produce a lightweight preview for triage
    preview = []
    for s in [*anchor_sugs, *page_sugs]:
        preview.append(
            {
                "src": s.src,
                "kind": s.kind,
                "original": s.original,
                "suggestion": s.suggestion,
                "score": round(s.score, 4),
                "reason": s.reason,
            }
        )

    out = CACHE_DIR / "suggestions_preview.json"
    out.write_text(json.dumps(preview, indent=2, ensure_ascii=False), encoding="utf-8")
    return out


def build_suggestions_scored(config_path: Path) -> Path:
    """
    Same data as preview, but grouped by 'safe to autofix' vs 'needs_review',
    based on high-confidence thresholds.
    """
    _ = load_config(config_path)
    preview_path = build_suggestions_preview(config_path)
    items = json.loads(preview_path.read_text(encoding="utf-8"))

    SAFE_ANCHOR = 0.95
    SAFE_PAGE = 0.92

    safe, review = [], []
    for it in items:
        if it["suggestion"] is None:
            review.append(it)
            continue
        if it["kind"] == "anchor" and it["score"] >= SAFE_ANCHOR:
            safe.append(it)
        elif it["kind"] == "page" and it["score"] >= SAFE_PAGE:
            safe.append(it)
        else:
            review.append(it)

    out = CACHE_DIR / "suggestions_scored.json"
    out.write_text(
        json.dumps({"safe": safe, "needs_review": review}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return out
