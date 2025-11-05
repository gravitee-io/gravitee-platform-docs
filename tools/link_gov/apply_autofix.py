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

# Inline markdown link: [link text](url)
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")

_SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")

# Allow cross-page anchor autofixes when explicitly enabled (default: off)
CROSS_PAGE_ANCHOR_OK = os.getenv("LG_CROSS_PAGE_ANCHOR_OK", "0").lower() in {"1", "true", "yes"}


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


def _candidate_old_urls(raw_url: str, src_path: str | None = "") -> list[str]:
    """
    Build a conservative set of variants the existing Markdown might contain so we
    can safely match and replace more cases:
      - strip './'
      - README.md <-> index.md <-> trailing slash directory
      - handle spaces vs %20
      - lowercased anchors
      - treat same-page forms as equivalent: 'README.md#frag' <-> '#frag'
    """
    if not raw_url:
        return []

    u = raw_url.replace("\\", "/")  # normalize slashes just in case
    cands: list[str] = []

    def add(v: str) -> None:
        if v and v not in cands:
            cands.append(v)

    add(u)  # as-is

    # split into path + fragment (anchor) if present
    path, frag = "", ""
    if "#" in u:
        path, frag = u.split("#", 1)
    else:
        path = u

    # add './' variant for simple relative forms (helps [text](./thing) vs [text](thing))
    if not u.startswith("./") and not _SCHEME_RE.match(u) and not u.startswith("/"):
        add(f"./{u}")
    if (
        path
        and not path.startswith("./")
        and not _SCHEME_RE.match(path)
        and not path.startswith("/")
    ):
        add(f"./{path}" + (f"#{frag}" if frag else ""))

    # strip leading "./" variants
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

    # trailing slash variants (path-only or path+frag)
    if path.endswith("/"):
        p = path[:-1]
        add(p + (f"#{frag}" if frag else ""))
        # directory default docs
        add(path + "README.md" + (f"#{frag}" if frag else ""))
        add(path + "index.md" + (f"#{frag}" if frag else ""))
    else:
        # allow adding a trailing slash if linking to a dir default
        if path.endswith("/README.md"):
            base = path[: -len("/README.md")]
            add(base + "/index.md" + (f"#{frag}" if frag else ""))
            add(base + "/" + (f"#{frag}" if frag else ""))
        if path.endswith("/index.md"):
            base = path[: -len("/index.md")]
            add(base + "/README.md" + (f"#{frag}" if frag else ""))
            add(base + "/" + (f"#{frag}" if frag else ""))

    # anchor case variants
    if frag:
        # keep as-is + lowercased anchor on same path
        add(path + "#" + frag.lower())
        # also generate './' stripped + lowercased
        if path.startswith("./"):
            p2 = path[2:]
            add(p2 + "#" + frag)
            add(p2 + "#" + frag.lower())

    # If this was a same-page link *authored with a path*, also accept pure '#frag'
    # Consider it "same page" when authored path resolves to the same file as src_path.
    if frag and src_path:
        authored = (path or "").lstrip("./")
        src_base = posixpath.basename(src_path or "")
        # same page if:
        #   - no path (already '#frag'), or
        #   - path is exactly the current file's basename, or
        #   - path is a default-doc in the same dir (README.md / index.md) and src is that file
        if (
            authored == ""
            or authored == src_base
            or (authored in {"README.md", "index.md"} and src_base in {"README.md", "index.md"})
        ):
            add("#" + frag)  # as authored
            add("#" + frag.lower())  # lowercased anchor only

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
) -> dict[str, list[dict]]:
    """
    Group rows by 'src' file.
    We log every row we skip with a reason so we can report later.
    """
    grouped: dict[str, list[dict]] = {}
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
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

            grouped.setdefault(src, []).append(row)

    return grouped


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
        old_candidates = _candidate_old_urls(raw_url, src_path)
        new_url = _assemble_target(src_path, raw_url, suggest_path, suggest_anchor)
        planned.append(
            {
                "old": old_candidates,
                "new": new_url,
                "row": r,
                "matched": False,
            }
        )

    changes: list[dict] = []

    for i, line in enumerate(lines):
        line_no = i + 1

        def _one_sub(m, _line_no=line_no):
            text, url = m.group(1), m.group(2)
            for plan in planned:
                if url in plan["old"]:
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
) -> tuple[int, int, Path, Path | None]:
    """
    Apply high-confidence suggestions to the docs (conservative).
    Returns (files_changed, links_changed, report_md_path, preview_json_path)
    Also writes a skip report JSON with reasons for every non-applied row.
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

        # Accumulate preview entries regardless of dry-run/apply
        if changes:
            for ch in changes:
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

        if changes:
            per_file_changes.append((file_path, changes))
            files_changed += 1
            links_changed += len(changes)

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


app = typer.Typer(add_completion=False)


# ---- Typer option singletons (avoid Ruff B008 in defaults) ----
CSV_PATH_OPT: Path | None = typer.Option(
    None,
    "--csv",
    help="Path to high_confidence_autofix.csv (defaults to tools/.cache/high_confidence_autofix.csv)",
)
DRY_RUN_OPT: bool = typer.Option(
    False,
    "--dry-run",
    help="Do not write files; produce preview JSON.",
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
        "Allow fixing missing anchors by moving links to a different page "
        "(still same product/version). Defaults to LG_CROSS_PAGE_ANCHOR_OK env."
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


@app.command()
def main(
    csv_path: Path | None = CSV_PATH_OPT,
    dry_run: bool = DRY_RUN_OPT,
    backup_dir: Path | None = BACKUP_DIR_OPT,
    preview_out: Path | None = PREVIEW_OUT_OPT,
    verbose: bool = VERBOSE_OPT,
    allow_cross_page_anchors: bool = ALLOW_XPAGE_ANCHORS_OPT,
    skips_out: Path | None = SKIPS_OUT_OPT,
    skips_csv: Path | None = SKIPS_CSV_OPT,  # <-- add
    explain: bool = EXPLAIN_OPT,  # <-- add
):
    """
    Apply (or preview) auto-fixes based on high_confidence_autofix.csv.
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
