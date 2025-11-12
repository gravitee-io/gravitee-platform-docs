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

    # If the path already has an extension, also try as-is
    if "." in base.name:
        yield base


def to_shortest_rel(src_path: pathlib.Path, target_path: pathlib.Path) -> str:
    rel = pathlib.Path(pathlib.os.path.relpath(target_path, start=src_path.parent)).as_posix()
    if rel.startswith("./"):
        rel = rel[2:]
    return rel


def resolve_docs_url(url: str) -> pathlib.Path | None:
    """Resolve a 'docs/...' URL to an actual file in the repo."""
    path_part, _ = split_anchor(url)
    if not path_part.startswith("docs/"):
        return None
    absolute = pathlib.Path(path_part).resolve()
    return absolute if absolute.exists() else None


def resolve_gravitee_site_url(url: str) -> pathlib.Path | None:
    """Convert a documentation.gravitee.io URL into a docs/ file if found."""
    path_part, _ = split_anchor(url)
    if not path_part.startswith(GRAVITEE_DOMAIN_PREFIX):
        return None
    site_path = path_part[len(GRAVITEE_DOMAIN_PREFIX) :]
    for cand in candidate_files_from_site_path(site_path):
        if cand.exists():
            return cand.resolve()
    return None


def resolve_site_root_url(url: str) -> pathlib.Path | None:
    """Convert a site-root link like '/am/4.9/...' into a docs/ file if found."""
    path_part, _ = split_anchor(url)
    if not path_part.startswith("/") or path_part.startswith("//"):
        return None
    site_path = path_part.lstrip("/")
    for cand in candidate_files_from_site_path(site_path):
        if cand.exists():
            return cand.resolve()
    return None


def resolve_existing_relative(url: str, src_file: pathlib.Path) -> pathlib.Path | None:
    """
    Resolve an existing relative link (../, ./, or bare path) against src_file.
    Only treat it as an in-repo markdown target if it resolves to a file under docs/.
    """
    path_part, _ = split_anchor(url)

    # Ignore obvious non-file/schemes
    if (
        path_part.startswith("http://")
        or path_part.startswith("https://")
        or path_part.startswith("mailto:")
        or path_part.startswith("tel:")
        or path_part.startswith("#")
    ):
        return None

    # Normalize against the source file’s directory
    candidate = (src_file.parent / path_part).resolve()

    # Only consider files within docs/ and with md/mdx extensions
    try:
        candidate.relative_to(DOCS)
    except ValueError:
        return None

    if candidate.is_file() and candidate.suffix.lower() in {".md", ".mdx"}:
        return candidate

    return None


def process_file(p: pathlib.Path, apply: bool) -> int:
    text = p.read_text(encoding="utf-8")
    changed = 0
    out = []
    last = 0

    for m in LINK_RE.finditer(text):
        url = m.group("url")
        text_start, text_end = m.span()

        target_file = None
        anchor = ""

        # Case A: repo-root style 'docs/...'
        if url.startswith("docs/"):
            path_part, anchor = split_anchor(url)
            target_file = resolve_docs_url(path_part)

        # Case B: absolute site URL
        elif url.startswith(GRAVITEE_DOMAIN_PREFIX):
            path_part, anchor = split_anchor(url)
            target_file = resolve_gravitee_site_url(path_part)

        # Case C: site-root '/...'
        elif url.startswith("/") and not url.startswith("//"):
            path_part, anchor = split_anchor(url)
            target_file = resolve_site_root_url(path_part)

        else:
            # Case D: existing relative (../, ./, or bare path) → canonicalize to shortest
            # (Skip external schemes, anchors, images already handled by regex negative lookbehind)
            target_file = resolve_existing_relative(url, p)
            if target_file:
                path_part, anchor = split_anchor(url)

        if target_file and target_file.exists():
            rel = to_shortest_rel(p, target_file)
            replacement = f"[{m.group('text')}]({rel}{anchor})"
            if replacement != text[text_start:text_end]:
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
        description=(
            "Relativize internal links to the shortest relative form.\n"
            "- Rewrites 'docs/...', documentation.gravitee.io absolutes, site-root '/...'\n"
            "  and existing relative links (../, ./, bare) to shortest relative.\n"
            "- Preserves anchors, skips images/external schemes."
        )
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
