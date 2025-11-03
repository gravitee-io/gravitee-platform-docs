from __future__ import annotations

import json
from pathlib import Path

import typer
from markdown_it import MarkdownIt
from slugify import slugify

from .utils import CACHE_DIR, load_config

MD_EXTS = {".md", ".mdx"}


def _iter_docs(dirs: list[str]) -> list[Path]:
    files: list[Path] = []
    for d in dirs:
        root = Path(d)
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if p.suffix.lower() in MD_EXTS and p.is_file():
                files.append(p)
    return files


def _slug(text: str) -> str:
    """
    GitHub/GitBook-like slug:
    - lowercase
    - spaces -> hyphens
    - strip punctuation
    - unicode-friendly
    """
    return slugify(text, lowercase=True, allow_unicode=True, separator="-")


def _extract_headings(md_text: str) -> list[dict[str, str]]:
    """
    Return a list of dicts: {"level": int, "text": str, "id": str}
    We now index H1..H6 and include explicit IDs (when present).
    """
    md = MarkdownIt("commonmark")
    tokens = md.parse(md_text)
    out: list[dict[str, str]] = []

    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t.type == "heading_open":
            # t.tag is like 'h1', 'h2', ...
            try:
                level = int(t.tag[1])
            except Exception:
                level = 0

            # capture explicit id if present on the heading_open token
            hid = ""
            try:
                if t.attrs:
                    for k, v in t.attrs:
                        if k == "id" and v:
                            hid = str(v).strip()
                            break
            except Exception:
                hid = ""

            if 1 <= level <= 6:
                # The next token after heading_open should be 'inline' with the text
                if i + 1 < len(tokens) and tokens[i + 1].type == "inline":
                    text = tokens[i + 1].content.strip()
                    if text:
                        out.append({"level": level, "text": text, "id": hid})
        i += 1
    return out


def _validate_indexes(
    files_index: dict[str, dict], headings_index: dict[str, str]
) -> dict[str, int]:
    """Return a small report and raise no exceptions."""
    # 1) totals match?
    expected_total = sum(meta.get("headings_count", 0) for meta in files_index.values())
    actual_total = len(headings_index)

    # 2) sample presence checks (first 10 files)
    sample_files = list(files_index.keys())[:10]
    missing_keys = 0
    for path in sample_files:
        slugs = files_index[path].get("h1_h4_slugs", [])
        for s in slugs:
            key = f"{path}#{s}"
            if key not in headings_index:
                missing_keys += 1

    return {
        "expected_total": expected_total,
        "actual_total": actual_total,
        "missing_keys_in_sample": missing_keys,
        "sampled_files": len(sample_files),
    }


def build_indexes(config_path: Path) -> None:
    cfg = load_config(config_path)
    roots = cfg.get("docs_roots", ["docs/"])

    files = _iter_docs(roots)

    files_index: dict[str, dict] = {}
    headings_index: dict[str, str] = {}

    for p in files:
        try:
            text = p.read_text(encoding="utf-8")
        except Exception:
            # If a file can’t be decoded as UTF-8, skip it
            continue

        headings = _extract_headings(text)

        # derive slugs (primary from heading text, optional alt from explicit id)
        # handle duplicates on a per-file basis for the *text-based* slug
        seen_text_slug: dict[str, int] = {}
        file_slugs: list[str] = []  # all valid slugs for this file (text + explicit id)
        pairs: list[tuple[dict[str, str], str]] = (
            []
        )  # (heading, slug) entries to write into headings_index

        for h in headings:
            # primary (text-based) slug with per-file disambiguation
            base = _slug(h["text"])
            n = seen_text_slug.get(base, 0)
            primary = base if n == 0 else f"{base}-{n}"
            seen_text_slug[base] = n + 1

            pairs.append((h, primary))
            file_slugs.append(primary)

            # optional explicit-id slug (no disambiguation; ids are unique by authoring)
            hid = (h.get("id") or "").strip().lower()
            if hid and hid != primary:
                pairs.append((h, hid))
                if hid not in file_slugs:
                    file_slugs.append(hid)

        # write to global headings_index as path#slug -> text
        for h, slug in pairs:
            key = f"{p.as_posix()}#{slug}"
            headings_index[key] = h["text"]

        # store per-file summary (title = first H1 if present, else filename)
        title = next((h["text"] for h in headings if h["level"] == 1), p.stem)
        files_index[p.as_posix()] = {
            "title": title,
            "headings_count": len(headings),  # count of headings, not of slugs
            "h1_h4_slugs": file_slugs,  # keep the original field name for downstream code
        }

        # store per-file summary (title = first H1 if present, else filename)
        title = next((h["text"] for h in headings if h["level"] == 1), p.stem)
        files_index[p.as_posix()] = {
            "title": title,
            "headings_count": len(headings),
            "h1_h4_slugs": file_slugs,
        }

    # --- Sanity check: detect duplicate slugs per file ---
    dupes: dict[str, list[str]] = {}
    for path, meta in files_index.items():
        slugs = meta.get("h1_h4_slugs", [])
        seen = {}
        for s in slugs:
            seen[s] = seen.get(s, 0) + 1
        dups = [slug for slug, n in seen.items() if n > 1]
        if dups:
            dupes[path] = dups

    if dupes:
        report_path = CACHE_DIR / "duplicate_slugs.json"
        report_path.write_text(json.dumps(dupes, indent=2, ensure_ascii=False), encoding="utf-8")
        typer.secho(
            f"⚠️  Duplicate slugs found in {len(dupes)} files → see {report_path}",
            fg=typer.colors.YELLOW,
        )
    else:
        typer.secho("✅ No duplicate slugs detected.", fg=typer.colors.GREEN)

    (CACHE_DIR / "files_index.json").write_text(
        json.dumps(files_index, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (CACHE_DIR / "headings_index.json").write_text(
        json.dumps(headings_index, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    # --- Integrity check ---
    report = _validate_indexes(files_index, headings_index)
    (CACHE_DIR / "index_integrity.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    if report["actual_total"] >= report["expected_total"] and report["missing_keys_in_sample"] == 0:
        typer.secho(
            f"✅ Index integrity OK (total={report['actual_total']}, sample missing=0).",
            fg=typer.colors.GREEN,
        )
    else:
        typer.secho(
            f"⚠️ Index integrity WARN: expected={report['expected_total']} "
            f"actual={report['actual_total']} sample-missing={report['missing_keys_in_sample']}. "
            f"See {CACHE_DIR / 'index_integrity.json'}",
            fg=typer.colors.YELLOW,
        )
