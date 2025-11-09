# tools/link_gov/denormalize_relatives.py
from __future__ import annotations

import csv
import posixpath
import re
import shutil
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

import typer

from .utils import CACHE_DIR, load_config

app = typer.Typer(
    add_completion=False, help="Convert repo-relative page links to shortest relative paths."
)

# Inline markdown link: [text](url "optional title")
MD_LINK_RE = re.compile(r'(?<!\!)\[([^\]]+)\]\(([^)\s]+?)(?:\s+"[^"]*")?\)')

# Anything that looks like a *repo-relative* page link we created during normalize:
# e.g. docs/apim/4.8/guide/foo.md, docs/apim/4.9/foo/bar/index.md, etc.
REPO_PAGE_RE = re.compile(r"^(?:\.?/)?docs/[^()\s#]+\.md(?:#[A-Za-z0-9_.\-]+)?$")

# Treat only markdown files
MD_EXTS = {".md", ".mdx"}

# Files we never rewrite
SKIP_BASENAMES = {"SUMMARY.md"}


# ---- Typer option singletons (avoid Ruff B008 in defaults) ----
CONFIG_OPT: Path = typer.Option(
    Path("tools/link_gov/config.yml"),
    help="Config path passed to load_config (only used for roots).",
)
DRY_RUN_OPT: bool = typer.Option(
    True, "--dry-run/--apply", help="Preview (default) or write changes."
)
BACKUP_DIR_OPT: Path | None = typer.Option(
    None, help="If applying, back up each changed file here first."
)
VERBOSE_OPT: bool = typer.Option(False, help="Verbose logging.")
PREVIEW_CSV_OPT: Path = typer.Option(
    CACHE_DIR / "denormalize_relatives_preview.csv",
    help="Where to write preview CSV.",
)


@dataclass
class Change:
    file: Path
    line_no: int
    link_text: str
    old_url: str
    new_url: str
    before: str
    after: str


def _iter_md_files(roots: Iterable[str]) -> list[Path]:
    out: list[Path] = []
    for d in roots:
        root = Path(d)
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if p.is_file() and p.suffix.lower() in MD_EXTS and p.name not in SKIP_BASENAMES:
                out.append(p)
    return out


def _split_anchor(u: str) -> tuple[str, str]:
    if "#" in u:
        path, frag = u.split("#", 1)
        return path, frag
    return u, ""


def _shortest_rel(from_file: Path, repo_path_str: str) -> str:
    """
    Compute shortest relative path from 'from_file' directory to 'repo_path_str'.
    Always return POSIX with no leading './'. Anchor handling is done by caller.
    """
    # Normalize to POSIX strings
    repo_path_str = repo_path_str.lstrip("./")
    # Build posix rel from source dir
    start = posixpath.dirname(from_file.as_posix()) or "."
    rel = posixpath.relpath(repo_path_str, start=start)
    # strip leading ./ if any
    return rel[2:] if rel.startswith("./") else rel


def _replace_in_file(p: Path) -> tuple[str, str, list[Change]]:
    original = p.read_text(encoding="utf-8")
    lines = original.splitlines(keepends=True)
    changes: list[Change] = []

    for i, line in enumerate(lines):
        line_no = i + 1

        def _one_sub(m, _line_no=line_no):
            text, url = m.group(1), m.group(2)

            # Only process repo-relative *page* links we normalized earlier
            if not REPO_PAGE_RE.match(url):
                return m.group(0)

            path_part, frag = _split_anchor(url)
            # sanity: only .md links
            if not path_part.endswith(".md"):
                return m.group(0)

            # Compute shortest relative path from this file to the repo path
            rel = _shortest_rel(p, path_part)

            new_url = f"{rel}#{frag}" if frag else rel

            # No-op? (already minimal relative)
            if new_url == url:
                return m.group(0)

            before = m.group(0)
            after = f"[{text}]({new_url})"

            changes.append(
                Change(
                    file=p,
                    line_no=_line_no,
                    link_text=text,
                    old_url=url,
                    new_url=new_url,
                    before=before,
                    after=after,
                )
            )
            return after

        lines[i] = MD_LINK_RE.sub(_one_sub, line)

    new_text = "".join(lines)
    return original, new_text, changes


def _write_preview_csv(path: Path, changes: list[Change]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["file", "line_no", "link_text", "old_url", "new_url"],
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
                }
            )


@app.command("run")
def run(
    config: Path = CONFIG_OPT,
    dry_run: bool = DRY_RUN_OPT,
    backup_dir: Path | None = BACKUP_DIR_OPT,
    verbose: bool = VERBOSE_OPT,
    preview_csv: Path = PREVIEW_CSV_OPT,
):
    """
    Convert repo-relative links (e.g. docs/apim/4.8/foo/bar.md#x) back to shortest relative links
    from each source file (e.g. ../foo/bar.md#x or foo/bar.md#x).
    """
    cfg = load_config(config)
    roots = cfg.get("docs_roots", ["docs/"])

    files = _iter_md_files(roots)
    all_changes: list[Change] = []

    for f in files:
        try:
            original, new_text, changes = _replace_in_file(f)
        except Exception as e:
            if verbose:
                typer.secho(f"[skip] {f}: {e}", fg=typer.colors.YELLOW)
            continue

        if not changes:
            continue

        all_changes.extend(changes)

        if not dry_run:
            if backup_dir:
                backup_target = (backup_dir / f).resolve()
                backup_target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, backup_target)
                if verbose:
                    typer.echo(f"[backup] {f} -> {backup_target}")
            f.write_text(new_text, encoding="utf-8")
            if verbose:
                typer.echo(f"[write]  {f} ({len(changes)} links)")

    if all_changes:
        _write_preview_csv(preview_csv, all_changes)

    typer.echo(
        f"{'DRY-RUN' if dry_run else 'APPLIED'}: {len(all_changes)} link(s) in "
        f"{len({c.file for c in all_changes})} file(s)."
    )
    if all_changes:
        typer.echo(f"Preview CSV → {preview_csv}")


if __name__ == "__main__":
    app()
