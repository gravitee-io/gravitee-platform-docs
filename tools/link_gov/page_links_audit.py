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
    help=(
        "Audit documentation page links (relative and absolute), write master + per-category CSVs, "
        "and optionally apply safe autofixes to existing, resolvable page links."
    ),
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
PER_CATEGORY_PREFIX = CACHE_DIR / "page_links_audit."

# Categories (single source of truth)
CATEGORIES = [
    # GitBook-flagged broken links (contain "broken-reference")
    "broken_ref",
    # PV-aware relative page links (source in docs/<product>/<version>/...)
    "inpv_rel_exists_sum",
    "inpv_rel_exists_nosum",
    "inpv_rel_missing_sum",
    "inpv_rel_missing_nosum",
    # PV-aware absolute (/docs/...) links within same PV
    "inpv_abs_exists_sum_reformat",
    "inpv_abs_missing_sum",
    "inpv_abs_missing_nosum",
    # Cross-PV absolute (/docs/...) links
    "xpv_abs_exists_sum",
    "xpv_abs_exists_nosum",
    "xpv_abs_missing_sum",
    "xpv_abs_missing_nosum",
    # External HTTP(S)
    "ext_abs",
    # Non-PV relative page links
    "rel_nonpv_exists",
    "rel_nonpv_missing",
    # Non-page URL types
    "anchor_only",
    "mailto",
    "tel",
    "nonpage_link",
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
    category: str
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

                # Classify anchors-only, mailto, tel explicitly
                if url_raw.startswith("#"):
                    out.append(
                        Finding(
                            src.as_posix(),
                            i,
                            text,
                            url_raw,
                            pv_product,
                            pv_version,
                            "anchor_only",
                            "",
                        )
                    )
                    continue

                if url_raw.startswith("mailto:"):
                    out.append(
                        Finding(
                            src.as_posix(),
                            i,
                            text,
                            url_raw,
                            pv_product,
                            pv_version,
                            "mailto",
                            "",
                        )
                    )
                    continue

                if url_raw.startswith("tel:"):
                    out.append(
                        Finding(
                            src.as_posix(),
                            i,
                            text,
                            url_raw,
                            pv_product,
                            pv_version,
                            "tel",
                            "",
                        )
                    )
                    continue

                # GitBook "broken-reference" marker: treat as its own broken category
                if "broken-reference" in url_raw:
                    out.append(
                        Finding(
                            src.as_posix(),
                            i,
                            text,
                            url_raw,
                            pv_product,
                            pv_version,
                            "broken_ref",
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
                            "ext_abs",
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
                                "nonpage_link",
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
                            out.append(
                                Finding(
                                    src.as_posix(),
                                    i,
                                    text,
                                    url_raw,
                                    pv_product,
                                    pv_version,
                                    "inpv_abs_exists_sum_reformat",
                                    resolved_repo_rel,
                                )
                            )
                        else:
                            # We couldn't safely map this non-PV docs URL → leave as ext_abs
                            out.append(
                                Finding(
                                    src.as_posix(),
                                    i,
                                    text,
                                    url_raw,
                                    pv_product,
                                    pv_version,
                                    "ext_abs",
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
                        #   - if target exists → inpv_abs_exists_sum_reformat (should be made relative)
                        #   - if target missing:
                        #       - inpv_abs_missing_sum    (target path in SUMMARY)
                        #       - inpv_abs_missing_nosum (target path not in SUMMARY)
                        #
                        in_summary = False
                        if cur_pv_key and cur_pv_key in pv_index:
                            pv_set = pv_index[cur_pv_key]
                            # Any candidate that appears in SUMMARY makes this "in_summary"
                            in_summary = any(rel in pv_set for rel in abs_candidates)

                        if exists:
                            category = "inpv_abs_exists_sum_reformat"
                        else:
                            category = (
                                "inpv_abs_missing_sum" if in_summary else "inpv_abs_missing_nosum"
                            )

                        out.append(
                            Finding(
                                src.as_posix(),
                                i,
                                text,
                                url_raw,
                                pv_product,
                                pv_version,
                                category,
                                repo_rel,
                            )
                        )
                    else:
                        #
                        # Cross-PV absolute link:
                        #   - if target exists:
                        #       - xpv_abs_exists_sum    (target path in target PV SUMMARY)
                        #       - xpv_abs_exists_nosum (target path not in target PV SUMMARY)
                        #   - if target missing:
                        #       - xpv_abs_missing_sum    (in target PV SUMMARY)
                        #       - xpv_abs_missing_nosum (not in target PV SUMMARY)
                        #
                        in_summary_tgt = False
                        if tgt_pv_key in pv_index:
                            pv_set = pv_index[tgt_pv_key]
                            in_summary_tgt = any(rel in pv_set for rel in abs_candidates)

                        if exists:
                            category = (
                                "xpv_abs_exists_sum" if in_summary_tgt else "xpv_abs_exists_nosum"
                            )
                        else:
                            category = (
                                "xpv_abs_missing_sum" if in_summary_tgt else "xpv_abs_missing_nosum"
                            )

                        out.append(
                            Finding(
                                src.as_posix(),
                                i,
                                text,
                                url_raw,
                                pv_product,
                                pv_version,
                                category,
                                repo_rel,
                            )
                        )

                    continue  # handled absolute-root case

                # ---------- Relative link handling ----------
                # Root-relative URLs that are not under /docs/... are not treated as page links
                if url.startswith("/") and not url.startswith("/docs/"):
                    out.append(
                        Finding(
                            src.as_posix(),
                            i,
                            text,
                            url_raw,
                            pv_product,
                            pv_version,
                            "nonpage_link",
                            "",
                        )
                    )
                    continue
                lower_url = url.lower()
                is_page_like = any(lower_url.endswith(ext) for ext in PAGE_EXTS)
                # Treat trailing '/' as a directory-style page link (README in that folder)
                is_dir_style = not is_page_like and url.endswith("/")

                # Ignore non-page links (images, downloads, etc.) that don't look like docs pages
                if not is_page_like and not is_dir_style:
                    out.append(
                        Finding(
                            src.as_posix(),
                            i,
                            text,
                            url_raw,
                            pv_product,
                            pv_version,
                            "nonpage_link",
                            "",
                        )
                    )
                    continue

                # --- Normalize to a repo-relative base path ---
                u_norm = url.replace("\\", "/")
                if u_norm.startswith("docs/") or u_norm.startswith("/docs/"):
                    # Already repo-rooted (or site-absolute pointing at repo root) → use as-is
                    base_repo_rel = re.sub(r"/{2,}", "/", u_norm.lstrip("/"))
                else:
                    # Resolve e.g. "../foo/bar" against the source file
                    base_repo_rel = _canonical_repo_path_from_relative(src, url)

                # For directory-style links, treat as <dir>/README.md(.mdx), then <dir>.md(.mdx)
                if is_dir_style:
                    base = base_repo_rel[:-1] if base_repo_rel.endswith("/") else base_repo_rel
                    candidates: list[str] = [
                        f"{base}/README.md",
                        f"{base}/README.mdx",
                        f"{base}.md",
                        f"{base}.mdx",
                    ]
                else:
                    # Explicit .md / .mdx link
                    candidates = [base_repo_rel]

                # Choose canonical repo-relative target and check on-disk existence
                repo_rel_target = candidates[0]
                exists_on_disk = False
                for candidate in candidates:
                    if Path(candidate).exists():
                        repo_rel_target = candidate
                        exists_on_disk = True
                        break

                if not pv:
                    # Non-PV source: we only care if the target file exists on disk
                    category = "rel_nonpv_exists" if exists_on_disk else "rel_nonpv_missing"
                    out.append(
                        Finding(
                            src.as_posix(),
                            i,
                            text,
                            url_raw,
                            "",
                            "",
                            category,
                            repo_rel_target,
                        )
                    )
                    continue

                # Compute PV key from the *source* page
                pv_key = _pv_key_from_repo_path(src)  # e.g. "apim/4.8"

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

                if exists_on_disk:
                    if in_summary:
                        category = "inpv_rel_exists_sum"
                    else:
                        category = "inpv_rel_exists_nosum"
                else:
                    if in_summary:
                        category = "inpv_rel_missing_sum"
                    else:
                        category = "inpv_rel_missing_nosum"

                out.append(
                    Finding(
                        src.as_posix(),
                        i,
                        text,
                        url_raw,
                        pv_product,
                        pv_version,
                        category,
                        repo_rel_target,
                    )
                )

    return out


def _write_csvs(findings: list[Finding]) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    master_rows: list[dict] = []
    per_category: dict[str, list[dict]] = {c: [] for c in CATEGORIES}

    for f in findings:
        row = {
            "src": f.src_file,
            "line": f.line_no,
            "text": f.text,
            "url": f.url,
            "pv_product": f.pv_product,
            "pv_version": f.pv_version,
            "category": f.category,
            "normalized_target": f.normalized_target,
        }
        master_rows.append(row)
        if f.category in per_category:
            per_category[f.category].append(row)

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
                    "category",
                    "normalized_target",
                ]
            ),
        )
        w.writeheader()
        for r in master_rows:
            w.writerow(r)

    # per category
    for category, rows in per_category.items():
        path = PER_CATEGORY_PREFIX.with_name(PER_CATEGORY_PREFIX.name + f"{category}.csv")
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
                        "category",
                        "normalized_target",
                    ]
                ),
            )
            w.writeheader()
            for r in rows:
                w.writerow(r)


def _print_summary(findings: list[Finding]) -> None:
    total = len(findings)
    counts: dict[str, int] = {c: 0 for c in CATEGORIES}
    for f in findings:
        if f.category in counts:
            counts[f.category] += 1

    typer.secho(
        "\nPage link audit (page links = URLs ending in .md or .mdx)\n",
        fg=typer.colors.BLUE,
    )
    typer.echo(f"Total links scanned: {total}")
    for k in CATEGORIES:
        typer.echo(f"  • {k}: {counts[k]}")

    typer.echo("\nCSV (master): " + MASTER_CSV.as_posix())
    typer.echo("CSV (per category):")
    for k in CATEGORIES:
        p = PER_CATEGORY_PREFIX.with_name(PER_CATEGORY_PREFIX.name + f"{k}.csv")
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
      - inpv_abs_exists_sum_reformat → make relative to src
      - inpv_rel_exists_*           → normalize relative paths
    Leaves missing_* alone (logged in CSV); we can extend later.
    """
    files_changed = 0
    links_changed = 0

    by_src: dict[str, list[Finding]] = {}
    for f in findings:
        if f.category in {
            "inpv_abs_exists_sum_reformat",
            "inpv_rel_exists_sum",
            "inpv_rel_exists_nosum",  # include off-nav but existing PV-relative links
            "rel_nonpv_exists",  # normalize existing non-PV relative links
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
    """Audit page links and write CSVs (master + per category)."""
    idx = _build_pv_index()
    findings = _scan_page_links(idx)
    _write_csvs(findings)
    _print_summary(findings)


@app.command()
def fix(dry_run: bool = True):
    """
    Apply safe autofixes to page links:
      - Rewrite same-PV absolute docs URLs (inpv_abs_exists_sum_reformat) to shortest relative paths
      - Normalize existing PV-relative links (inpv_rel_exists_*) to shortest relative paths
      - Normalize existing non-PV relative links (rel_nonpv_exists) to shortest relative paths

    Broken / missing targets and cross-PV or external links are not modified; they are only reported in the CSVs.
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
