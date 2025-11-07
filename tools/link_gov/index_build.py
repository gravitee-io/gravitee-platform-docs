from __future__ import annotations

import json
import re
from pathlib import Path

import typer
from markdown_it import MarkdownIt

from .utils import CACHE_DIR, load_config

MD_EXTS = {".md", ".mdx"}

# Files we never index (avoid noise)
SKIP_BASENAMES = {"SUMMARY.md"}

# --- GitBook / HTML anchor helpers ---
# Strip fenced code so we don't match ids/titles inside code blocks.
FENCE_RE = re.compile(
    r"(?m)^\s*```[\s\S]*?^\s*```|^\s*~~~[\s\S]*?^\s*~~~",
    re.MULTILINE,
)

# {% tab title="..." %} (allow single/double/curly quotes, extra attrs, odd spacing)
TAB_TITLE_RE = re.compile(
    r"""\{\%\s*tab\b[^%]*?\btitle\s*=\s*   # {% tab ... title =
        (?:
           "([^"]+)"                       # "foo"
         | '([^']+)'                       # 'foo'
         | “([^”]+)”                       # “foo”
        )
        [^%]*?\%\}                         # ... %}
    """,
    re.IGNORECASE | re.VERBOSE,
)

# <summary ...>Title</summary>  -> anchor slug(Title)
SUMMARY_RE = re.compile(
    r"<summary[^>]*>([\s\S]*?)</summary>",
    re.IGNORECASE,
)

# id="..." OR name="..." (catch legacy <a name="..."> anchors too)
HTML_ID_RE = re.compile(
    r"""\b(?:id|name)\s*=\s*
        (?:
           "([^"\s>]+)"      # "id"
         | '([^'\s>]+)'      # 'id'
        )
    """,
    re.IGNORECASE | re.VERBOSE,
)

# Remove any inline tags when extracting <summary> text
TAG_RE = re.compile(r"<[^>]+>")


def _iter_docs(dirs: list[str]) -> list[Path]:
    files: list[Path] = []
    for d in dirs:
        root = Path(d)
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if p.is_file() and p.suffix.lower() in MD_EXTS and p.name not in SKIP_BASENAMES:
                files.append(p)
    return files


def _slug(text: str) -> str:
    """
    GitHub/GitBook-like slug that preserves underscores ( _ ):
    - strip inline code backticks
    - lowercase
    - collapse whitespace -> hyphens
    - remove chars except [a-z0-9_-]
    """
    # 1) strip inline code ticks: `FOO_BAR` -> FOO_BAR
    text = re.sub(r"`([^`]*)`", r"\1", text or "")
    # 2) lowercase
    text = text.strip().lower()
    # 3) collapse any whitespace to single hyphen
    text = re.sub(r"\s+", "-", text)
    # 4) drop anything that's not a-z, 0-9, underscore, or hyphen
    text = re.sub(r"[^a-z0-9_-]", "", text)
    # 5) collapse multi-hyphens and trim edge hyphens
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return text


def _strip_code_fences(text: str) -> str:
    """Remove fenced code blocks so regexes don't match inside code."""
    return FENCE_RE.sub("", text)


def _strip_html_tags(text: str) -> str:
    """Very light tag stripper for <summary> content."""
    return TAG_RE.sub("", text)


def _extract_gitbook_and_html_ids(md_text: str) -> list[dict[str, str]]:
    """
    Return pseudo-headings for anchors GitBook injects:
      - Tabs: {% tab title="RBAC" %}  -> id slug('rbac')
      - Expandables: <summary>Title</summary>  -> id slug('Title')
      - Generic HTML id= / legacy name=  -> id itself (lowercased)
    Each item: {"level": 0, "text": <label>, "id": <slug or id>}
    """
    clean = _strip_code_fences(md_text)
    pseudo: list[dict[str, str]] = []

    # Tabs — handle "..." / '...' / “...”
    for m in TAB_TITLE_RE.finditer(clean):
        label = next((g for g in m.groups() if g), "").strip()
        if label:
            slugged = _slug(label)
            pseudo.append({"level": 0, "text": label, "id": slugged})

    # Expandables (<details><summary ...>Title</summary>...</details>)
    for raw in SUMMARY_RE.findall(clean):
        label = _strip_html_tags(raw or "").strip()
        if label:
            pseudo.append({"level": 0, "text": label, "id": _slug(label)})

    # Generic HTML id= / name=
    for m in HTML_ID_RE.finditer(clean):
        hid = next((g for g in m.groups() if g), "")
        hid = (hid or "").strip().lower()
        if hid:
            pseudo.append({"level": 0, "text": hid, "id": hid})

    return pseudo


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
    # Also collect GitBook/HTML-generated anchors (tabs, expandables, id="...").
    out.extend(_extract_gitbook_and_html_ids(md_text))
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
            txt_for_slug = re.sub(r"\s+", " ", h["text"]).strip()
            base = _slug(txt_for_slug)
            n = seen_text_slug.get(base, 0)
            primary = base if n == 0 else f"{base}-{n}"
            seen_text_slug[base] = n + 1

            pairs.append((h, primary))
            file_slugs.append(primary)

            # --- NEW: GitBook "numbered heading" anchor variants ---
            # If the heading text starts with "3. " / "10. " / "3) " / "3: " etc., GitBook often emits anchors like:
            #   id-3.-<slug>  (note the "id-" prefix and the dot after the number)
            m = re.match(r"^\s*(\d+)[\.\):-]\s+", h["text"])
            if m:
                _num = m.group(1)
                # take the text AFTER the numeric prefix, normalize whitespace, then slugify
                _tail = h["text"][m.end() :]
                _tail = re.sub(r"\s+", " ", _tail).strip()
                _tail_slug = _slug(_tail)
                _variants = [
                    f"id-{_num}.-{_tail_slug}",  # common GitBook form
                    f"id-{_num}-{_tail_slug}",  # seen in some renders
                    f"{_num}.-{_tail_slug}",  # bare numeric-prefixed
                    f"{_num}-{_tail_slug}",
                ]
                for v in _variants:
                    if v not in file_slugs:
                        pairs.append((h, v))
                        file_slugs.append(v)

            # optional explicit-id slug (no disambiguation; ids are unique by authoring)
            hid = (h.get("id") or "").strip().lower()
            if hid and hid != primary:
                pairs.append((h, hid))
                if hid not in file_slugs:
                    file_slugs.append(hid)

            # --- OPTIONAL: accept GitHub's 'user-content-' prefix for slugs of THIS heading ---
            # Build 'user-content-<slug>' for every slug we just added for this heading.
            # (Do NOT do this for all slugs in the file, or you'll mis-attach headings.)
            _new_for_this_heading = []
            _new_for_this_heading.append(primary)
            if m:  # we added numbered variants above
                _new_for_this_heading.extend(_variants)
            if hid and hid != primary:
                _new_for_this_heading.append(hid)

            for _s in _new_for_this_heading:
                _uc = f"user-content-{_s}"
                if _uc not in file_slugs:
                    pairs.append((h, _uc))
                    file_slugs.append(_uc)
            # --- END OPTIONAL ---

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
