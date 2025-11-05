from __future__ import annotations

import csv
import json
import posixpath
import re
import shutil
import textwrap
from datetime import UTC, datetime
from pathlib import Path

import typer

from .utils import CACHE_DIR

# Inline markdown link: [link text](url)
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")

_SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")


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
    Extra guards:
      - skip any row where src/normalized_path/suggest_path is SUMMARY.md
      - enforce same product+version unless changelog/release-notes is involved
      - for missing_anchor, require same page + non-empty suggest_anchor
    """
    grouped: dict[str, list[dict]] = {}
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            reason = (row.get("reason") or "").strip()
            if reason not in {"missing_file", "missing_anchor"}:
                continue

            # Must have either a target path or an anchor to fix.
            has_suggest = (row.get("suggest_path") or "").strip() or (
                row.get("suggest_anchor") or ""
            ).strip()
            if not has_suggest:
                continue

            # Source (guard BOM) and early exits.
            src = (row.get("src") or row.get("\ufeffsrc") or "").strip()
            if not src:
                continue

            # Never touch SUMMARY.md anywhere in the row (source or targets)
            if (
                _is_summary(src)
                or _is_summary(row.get("normalized_path", ""))
                or _is_summary(row.get("suggest_path", ""))
            ):
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
                continue

            # Extra safety for missing_anchor: must stay on same page and have an anchor.
            if reason == "missing_anchor":
                normalized_page = (row.get("normalized_path") or src or "").strip()
                if spath and spath != normalized_page:
                    continue
                if not (row.get("suggest_anchor") or "").strip():
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


def apply_autofix(
    high_csv: Path | None = None,
    dry_run: bool = True,
    backup_dir: Path | None = None,
    preview_out: Path | None = None,
    verbose: bool = False,
) -> tuple[int, int, Path, Path | None]:
    """
    Apply high-confidence suggestions to the docs.
    Returns (files_changed, links_changed, report_md_path, preview_json_path)
    - In dry-run mode, always writes a JSON preview (autofix_preview.json by default).
    - In apply mode, writes a markdown report and (if backup_dir is provided) backs up originals first.
    """
    csv_path = high_csv or (CACHE_DIR / "high_confidence_autofix.csv")
    grouped = _load_autofix_rows(csv_path)

    per_file_changes: list[tuple[Path, list[dict]]] = []
    files_changed = 0
    links_changed = 0

    # For JSON preview
    preview_changes: list[dict] = []

    for src_rel, rows in grouped.items():
        file_path = Path(src_rel)
        if not file_path.exists():
            # safety: skip if file missing
            continue

        original, new_text, changes = _replace_in_file(file_path, rows)

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

    # Markdown report (same path as before)
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


@app.command()
def main(
    csv_path: Path | None = CSV_PATH_OPT,
    dry_run: bool = DRY_RUN_OPT,
    backup_dir: Path | None = BACKUP_DIR_OPT,
    preview_out: Path | None = PREVIEW_OUT_OPT,
    verbose: bool = VERBOSE_OPT,
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
