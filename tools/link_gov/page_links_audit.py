# tools/link_gov/page_links_audit.py
from __future__ import annotations

import csv
import json
import re
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

import typer

from .utils import CACHE_DIR

app = typer.Typer(
    add_completion=False,
    help="Audit & autofix *page links* (links ending in .md) against PV SUMMARY.md.",
)

# --- Config ---
DOCS_ROOT = Path("docs")
SUMMARY_BASENAME = "SUMMARY.md"
PV_RE = re.compile(r"^docs/([^/]+)/(\d+(?:\.\d+)*)/")  # docs/<product>/<version>/

# Absolute docs root (normalize trailing slash off)
DOCS_HOST = "https://documentation.gravitee.io".rstrip("/")
ABS_RE = re.compile(r"^https?://", re.I)

# Simple inline md link (no title capture on purpose)
MD_LINK = re.compile(r"(?<!\!)\[([^\]]+)\]\(([^)\s]+)\)")

# File types we consider "page links"
PAGE_EXTS = {".md", ".mdx"}

# CSV output names
MASTER_CSV = CACHE_DIR / "page_links_audit.all.csv"
PER_REASON_PREFIX = CACHE_DIR / "page_links_audit."

# Reasons (single source of truth)
REASONS = [
    "correct_relative",
    "needs_reformat_absolute_in_pv",
    "broken_relative_in_pv_not_in_summary",
    "correct_absolute_cross_pv",
    "broken_absolute_cross_pv",
    "external_absolute",
    "skipped_other_scheme",
]

# ---------- Data structures ----------


@dataclass
class PV:
    product: str
    version: str


@dataclass
class Finding:
    src_file: str
    line_no: int
    text: str
    url: str
    pv_product: str
    pv_version: str
    reason: str
    normalized_target: str  # canonical repo-relative target path for fixes when applicable


# ---------- Helpers ----------


def _iter_md_files(root: Path) -> Iterator[Path]:
    for p in root.rglob("*.md"):
        if p.name == SUMMARY_BASENAME:
            continue
        yield p


def _pv_from_path(p: Path) -> PV | None:
    m = PV_RE.match(p.as_posix())
    if not m:
        return None
    return PV(m.group(1), m.group(2))


def _read_summary_links(summary_path: Path) -> list[str]:
    """Return list of repo-relative .md paths that appear in this SUMMARY.md."""
    if not summary_path.exists():
        return []
    rels: list[str] = []
    txt = summary_path.read_text(encoding="utf-8", errors="ignore")
    for m in MD_LINK.finditer(txt):
        url = m.group(2)
        if url.startswith("#"):
            continue
        if not any(url.lower().endswith(ext) for ext in PAGE_EXTS):
            continue
        # Normalize to repo-relative path from this summary's directory
        repo_rel = (summary_path.parent / url).resolve().as_posix()
        # Re-express as repo-relative from repo root
        try:
            repo_rel = str(Path(repo_rel).relative_to(Path.cwd()))
        except Exception:
            pass
        rels.append(repo_rel.replace("\\", "/"))
    return rels


def _build_pv_index() -> dict[tuple[str, str], dict[str, str]]:
    """
    Build a product/version index from all SUMMARY.md files:
    key: (product, version)
    value: { repo_rel_path -> canonical_repo_rel_path }
    We store a dict for O(1) membership checks and canonicalization.
    """
    index: dict[tuple[str, str], dict[str, str]] = {}
    for summary in DOCS_ROOT.rglob(SUMMARY_BASENAME):
        pv = _pv_from_path(summary)
        if not pv:
            continue
        entries = _read_summary_links(summary)
        bucket: dict[str, str] = {}
        for abs_repo_rel in entries:
            # Normalize to posix & collapse ./ ../ based on repo root
            norm = Path(abs_repo_rel).as_posix()
            bucket[norm] = norm
        index[(pv.product, pv.version)] = bucket
    (CACHE_DIR / "pv_index.json").write_text(
        json.dumps({f"{k[0]}/{k[1]}": sorted(v.keys()) for k, v in index.items()}, indent=2),
        encoding="utf-8",
    )
    return index


def _is_absolute_root_docs(u: str) -> bool:
    return u.startswith(DOCS_HOST + "/")


def _split_abs_root(u: str) -> tuple[str, str, str] | None:
    """
    Given https://documentation.gravitee.io/<product>/<version>/<rest>
    return (product, version, rest) or None
    """
    if not _is_absolute_root_docs(u):
        return None
    tail = u[len(DOCS_HOST) :].lstrip("/")
    parts = tail.split("/", 2)
    if len(parts) < 3:
        return None
    product, version, rest = parts[0], parts[1], parts[2]
    return product, version, rest


def _canonical_repo_path_from_relative(src_file: Path, rel_url: str) -> str:
    """
    Resolve a relative URL like '../../foo/bar.md' against the source file's directory,
    collapse ./ and ../, and return a repo-relative POSIX path, e.g.:
      'docs/apim/4.8/getting-started/local-install-with-docker.md'
    """
    try:
        abs_path = (src_file.parent / rel_url).resolve()
        repo_rel = abs_path.relative_to(Path.cwd()).as_posix()
        return repo_rel
    except Exception:
        # Fallback if resolve()/relative_to() can’t be computed (unlikely in this repo):
        import posixpath

        return posixpath.normpath((src_file.parent / rel_url).as_posix())


# ---------- Audit ----------


def _scan_page_links(pv_index: dict[tuple[str, str], dict[str, str]]) -> list[Finding]:
    out: list[Finding] = []

    for src in _iter_md_files(DOCS_ROOT):
        pv = _pv_from_path(src)
        pv_product = pv.product if pv else ""
        pv_version = pv.version if pv else ""

        lines = src.read_text(encoding="utf-8", errors="ignore").splitlines()
        for i, line in enumerate(lines, 1):
            for m in MD_LINK.finditer(line):
                url = m.group(2)
                text = m.group(1)

                # Skip anchors-only, mailto, tel, images or non-page links
                if url.startswith("#") or url.startswith("mailto:") or url.startswith("tel:"):
                    out.append(
                        Finding(
                            src.as_posix(),
                            i,
                            text,
                            url,
                            pv_product,
                            pv_version,
                            "skipped_other_scheme",
                            "",
                        )
                    )
                    continue

                # External (non Gravitee docs) absolute links
                if ABS_RE.match(url) and not _is_absolute_root_docs(url):
                    out.append(
                        Finding(
                            src.as_posix(),
                            i,
                            text,
                            url,
                            pv_product,
                            pv_version,
                            "external_absolute",
                            "",
                        )
                    )
                    continue

                # Absolute root into docs host?
                if _is_absolute_root_docs(url):
                    split = _split_abs_root(url)
                    if not split:
                        out.append(
                            Finding(
                                src.as_posix(),
                                i,
                                text,
                                url,
                                pv_product,
                                pv_version,
                                "skipped_other_scheme",
                                "",
                            )
                        )
                        continue
                    tgt_product, tgt_version, rest = split
                    if not any(rest.lower().endswith(ext) for ext in PAGE_EXTS):
                        out.append(
                            Finding(
                                src.as_posix(),
                                i,
                                text,
                                url,
                                pv_product,
                                pv_version,
                                "skipped_other_scheme",
                                "",
                            )
                        )
                        continue
                    # Build canonical repo path for lookup
                    repo_rel = f"docs/{tgt_product}/{tgt_version}/{rest}".replace("\\", "/")
                    repo_rel = str(Path(repo_rel).resolve().relative_to(Path.cwd()).as_posix())
                    exists = repo_rel in pv_index.get((tgt_product, tgt_version), {})
                    if pv and tgt_product == pv.product and tgt_version == pv.version:
                        # Same PV: should be relative
                        reason = (
                            "needs_reformat_absolute_in_pv"
                            if exists
                            else "broken_relative_in_pv_not_in_summary"
                        )
                        out.append(
                            Finding(
                                src.as_posix(),
                                i,
                                text,
                                url,
                                pv_product,
                                pv_version,
                                reason,
                                repo_rel,
                            )
                        )
                    else:
                        out.append(
                            Finding(
                                src.as_posix(),
                                i,
                                text,
                                url,
                                pv_product,
                                pv_version,
                                (
                                    "correct_absolute_cross_pv"
                                    if exists
                                    else "broken_absolute_cross_pv"
                                ),
                                repo_rel,
                            )
                        )
                    continue

                # Relative link
                if not any(url.lower().endswith(ext) for ext in PAGE_EXTS):
                    out.append(
                        Finding(
                            src.as_posix(),
                            i,
                            text,
                            url,
                            pv_product,
                            pv_version,
                            "skipped_other_scheme",
                            "",
                        )
                    )
                    continue

                if not pv:
                    # Relative page link outside a PV tree — skip-as-other
                    out.append(
                        Finding(src.as_posix(), i, text, url, "", "", "skipped_other_scheme", "")
                    )
                    continue

                repo_rel = _canonical_repo_path_from_relative(src, url)
                exists = repo_rel in pv_index.get((pv.product, pv.version), {})
                out.append(
                    Finding(
                        src.as_posix(),
                        i,
                        text,
                        url,
                        pv.product,
                        pv.version,
                        "correct_relative" if exists else "broken_relative_in_pv_not_in_summary",
                        repo_rel,
                    )
                )
    return out


def _write_csvs(findings: list[Finding]) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    master_rows = []
    per_reason: dict[str, list[dict]] = {r: [] for r in REASONS}

    for f in findings:
        row = {
            "src": f.src_file,
            "line": f.line_no,
            "text": f.text,
            "url": f.url,
            "pv_product": f.pv_product,
            "pv_version": f.pv_version,
            "reason": f.reason,
            "normalized_target": f.normalized_target,
        }
        master_rows.append(row)
        if f.reason in per_reason:
            per_reason[f.reason].append(row)

    # master
    with MASTER_CSV.open("w", newline="", encoding="utf-8") as fo:
        w = csv.DictWriter(
            fo,
            fieldnames=(
                list(master_rows[0].keys())
                if master_rows
                else [
                    "src",
                    "line",
                    "text",
                    "url",
                    "pv_product",
                    "pv_version",
                    "reason",
                    "normalized_target",
                ]
            ),
        )
        w.writeheader()
        for r in master_rows:
            w.writerow(r)

    # per reason
    for reason, rows in per_reason.items():
        path = PER_REASON_PREFIX.with_name(PER_REASON_PREFIX.name + f"{reason}.csv")
        with path.open("w", newline="", encoding="utf-8") as fo:
            w = csv.DictWriter(
                fo,
                fieldnames=(
                    list(rows[0].keys())
                    if rows
                    else [
                        "src",
                        "line",
                        "text",
                        "url",
                        "pv_product",
                        "pv_version",
                        "reason",
                        "normalized_target",
                    ]
                ),
            )
            w.writeheader()
            for r in rows:
                w.writerow(r)


def _print_summary(findings: list[Finding]) -> None:
    total = len(findings)
    counts: dict[str, int] = {r: 0 for r in REASONS}
    for f in findings:
        if f.reason in counts:
            counts[f.reason] += 1
    typer.secho(
        "\nPage link audit (page links = URLs ending in .md or .mdx)\n", fg=typer.colors.BLUE
    )
    typer.echo(f"Total links scanned: {total}")
    for k in REASONS:
        typer.echo(f"  • {k}: {counts[k]}")

    typer.echo("\nCSV (master): " + MASTER_CSV.as_posix())
    typer.echo("CSV (per reason):")
    for k in REASONS:
        p = PER_REASON_PREFIX.with_name(PER_REASON_PREFIX.name + f"{k}.csv")
        typer.echo(f"  - {k}: {p.as_posix()}")


# ---------- Fix (dry-run by default) ----------


def _rel_from_src(src_file: Path, repo_rel_target: str) -> str:
    """Make a relative link from src_file to repo_rel_target."""
    try:
        rel = Path(repo_rel_target).relative_to(src_file.parent)
        return rel.as_posix()
    except Exception:
        # Fallback: best-effort relativize
        return Path(repo_rel_target).as_posix()


def _apply_fixes(findings: list[Finding], dry_run: bool = True) -> tuple[int, int]:
    """
    Currently only rewrites:
      - needs_reformat_absolute_in_pv → make relative to src
    Leaves broken_* alone (logged in CSV); we can extend later when targets are discoverable.
    """
    files_changed = 0
    links_changed = 0

    # group by src file
    by_src: dict[str, list[Finding]] = {}
    for f in findings:
        if f.reason == "needs_reformat_absolute_in_pv":
            by_src.setdefault(f.src_file, []).append(f)

    for src_path, to_fix in by_src.items():
        p = Path(src_path)
        txt = p.read_text(encoding="utf-8", errors="ignore")
        orig = txt

        def repl(m, to_fix=to_fix, p=p):  # bind loop vars for closure safety (Ruff B023)
            text = m.group(1)
            url = m.group(2)
            for f in to_fix:
                if url == f.url:
                    rel = _rel_from_src(p, f.normalized_target)
                    nonlocal links_changed
                    links_changed += 1
                    return f"[{text}]({rel})"
            return m.group(0)

        txt = MD_LINK.sub(repl, txt)

        if txt != orig:
            files_changed += 1
            if not dry_run:
                p.write_text(txt, encoding="utf-8")

    return files_changed, links_changed


# ---------- CLI ----------


@app.command()
def index():
    """Build PV index from SUMMARY.md files (writes tools/.cache/pv_index.json)."""
    idx = _build_pv_index()
    typer.secho(
        f"Indexed {sum(len(v) for v in idx.values())} page entries across {len(idx)} PVs.",
        fg=typer.colors.GREEN,
    )
    typer.echo(f"Wrote → {CACHE_DIR / 'pv_index.json'}")


@app.command("audit-cmd")
def audit_cmd():
    """Audit page links and write CSVs (master + per reason)."""
    idx = _build_pv_index()
    findings = _scan_page_links(idx)
    _write_csvs(findings)
    _print_summary(findings)


@app.command()
def fix(dry_run: bool = True):
    """
    Apply safe autofixes (currently: rewrite absolute-in-PV to relative).
    """
    # require a fresh index for safety
    idx = _build_pv_index()
    findings = _scan_page_links(idx)
    files, links = _apply_fixes(findings, dry_run=dry_run)
    if dry_run:
        typer.secho(
            f"📝 DRY-RUN: would change {links} links across {files} files.", fg=typer.colors.BLUE
        )
    else:
        typer.secho(
            f"✅ Applied changes: {links} links across {files} files.", fg=typer.colors.GREEN
        )


if __name__ == "__main__":
    app()
