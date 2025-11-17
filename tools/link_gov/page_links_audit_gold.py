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

VERSION_RE = re.compile(r"^\d+(?:\.\d+)*(?:\.x)?$")


def _looks_like_version(s: str) -> bool:
    """Return True if s looks like a version: 4, 4.8, 4.8.1, 4.8.x, etc."""
    return bool(VERSION_RE.match(s))


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
    "relative_exists_not_in_summary",
    "needs_reformat_absolute_in_pv",
    "broken_relative_in_pv_not_in_summary",
    "correct_absolute_cross_pv",
    "broken_absolute_cross_pv",
    "external_absolute",
    "skipped_other_scheme",
]


# --- PV helpers: convert repo-relative to PV-root-relative and compute PV key ---
# Repo layout assumed: docs/<product>/<version>/...
PV_PREFIX_RE = re.compile(r"^docs/[^/]+/[^/]+/")


def _repo_rel_to_pv_rel(repo_rel: str) -> str:
    """
    Convert a repo-relative path like 'docs/apim/4.8/foo/bar.md' to a
    PV-root-relative 'foo/bar.md' by stripping the 'docs/<product>/<version>/' prefix.
    Accepts leading './' and normalizes separators.
    """
    s = repo_rel.replace("\\", "/").lstrip("./")
    s = re.sub(r"/{2,}", "/", s)
    return PV_PREFIX_RE.sub("", s).lstrip("/")


def _pv_key_from_repo_path(repo_path: Path) -> str | None:
    """
    From a repo path like 'docs/apim/4.8/foo/bar.md', return the PV key 'apim/4.8'.
    Returns None if the path doesn't match docs/<product>/<version>/...
    """
    parts = repo_path.as_posix().split("/")
    if len(parts) >= 4 and parts[0] == "docs":
        return f"{parts[1]}/{parts[2]}"
    return None


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
    """
    Return PV-root-relative page paths referenced by this SUMMARY.md.

    Accepts any of these SUMMARY forms and maps them to canonical page paths:
      - 'foo/bar.md' or 'foo/bar.mdx' -> keep as-is
      - 'foo/bar' or 'foo/bar/'       -> generate candidates:
            'foo/bar.md', 'foo/bar.mdx',
            'foo/bar/README.md', 'foo/bar/README.mdx',
            'foo/bar/index.md',  'foo/bar/index.mdx'
    Skips anchors, externals (scheme://), and root-absolute (/).
    Normalizes to POSIX and collapses duplicate slashes.
    """
    if not summary_path.exists():
        return []
    results: set[str] = set()
    txt = summary_path.read_text(encoding="utf-8", errors="ignore")

    for m in MD_LINK.finditer(txt):
        raw = m.group(2)

        # Skip anchors, externals, or site-absolute links
        if (
            raw.startswith("#")
            or re.match(r"^[a-zA-Z][a-zA-Z0-9+.\-]*:", raw)
            or raw.startswith("/")
        ):
            continue

        # Strip fragment, normalize slashes, strip leading './', collapse '//' runs
        url = raw.split("#", 1)[0].replace("\\", "/").lstrip("./")
        url = re.sub(r"/{2,}", "/", url)

        # Remove a single trailing slash for directory-style entries
        url_noslash = url[:-1] if url.endswith("/") else url
        lower = url_noslash.lower()

        # Explicit page link with known extension: keep as-is
        if any(lower.endswith(ext) for ext in PAGE_EXTS):
            results.add(url_noslash)
            continue

        # Extensionless or directory entries -> add canonical candidates
        candidates: list[str] = []
        for ext in (".md", ".mdx"):
            candidates.append(f"{url_noslash}{ext}")
        for base in ("README", "index"):
            for ext in (".md", ".mdx"):
                candidates.append(f"{url_noslash}/{base}{ext}")

        for c in candidates:
            results.add(re.sub(r"/{2,}", "/", c))

    return sorted(results)


def _build_pv_index() -> dict[str, set[str]]:
    """
    Build a mapping from PV key ('<product>/<version>') to a set of
    PV-root-relative page paths that appear in that PV's SUMMARY.md.

    Example:
      'apim/4.8' -> {
          'getting-started/README.md',
          'create-and-configure-apis/configure-v4-apis/entrypoints/http-post.md',
          ...
      }

    Side effect: writes a debug JSON snapshot to tools/.cache/pv_index.json
    so we can inspect what the audit will consider "in SUMMARY" for each PV.
    """
    from collections import defaultdict

    pv_index: dict[str, set[str]] = defaultdict(set)

    # Walk all PVs: docs/<product>/<version>/SUMMARY.md
    for summary in DOCS_ROOT.rglob(SUMMARY_BASENAME):
        # Compute PV key like 'apim/4.8'
        parts = summary.as_posix().split("/")
        if len(parts) < 4 or parts[0] != "docs":
            continue
        pv_key = f"{parts[1]}/{parts[2]}"

        # Parse SUMMARY links; these are PV-root-relative (by design of _read_summary_links)
        for pv_rel in _read_summary_links(summary):
            # Normalize: POSIX separators, strip ./ and leading /, collapse //
            s = pv_rel.replace("\\", "/").lstrip("./").lstrip("/")
            s = re.sub(r"/{2,}", "/", s)
            pv_index[pv_key].add(s)

    # Write a deterministic snapshot for debugging
    try:
        debug_json = {k: sorted(v) for k, v in sorted(pv_index.items())}
        Path("tools/.cache/pv_index.json").write_text(
            json.dumps(debug_json, indent=2),
            encoding="utf-8",
        )
    except Exception:
        pass

    return pv_index


def _is_absolute_root_docs(u: str) -> bool:
    return u.startswith(DOCS_HOST + "/")


def _split_abs_root(u: str) -> tuple[str, str | None, str] | None:
    """
    Given https://documentation.gravitee.io/<product>/<version>/<rest>
    OR    https://documentation.gravitee.io/<product>/<non-pv-tail>

    Return (product, version_or_None, rest_tail) or None.

    - If the second segment looks like a version ("4.8", "4.9.1", "4.8.x"),
      we treat it as PV: (product, version, rest).
    - Otherwise, we treat everything after <product> as a "non-PV tail":
      (product, None, "<second>/<third>/...").
    """
    if not _is_absolute_root_docs(u):
        return None

    tail = u[len(DOCS_HOST) :].lstrip("/")  # e.g. "am/4.8/guides/applications"
    parts = tail.split("/")

    if len(parts) < 2:
        return None

    product = parts[0]

    if len(parts) == 2:
        # e.g. /am/guides  (no version, no deeper rest)
        # non-PV: product + tail
        non_pv_tail = parts[1]
        return product, None, non_pv_tail

    # >= 3 segments
    second = parts[1]
    rest = "/".join(parts[2:])  # "guides/applications" or "foo/bar"

    if _looks_like_version(second):
        # Standard PV path: /<product>/<version>/<rest>
        return product, second, rest

    # Non-PV docs path: treat everything after <product> as a logical tail
    # e.g. "guides/applications"
    non_pv_tail = "/".join(parts[1:])
    return product, None, non_pv_tail


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


def _scan_page_links(pv_index: dict[str, set[str]]) -> list[Finding]:
    out: list[Finding] = []

    for src in _iter_md_files(DOCS_ROOT):
        pv = _pv_from_path(src)
        pv_product = pv.product if pv else ""
        pv_version = pv.version if pv else ""

        lines = src.read_text(encoding="utf-8", errors="ignore").splitlines()
        for i, line in enumerate(lines, 1):
            for m in MD_LINK.finditer(line):
                text = m.group(1)
                url_raw = m.group(2)
                url = url_raw.split("#", 1)[0]  # strip fragment for all checks

                # Skip anchors-only, mailto, tel
                if (
                    url_raw.startswith("#")
                    or url_raw.startswith("mailto:")
                    or url_raw.startswith("tel:")
                ):
                    out.append(
                        Finding(
                            src.as_posix(),
                            i,
                            text,
                            url_raw,
                            pv_product,
                            pv_version,
                            "skipped_other_scheme",
                            "",
                        )
                    )
                    continue

                # External (non Gravitee docs) absolute links
                if ABS_RE.match(url_raw) and not _is_absolute_root_docs(url):
                    out.append(
                        Finding(
                            src.as_posix(),
                            i,
                            text,
                            url_raw,
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
                                url_raw,
                                pv_product,
                                pv_version,
                                "external_absolute",
                                "",
                            )
                        )
                        continue

                    abs_product, abs_version, abs_tail = split
                    # Normalize the tail to match how _build_pv_index() stores entries
                    abs_tail_norm = abs_tail.replace("\\", "/").lstrip("./").lstrip("/")
                    abs_tail_norm = re.sub(r"/{2,}", "/", abs_tail_norm)

                    # PV key of the *source* page, e.g. "am/4.5"
                    cur_pv_key = _pv_key_from_repo_path(src)

                    # ---------- NEW: non-PV docs paths ----------
                    if abs_version is None:
                        #
                        # e.g. https://documentation.gravitee.io/am/guides/applications
                        # abs_product = "am", abs_version = None, abs_tail_norm = "guides/applications"
                        #
                        resolved_repo_rel = ""
                        reason = "external_absolute"  # safe default

                        if cur_pv_key and cur_pv_key.startswith(abs_product + "/"):
                            # Same product; treat tail as PV-root-relative in *this* PV
                            tgt_pv_key = cur_pv_key  # e.g. "am/4.5"
                            # docs/<product>/<version>/<tail>
                            candidate_base = f"docs/{tgt_pv_key}/{abs_tail_norm}"

                            # Try common page candidates in this PV
                            candidates = [
                                Path(candidate_base + ".md"),
                                Path(candidate_base + ".mdx"),
                                Path(candidate_base) / "README.md",
                                Path(candidate_base) / "README.mdx",
                                Path(candidate_base) / "index.md",
                                Path(candidate_base) / "index.mdx",
                            ]

                            for c in candidates:
                                if c.exists():
                                    resolved_repo_rel = c.as_posix()
                                    break

                            if resolved_repo_rel:
                                # Treat as a same-PV absolute that should be relative
                                reason = "needs_reformat_absolute_in_pv"

                        if resolved_repo_rel and reason == "needs_reformat_absolute_in_pv":
                            out.append(
                                Finding(
                                    src.as_posix(),
                                    i,
                                    text,
                                    url_raw,
                                    pv_product,
                                    pv_version,
                                    reason,
                                    resolved_repo_rel,
                                )
                            )
                        else:
                            # We couldn't safely map this non-PV docs URL → leave as external_absolute
                            out.append(
                                Finding(
                                    src.as_posix(),
                                    i,
                                    text,
                                    url_raw,
                                    pv_product,
                                    pv_version,
                                    "external_absolute",
                                    "",
                                )
                            )

                        continue  # handled non-PV absolute docs case

                    # ---------- Existing PV-aware logic (versioned paths) ----------

                    # Build PV-root-relative candidate paths for this absolute URL.
                    # Handles both explicit .md/.mdx and extension-less /dir/page forms.
                    if any(abs_tail_norm.lower().endswith(ext) for ext in PAGE_EXTS):
                        # URL already has .md / .mdx → use exactly that
                        abs_candidates: list[str] = [abs_tail_norm]
                    else:
                        abs_candidates: list[str] = []
                        # page.md / page.mdx
                        for ext in (".md", ".mdx"):
                            abs_candidates.append(f"{abs_tail_norm}{ext}")
                        # page/README*.mdx and page/index*.mdx
                        for base in ("README", "index"):
                            for ext in (".md", ".mdx"):
                                abs_candidates.append(f"{abs_tail_norm}/{base}{ext}")

                    # Choose a canonical candidate and check on-disk existence.
                    # We prefer "the first one that actually exists", otherwise
                    # just use the first candidate string as our normalized target.
                    canonical_rel = abs_candidates[0]
                    exists = False
                    for rel in abs_candidates:
                        candidate_path = DOCS_ROOT / abs_product / abs_version / rel
                        if candidate_path.exists():
                            canonical_rel = rel
                            exists = True
                            break

                    repo_rel = f"docs/{abs_product}/{abs_version}/{canonical_rel}"

                    # Cross-PV vs same-PV
                    tgt_pv_key = f"{abs_product}/{abs_version}"  # pv of the *target* link

                    if cur_pv_key == tgt_pv_key:
                        #
                        # Same-PV absolute link:
                        #   - should be relative
                        #   - classify as needs_reformat_absolute_in_pv if the target is in SUMMARY
                        #   - otherwise as broken_relative_in_pv_not_in_summary
                        #
                        in_summary = False
                        if cur_pv_key and cur_pv_key in pv_index:
                            pv_set = pv_index[cur_pv_key]
                            # Any candidate that appears in SUMMARY makes this "in_summary"
                            in_summary = any(rel in pv_set for rel in abs_candidates)

                        reason = (
                            "needs_reformat_absolute_in_pv"
                            if in_summary
                            else "broken_relative_in_pv_not_in_summary"
                        )
                        out.append(
                            Finding(
                                src.as_posix(),
                                i,
                                text,
                                url_raw,
                                pv_product,
                                pv_version,
                                reason,
                                repo_rel,
                            )
                        )
                    else:
                        #
                        # Cross-PV absolute link:
                        #   - "correct" if the target either exists on disk OR appears
                        #     in the target PV's SUMMARY.md
                        #   - "broken" only if it is missing from both disk and SUMMARY
                        #
                        in_summary_tgt = False
                        if tgt_pv_key in pv_index:
                            pv_set = pv_index[tgt_pv_key]
                            in_summary_tgt = any(rel in pv_set for rel in abs_candidates)

                        reason = (
                            "correct_absolute_cross_pv"
                            if (exists or in_summary_tgt)
                            else "broken_absolute_cross_pv"
                        )

                        out.append(
                            Finding(
                                src.as_posix(),
                                i,
                                text,
                                url_raw,
                                pv_product,
                                pv_version,
                                reason,
                                repo_rel,
                            )
                        )

                    continue  # handled absolute-root case

                # Relative link: only consider page links (.md/.mdx)
                if not any(url.lower().endswith(ext) for ext in PAGE_EXTS):
                    out.append(
                        Finding(
                            src.as_posix(),
                            i,
                            text,
                            url_raw,
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
                        Finding(
                            src.as_posix(), i, text, url_raw, "", "", "skipped_other_scheme", ""
                        )
                    )
                    continue

                # Compute PV key from the *source* page
                pv_key = _pv_key_from_repo_path(src)  # e.g. "apim/4.8"

                # --- Normalize target & check SUMMARY membership ---
                # Treat repo-rooted docs paths as canonical; only resolve truly relative paths.
                u_norm = url.replace("\\", "/")

                if u_norm.startswith("docs/") or u_norm.startswith("/docs/"):
                    # Already repo-rooted (or site-absolute pointing at repo root) → use as-is
                    repo_rel_target = re.sub(r"/{2,}", "/", u_norm.lstrip("/"))
                else:
                    # Resolve e.g. "../foo/bar.md" against the source file
                    repo_rel_target = _canonical_repo_path_from_relative(src, url)

                # Convert repo-relative target to PV-root-relative for membership check
                pv_rel = _repo_rel_to_pv_rel(repo_rel_target)

                # --- Check SUMMARY membership and on-disk existence ---
                in_summary = False
                if pv_key:
                    same_file_pv_rel = _repo_rel_to_pv_rel(src.as_posix())
                    if pv_rel == same_file_pv_rel:
                        in_summary = True
                    elif pv_key in pv_index:
                        in_summary = pv_rel in pv_index[pv_key]

                exists_on_disk = Path(repo_rel_target).exists()

                if in_summary:
                    reason = "correct_relative"
                elif exists_on_disk:
                    reason = "relative_exists_not_in_summary"
                else:
                    reason = "broken_relative_in_pv_not_in_summary"

                out.append(
                    Finding(
                        src.as_posix(),
                        i,
                        text,
                        url_raw,
                        pv_product,
                        pv_version,
                        reason,
                        repo_rel_target,
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
    """Return the shortest POSIX-style relative path from src_file to repo_rel_target."""
    try:
        import os

        rel = os.path.relpath(repo_rel_target, start=src_file.parent.as_posix())
        # Normalize to POSIX separators for markdown
        return rel.replace("\\", "/")
    except Exception:
        # Fallback: best-effort
        return Path(repo_rel_target).as_posix()


def _apply_fixes(findings: list[Finding], dry_run: bool = True) -> tuple[int, int]:
    """
    Currently only rewrites:
      - needs_reformat_absolute_in_pv → make relative to src
    Leaves broken_* alone (logged in CSV); we can extend later when targets are discoverable.
    """
    files_changed = 0
    links_changed = 0

    by_src: dict[str, list[Finding]] = {}
    for f in findings:
        if f.reason in {
            "needs_reformat_absolute_in_pv",
            "relative_exists_not_in_summary",
            "correct_relative",  # <-- include this so every valid relative link gets shortened
        }:
            by_src.setdefault(f.src_file, []).append(f)

    for src_path, to_fix in by_src.items():
        p = Path(src_path)
        txt = p.read_text(encoding="utf-8", errors="ignore")
        orig = txt

        def repl(m, to_fix=to_fix, p=p):  # bind loop vars for closure safety (Ruff B023)
            text = m.group(1)
            url_in_doc = m.group(2)

            for f in to_fix:
                if url_in_doc == f.url:
                    # Compute the normalized shortest relative path from src -> canonical repo target
                    rel = _rel_from_src(p, f.normalized_target)

                    # Preserve original fragment if present
                    frag = ""
                    if "#" in url_in_doc:
                        frag = "#" + url_in_doc.split("#", 1)[1]

                    new_href = f"{rel}{frag}"

                    # Only replace if it actually changes something (idempotent)
                    if new_href != url_in_doc:
                        nonlocal links_changed
                        links_changed += 1
                        return f"[{text}]({new_href})"

                    # no-op if identical
                    return m.group(0)

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
