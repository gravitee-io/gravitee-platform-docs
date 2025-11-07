"""
Auto-apply link fixes from a CSV.

Typical usage:
  • Dry-run against fuzzy same-page fixes:
      python -m tools.autofix_apply --csv tools/.cache/autofix_fuzzy_same_page.csv --dry-run
  • Apply (with backups) trusting the CSV completely:
      python -m tools.autofix_apply --csv tools/.cache/autofix_fuzzy_same_page.csv --force-all --no-dry-run --backup-dir backups/

Notes:
  • --force-all bypasses most safety checks and attempts every row grouped by 'src'
    (SUMMARY.md remains guarded; missing 'src' rows are skipped).
  • No-ops (where the new URL already matches) are filtered out before planning changes,
    so “Links updated” counts only real edits.
"""

from __future__ import annotations

import csv
import json
import os
import posixpath
import re
import shutil
import textwrap
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

import typer

from .utils import CACHE_DIR

# Inline markdown link: [link text](url "optional title")
MD_LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)\s]+?)(?:\s+"[^"]*")?\)')

_SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")

# Allow cross-page anchor autofixes when explicitly enabled (default: off)
CROSS_PAGE_ANCHOR_OK = os.getenv("LG_CROSS_PAGE_ANCHOR_OK", "0").lower() in {"1", "true", "yes"}
# Anchors we never want to auto-redirect to on a different page
_BANNED_XPAGE_ANCHORS = {
    "overview",
    "introduction",
    "configuration",
    "compatibility-matrix",
    "supported-databases",
    "federation",
    "implementation",
    "reference",
    "architecture",
}

# Prefixes/Patterns we also want to block on cross-page redirects
# e.g. "use-a-custom-prefix" and "use-a-custom-prefix-1"
_BANNED_XPAGE_ANCHOR_PREFIXES = ("use-a-custom-prefix",)

# e.g. "step-5-documentation", "step-12-documentation", etc.
_BANNED_XPAGE_ANCHOR_REGEXES = [
    re.compile(r"^step-\d+-documentation$", re.IGNORECASE),
]
DEBUG_APPLY = os.getenv("LG_DEBUG_APPLY", "0").lower() in {"1", "true", "yes"}


def _is_banned_cross_page_anchor(anchor: str) -> bool:
    """True if this anchor should never be auto-redirected to another page."""
    a = (anchor or "").strip().lower()
    if not a:
        return False
    if a in _BANNED_XPAGE_ANCHORS:
        return True
    if any(a == p or a.startswith(p + "-") for p in _BANNED_XPAGE_ANCHOR_PREFIXES):
        return True
    for rx in _BANNED_XPAGE_ANCHOR_REGEXES:
        if rx.match(a):
            return True
    return False


def _write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")


def _utc_now_iso() -> str:
    return datetime.now(UTC).isoformat()


# --- extra safety helpers (mirror gate rules) ---
_PV_RE = re.compile(r"^docs/([^/]+)/([^/]+)/")


def _pv(p: str) -> tuple[str, str]:
    m = _PV_RE.match(p or "")
    return (m.group(1), m.group(2)) if m else ("", "")


def _is_changelog_context(path: str) -> bool:
    p = (path or "").lower()
    return ("releases-and-changelog" in p) or ("release-notes" in p)


def _is_summary(path: str) -> bool:
    return Path(path or "").name.lower() == "summary.md"


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


# Insert just above _candidate_old_urls (near the other helpers)
_ANCHOR_NUM_SUFFIXES = ("-1", "-2", "-3")


def _mutate_anchor_for_legacy_forms(frag: str) -> list[str]:
    """
    Legacy/erroneous anchor variants observed in the repo:
    - lowercase
    - dots removed: plugin.properties -> pluginproperties; values.yaml -> valuesyaml
    - collapse multiple hyphens
    - hyphenless
    - GitBook 'id-N.-slug' <-> 'id-N-slug'
    - add/remove GH duplicate suffixes: -1/-2/-3
    - trailing 'x20'
    """
    base = (frag or "").strip().lower()
    if not base:
        return []
    out: set[str] = {base}

    nodots = base.replace(".", "")
    out.add(nodots)

    out.add(re.sub(r"-{2,}", "-", base))  # collapse --
    out.add(base.replace("-", ""))  # hyphenless

    m = re.match(r"^id-(\d+)\.\-(.+)$", base)
    if m:
        out.add(f"id-{m.group(1)}-{m.group(2)}")
    m2 = re.match(r"^id-(\d+)\-(.+)$", base)
    if m2:
        out.add(f"id-{m2.group(1)}.-{m2.group(2)}")

    # add -1/-2/-3 variants and a no-suffix version
    for s in list(out):
        if not re.search(r"-\d+$", s):
            for suf in _ANCHOR_NUM_SUFFIXES:
                out.add(s + suf)
        else:
            out.add(re.sub(r"-\d+$", "", s))

    # accidental '%20' that landed as 'x20'
    for s in list(out):
        out.add(s + "x20")

    return list(out)


def _candidate_old_urls(raw_url: str, src_path: str | None = "") -> list[str]:
    if not raw_url:
        return []

    u = raw_url.replace("\\", "/")
    cands: list[str] = []

    def add(v: str) -> None:
        if v and v not in cands:
            cands.append(v)

    add(u)  # as-authored

    # split path + fragment if present
    if "#" in u:
        path, frag = u.split("#", 1)
    else:
        path, frag = u, ""

    # './' forms (both full and path-only)
    if not u.startswith("./") and not _SCHEME_RE.match(u) and not u.startswith("/"):
        add(f"./{u}")
    if (
        path
        and not path.startswith("./")
        and not _SCHEME_RE.match(path)
        and not path.startswith("/")
    ):
        add(f"./{path}" + (f"#{frag}" if frag else ""))

    # strip leading './'
    if u.startswith("./"):
        add(u[2:])
    if path.startswith("./"):
        p2 = path[2:]
        add(p2 + (f"#{frag}" if frag else ""))

    # spaces <-> %20
    if "%20" in u:
        add(u.replace("%20", " "))
    if " " in u:
        add(u.replace(" ", "%20"))

    # README/index/trailing-slash
    if path.endswith("/"):
        p = path[:-1]
        add(p + (f"#{frag}" if frag else ""))
        add(path + "README.md" + (f"#{frag}" if frag else ""))
        add(path + "index.md" + (f"#{frag}" if frag else ""))
    else:
        if path.endswith("/README.md"):
            base = path[: -len("/README.md")]
            add(base + "/index.md" + (f"#{frag}" if frag else ""))
            add(base + "/" + (f"#{frag}" if frag else ""))
        if path.endswith("/index.md"):
            base = path[: -len("/index.md")]
            add(base + "/README.md" + (f"#{frag}" if frag else ""))
            add(base + "/" + (f"#{frag}" if frag else ""))

    # --- NEW: extensionless & .html variants for path ---
    if path.endswith(".md"):
        stem = path[:-3]  # drop '.md'
        add(stem + (f"#{frag}" if frag else ""))
        if path.startswith("./"):
            add(stem[2:] + (f"#{frag}" if frag else ""))
        # .html (some docs render to html links)
        add(stem + ".html" + (f"#{frag}" if frag else ""))
        if path.startswith("./"):
            add(stem[2:] + ".html" + (f"#{frag}" if frag else ""))

    # --- Anchor variants (lowercased + legacy forms) ---
    if frag:
        add(path + "#" + frag.lower())
        if path.startswith("./"):
            p2 = path[2:]
            add(p2 + "#" + frag)
            add(p2 + "#" + frag.lower())
        for f2 in _mutate_anchor_for_legacy_forms(frag):
            add(path + "#" + f2)
            if path.startswith("./"):
                add(path[2:] + "#" + f2)
        # if extensionless path is plausible, include those with mutated anchors too
        if path.endswith(".md"):
            stem = path[:-3]
            for f2 in _mutate_anchor_for_legacy_forms(frag):
                add(stem + "#" + f2)
                add(stem + ".html#" + f2)
                if path.startswith("./"):
                    add(stem[2:] + "#" + f2)
                    add(stem[2:] + ".html#" + f2)

    # Pure same-page '#frag' (and all mutated variants)
    if frag and src_path:
        authored = (path or "").lstrip("./")
        src_base = posixpath.basename(src_path or "")
        if (
            authored == ""
            or authored == src_base
            or (authored in {"README.md", "index.md"} and src_base in {"README.md", "index.md"})
            or (
                authored.endswith(".md") and src_base in {"README.md", "index.md"}
            )  # common same-dir case
        ):
            add("#" + frag)
            add("#" + frag.lower())
            for f2 in _mutate_anchor_for_legacy_forms(frag):
                add("#" + f2)

    return cands


def _relativize(from_src_path: str, to_repo_path: str) -> str:
    """
    Build a relative URL from the source file to a repo-relative target path.
    Both are POSIX (e.g., 'docs/apim/4.5/.../README.md').
    """
    base = posixpath.dirname(from_src_path) or "."
    rel = posixpath.relpath(to_repo_path, start=base)
    return rel if not rel.startswith("./") else rel[2:]


def _load_autofix_rows(
    csv_path: Path,
    allow_cross_page_anchors: bool = False,
    skip_log: list[dict] | None = None,
    force_all: bool = False,
) -> dict[str, list[dict]]:
    """
    Group rows by 'src' file.
    We log every row we skip with a reason so we can report later.
    """
    grouped: dict[str, list[dict]] = {}
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if force_all:
            # Passthrough: group *every* row by src, minimal guards.
            for row in reader:
                # source (guard BOM)
                src = (row.get("src") or row.get("\ufeffsrc") or "").strip()
                if not src:
                    if skip_log is not None:
                        _log_skip(skip_log, row, stage="load", reason="missing_src")
                    continue

                # Keep SUMMARY.md off-limits even in force mode (source *or* targets)
                if (
                    _is_summary(src)
                    or _is_summary(row.get("normalized_path", ""))
                    or _is_summary(row.get("suggest_path", ""))
                ):
                    if skip_log is not None:
                        _log_skip(skip_log, row, stage="load", reason="summary_guard")
                    continue

                grouped.setdefault(src, []).append(row)
            return grouped
        for row in reader:
            reason = (row.get("reason") or "").strip()
            if reason not in {"missing_file", "missing_anchor"}:
                if skip_log is not None:
                    _log_skip(skip_log, row, stage="load", reason="unsupported_reason")
                continue

            # Must have either a target path or an anchor to fix.
            has_suggest = (row.get("suggest_path") or "").strip() or (
                row.get("suggest_anchor") or ""
            ).strip()
            if not has_suggest:
                if skip_log is not None:
                    _log_skip(skip_log, row, stage="load", reason="no_suggestion")
                continue

            # Source (guard BOM) and early exits.
            src = (row.get("src") or row.get("\ufeffsrc") or "").strip()
            if not src:
                if skip_log is not None:
                    _log_skip(skip_log, row, stage="load", reason="missing_src")
                continue

            # Never touch SUMMARY.md anywhere in the row (source or targets)
            if (
                _is_summary(src)
                or _is_summary(row.get("normalized_path", ""))
                or _is_summary(row.get("suggest_path", ""))
            ):
                if skip_log is not None:
                    _log_skip(skip_log, row, stage="load", reason="summary_guard")
                continue

            # Enforce strict same-version rule unless changelog context.
            spath = (row.get("suggest_path") or "").strip()
            normalized_page = (row.get("normalized_path") or src or "").strip()

            # If this is a same-page anchor fix (no suggest_path OR suggest_path equals the normalized page),
            # force the version check to pass; we’re staying on the same file.
            same_page_anchor_fix = (reason == "missing_anchor") and (
                not spath or spath == normalized_page
            )

            if same_page_anchor_fix:
                same_product = True
                same_version = True
            else:
                sprod, sver = _pv(src)
                dprod, dver = _pv(spath)
                same_product = sprod and dprod and (sprod == dprod)
                same_version = same_product and sver and dver and (sver == dver)

            allowed_cross = (
                same_product
                and (not same_version)
                and (_is_changelog_context(src) or _is_changelog_context(spath))
            )
            if not (same_version or allowed_cross):
                if skip_log is not None:
                    _log_skip(skip_log, row, stage="load", reason="cross_version_blocked")
                continue

            # Extra safety for missing_anchor
            if reason == "missing_anchor":
                normalized_page = (row.get("normalized_path") or src or "").strip()
                if not (row.get("suggest_anchor") or "").strip():
                    if skip_log is not None:
                        _log_skip(
                            skip_log, row, stage="load", reason="missing_anchor_no_suggest_anchor"
                        )
                    continue
                if (not allow_cross_page_anchors) and spath and spath != normalized_page:
                    if skip_log is not None:
                        _log_skip(skip_log, row, stage="load", reason="cross_page_anchor_blocked")
                    continue
                # If this fix would redirect to a different page's *generic* section, skip it.
                # (We only apply this rule for cross-page anchor moves.)
                if spath and spath != normalized_page:
                    if _is_banned_cross_page_anchor(row.get("suggest_anchor") or ""):
                        if skip_log is not None:
                            _log_skip(
                                skip_log, row, stage="load", reason="cross_page_anchor_denied"
                            )
                        continue

            grouped.setdefault(src, []).append(row)

    return grouped


def _extract_csv_candidates(row: dict) -> list[str]:
    """
    If the CSV already provides multiple old-URL variants in one field (semicolon-separated),
    use them verbatim. We support several likely header names.
    """
    fields = [
        "candidate_old_urls",
        "old_url_variants",
        "old_urls",
        "candidates",
        "all_old_urls",
        "tried",  # sometimes exported under this name
    ]
    for k in fields:
        v = (row.get(k) or "").strip()
        if v:
            # accept both ';' and ',' as separators, but prefer ';'
            parts = [p.strip() for p in re.split(r"[;,]", v) if p.strip()]
            if parts:
                return parts
    return []


def _replace_in_file(
    file_path: Path,
    rows: list[dict],
) -> tuple[str, str, list[dict], list[dict]]:
    """
    Perform conservative replacements in a file’s content.
    Returns (original_text, new_text, changes[], unmatched_rows[])
    where each 'change' is a dict with:
        line_no, link_text, old_url, new_url, before, after
    """
    original = file_path.read_text(encoding="utf-8")
    lines = original.splitlines(keepends=True)

    # plan entries keep a direct reference to the source row so we can log unmatched
    planned: list[dict] = []
    for r in rows:
        src_path = r.get("src", "")
        suggest_path = r.get("suggest_path", "") or ""
        suggest_anchor = r.get("suggest_anchor", "") or ""
        raw_url = r.get("raw_url", "") or r.get("normalized_path", "") or ""

        # NEW: prefer old-URL variants precomputed in CSV; otherwise fall back.
        csv_old_variants = _extract_csv_candidates(r)
        old_candidates = csv_old_variants or _candidate_old_urls(raw_url, src_path)
        # --- ensure path+anchor variant is present for same-page fixes ---
        # If the author wrote links as "file.md#frag" but the CSV normalized to "#frag",
        # include the authored-with-path form so we can match either.
        if raw_url and "#" in raw_url and src_path:
            path_part, frag_part = raw_url.split("#", 1)
            basenames = {posixpath.basename(src_path)}
            if path_part:
                basenames.add(posixpath.basename(path_part))
            for b in basenames:
                for prefix in ("", "./"):
                    cand = f"{prefix}{b}#{frag_part}"
                    if cand not in old_candidates:
                        old_candidates.append(cand)

        new_url = _assemble_target(src_path, raw_url, suggest_path, suggest_anchor)
        # ✅ filter out no-ops here
        if new_url in old_candidates:
            continue
        planned.append(
            {
                "old": old_candidates,
                "new": new_url,
                "row": r,
                "matched": False,
            }
        )

    if DEBUG_APPLY:
        print(f"[apply] file={file_path} planned={len(planned)}")
        for p in planned[:5]:
            olds_preview = p["old"][:3]
            print(f"  new={p['new']!r} old0..2={olds_preview!r} (total_old={len(p['old'])})")

    changes: list[dict] = []

    for i, line in enumerate(lines):
        line_no = i + 1

        def _one_sub(m, _line_no=line_no):
            text, url = m.group(1), m.group(2)
            for plan in planned:
                if url in plan["old"]:
                    # If the replacement is identical to the current URL, do nothing (no-op, not recorded).
                    if plan["new"] == url:
                        plan["matched"] = True
                        return m.group(0)

                    before = m.group(0)
                    after = f"[{text}]({plan['new']})"
                    changes.append(
                        {
                            "line_no": _line_no,
                            "link_text": text,
                            "old_url": url,
                            "new_url": plan["new"],
                            "before": before,
                            "after": after,
                        }
                    )
                    plan["matched"] = True
                    return after
            return m.group(0)

        if DEBUG_APPLY:
            for m in MD_LINK_RE.finditer(line):
                print(f"[apply] L{line_no} captured_url={m.group(2)!r}")

        lines[i] = MD_LINK_RE.sub(_one_sub, line)

    new_text = "".join(lines)

    # collect any rows that never matched text in file; attach candidates for debugging
    unmatched_rows: list[dict] = []
    for p in planned:
        if not p["matched"]:
            r = dict(p["row"])
            r["candidate_old_urls"] = list(p["old"])
            unmatched_rows.append(r)

    return original, new_text, changes, unmatched_rows


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


def _log_skip(skip_log: list[dict], row: dict, stage: str, reason: str) -> None:
    skip_log.append(
        {
            "stage": stage,  # "load" or "apply"
            "reason": reason,  # machine-friendly reason
            "src": row.get("src", ""),
            "kind": row.get("reason", ""),  # missing_file / missing_anchor
            "raw_url": row.get("raw_url", ""),
            "normalized_path": row.get("normalized_path", ""),
            "normalized_anchor": row.get("normalized_anchor", ""),
            "suggest_path": row.get("suggest_path", ""),
            "suggest_anchor": row.get("suggest_anchor", ""),
            # optional debugging fields (only present for 'apply' unmatched rows)
            "candidate_old_urls": row.get("candidate_old_urls", []),
        }
    )


def _write_skip_report(
    path: Path,
    skip_log: list[dict],
    high_total: int,
    grouped_total: int,
    applied_links: int,
) -> None:
    # Aggregate by reason for quick at-a-glance summary
    by_reason = Counter(e["reason"] for e in skip_log)
    doc = {
        "generated_at": _utc_now_iso(),
        "input_rows_total": high_total,
        "kept_after_filters": grouped_total,
        "applied_link_changes": applied_links,
        "skipped_items": skip_log,
        "skipped_by_reason": dict(by_reason),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False), encoding="utf-8")


def _write_skip_csv(path: Path, skip_log: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "stage",
                "reason",
                "src",
                "kind",
                "raw_url",
                "normalized_path",
                "normalized_anchor",
                "suggest_path",
                "suggest_anchor",
                "candidate_old_urls",
            ],
        )
        writer.writeheader()
        for r in skip_log:
            writer.writerow(
                {
                    **r,
                    "candidate_old_urls": ";".join(r.get("candidate_old_urls", [])),
                }
            )


def _print_skip_explanations(skip_log: list[dict]) -> None:
    # summary by reason
    by_reason = Counter(e["reason"] for e in skip_log)
    if not by_reason:
        print("No skips.")
        return

    print("\nSkipped by reason")
    for reason, count in sorted(by_reason.items(), key=lambda x: -x[1]):
        print(f"  • {reason}: {count}")

    # detailed rows
    print("\nDetails")
    for r in skip_log:
        line = f"- [{r['stage']}] {r['reason']} :: {r.get('src','')} | {r.get('raw_url','')}"
        print(line)
        if r["reason"] == "no_textual_match_in_file" and r.get("candidate_old_urls"):
            print(f"    tried: {', '.join(r['candidate_old_urls'])}")


def apply_autofix(
    high_csv: Path | None = None,
    dry_run: bool = True,
    backup_dir: Path | None = None,
    preview_out: Path | None = None,
    verbose: bool = False,
    allow_cross_page_anchors: bool = False,
    skips_out: Path | None = None,
    explain: bool = True,
    skips_csv: Path | None = None,
    force_all: bool = False,
) -> tuple[int, int, Path, Path | None]:
    """
    Apply CSV-driven link fixes to the docs.

    In normal mode, conservative safety checks are used. With force_all=True,
    most checks are bypassed (except SUMMARY.md and missing 'src'), and every
    CSV row is attempted. No-ops are filtered out before application.

    Returns (files_changed, links_changed, report_md_path, preview_json_path).
    Also writes a skip report JSON with reasons for non-applied rows.
    """
    csv_path = high_csv or (CACHE_DIR / "high_confidence_autofix.csv")

    # Count input rows for summary
    total_rows = 0
    with csv_path.open("r", encoding="utf-8-sig", newline="") as _f:
        for _ in csv.DictReader(_f):
            total_rows += 1

    skip_log: list[dict] = []
    grouped = _load_autofix_rows(
        csv_path,
        allow_cross_page_anchors=allow_cross_page_anchors,
        skip_log=skip_log,
        force_all=force_all,
    )

    per_file_changes: list[tuple[Path, list[dict]]] = []
    files_changed = 0
    links_changed = 0
    grouped_total = sum(len(v) for v in grouped.values())

    # For JSON preview
    preview_changes: list[dict] = []

    for src_rel, rows in grouped.items():
        file_path = Path(src_rel)
        if not file_path.exists():
            # Record a skip for all rows in this file if the file is missing
            for r in rows:
                _log_skip(skip_log, r, stage="apply", reason="source_file_missing")
            continue

        original, new_text, changes, unmatched_rows = _replace_in_file(file_path, rows)

        # Keep only real edits (no no-ops by construction, but protect anyway)
        real_changes = [ch for ch in changes if not ch.get("noop")]

        # Accumulate preview entries regardless of dry-run/apply
        if real_changes:
            for ch in real_changes:
                preview_changes.append(
                    {
                        "file": file_path.as_posix(),
                        "line_no": ch["line_no"],
                        "link_text": ch["link_text"],
                        "old_url": ch["old_url"],
                        "new_url": ch["new_url"],
                    }
                )

        # Any planned rows that didn’t match text in this file → log as skip
        for ur in unmatched_rows:
            _log_skip(skip_log, ur, stage="apply", reason="no_textual_match_in_file")

        if real_changes:
            per_file_changes.append((file_path, real_changes))
            files_changed += 1
            links_changed += len(real_changes)

            if not dry_run:
                # Back up first (if requested)
                if backup_dir:
                    backup_target = (backup_dir / file_path).resolve()
                    backup_target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(file_path, backup_target)
                    if verbose:
                        print(f"[backup] {file_path} -> {backup_target}")

                # Write the modified file
                file_path.write_text(new_text, encoding="utf-8")
                if verbose:
                    print(f"[write]  {file_path}")

    # Markdown report
    report_path = CACHE_DIR / "autofix_report.md"
    _write_report(report_path, per_file_changes, dry_run, files_changed, links_changed)

    # Always write preview JSON in dry-run
    preview_path: Path | None = None
    if dry_run:
        preview_path = preview_out or (CACHE_DIR / "autofix_preview.json")
        doc = {
            "generated_at": _utc_now_iso(),
            "dry_run": True,
            "files_changed": files_changed,
            "links_changed": links_changed,
            "changes": preview_changes,
        }
        _write_json(preview_path, doc)
        if verbose:
            print(f"[preview] wrote {preview_path} with {len(preview_changes)} entries")

    # Skips report (always write)
    skips_path = skips_out or (CACHE_DIR / "autofix_skipped.json")
    _write_skip_report(
        skips_path,
        skip_log,
        high_total=total_rows,
        grouped_total=grouped_total,
        applied_links=links_changed,
    )
    if verbose:
        print(f"[skips] wrote {skips_path} with {len(skip_log)} items")

    # Optional CSV and console explanations
    if skips_csv:
        _write_skip_csv(skips_csv, skip_log)
        if verbose:
            print(f"[skips] wrote CSV {skips_csv}")

    if explain:
        _print_skip_explanations(skip_log)

    return files_changed, links_changed, report_path, preview_path


app = typer.Typer(
    add_completion=False,
    help="Apply CSV-driven docs link fixes (dry-run by default). Pass --csv to use your fuzzy file.",
)


# ---- Typer option singletons (avoid Ruff B008 in defaults) ----
CSV_PATH_OPT: Path | None = typer.Option(
    None,
    "--csv",
    help=(
        "Path to the fixes CSV. Defaults to tools/.cache/high_confidence_autofix.csv. "
        "Point this at tools/.cache/autofix_fuzzy_same_page.csv to apply same-page fixes."
    ),
)
BACKUP_DIR_OPT: Path | None = typer.Option(
    None,
    "--backup-dir",
    help="Directory to store backups when applying changes.",
)
PREVIEW_OUT_OPT: Path | None = typer.Option(
    None,
    "--preview-out",
    help="Where to write the dry-run preview JSON (default: tools/.cache/autofix_preview.json)",
)
VERBOSE_OPT: bool = typer.Option(False, "--verbose", help="Verbose logging")
ALLOW_XPAGE_ANCHORS_OPT: bool = typer.Option(
    CROSS_PAGE_ANCHOR_OK,
    "--allow-cross-page-anchors",
    help=(
        "Permit moving links to a different page (same product/version unless in changelog context). "
        "Default is taken from LG_CROSS_PAGE_ANCHOR_OK."
    ),
)
# ---- Typer option singletons for 'autofix' command (avoid B008) ----
DRY_RUN_TOGGLE_OPT: bool = typer.Option(
    True,
    "--dry-run/--no-dry-run",
    help="Preview only (default). Use --no-dry-run to write files.",
)

SKIPS_OUT_OPT: Path | None = typer.Option(
    None,
    "--skips-out",
    help="Where to write JSON report of skipped rows (default: tools/.cache/autofix_skipped.json).",
)

SKIPS_CSV_OPT: Path | None = typer.Option(
    None,
    "--skips-csv",
    help="Also write a CSV of non-applied rows and reasons.",
)

EXPLAIN_OPT: bool = typer.Option(
    True,
    "--explain/--no-explain",
    help="Print grouped and per-row reasons for skipped high-confidence rows (default on).",
)

FORCE_ALL_OPT: bool = typer.Option(
    False,
    "--force-all",
    help=(
        "Trust the CSV completely: bypass normal safety checks and attempt every row grouped by 'src'. "
        "Still skips SUMMARY.md and rows missing 'src'."
    ),
)


@app.command()
def main(
    csv_path: Path | None = CSV_PATH_OPT,
    dry_run: bool = DRY_RUN_TOGGLE_OPT,
    backup_dir: Path | None = BACKUP_DIR_OPT,
    preview_out: Path | None = PREVIEW_OUT_OPT,
    verbose: bool = VERBOSE_OPT,
    allow_cross_page_anchors: bool = ALLOW_XPAGE_ANCHORS_OPT,
    skips_out: Path | None = SKIPS_OUT_OPT,
    skips_csv: Path | None = SKIPS_CSV_OPT,  # <-- add
    explain: bool = EXPLAIN_OPT,  # <-- add
    force_all: bool = FORCE_ALL_OPT,  # <--- NEW
):
    """
    Apply (or preview) auto-fixes sourced from a CSV.

    Examples:
      python -m tools.link_gov.apply_autofix --csv tools/.cache/autofix_fuzzy_same_page.csv --dry-run
      python -m tools.link_gov.apply_autofix --csv tools/.cache/autofix_fuzzy_same_page.csv --force-all --no-dry-run --backup-dir backups/

    Exit codes:
      0 = success and changes exist (or preview has changes)
      2 = no changes to make
      1 = error
    """
    try:
        files, links, report_md, preview_json = apply_autofix(
            high_csv=csv_path,
            dry_run=dry_run,
            backup_dir=backup_dir,
            preview_out=preview_out,
            verbose=verbose,
            allow_cross_page_anchors=allow_cross_page_anchors,
            skips_out=skips_out,
            explain=explain,  # <-- add
            skips_csv=skips_csv,  # <-- add
            force_all=force_all,
        )

        # In dry-run, success=0 if we *would* change anything; 2 if nothing to do.
        # In apply mode, success=0 if we *did* change anything; 2 if nothing to do.
        if dry_run:
            if files > 0 or links > 0:
                typer.secho(
                    f"📝 DRY-RUN: would change {links} links across {files} files.",
                    fg=typer.colors.BLUE,
                )
                typer.secho(f"Preview → {preview_json}", fg=typer.colors.BLUE)
                raise SystemExit(0)
            else:
                typer.secho("DRY-RUN: no changes to make.", fg=typer.colors.YELLOW)
                raise SystemExit(2)
        else:
            typer.secho(
                f"✅ Applied changes: {links} links across {files} files.", fg=typer.colors.GREEN
            )
            typer.secho(f"Report → {report_md}", fg=typer.colors.GREEN)
            # If nothing was applied, return 2 so CI can short-circuit.
            raise SystemExit(0 if (files > 0 or links > 0) else 2)

    except SystemExit as e:
        raise e
    except Exception as e:
        typer.secho(f"❌ apply_autofix failed: {e}", fg=typer.colors.RED)
        raise SystemExit(1) from e


if __name__ == "__main__":
    app()
