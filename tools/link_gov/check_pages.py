# tools/link_gov/check_pages.py
from __future__ import annotations

import csv
import posixpath
import re
from dataclasses import dataclass
from pathlib import Path

import typer

DOCS_ROOT = Path("docs")
CACHE_DIR = Path("tools/.cache")
SITE_BASE = "https://documentation.gravitee.io"

# ---- Typer option singletons (avoid Ruff B008 in defaults) ----
CSV_OUT_OPT: Path = typer.Option(
    CACHE_DIR / "page_links_audit.csv",
    "--csv-out",
    help="Write non-correct links here.",
)
DRY_RUN_OPT: bool = typer.Option(
    True,
    "--dry-run/--no-dry-run",
    help="Preview only (default: on)",
)
BACKUP_DIR_OPT: Path | None = typer.Option(
    None,
    "--backup-dir",
    help="Backup originals when applying.",
)

MD_LINK_RE = re.compile(r'(?<!\!)\[(?P<text>[^\]]+)\]\((?P<url>[^)\s]+)(?:\s+"[^"]*")?\)')
SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")

PV_RE = re.compile(r"^docs/([^/]+)/([^/]+)/")

app = typer.Typer(add_completion=False, help="Audit & autofix page links (no anchors).")


@dataclass
class PVIndex:
    """Index of valid targets for a product/version, from SUMMARY.md only."""

    product: str
    version: str
    root: Path  # e.g., docs/apim/4.8
    valid_rel: set[str]  # version-root-relative paths from SUMMARY.md (e.g., readme/core.md)


@dataclass
class Finding:
    src: str
    line: int
    text: str
    url: str
    classification: str  # correct | needs_reformat | broken | skipped
    reason: str
    suggest: str | None  # only for needs_reformat
    pv_src: tuple[str, str]  # (product, version)


# ----------------- helpers -----------------


def _pv_from_path(p: Path) -> tuple[str, str]:
    m = PV_RE.match(p.as_posix())
    if not m:
        return ("", "")
    return (m.group(1), m.group(2))


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="ignore")


def _is_absolute_site(url: str) -> bool:
    return url.startswith(SITE_BASE + "/")


def _is_relative(url: str) -> bool:
    return (not SCHEME_RE.match(url)) and (not url.startswith("/"))


def _norm_rel(s: str) -> str:
    s = s.replace("\\", "/")
    s = s.lstrip("./")
    s = re.sub(r"/{2,}", "/", s)
    return s


def _resolve_rel_to_version_root(src_file: Path, rel_url: str, pv_root: Path) -> str:
    """
    Resolve a relative URL against the *file's* directory, then express it as
    a path relative to the version root (for comparison with SUMMARY entries).
    """
    # Absolute filesystem path of the target
    base_dir = src_file.parent
    abs_target = (base_dir / rel_url).resolve()
    # Make both absolute paths comparable via POSIX strings
    try:
        rel_to_root = abs_target.relative_to(pv_root.resolve())
    except Exception:
        # Escaped the version root (e.g., ../.. to a different product/version)
        return _norm_rel(posixpath.normpath(rel_url))
    return _norm_rel(rel_to_root.as_posix())


def _pv_from_abs_site(url: str) -> tuple[str, str, str]:
    """
    Parse absolute site URL → (product, version, version-root-relative path)
    Example:
      https://documentation.gravitee.io/apim/4.8/getting-started/foo.md
      -> ("apim", "4.8", "getting-started/foo.md")
    """
    tail = url[len(SITE_BASE) :].lstrip("/")
    parts = tail.split("/", 2)
    if len(parts) < 3:
        return ("", "", "")
    product, version, rest = parts[0], parts[1], parts[2]
    return (product, version, _norm_rel(rest))


def _all_summary_paths(root: Path) -> set[str]:
    """
    Parse version-root SUMMARY.md for page links (no anchors).
    We trust SUMMARY as the source of truth for valid version-internal page paths.
    """
    summary = root / "SUMMARY.md"
    valid: set[str] = set()
    if not summary.exists():
        return valid
    for m in MD_LINK_RE.finditer(_read(summary)):
        url = m.group("url")
        if "#" in url:
            continue
        if SCHEME_RE.match(url) or url.startswith("/"):
            # ignore externals/absolutes in SUMMARY (should be rare)
            continue
        valid.add(_norm_rel(url))
    return valid


def _build_index() -> dict[tuple[str, str], PVIndex]:
    """
    Build PVIndex for every docs/<product>/<version>/ that has a SUMMARY.md.
    """
    idx: dict[tuple[str, str], PVIndex] = {}
    for p in DOCS_ROOT.glob("*/*/SUMMARY.md"):
        pv_root = p.parent
        product, version = _pv_from_path(pv_root / "DUMMY.md")
        if not product:
            continue
        idx[(product, version)] = PVIndex(
            product=product,
            version=version,
            root=pv_root,
            valid_rel=_all_summary_paths(pv_root),
        )
    return idx


# ----------------- audit -----------------


def audit_links(write_csv: Path | None = None) -> tuple[list[Finding], dict[str, int]]:
    """
    Scan all markdown files for page links (no anchors) and classify.
    """
    pv_index = _build_index()
    findings: list[Finding] = []
    counts = {"total": 0, "correct": 0, "needs_reformat": 0, "broken": 0, "skipped": 0}

    for md in DOCS_ROOT.rglob("*.md"):
        if md.name == "SUMMARY.md":
            continue
        src_pv = _pv_from_path(md)
        if not all(src_pv):
            # outside product/version structure; skip
            continue

        src_root = pv_index.get(src_pv)
        if not src_root:
            # No summary for this pv; skip this file entirely
            continue

        text = _read(md)
        for i, line in enumerate(text.splitlines(), start=1):
            for m in MD_LINK_RE.finditer(line):
                url = m.group("url")
                if "#" in url:
                    continue  # anchors are out of scope for this pass
                if url.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".bmp")):
                    continue  # image files are out of scope

                counts["total"] += 1
                link_text = m.group("text")

                if _is_relative(url):
                    # resolve to version root
                    resolved_rel = _resolve_rel_to_version_root(md, url, src_root.root)
                    # Did it escape the pv root? If so → should be absolute
                    escaped = (
                        not resolved_rel
                        or resolved_rel.startswith("../")
                        or resolved_rel.startswith("/")
                    )
                    if not escaped and resolved_rel in src_root.valid_rel:
                        findings.append(
                            Finding(
                                src=md.as_posix(),
                                line=i,
                                text=link_text,
                                url=url,
                                classification="correct",
                                reason="relative_within_pv",
                                suggest=None,
                                pv_src=src_pv,
                            )
                        )
                        counts["correct"] += 1
                    else:
                        # Try to detect if it is aiming another pv:
                        # crude heuristic: a relative that escapes pv shouldn't be used → needs absolute
                        # We *don't* try to guess existence across pv here (no guesswork).
                        counts["needs_reformat"] += 1
                        findings.append(
                            Finding(
                                src=md.as_posix(),
                                line=i,
                                text=link_text,
                                url=url,
                                classification="needs_reformat",
                                reason="relative_cross_pv_or_not_in_summary",
                                suggest=None,  # we won't invent the target
                                pv_src=src_pv,
                            )
                        )
                elif _is_absolute_site(url):
                    tgt_prod, tgt_ver, tgt_rel = _pv_from_abs_site(url)
                    if not tgt_prod:
                        counts["broken"] += 1
                        findings.append(
                            Finding(
                                src=md.as_posix(),
                                line=i,
                                text=link_text,
                                url=url,
                                classification="broken",
                                reason="malformed_absolute",
                                suggest=None,
                                pv_src=src_pv,
                            )
                        )
                        continue

                    tgt_idx = pv_index.get((tgt_prod, tgt_ver))
                    if not tgt_idx or tgt_rel not in tgt_idx.valid_rel:
                        counts["broken"] += 1
                        findings.append(
                            Finding(
                                src=md.as_posix(),
                                line=i,
                                text=link_text,
                                url=url,
                                classification="broken",
                                reason="absolute_target_not_in_summary",
                                suggest=None,
                                pv_src=src_pv,
                            )
                        )
                        continue

                    # Now it exists. If it’s the same pv → should be relative
                    if (tgt_prod, tgt_ver) == src_pv:
                        counts["needs_reformat"] += 1
                        findings.append(
                            Finding(
                                src=md.as_posix(),
                                line=i,
                                text=link_text,
                                url=url,
                                classification="needs_reformat",
                                reason="same_pv_absolute_should_be_relative",
                                suggest=_norm_rel(tgt_rel),
                                pv_src=src_pv,
                            )
                        )
                    else:
                        # cross-pv absolute is correct
                        counts["correct"] += 1
                        findings.append(
                            Finding(
                                src=md.as_posix(),
                                line=i,
                                text=link_text,
                                url=url,
                                classification="correct",
                                reason="cross_pv_absolute_ok",
                                suggest=None,
                                pv_src=src_pv,
                            )
                        )
                else:
                    # external absolute to another domain → ignore
                    counts["skipped"] += 1
                    findings.append(
                        Finding(
                            src=md.as_posix(),
                            line=i,
                            text=link_text,
                            url=url,
                            classification="skipped",
                            reason="external_or_root_absolute",
                            suggest=None,
                            pv_src=src_pv,
                        )
                    )

    # write CSV (non-correct only) for review
    if write_csv:
        write_csv.parent.mkdir(parents=True, exist_ok=True)
        with write_csv.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(
                f,
                fieldnames=[
                    "src",
                    "line",
                    "text",
                    "url",
                    "classification",
                    "reason",
                    "suggest",
                    "product",
                    "version",
                ],
            )
            w.writeheader()
            for r in findings:
                if r.classification == "correct":
                    continue
                w.writerow(
                    {
                        "src": r.src,
                        "line": r.line,
                        "text": r.text,
                        "url": r.url,
                        "classification": r.classification,
                        "reason": r.reason,
                        "suggest": r.suggest or "",
                        "product": r.pv_src[0],
                        "version": r.pv_src[1],
                    }
                )
    return findings, counts


# ----------------- apply (formatting-only) -----------------


def _apply_autofix(
    findings: list[Finding], dry_run: bool = True, backup_dir: Path | None = None
) -> tuple[int, int]:
    """
    Apply formatting-only changes:
      - absolute within same pv -> relative
      - (optional later) relative that escapes pv -> absolute [not applied here to avoid guesswork]
    Returns (files_changed, links_changed).
    """
    by_file: dict[str, list[Finding]] = {}
    for f in findings:
        if (
            f.classification == "needs_reformat"
            and f.reason == "same_pv_absolute_should_be_relative"
            and f.suggest
        ):
            by_file.setdefault(f.src, []).append(f)

    files_changed = 0
    links_changed = 0

    for src, items in by_file.items():
        path = Path(src)
        original = path.read_text(encoding="utf-8")
        lines = original.splitlines(keepends=True)
        changed_any = False

        for f in items:
            line_idx = f.line - 1
            line = lines[line_idx]

            def _sub(m, f=f):  # bind loop variable for closure safety
                url = m.group("url")
                if url == f.url:
                    new = f"[{m.group('text')}]({f.suggest})"
                    nonlocal links_changed, changed_any
                    links_changed += 1
                    changed_any = True
                    return new
                return m.group(0)

            lines[line_idx] = MD_LINK_RE.sub(_sub, line)

        if changed_any:
            files_changed += 1
            new_text = "".join(lines)
            if not dry_run:
                if backup_dir:
                    b = (backup_dir / path).resolve()
                    b.parent.mkdir(parents=True, exist_ok=True)
                    b.write_text(original, encoding="utf-8")
                path.write_text(new_text, encoding="utf-8")

    return files_changed, links_changed


# ----------------- CLI -----------------


@app.command()
def audit(
    csv_out: Path = CSV_OUT_OPT,
):
    """Audit page links (no anchors) and print counts."""
    findings, counts = audit_links(write_csv=csv_out)
    typer.echo(
        f"Links scanned: {counts['total']}\n"
        f"  correct:        {counts['correct']}\n"
        f"  needs_reformat: {counts['needs_reformat']}\n"
        f"  broken:         {counts['broken']}\n"
        f"  skipped:        {counts['skipped']}\n"
        f"CSV → {csv_out}"
    )


@app.command()
def autofix(
    dry_run: bool = DRY_RUN_OPT,
    backup_dir: Path | None = BACKUP_DIR_OPT,
):
    """Apply formatting-only fixes (safe refactors, no guesswork)."""
    findings, _ = audit_links(write_csv=CACHE_DIR / "page_links_audit.csv")
    files, links = _apply_autofix(findings, dry_run=dry_run, backup_dir=backup_dir)
    if dry_run:
        typer.secho(
            f"📝 DRY-RUN: would change {links} links across {files} files.", fg=typer.colors.BLUE
        )
    else:
        typer.secho(f"✅ Applied: {links} links across {files} files.", fg=typer.colors.GREEN)


if __name__ == "__main__":
    app()
