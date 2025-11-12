#!/usr/bin/env python3
import argparse
import pathlib
import re
import sys

DOCS = pathlib.Path("docs").resolve()

# Match normal markdown links only (skip images): [text](url)
LINK_RE = re.compile(r"(?<!\!)\[(?P<text>[^\]]+)\]\((?P<url>[^)\s]+)\)")

GRAVITEE_DOMAIN_PREFIX = "https://documentation.gravitee.io/"


def split_anchor(url: str) -> tuple[str, str]:
    if "#" in url:
        path, frag = url.split("#", 1)
        return path, "#" + frag
    return url, ""


def candidate_files_from_site_path(site_path: str):
    """
    Map a site path like 'apim/4.6/overview/release-notes/apim-4.6'
    to possible files under docs/.
    """
    base = DOCS / site_path.strip("/")

    # Try exact with .md/.mdx if missing extension
    yield base.with_suffix(".md")
    yield base.with_suffix(".mdx")

    # Try README.md / index.md within a directory
    yield base / "README.md"
    yield base / "index.md"

    # If the path already has an extension, just use it
    if "." in base.name:
        yield base


def to_shortest_rel(src_path: pathlib.Path, target_path: pathlib.Path) -> str:
    rel = pathlib.Path(pathlib.os.path.relpath(target_path, start=src_path.parent)).as_posix()
    # Prefer no leading "./" unless it's exactly "."
    if rel.startswith("./"):
        rel = rel[2:]
    return rel


def resolve_docs_url(url: str) -> pathlib.Path | None:
    """
    Resolve a 'docs/...' URL to an actual file in the repo.
    Returns None if no matching file exists.
    """
    path_part, _ = split_anchor(url)
    if not path_part.startswith("docs/"):
        return None
    absolute = (pathlib.Path(path_part)).resolve()
    if absolute.exists():
        return absolute
    return None


def resolve_gravitee_site_url(url: str) -> pathlib.Path | None:
    """
    Convert a documentation.gravitee.io URL into a docs/ file if we can find one.
    """
    path_part, _ = split_anchor(url)
    if not path_part.startswith(GRAVITEE_DOMAIN_PREFIX):
        return None
    site_path = path_part[len(GRAVITEE_DOMAIN_PREFIX) :]
    for cand in candidate_files_from_site_path(site_path):
        if cand.exists():
            return cand.resolve()
    return None


def process_file(p: pathlib.Path, apply: bool) -> int:
    text = p.read_text(encoding="utf-8")
    changed = 0
    out = []
    last = 0

    for m in LINK_RE.finditer(text):
        url = m.group("url")
        text_start, text_end = m.span()

        # Skip already-short relative links (../ or ./ or plain name)
        if (
            url.startswith("../")
            or url.startswith("./")
            or (not url.startswith("docs/") and not url.startswith(GRAVITEE_DOMAIN_PREFIX))
        ):
            continue

        target_file = None
        anchor = ""

        # Case 1: repo-root style 'docs/...'
        if url.startswith("docs/"):
            path_part, anchor = split_anchor(url)
            target_file = resolve_docs_url(path_part)

        # Case 2: absolute site URL
        elif url.startswith(GRAVITEE_DOMAIN_PREFIX):
            path_part, anchor = split_anchor(url)
            target_file = resolve_gravitee_site_url(path_part)

        if target_file and target_file.exists():
            rel = to_shortest_rel(p, target_file)
            replacement = f"[{m.group('text')}]({rel}{anchor})"
            out.append(text[last:text_start])
            out.append(replacement)
            last = text_end
            changed += 1

    if changed:
        out.append(text[last:])
        new_text = "".join(out)
        if apply:
            p.write_text(new_text, encoding="utf-8")
    return changed


def main():
    ap = argparse.ArgumentParser(
        description="Relativize repo-root docs/ links (and optional Gravitee site links) to shortest relative paths."
    )
    ap.add_argument(
        "--apply", action="store_true", help="Write changes to files. Omit for dry run."
    )
    ap.add_argument(
        "--glob", default="**/*.md,**/*.mdx", help="Comma-separated glob(s) under docs/"
    )
    args = ap.parse_args()

    globs = [g.strip() for g in args.glob.split(",") if g.strip()]
    total = 0
    files = 0

    for g in globs:
        for p in DOCS.glob(g):
            if not p.is_file():
                continue
            changed = process_file(p, apply=args.apply)
            if changed:
                files += 1
                total += changed

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"[{mode}] Updated links in {files} files; {total} link(s) rewritten.")


if __name__ == "__main__":
    sys.exit(main())
