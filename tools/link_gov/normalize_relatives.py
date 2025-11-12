# tools/link_gov/normalize_relatives.py
from __future__ import annotations

import csv
import re
import shutil
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

import typer

app = typer.Typer(
    add_completion=False, help="Normalize deep relative .md links to repo-relative paths"
)

REPO_ROOT = Path(__file__).resolve().parents[2]  # repo/
DOCS_ROOT = REPO_ROOT / "docs"

MD_FILE_GLOB = "**/*.md"

# ---- Typer option singletons (avoid Ruff B008 in defaults) ----
DRY_RUN_OPT: bool = typer.Option(
    True, "--dry-run/--apply", help="Preview by default; write files with --apply"
)
BACKUP_DIR_OPT: Path | None = typer.Option(
    None, "--backup-dir", help="Where to back up changed files"
)
CSV_OUT_OPT: Path = typer.Option(Path("tools/.cache/normalize_relatives.changes.csv"), "--csv-out")
CSV_SKIPS_OPT: Path = typer.Option(
    Path("tools/.cache/normalize_relatives.skips.csv"), "--csv-skips"
)
VERBOSE_OPT: bool = typer.Option(False, "--verbose")

# markdown inline link: [text](url "optional")
MD_LINK_RE = re.compile(r"(?<!\!)\[([^\]]+)\]\(([^)\s]+?)(?:\s+\"[^\"]*\")?\)")

SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
HASH_RE = re.compile(r"#(.+)$")


@dataclass
class Change:
    file: Path
    line_no: int
    link_text: str
    old_url: str
    new_url: str
    reason: str


def _is_relative(u: str) -> bool:
    if not u:
        return False
    if SCHEME_RE.match(u):  # http:, mailto:, etc
        return False
    if u.startswith("/"):  # site-root absolute
        return False
    return True


def _split_anchor(u: str) -> tuple[str, str]:
    """Return (path_part, anchor or '')"""
    m = HASH_RE.search(u)
    if not m:
        return u, ""
    anchor = m.group(1)
    return u[: m.start()], anchor


def _needs_rewrite_to_repo_rel(url: str) -> bool:
    """We only rewrite 'deep dot' relatives: anything containing ./ or ../"""
    return url.startswith("./") or url.startswith("../") or "/./" in url or "/../" in url


def _target_repo_relative(src_file: Path, url_path: str) -> tuple[str, str]:
    """
    Resolve url_path relative to src_file's directory and return:
      (repo_relative_path, reason)
    If resolution fails or escapes repo, return ("", reason)
    """
    try:
        # Resolve *syntactically* against filesystem
        abs_target = (src_file.parent / url_path).resolve()
    except Exception:
        return "", "resolve_error"

    try:
        repo_rel = abs_target.relative_to(REPO_ROOT).as_posix()
    except Exception:
        return "", "outside_repo"

    if not abs_target.exists():
        return "", "target_missing"

    if not abs_target.is_file():
        return "", "target_not_file"

    if not repo_rel.endswith(".md"):
        return "", "not_md"

    return repo_rel, "ok"


def _iter_md_files() -> Iterable[Path]:
    if not DOCS_ROOT.exists():
        return []
    return DOCS_ROOT.rglob(MD_FILE_GLOB)


def _backup_file(src: Path, backup_dir: Path) -> None:
    dst = backup_dir / src.relative_to(REPO_ROOT)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


@app.command()
def run(
    dry_run: bool = DRY_RUN_OPT,
    backup_dir: Path | None = BACKUP_DIR_OPT,
    csv_out: Path = CSV_OUT_OPT,
    csv_skips: Path = CSV_SKIPS_OPT,
    verbose: bool = VERBOSE_OPT,
):
    """
    Rewrite Markdown links like '../../x/y.md#z' to repo-relative 'docs/.../x/y.md#z'.
    Only affects .md links that are truly relative (no scheme, not starting with '/').
    """

    changes: list[Change] = []
    skips: list[dict] = []

    files_scanned = 0
    links_seen = 0

    for md in _iter_md_files():
        try:
            text = md.read_text(encoding="utf-8")
        except Exception:
            continue

        files_scanned += 1
        lines = text.splitlines(keepends=True)
        new_lines = list(lines)
        file_changes: list[Change] = []

        for i, line in enumerate(lines):
            line_no = i + 1

            def _one_sub(
                m,
                md=md,  # bind loop var
                line_no=line_no,  # bind loop var
                file_changes=file_changes,  # safe capture
                skips=skips,  # safe capture
            ):
                nonlocal links_seen
                links_seen += 1
                link_text, url = m.group(1), m.group(2)

                if not _is_relative(url):
                    # external or root-absolute -> skip
                    skips.append(
                        {
                            "file": md.as_posix(),
                            "line_no": line_no,
                            "link_text": link_text,
                            "url": url,
                            "reason": "skip_not_relative",
                        }
                    )
                    return m.group(0)

                path_part, anchor = _split_anchor(url)

                # only page links (.md)
                if not (path_part.endswith(".md") or path_part.endswith(".MD")):
                    skips.append(
                        {
                            "file": md.as_posix(),
                            "line_no": line_no,
                            "link_text": link_text,
                            "url": url,
                            "reason": "skip_not_md",
                        }
                    )
                    return m.group(0)

                if not _needs_rewrite_to_repo_rel(path_part):
                    # It's already a "clean" relative like 'section/page.md' — leave it
                    skips.append(
                        {
                            "file": md.as_posix(),
                            "line_no": line_no,
                            "link_text": link_text,
                            "url": url,
                            "reason": "skip_clean_relative",
                        }
                    )
                    return m.group(0)

                repo_rel, status = _target_repo_relative(md, path_part)
                if status != "ok":
                    skips.append(
                        {
                            "file": md.as_posix(),
                            "line_no": line_no,
                            "link_text": link_text,
                            "url": url,
                            "reason": f"skip_{status}",
                        }
                    )
                    return m.group(0)

                # Compose new URL: repo-relative + (optional) #anchor
                new_url = repo_rel + (f"#{anchor}" if anchor else "")
                if new_url == url:
                    # no-op
                    skips.append(
                        {
                            "file": md.as_posix(),
                            "line_no": line_no,
                            "link_text": link_text,
                            "url": url,
                            "reason": "skip_noop",
                        }
                    )
                    return m.group(0)

                # Record change
                file_changes.append(
                    Change(
                        file=md,
                        line_no=line_no,
                        link_text=link_text,
                        old_url=url,
                        new_url=new_url,
                        reason="rewrite_deep_relative_to_repo",
                    )
                )
                return f"[{link_text}]({new_url})"

            new_lines[i] = MD_LINK_RE.sub(_one_sub, line)

        if file_changes and not dry_run:
            if backup_dir:
                _backup_file(md, backup_dir)
            md.write_text("".join(new_lines), encoding="utf-8")
        changes.extend(file_changes)

    # --- Reporting ---
    changed_files = len({c.file for c in changes})
    typer.secho(
        f"Scanned {files_scanned} markdown files, saw {links_seen} links.", fg=typer.colors.BLUE
    )
    typer.secho(
        f"Planned rewrites: {len(changes)} across {changed_files} files "
        f"({ 'DRY-RUN' if dry_run else 'APPLIED' })",
        fg=typer.colors.GREEN if not dry_run else typer.colors.YELLOW,
    )

    # CSV (changes)
    csv_out.parent.mkdir(parents=True, exist_ok=True)
    with csv_out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["file", "line_no", "link_text", "old_url", "new_url", "reason"],
        )
        w.writeheader()
        for c in changes:
            w.writerow(
                {
                    "file": c.file.as_posix(),
                    "line_no": c.line_no,
                    "link_text": c.link_text,
                    "old_url": c.old_url,
                    "new_url": c.new_url,
                    "reason": c.reason,
                }
            )

    # CSV (skips)
    with csv_skips.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["file", "line_no", "link_text", "url", "reason"],
        )
        w.writeheader()
        for s in skips:
            w.writerow(s)

    typer.secho(f"Changes CSV → {csv_out}", fg=typer.colors.BLUE)
    typer.secho(f"Skips CSV   → {csv_skips}", fg=typer.colors.BLUE)


if __name__ == "__main__":
    app()
