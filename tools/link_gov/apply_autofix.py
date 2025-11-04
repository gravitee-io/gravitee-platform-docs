from __future__ import annotations

import csv
import posixpath
import re
import textwrap
from pathlib import Path

from .utils import CACHE_DIR

# Inline markdown link: [link text](url)
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")

_SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")


def _is_relative_url(u: str) -> bool:
    """True if it's a relative URL like 'foo/bar.md#x' or '../x'."""
    return bool(u) and not _SCHEME_RE.match(u) and not u.startswith("/")


def _assemble_target(src_path: str, raw_url: str, suggest_path: str, suggest_anchor: str) -> str:
    """
    Build the replacement URL:
    - If only anchor changes or suggest_path == src_path → '#anchor'
    - Otherwise combine path + anchor
    - Preserve relative paths if the original was relative
    """
    suggest_path = suggest_path or ""
    suggest_anchor = suggest_anchor or ""

    # same-page anchor only
    if suggest_anchor and (not suggest_path or suggest_path == src_path):
        return f"#{suggest_anchor}"

    if not suggest_path:
        return raw_url  # nothing to do

    target_path = suggest_path
    if _is_relative_url(raw_url):
        target_path = _relativize(src_path, suggest_path)

    return f"{target_path}#{suggest_anchor}" if suggest_anchor else target_path


def _candidate_old_urls(raw_url: str) -> list[str]:
    """
    Generate a tiny set of 'old url' variants to catch small formatting differences.
    We stay conservative to avoid unintended edits.
    """
    cands = []
    if raw_url:
        cands.append(raw_url)
        # common variants
        if raw_url.startswith("./"):
            cands.append(raw_url[2:])
        if raw_url.startswith("../"):
            # don't guess too much for parent-links; keep exact
            pass
        if "#" in raw_url:
            path, frag = raw_url.split("#", 1)
            if not path:  # hash-only case like '#some-anchor'
                cands.append(f"#{frag}")
    # de-dupe preserving order
    seen = set()
    out = []
    for u in cands:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def _relativize(from_src_path: str, to_repo_path: str) -> str:
    """
    Build a relative URL from the source file to a repo-relative target path.
    Both are POSIX (e.g., 'docs/apim/4.5/.../README.md').
    """
    base = posixpath.dirname(from_src_path) or "."
    rel = posixpath.relpath(to_repo_path, start=base)
    return rel if not rel.startswith("./") else rel[2:]


def _load_autofix_rows(csv_path: Path) -> dict[str, list[dict]]:
    """
    Group rows by 'src' file.
    Accept only internal broken-link reasons we can actually fix,
    and only when we have a suggested target (path or anchor).
    """
    grouped: dict[str, list[dict]] = {}
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            reason = (row.get("reason") or "").strip()
            if reason not in {"missing_file", "missing_anchor"}:
                continue
            if not (
                (row.get("suggest_path") or "").strip() or (row.get("suggest_anchor") or "").strip()
            ):
                continue
            # src may be prefixed by BOM in some spreadsheets; guard for that
            src = (row.get("src") or row.get("\ufeffsrc") or "").strip()
            if not src:
                continue
            grouped.setdefault(src, []).append(row)
    return grouped


def _replace_in_file(
    file_path: Path,
    rows: list[dict],
) -> tuple[str, str, list[dict]]:
    """
    Perform conservative replacements in a file’s content.
    Returns (original_text, new_text, changes[])
    where each 'change' is a dict with:
        line_no, link_text, old_url, new_url, before, after
    """
    original = file_path.read_text(encoding="utf-8")
    lines = original.splitlines(keepends=True)

    # rows may share the same src file; resolve each independently
    # build map of old->new for quick lookup per row, but match only when exact
    planned = []
    for r in rows:
        src_path = r.get("src", "")
        suggest_path = r.get("suggest_path", "") or ""
        suggest_anchor = r.get("suggest_anchor", "") or ""
        raw_url = r.get("raw_url", "") or r.get("normalized_path", "") or ""
        old_candidates = _candidate_old_urls(raw_url)
        new_url = _assemble_target(src_path, raw_url, suggest_path, suggest_anchor)
        planned.append((old_candidates, new_url))

    changes: list[dict] = []
    # Work line by line so we can record line numbers in the report
    for i, line in enumerate(lines):
        line_no = i + 1

        def _one_sub(m, _line_no=line_no):
            text, url = m.group(1), m.group(2)
            for old_cands, new_url in planned:
                if url in old_cands:
                    before = m.group(0)
                    after = f"[{text}]({new_url})"
                    changes.append(
                        {
                            "line_no": _line_no,  # use bound value
                            "link_text": text,
                            "old_url": url,
                            "new_url": new_url,
                            "before": before,
                            "after": after,
                        }
                    )
                    return after
            return m.group(0)

        new_line = MD_LINK_RE.sub(_one_sub, line)
        lines[i] = new_line

    new_text = "".join(lines)
    return original, new_text, changes


def _write_report(
    report_path: Path,
    per_file_changes: list[tuple[Path, list[dict]]],
    dry_run: bool,
    total_changed_files: int,
    total_links: int,
) -> None:
    md = []
    md.append("# Auto-fix report")
    md.append("")
    md.append(f"- Mode: {'DRY-RUN (no files written)' if dry_run else 'APPLIED (files updated)'}")
    md.append(f"- Files with changes: **{total_changed_files}**")
    md.append(f"- Links updated: **{total_links}**")
    md.append("")
    for fpath, changes in per_file_changes:
        if not changes:
            continue
        md.append(f"## {fpath.as_posix()}")
        for ch in changes:
            md.append(f"### Line {ch['line_no']}")
            md.append("")
            md.append(f"- text: `{ch['link_text']}`")
            md.append(f"- from: `{ch['old_url']}`")
            md.append(f"- to:   `{ch['new_url']}`")
            md.append("")
            # mini diff block
            diff = textwrap.dedent(
                f"""\
            ```diff
            - {ch['before']}
            + {ch['after']}
            ```
            """
            ).rstrip()
            md.append(diff)
            md.append("")
    report_path.write_text("\n".join(md) + "\n", encoding="utf-8")


def apply_autofix(high_csv: Path | None = None, dry_run: bool = True) -> tuple[int, int, Path]:
    """
    Apply high-confidence suggestions to the docs.
    Returns (files_changed, links_changed, report_path)
    """
    csv_path = high_csv or (CACHE_DIR / "high_confidence_autofix.csv")
    grouped = _load_autofix_rows(csv_path)

    per_file_changes: list[tuple[Path, list[dict]]] = []
    files_changed = 0
    links_changed = 0

    for src_rel, rows in grouped.items():
        file_path = Path(src_rel)
        if not file_path.exists():
            # safety: skip if file missing
            continue
        original, new_text, changes = _replace_in_file(file_path, rows)
        if changes:
            files_changed += 1
            links_changed += len(changes)
            per_file_changes.append((file_path, changes))
            if not dry_run:
                file_path.write_text(new_text, encoding="utf-8")

    report_path = CACHE_DIR / "autofix_report.md"
    _write_report(report_path, per_file_changes, dry_run, files_changed, links_changed)
    return files_changed, links_changed, report_path
