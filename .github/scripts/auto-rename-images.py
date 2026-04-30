#!/usr/bin/env python3
"""
Auto-rename generic image files to descriptive, page-scoped names.

Triggered by CI on push to main. Detects any generic image files in
.gitbook/assets/ directories and renames them to collision-proof,
descriptive names derived from the referencing page's path.

Matches all GitBook generic naming patterns:
  - image.png
  - image (N).png
  - image (N) (M).png
  - image (N) (M) (K).png
  - image (N)-1.png
  - HsfV91lH__image.png  (hash-prefixed GitBook uploads)
  - abcd1234__image (N).png
  - etc.

Exit codes:
  0 — no generic images found (or all renamed successfully)
  1 — error during processing
"""

import os
import re
import shutil
import sys
from pathlib import Path


DOCS = Path("docs")

# Match any file starting with "image" (optionally prefixed by an 8-char
# alphanumeric hash and double-underscore) followed by optional parenthesized
# numbers and/or suffixes, ending in an image extension.
# Handles both real spaces and literal %20 in filenames on disk.
# Examples: image.png, image (12).png, image (3) (1).png, HsfV91lH__image.png
GENERIC_PATTERN = re.compile(
    r"^(?:[a-zA-Z0-9]{8}__)?image(?:(?:\s|%20)*\(\d+\))*(?:-\d+)?\.(?:png|jpg|jpeg|gif|svg|webp)$", re.I
)

# Extract the primary sequence number from the filename for use in descriptive names
SEQ_EXTRACT = re.compile(r"^image\s*(?:\((\d+)\))?")


def slugify(text: str) -> str:
    """Create a filename-safe slug from a single path segment."""
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def build_slug(page_path: Path, version_root: Path, max_len: int = 40) -> str:
    """Build a descriptive slug prioritizing the page name.

    Starts with the page basename and prepends parent directory names
    from right-to-left until the slug reaches max_len. This ensures
    the most-descriptive segment (the page name) is always preserved,
    unlike a left-to-right truncation which loses it on deep paths.
    """
    rel = page_path.relative_to(version_root)
    parts = list(rel.with_suffix("").parts)

    # Start with the page name (most important)
    slug = slugify(parts[-1])

    # Prepend parent dirs from right-to-left until we hit max_len
    for part in reversed(parts[:-1]):
        parent = slugify(part)
        candidate = f"{parent}-{slug}"
        if len(candidate) <= max_len:
            slug = candidate
        else:
            break

    return slug[:max_len].rstrip("-")


def find_generic_images() -> list[Path]:
    """Find all generic image files in .gitbook/assets/ dirs."""
    generics = []
    for dirpath, dirnames, filenames in os.walk(DOCS):
        if not dirpath.endswith("/.gitbook/assets"):
            continue
        for f in filenames:
            if GENERIC_PATTERN.match(f):
                generics.append(Path(dirpath) / f)
    return generics


def find_version_root(image_path: Path) -> Path:
    """Walk up from .gitbook/assets/ to find the version/product root."""
    return image_path.parent.parent.parent


def find_referencing_pages(image_path: Path, version_root: Path) -> list[Path]:
    """Find markdown files that reference this image via local paths.

    Only matches local .gitbook/assets/ references, not external CDN URLs
    that happen to contain the filename as a substring.
    """
    image_name = image_path.name
    encoded_name = image_name.replace(" ", "%20")

    referencing = []
    # Build all search variants anchored to the local assets path.
    # This prevents false positives from GitBook CDN URLs like:
    #   https://...gitbook.io/.../image%20(16).png?alt=media
    search_variants = {
        f".gitbook/assets/{image_name}",
        f".gitbook/assets/{encoded_name}",
    }
    if "%20" in image_name:
        search_variants.add(f".gitbook/assets/{image_name.replace('%20', ' ')}")

    for dirpath, dirnames, filenames in os.walk(version_root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for f in filenames:
            if not f.endswith(".md"):
                continue
            fpath = Path(dirpath) / f
            try:
                content = fpath.read_text("utf-8", errors="replace")
            except OSError:
                continue
            if any(v in content for v in search_variants):
                referencing.append(fpath)
    return referencing


def generate_name(page_path: Path, original_name: str, version_root: Path) -> str:
    """Generate a descriptive name from the page path and original sequence number."""
    # If there are parenthesized numbers, join them to form the suffix
    all_nums = re.findall(r"\((\d+)\)", original_name)
    suffix = "-".join(all_nums) if all_nums else "0"

    ext = original_name.rsplit(".", 1)[-1]
    slug = build_slug(page_path, version_root)

    return f"{slug}-{suffix}.{ext}"


def update_references(md_path: Path, old_name: str, new_name: str) -> bool:
    """Replace image references in a markdown file."""
    try:
        content = md_path.read_text("utf-8")
    except OSError:
        return False

    # Build all reference variants to replace
    variants = {old_name}
    variants.add(old_name.replace(" ", "%20"))
    if "%20" in old_name:
        variants.add(old_name.replace("%20", " "))
        variants.add(old_name)  # literal %20 in ref

    new_content = content
    for variant in variants:
        new_content = new_content.replace(
            f".gitbook/assets/{variant}", f".gitbook/assets/{new_name}"
        )

    if new_content != content:
        md_path.write_text(new_content, "utf-8")
        return True
    return False


def process_image(image_path: Path) -> list[str]:
    """Process a single generic image: rename and update references.

    Returns a list of action descriptions for logging.
    """
    version_root = find_version_root(image_path)
    pages = find_referencing_pages(image_path, version_root)
    actions = []

    if not pages:
        # Before deleting as orphan, check if any OTHER version references
        # this file via cross-version relative paths (e.g. ../../../4.10/.gitbook/assets/...)
        # Only match local .gitbook/assets/ references, NOT external CDN URLs.
        image_name = image_path.name
        encoded_name = image_name.replace(" ", "%20")
        search_variants = {
            f".gitbook/assets/{image_name}",
            f".gitbook/assets/{encoded_name}",
        }
        if "%20" in image_name:
            search_variants.add(f".gitbook/assets/{image_name.replace('%20', ' ')}")

        cross_ref = False
        for dirpath, dirnames, filenames in os.walk(DOCS):
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]
            if Path(dirpath).is_relative_to(version_root):
                continue  # Already checked within version_root
            for f in filenames:
                if not f.endswith(".md"):
                    continue
                try:
                    content = (Path(dirpath) / f).read_text("utf-8", errors="replace")
                except OSError:
                    continue
                if any(v in content for v in search_variants):
                    cross_ref = True
                    actions.append(
                        f"  Skipped (cross-product ref): {image_path.relative_to(DOCS)} "
                        f"(referenced by {Path(dirpath) / f})"
                    )
                    break
            if cross_ref:
                break

        if cross_ref:
            return actions

        if not pages:
            image_path.unlink()
            actions.append(f"  Deleted orphan: {image_path.relative_to(DOCS)}")
            return actions

    if len(pages) == 1:
        # Single reference — rename in place
        new_name = generate_name(pages[0], image_path.name, version_root)
        new_path = image_path.parent / new_name

        if new_path.exists() and new_path != image_path:
            base, ext = new_name.rsplit(".", 1)
            i = 2
            while (image_path.parent / f"{base}-v{i}.{ext}").exists():
                i += 1
            new_name = f"{base}-v{i}.{ext}"
            new_path = image_path.parent / new_name

        image_path.rename(new_path)
        update_references(pages[0], image_path.name, new_name)
        actions.append(
            f"  Renamed: {image_path.name} → {new_name} "
            f"(ref: {pages[0].name})"
        )
    else:
        # Multiple pages reference the same image — create unique copies
        for i, page in enumerate(pages):
            new_name = generate_name(page, image_path.name, version_root)
            new_path = image_path.parent / new_name

            if new_path.exists():
                base, ext = new_name.rsplit(".", 1)
                j = 2
                while (image_path.parent / f"{base}-v{j}.{ext}").exists():
                    j += 1
                new_name = f"{base}-v{j}.{ext}"
                new_path = image_path.parent / new_name

            if i == len(pages) - 1:
                image_path.rename(new_path)
            else:
                shutil.copy2(str(image_path), str(new_path))

            update_references(page, image_path.name, new_name)
            actions.append(
                f"  {'Renamed' if i == len(pages) - 1 else 'Copied'}: "
                f"{image_path.name} → {new_name} (ref: {page.name})"
            )

    return actions


def main() -> int:
    generics = find_generic_images()

    if not generics:
        print("✅ No generic image files found. Nothing to do.")
        return 0

    print(f"Found {len(generics)} generic image file(s). Renaming...")

    all_actions = []
    for img in sorted(generics):
        try:
            actions = process_image(img)
            all_actions.extend(actions)
        except Exception as e:
            print(f"❌ Error processing {img}: {e}", file=sys.stderr)
            return 1

    for action in all_actions:
        print(action)

    print(f"\n✅ Processed {len(generics)} generic images ({len(all_actions)} actions)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
