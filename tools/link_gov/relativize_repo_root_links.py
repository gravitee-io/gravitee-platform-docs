#!/usr/bin/env python3
import argparse
import fnmatch
import pathlib
import re
import subprocess
import sys
from collections.abc import Iterable

REPO = pathlib.Path(__file__).resolve().parents[2]
DOCS = REPO / "docs"

TOPS = {"apim", "am", "gko", "ae", "platform-overview", "gravitee-cloud"}
DOCS_DOMAIN = "https://documentation.gravitee.io/"

LINK_RE = re.compile(
    r"""(?x)
    (?<!\!)                          # not an image
    \[ (?P<text>[^\]]+) \]
    \( (?P<url><[^>]+>|[^)\s]+)
       (?P<tail>\s+"[^"]*"|\s+'[^']*'|\s+\([^)]+\))?
    \)
"""
)


def strip_brackets(s: str) -> str:
    return s[1:-1] if s.startswith("<") and s.endswith(">") else s


def split_anchor(u: str) -> tuple[str, str]:
    if "#" in u:
        h, f = u.split("#", 1)
        return h, "#" + f
    return u, ""


def shortest_rel(from_file: pathlib.Path, to_path: pathlib.Path) -> str:
    rel = pathlib.Path(pathlib.os.path.relpath(to_path, start=from_file.parent)).as_posix()
    return rel[2:] if rel.startswith("./") else rel


def product_version_from_source(src: pathlib.Path) -> tuple[str | None, str | None]:
    try:
        parts = src.relative_to(DOCS).parts
    except ValueError:
        return None, None
    if len(parts) >= 2 and parts[0] in TOPS:
        return parts[0], parts[1]
    return None, None


def looks_like_version(s: str) -> bool:
    return bool(re.match(r"^\d+(?:\.\d+)?(?:\.x)?$", s))


def normalize_site_path(site_path: str, pv_hint: str | None) -> str | None:
    """
    Accepts '/apim/4.9/foo/bar' or '/apim/foo/bar' or 'apim/4.9/foo/bar' (and https form).
    Ensures we end with a *file stem* (no extension here); we will append .md/.mdx when resolving.
    Injects pv_hint when version missing.
    """
    parts = [p for p in site_path.strip("/").split("/") if p]
    if not parts or parts[0] not in TOPS:
        return None
    # drop 'v' in '/apim/v/4.9/...'
    if len(parts) >= 2 and parts[1] == "v":
        parts.pop(1)
    # inject PV if missing
    if len(parts) < 2 or not looks_like_version(parts[1]):
        if pv_hint:
            parts.insert(1, pv_hint)
        # if we can't infer PV we still proceed; resolution will likely fail -> REVIEW
    # the normalized path is docs/<product>/<pv>/.../<stem>  (no extension yet)
    return "/".join(parts)


def candidates(norm: str) -> Iterable[pathlib.Path]:
    """
    Candidate resolution order:
      <path>.md, <path>.mdx, <path>/README.md, <path>/index.md,
      for directory aliases like '.../changelog' also try '.../changelog/README.md'
    If the last component already has an extension, try as-is.
    """
    base = DOCS / norm
    name = pathlib.Path(norm).name

    # If an explicit extension was provided
    if "." in name:
        yield base

    # Common page candidates
    yield base.with_suffix(".md")
    yield base.with_suffix(".mdx")
    yield base / "README.md"
    yield base / "index.md"


def slug_search(product: str, pv: str | None, last_segment: str) -> list[pathlib.Path]:
    """
    Fallback: search files whose basename contains 'last_segment' (case-insensitive)
    under docs/<product>/<pv> (or docs/<product> if pv missing).
    Prefer .md/.mdx files; return deterministic order.
    """
    root = DOCS / product / (pv if pv else "")
    if not root.exists():
        return []
    matches: list[pathlib.Path] = []
    pattern = f"*{last_segment}*"
    for p in root.rglob("*.md"):
        if fnmatch.fnmatch(p.stem.lower(), pattern.lower()):
            matches.append(p)
    for p in root.rglob("*.mdx"):
        if fnmatch.fnmatch(p.stem.lower(), pattern.lower()):
            matches.append(p)
    # Dedup + sort by shortest path first
    uniq = sorted(set(matches), key=lambda p: (len(p.as_posix()), p.as_posix()))
    return uniq


def resolve_to_file(
    raw_url: str, src_file: pathlib.Path, debug: bool = False
) -> pathlib.Path | None:
    u = strip_brackets(raw_url)
    head, _ = split_anchor(u)

    product_hint, pv_hint = product_version_from_source(src_file)

    if head.startswith(DOCS_DOMAIN):
        site_path = head[len(DOCS_DOMAIN) :]
    elif head.startswith("/"):
        site_path = head
    else:
        return None

    norm = normalize_site_path(site_path, pv_hint)
    if not norm:
        return None

    base = DOCS / norm  # stem (no extension)
    # Only treat as a FILE: try .md, then .mdx
    md = base.with_suffix(".md")
    if md.exists():
        return md.resolve()
    mdx = base.with_suffix(".mdx")
    if mdx.exists():
        return mdx.resolve()

    # If we got here, it's a miss; report for manual review.
    return None


def process_file(p: pathlib.Path, apply: bool, debug: bool) -> int:
    text = p.read_text(encoding="utf-8")
    out, last, rewrites = [], 0, 0

    for m in LINK_RE.finditer(text):
        url_token = m.group("url")
        url_clean = strip_brackets(url_token)

        is_docs_https = url_clean.startswith(DOCS_DOMAIN)
        is_root_top = any(url_clean.startswith(f"/{t}/") for t in TOPS)

        if not (is_docs_https or is_root_top):
            continue

        target = resolve_to_file(url_token, p, debug=debug)
        if target:
            head, anchor = split_anchor(url_clean)
            rel = shortest_rel(p, target) + anchor
            s, e = m.span()
            out.append(text[last:s])
            out.append(f"[{m.group('text')}]({rel}{m.group('tail') or ''})")
            last = e
            rewrites += 1
        else:
            # No local match: if it's a root-anchored product path (/apim, /am, etc),
            # rewrite to the absolute docs URL as a safe fallback.
            s, e = m.span()
            if url_clean.startswith("/") and any(url_clean.startswith(f"/{t}/") for t in TOPS):
                head, anchor = split_anchor(url_clean)
                abs_url = f"{DOCS_DOMAIN}{head.lstrip('/')}{anchor}"
                out.append(text[last:s])
                out.append(f"[{m.group('text')}]({abs_url}{m.group('tail') or ''})")
                last = e
                rewrites += 1
                if debug:
                    relpath = p.relative_to(REPO).as_posix()
                    print(f"[ABSOLUTE] No local match; rewrote to: {abs_url}  (in {relpath})")
            else:
                if debug:
                    relpath = p.relative_to(REPO).as_posix()
                    print(f"[REVIEW] No local match for: {url_clean}  (in {relpath})")
    if rewrites:
        out.append(text[last:])
        if apply:
            p.write_text("".join(out), encoding="utf-8")
    return rewrites


def changed_markdown_paths(rev_range: str) -> list[pathlib.Path]:
    cmd = [
        "git",
        "-C",
        str(REPO),
        "diff",
        "--name-only",
        "--diff-filter=ACMR",
        rev_range,
        "--",
        "*.md",
        "*.mdx",
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(res.stderr.strip(), file=sys.stderr)
        sys.exit(1)
    paths = []
    for line in res.stdout.splitlines():
        p = (REPO / line.strip()).resolve()
        if p.name.lower() == "summary.md":
            continue
        if p.exists() and p.is_file():
            paths.append(p)
    return paths


def main():
    ap = argparse.ArgumentParser(
        description="Relativize root-anchored Gravitee docs links to shortest relative paths."
    )
    ap.add_argument("--range", default="HEAD~1..HEAD", help="Git rev range (default: last commit)")
    ap.add_argument("--apply", action="store_true", help="Write changes (default: dry run)")
    ap.add_argument("--debug", action="store_true", help="Log unresolved links as [REVIEW]")
    args = ap.parse_args()

    files = changed_markdown_paths(args.range)
    total_files = total_links = 0
    for p in files:
        n = process_file(p, apply=args.apply, debug=args.debug)
        if n:
            total_files += 1
            total_links += n

    print(
        f"[{'APPLY' if args.apply else 'DRY-RUN'}] Updated links in {total_files} files; {total_links} link(s) rewritten."
    )


if __name__ == "__main__":
    main()
