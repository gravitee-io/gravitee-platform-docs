from __future__ import annotations

import csv
import json
import math
import re
from collections import defaultdict
from pathlib import Path

from .utils import CACHE_DIR, load_config

# --------- small helpers ---------
_WORD_RE = re.compile(r"[A-Za-z0-9]+")


def _words(text: str) -> list[str]:
    if not text:
        return []
    return [w.lower() for w in _WORD_RE.findall(text)]


def _stem(name: str) -> str:
    return Path(name).stem.lower()


def _product_version_from_path(p: str) -> tuple[str, str]:
    """
    Expect paths like 'docs/<product>/<version>/...'
    Returns (product, version) or ('','') if not available.
    """
    parts = p.split("/")
    if len(parts) >= 3 and parts[0] == "docs":
        return parts[1], parts[2]
    return "", ""


_PV_RE = re.compile(r"^docs/([^/]+)/([^/]+)/")


def _prod_ver(path: str) -> tuple[str, str]:
    m = _PV_RE.match(path or "")
    if not m:
        return "", ""
    return m.group(1), m.group(2)


def _is_changelog_context(path: str) -> bool:
    p = (path or "").lower()
    return ("releases-and-changelog" in p) or ("release-notes" in p)


# Jaccard overlap with small smoothing
def _jaccard(a: list[str], b: list[str]) -> float:
    A, B = set(a), set(b)
    if not A or not B:
        return 0.0
    inter = len(A & B)
    union = len(A | B)
    return inter / union if union else 0.0


# Score in [0, 100]
def _score_text_match(query_words: list[str], cand_words: list[str]) -> float:
    return round(100.0 * _jaccard(query_words, cand_words), 2)


# --------- load indexes ---------
def _load_indexes() -> tuple[dict[str, dict], dict[str, str], dict[str, list[tuple[str, str]]]]:
    """
    files_index: path -> {title, headings_count, h1_h4_slugs}
    headings_index: "path#slug" -> heading text
    per_file_headings: path -> list[(slug, text)]
    """
    files_index = json.loads((CACHE_DIR / "files_index.json").read_text(encoding="utf-8"))
    headings_index_raw = json.loads((CACHE_DIR / "headings_index.json").read_text(encoding="utf-8"))
    per_file: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for key, text in headings_index_raw.items():
        if "#" not in key:
            continue
        path, slug = key.split("#", 1)
        per_file[path].append((slug, text))
    return files_index, headings_index_raw, per_file


# --------- candidate building ---------
def _candidate_pages_for(src_path: str, files_index: dict[str, dict]) -> list[str]:
    """
    Narrow the candidate set by product (and keep all versions of that product).
    Falls back to *all* docs if we can't parse.
    """
    prod, _ver = _product_version_from_path(src_path)
    if not prod:
        return list(files_index.keys())
    return [p for p in files_index.keys() if p.split("/")[1] == prod]


# --------- suggestion core ---------
def _suggest_for_missing_file(
    rec: dict, files_index: dict[str, dict], per_file_heads: dict[str, list[tuple[str, str]]]
) -> list[dict]:
    src = rec.get("src", "")
    text = rec.get("text", "")
    raw_url = rec.get("raw_url") or rec.get("url") or ""
    anchor_hint = ""
    if "#" in raw_url:
        anchor_hint = raw_url.split("#", 1)[1]

    q_words = _words(text) + _words(_stem(raw_url)) + _words(anchor_hint)
    cand_paths = _candidate_pages_for(src, files_index)

    suggestions: list[tuple[float, dict]] = []
    src_prod, src_ver = _product_version_from_path(src)

    for path in cand_paths:
        title = files_index[path].get("title", "")
        title_w = _words(title) + _words(_stem(path))
        score = _score_text_match(q_words, title_w)

        # locality boosts
        prod, ver = _product_version_from_path(path)
        if prod and prod == src_prod:
            score += 8.0
        if ver and ver == src_ver:
            score += 5.0

        # if we saw an anchor hint, see if a heading in this page fits even better
        best_slug = ""
        best_heading = ""
        best_hscore = 0.0
        if anchor_hint and path in per_file_heads:
            for slug, htxt in per_file_heads[path]:
                h_w = _words(htxt) + [slug.lower()]
                hs = _score_text_match(_words(anchor_hint) + q_words, h_w)
                if hs > best_hscore:
                    best_hscore, best_slug, best_heading = hs, slug, htxt
            # modest bonus if heading looks very good
            score += min(best_hscore, 12.0)

        suggestions.append(
            (
                score,
                {
                    "suggest_path": path,
                    "suggest_anchor": best_slug,
                    "suggest_heading": best_heading,
                    "score": round(score, 2),
                },
            )
        )

    suggestions.sort(key=lambda t: t[0], reverse=True)
    # return top 3
    return [s for _, s in suggestions[:3]]


def _suggest_for_missing_anchor(
    rec: dict, per_file_heads: dict[str, list[tuple[str, str]]]
) -> list[dict]:
    """
    We already know the page exists; pick the best heading within this page.
    """
    path = rec.get("normalized_path", "") or rec.get("src", "")
    text = rec.get("text", "")
    anchor_hint = rec.get("normalized_anchor", "")

    q_words = _words(text) + _words(anchor_hint)

    cands = per_file_heads.get(path, [])
    scored: list[tuple[float, dict]] = []
    for slug, htxt in cands:
        h_w = _words(htxt) + [slug.lower()]
        sc = _score_text_match(q_words, h_w)
        scored.append(
            (
                sc,
                {
                    "suggest_path": path,
                    "suggest_anchor": slug,
                    "suggest_heading": htxt,
                    "score": round(sc, 2),
                },
            )
        )

    scored.sort(key=lambda t: t[0], reverse=True)
    return [s for _, s in scored[:3]]


# --------- public entry ---------
def build_suggestions_preview(
    config_path: Path, in_csv: Path | None = None, out_csv: Path | None = None, limit: int = 500
) -> tuple[int, Path]:
    """
    Read broken_links.csv, generate up to `limit` suggestions for internal records,
    and write tools/.cache/suggestions_preview.csv (top suggestion + two alternates).
    """
    _ = load_config(config_path)
    files_index, _headings_idx, per_file_heads = _load_indexes()

    src_csv = in_csv or (CACHE_DIR / "broken_links.csv")
    dst_csv = out_csv or (CACHE_DIR / "suggestions_preview.csv")

    # load broken rows
    broken: list[dict] = []
    with src_csv.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # only internal issues
            if row.get("category") in ("internal_page", "internal_anchor"):
                broken.append(row)
            if len(broken) >= limit:
                break

    out_rows: list[dict] = []
    for r in broken:
        reason = r.get("reason")
        if reason == "missing_file":
            suggs = _suggest_for_missing_file(r, files_index, per_file_heads)
        elif reason == "missing_anchor":
            suggs = _suggest_for_missing_anchor(r, per_file_heads)
        else:
            continue

        # flatten top 3 for quick review
        top = (
            suggs[0]
            if suggs
            else {"suggest_path": "", "suggest_anchor": "", "suggest_heading": "", "score": 0}
        )
        alt1 = (
            suggs[1]
            if len(suggs) > 1
            else {"suggest_path": "", "suggest_anchor": "", "suggest_heading": "", "score": ""}
        )
        alt2 = (
            suggs[2]
            if len(suggs) > 2
            else {"suggest_path": "", "suggest_anchor": "", "suggest_heading": "", "score": ""}
        )

        out_rows.append(
            {
                "src": r.get("src", ""),
                "text": r.get("text", ""),
                "reason": reason,
                "raw_url": r.get("raw_url", ""),
                "normalized_path": r.get("normalized_path", ""),
                "normalized_anchor": r.get("normalized_anchor", ""),
                # top suggestion
                "suggest_path": top.get("suggest_path", ""),
                "suggest_anchor": top.get("suggest_anchor", ""),
                "suggest_heading": top.get("suggest_heading", ""),
                "suggest_score": top.get("score", 0),
                # alternates (for quick eyeballing)
                "alt1_path": alt1.get("suggest_path", ""),
                "alt1_anchor": alt1.get("suggest_anchor", ""),
                "alt1_score": alt1.get("score", ""),
                "alt2_path": alt2.get("suggest_path", ""),
                "alt2_anchor": alt2.get("suggest_anchor", ""),
                "alt2_score": alt2.get("score", ""),
            }
        )

    # write preview CSV
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
        "alt1_path",
        "alt1_anchor",
        "alt1_score",
        "alt2_path",
        "alt2_anchor",
        "alt2_score",
    ]
    with (dst_csv).open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in out_rows:
            w.writerow(row)

    return len(out_rows), dst_csv


# ======== Step 3.2: improved scoring + confidence ========
def _idf(corpus_docs: list[list[str]]) -> dict[str, float]:
    """Compute IDF for tokens across a small corpus."""
    df: dict[str, int] = {}
    for doc in corpus_docs:
        for t in set(doc):
            df[t] = df.get(t, 0) + 1
    N = max(1, len(corpus_docs))
    return {t: math.log((N + 1) / (df_t + 1)) + 1.0 for t, df_t in df.items()}  # smoothed


def _tfidf_vec(words: list[str], idf: dict[str, float]) -> dict[str, float]:
    tf: dict[str, int] = {}
    for w in words:
        tf[w] = tf.get(w, 0) + 1
    # l2-normalize
    vec: dict[str, float] = {}
    for w, c in tf.items():
        vec[w] = c * idf.get(w, 0.0)
    norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
    return {w: v / norm for w, v in vec.items()}


def _cosine(q: dict[str, float], d: dict[str, float]) -> float:
    # sparse dot
    keys = q.keys() if len(q) <= len(d) else d.keys()
    s = 0.0
    for k in keys:
        if k in q and k in d:
            s += q[k] * d[k]
    return s  # already normalized


def _blend_scores(jaccard_0_1: float, tfidf_0_1: float) -> float:
    # light blend (tuned to favor semantic match; keep overlap signal)
    return 0.35 * jaccard_0_1 + 0.65 * tfidf_0_1


def _confidence(score: float, has_anchor: bool) -> str:
    # simple, transparent thresholds
    if score >= 80 and (has_anchor or score >= 85):
        return "high"
    if score >= 60:
        return "medium"
    return "low"


def _build_corpus_for_idf(
    files_index: dict, per_file_heads: dict[str, list[tuple[str, str]]]
) -> dict[str, float]:
    docs: list[list[str]] = []
    # titles + filename tokens
    for path, meta in files_index.items():
        docs.append(_words(meta.get("title", "")) + _words(_stem(path)))
        # headings per file (short docs; adding each heading as its own doc stabilizes IDF)
        for slug, htxt in per_file_heads.get(path, []):
            docs.append(_words(htxt) + [slug.lower()])
    return _idf(docs)


def build_suggestions_scored(
    config_path: Path, in_csv: Path | None = None, out_csv: Path | None = None, limit: int = 2000
) -> tuple[int, Path]:
    """
    Re-run suggestion generation with TF-IDF + locality bonuses and tag confidence.
    Writes tools/.cache/suggestions_scored.csv
    """
    _ = load_config(config_path)
    files_index, _headings_idx, per_file_heads = _load_indexes()

    # precompute IDF on titles + headings
    idf = _build_corpus_for_idf(files_index, per_file_heads)

    src_csv = in_csv or (CACHE_DIR / "broken_links.csv")
    dst_csv = out_csv or (CACHE_DIR / "suggestions_scored.csv")

    # load broken rows (internals only)
    broken: list[dict] = []
    with src_csv.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("category") in ("internal_page", "internal_anchor"):
                broken.append(row)
            if len(broken) >= limit:
                break

    out_rows: list[dict] = []
    for r in broken:
        reason = r.get("reason")
        src = r.get("src", "")
        link_text = r.get("text", "")
        raw_url = r.get("raw_url") or r.get("normalized_path") or ""
        anchor_hint = r.get("normalized_anchor") or (
            raw_url.split("#", 1)[1] if "#" in raw_url else ""
        )

        # ----- Build query words / vec
        q_words = _words(link_text) + _words(_stem(raw_url)) + _words(anchor_hint)
        q_vec = _tfidf_vec(q_words, idf)

        # candidate pool
        if reason == "missing_file":
            cand_paths = _candidate_pages_for(src, files_index)
        elif reason == "missing_anchor":
            # same page
            cand_paths = [r.get("normalized_path") or r.get("src", "")]
        else:
            continue

        src_prod, src_ver = _product_version_from_path(src)

        ranked: list[tuple[float, dict]] = []
        for path in cand_paths:
            meta = files_index.get(path)
            if not meta:
                continue

            # title/filename vector
            cand_words = _words(meta.get("title", "")) + _words(_stem(path))
            j = _jaccard(q_words, cand_words)
            c_vec = _tfidf_vec(cand_words, idf)
            cos = _cosine(q_vec, c_vec)
            base = _blend_scores(j, cos)  # 0..1

            # locality boosts
            prod, ver = _product_version_from_path(path)
            bonus = 0.0
            if prod and prod == src_prod:
                bonus += 0.08
            if ver and ver == src_ver:
                bonus += 0.05

            best_slug, best_heading, best_hscore = "", "", 0.0
            if reason == "missing_file" and anchor_hint and path in per_file_heads:
                # refine via headings if we know we want an anchor
                for slug, htxt in per_file_heads[path]:
                    h_words = _words(htxt) + [slug.lower()]
                    h_j = _jaccard(q_words + _words(anchor_hint), h_words)
                    h_vec = _tfidf_vec(h_words, idf)
                    h_cos = _cosine(q_vec, h_vec)
                    h_score = _blend_scores(h_j, h_cos)  # 0..1
                    if h_score > best_hscore:
                        best_hscore, best_slug, best_heading = h_score, slug, htxt
                bonus += min(best_hscore, 0.12)

            if reason == "missing_anchor":
                # pick best heading within page
                for slug, htxt in per_file_heads.get(path, []):
                    h_words = _words(htxt) + [slug.lower()]
                    h_j = _jaccard(q_words, h_words)
                    h_vec = _tfidf_vec(h_words, idf)
                    h_cos = _cosine(q_vec, h_vec)
                    h_score = _blend_scores(h_j, h_cos)
                    if h_score > best_hscore:
                        best_hscore, best_slug, best_heading = h_score, slug, htxt
                bonus += min(best_hscore, 0.12)

            final_score = max(0.0, min(100.0, round(100.0 * (base + bonus), 2)))
            ranked.append(
                (
                    final_score,
                    {
                        "suggest_path": path,
                        "suggest_anchor": best_slug if best_slug else "",
                        "suggest_heading": best_heading if best_heading else "",
                        "score": final_score,
                    },
                )
            )

        ranked.sort(key=lambda t: t[0], reverse=True)
        top = (
            ranked[0][1]
            if ranked
            else {"suggest_path": "", "suggest_anchor": "", "suggest_heading": "", "score": 0.0}
        )
        conf = _confidence(top["score"], bool(top.get("suggest_anchor")))

        out_rows.append(
            {
                "src": r.get("src", ""),
                "text": link_text,
                "reason": reason,
                "raw_url": raw_url,
                "normalized_path": r.get("normalized_path", ""),
                "normalized_anchor": r.get("normalized_anchor", ""),
                "suggest_path": top["suggest_path"],
                "suggest_anchor": top.get("suggest_anchor", ""),
                "suggest_heading": top.get("suggest_heading", ""),
                "suggest_score": top["score"],
                "confidence": conf,
            }
        )

    # write
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
    with (dst_csv).open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in out_rows:
            w.writerow(row)

    return len(out_rows), dst_csv


def build_gate_files_strict(
    config_path: Path,
    scored_csv: Path | None = None,
    out_high: Path | None = None,
    out_medium: Path | None = None,
    out_low: Path | None = None,
) -> tuple[int, int, int]:
    """
    Read suggestions_scored.csv and split into:
      - high_confidence_autofix.csv (STRICT: same version required, except changelog contexts)
      - needs_review.csv (everything else with confidence != low)
      - low_confidence.csv  (confidence == low)
    """
    _ = load_config(config_path)
    src_csv = scored_csv or (CACHE_DIR / "suggestions_scored.csv")
    high_csv = out_high or (CACHE_DIR / "high_confidence_autofix.csv")
    med_csv = out_medium or (CACHE_DIR / "needs_review.csv")
    low_csv = out_low or (CACHE_DIR / "low_confidence.csv")

    rows = []
    with src_csv.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            # internal-only reasons
            if row.get("reason") not in {"missing_file", "missing_anchor"}:
                continue
            rows.append(row)

    high, medium, low = [], [], []
    for row in rows:
        conf = (row.get("confidence") or "").strip().lower()
        src = row.get("src", "")
        spath = row.get("suggest_path", "")
        sprod, sver = _prod_ver(src)
        dprod, dver = _prod_ver(spath)

        same_product = sprod and dprod and (sprod == dprod)
        same_version = same_product and sver and dver and (sver == dver)

        # allow cross-version ONLY for changelog/release-notes contexts
        allowed_cross_version = (
            same_product
            and (not same_version)
            and (_is_changelog_context(src) or _is_changelog_context(spath))
        )

        ok_version = same_version or allowed_cross_version

        # extra safety for anchors: must stay on the same page
        if row.get("reason") == "missing_anchor":
            ok_version = (
                ok_version
                and (spath == (row.get("normalized_path") or row.get("src") or ""))
                and bool(row.get("suggest_anchor"))
            )

        # final assignment
        if conf == "low":
            low.append(row)
        elif conf == "high" and ok_version:
            high.append(row)
        else:
            medium.append(row)

    # write files
    fieldnames = [
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
    for path, bucket in [(high_csv, high), (med_csv, medium), (low_csv, low)]:
        with path.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            for row in bucket:
                w.writerow(row)

    # ----- diagnostics: how many “would-be high” got downgraded, and why? -----
    # Compute baseline “would-be-high”
    would_be_high = []
    with src_csv.open("r", encoding="utf-8", newline="") as f_in:
        r_in = csv.DictReader(f_in)
        for row in r_in:
            if (
                row.get("reason") in {"missing_file", "missing_anchor"}
                and (row.get("confidence") or "").lower() == "high"
            ):
                would_be_high.append(row)

    # Build a set of actually-kept highs for fast membership checks
    kept_set = set((r["src"], r["suggest_path"], r.get("suggest_anchor", "")) for r in high)

    def _pv(p: str) -> tuple[str, str]:
        m = _PV_RE.match(p or "")
        return (m.group(1), m.group(2)) if m else ("", "")

    def _is_changelog(p: str) -> bool:
        return _is_changelog_context(p)

    from collections import Counter

    reasons = Counter()
    kept_count = 0

    for row in would_be_high:
        key = (row.get("src", ""), row.get("suggest_path", ""), row.get("suggest_anchor", ""))
        if key in kept_set:
            kept_count += 1
            continue

        sprod, sver = _pv(row.get("src", ""))
        dprod, dver = _pv(row.get("suggest_path", ""))
        cross_version_same_product = (
            sprod and dprod and (sprod == dprod) and sver and dver and (sver != dver)
        )
        changelog_ok = _is_changelog(row.get("src", "")) or _is_changelog(
            row.get("suggest_path", "")
        )

        if row.get("reason") == "missing_anchor":
            same_page = row.get("suggest_path", "") == (
                row.get("normalized_path") or row.get("src", "")
            )
            has_anchor = bool(row.get("suggest_anchor"))
            if (not same_page) or (not has_anchor):
                reasons["missing_anchor_strict_rule"] += 1
            elif cross_version_same_product and not changelog_ok:
                reasons["cross_version_disallowed"] += 1
            else:
                reasons["other"] += 1
        else:
            if cross_version_same_product and not changelog_ok:
                reasons["cross_version_disallowed"] += 1
            else:
                reasons["other"] += 1

    stats = {
        "would_be_high": len(would_be_high),
        "kept_in_high": kept_count,
        "downgraded_total": len(would_be_high) - kept_count,
        "downgraded_breakdown": dict(reasons),
        "written": {
            "high_confidence_autofix.csv": len(high),
            "needs_review.csv": len(medium),
            "low_confidence.csv": len(low),
        },
    }

    # Save and print a friendly line
    (CACHE_DIR / "gate_stats.json").write_text(json.dumps(stats, indent=2), encoding="utf-8")
    print(
        f"ℹ️  Gate stats → tools/.cache/gate_stats.json | downgraded={stats['downgraded_total']} "
        f"(cross-version={stats['downgraded_breakdown'].get('cross_version_disallowed',0)}, "
        f"missing-anchor-safety={stats['downgraded_breakdown'].get('missing_anchor_strict_rule',0)})"
    )

    return len(high), len(medium), len(low)
