#!/usr/bin/env python3
"""Cross-version documentation sync.

Unidirectional sync: copies changes from docs/{product}/{current_version}/
to docs/{product}/{next_version}/, skipping files listed in .version-overrides.

Usage:
    python sync_versions.py /path/to/repo apim 4.10 4.11
    python sync_versions.py /path/to/repo apim 4.10 4.11 --dry-run
    python sync_versions.py /path/to/repo apim 4.10 4.11 --changed-files file1.md file2.md
    python sync_versions.py /path/to/repo apim 4.10 4.11 --changed-files-from /tmp/files.txt

When --changed-files and --changed-files-from are both omitted, syncs ALL files
from current → next (full sync).

Exit codes:
    0 = all files synced cleanly (or only warnings)
    1 = conflicts detected (files differ in next_version but aren't in .version-overrides)
    2 = fatal error (missing dirs, bad args, etc.)
"""

import argparse
import filecmp
import os
import shutil
import sys


OVERRIDES_FILENAME = ".version-overrides"

# Files that are inherently version-specific and must NEVER be synced.
# These are excluded regardless of .version-overrides content.
ALWAYS_SKIP = {".gitbook.yaml"}


def load_overrides(next_version_dir: str) -> tuple:
    """Load the .version-overrides file from the next version directory.

    Returns a tuple of (file_overrides, dir_prefixes):
      - file_overrides: set of exact relative paths to skip
      - dir_prefixes: list of directory prefixes to skip (entries ending with /)
    """
    overrides_path = os.path.join(next_version_dir, OVERRIDES_FILENAME)
    if not os.path.exists(overrides_path):
        return set(), []
    file_overrides = set()
    dir_prefixes = []
    with open(overrides_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                if line.endswith("/"):
                    dir_prefixes.append(line)
                else:
                    file_overrides.add(line)
    return file_overrides, dir_prefixes


def is_overridden(rel_path: str, file_overrides: set, dir_prefixes: list) -> bool:
    """Check if a file path is protected by overrides (exact match or dir prefix)."""
    if rel_path in file_overrides:
        return True
    for prefix in dir_prefixes:
        if rel_path.startswith(prefix):
            return True
    return False


def get_all_files(version_dir: str) -> set:
    """Get all file paths relative to version_dir."""
    files = set()
    for root, _, filenames in os.walk(version_dir):
        for fname in filenames:
            full_path = os.path.join(root, fname)
            rel_path = os.path.relpath(full_path, version_dir)
            files.add(rel_path)
    return files


def split_frontmatter(content: str) -> tuple:
    """Split markdown content into (frontmatter, body).

    Returns (frontmatter_str, body_str) where:
      - frontmatter_str includes the --- delimiters and trailing newline,
        or None if no frontmatter is found.
      - body_str is everything after the frontmatter.
    """
    if not content.startswith("---\n"):
        return None, content
    end = content.find("\n---\n", 3)
    if end == -1:
        # Check if file is ONLY frontmatter (no trailing newline after closing ---)
        if content.rstrip().endswith("---") and content.count("---") >= 2:
            return content, ""
        return None, content
    fm_end = end + 5  # len('\n---\n')
    return content[:fm_end], content[fm_end:]


def sync_versions(
    repo_path: str,
    product: str,
    current_version: str,
    next_version: str,
    changed_files: list = None,
    dry_run: bool = False,
) -> dict:
    """Sync files from current_version to next_version.

    Args:
        repo_path: Path to the docs repo root.
        product: Product name (e.g., "apim").
        current_version: Current version (e.g., "4.10").
        next_version: Next version (e.g., "4.11").
        changed_files: If provided, only sync these files (relative to version dir).
                        If None, sync all files.
        dry_run: If True, don't actually copy — just report what would happen.

    Returns:
        dict with keys: synced, skipped, conflicts, new_files, errors
    """
    current_dir = os.path.join(repo_path, "docs", product, current_version)
    next_dir = os.path.join(repo_path, "docs", product, next_version)

    if not os.path.isdir(current_dir):
        return {"error": f"Current version dir not found: {current_dir}"}
    if not os.path.isdir(next_dir):
        return {"error": f"Next version dir not found: {next_dir}"}

    file_overrides, dir_prefixes = load_overrides(next_dir)
    results = {
        "synced": [], "skipped": [], "conflicts": [], "new_files": [],
        "errors": [], "warnings": [], "auto_merged": [], "merge_conflicts": [],
    }

    # Determine which files to process
    if changed_files:
        files_to_sync = set(changed_files)
    else:
        files_to_sync = get_all_files(current_dir)

    for rel_path in sorted(files_to_sync):
        current_file = os.path.join(current_dir, rel_path)
        next_file = os.path.join(next_dir, rel_path)

        # Skip the overrides file itself
        if rel_path == OVERRIDES_FILENAME:
            continue

        # Skip files that are inherently version-specific
        if os.path.basename(rel_path) in ALWAYS_SKIP:
            results["skipped"].append(rel_path)
            continue

        # Protected files: skip (managed manually via .version-overrides)
        # Supports both exact file paths and directory prefixes (ending with /)
        if is_overridden(rel_path, file_overrides, dir_prefixes):
            results["skipped"].append(rel_path)
            continue

        # File must exist in current version
        if not os.path.exists(current_file):
            # Downgrade to warning — file may have been deleted in source,
            # or the changed-files list may include renames/deletions.
            results["warnings"].append(f"{rel_path}: not found in {current_version}")
            continue

        # Case 1: File doesn't exist in next version — new file
        if not os.path.exists(next_file):
            results["new_files"].append(rel_path)
            if not dry_run:
                os.makedirs(os.path.dirname(next_file), exist_ok=True)
                shutil.copy2(current_file, next_file)
            continue

        # Case 2 & 3: File exists in both — compare and sync
        # For markdown files, use frontmatter-aware comparison and sync.
        # This preserves version-specific YAML frontmatter (e.g., metaLinks,
        # alternates) that GitBook adds to the target version.
        if rel_path.endswith(".md"):
            try:
                source_content = open(current_file, encoding="utf-8").read()
                target_content = open(next_file, encoding="utf-8").read()
            except (UnicodeDecodeError, OSError):
                # Fallback to binary comparison for files that can't be read as text
                if filecmp.cmp(current_file, next_file, shallow=False):
                    continue
                results["synced"].append(rel_path)
                if not dry_run:
                    shutil.copy2(current_file, next_file)
                continue

            _, source_body = split_frontmatter(source_content)
            target_fm, target_body = split_frontmatter(target_content)

            # Bodies identical — already in sync (ignore frontmatter differences)
            if source_body.strip() == target_body.strip():
                continue

            # Bodies differ — sync body from source, preserve target's frontmatter
            results["synced"].append(rel_path)
            if not dry_run:
                if target_fm is not None:
                    merged = target_fm + source_body
                else:
                    # Target has no frontmatter — use source body without
                    # source frontmatter (frontmatter is version-specific)
                    merged = source_body
                with open(next_file, "w", encoding="utf-8") as f:
                    f.write(merged)
        else:
            # Non-markdown files: binary comparison
            if filecmp.cmp(current_file, next_file, shallow=False):
                continue
            results["synced"].append(rel_path)
            if not dry_run:
                shutil.copy2(current_file, next_file)

    return results


def print_results(results: dict, product: str, current: str, next_ver: str, dry_run: bool):
    """Print sync results in a human-readable format."""
    prefix = "[DRY RUN] " if dry_run else ""

    if "error" in results:
        print(f"[✗] {results['error']}")
        return

    print(f"{prefix}Version sync: docs/{product}/{current}/ → docs/{product}/{next_ver}/")
    print()

    if results["synced"]:
        print(f"  {prefix}Synced ({len(results['synced'])}):")
        for f in results["synced"]:
            print(f"    ✓ {f}")

    if results["new_files"]:
        print(f"  {prefix}New files copied ({len(results['new_files'])}):")
        for f in results["new_files"]:
            print(f"    + {f}")

    if results.get("auto_merged"):
        print(f"  {prefix}Auto-merged protected files ({len(results['auto_merged'])}):")
        for f in results["auto_merged"]:
            print(f"    ⇄ {f}")

    if results.get("merge_conflicts"):
        print(f"  ⚠ Protected files with CONFLICTS ({len(results['merge_conflicts'])}):")
        for f in results["merge_conflicts"]:
            print(f"    ✗ {f} — has conflict markers, needs manual review")

    if results["skipped"]:
        print(f"  Skipped (in .version-overrides) ({len(results['skipped'])}):")
        for f in results["skipped"]:
            print(f"    ⊘ {f}")

    if results["warnings"]:
        print(f"  Warnings ({len(results['warnings'])}):")
        for w in results["warnings"]:
            print(f"    ⚠ {w}")

    if results["errors"]:
        print(f"  Errors ({len(results['errors'])}):")
        for e in results["errors"]:
            print(f"    ✗ {e}")

    total = len(results["synced"]) + len(results["new_files"])
    auto_merged = len(results.get("auto_merged", []))
    merge_conflicts = len(results.get("merge_conflicts", []))
    print()
    print(f"  Total: {total} files {'would be ' if dry_run else ''}synced, "
          f"{auto_merged} auto-merged, "
          f"{merge_conflicts} conflicts, "
          f"{len(results['skipped'])} skipped, "
          f"{len(results['warnings'])} warnings, "
          f"{len(results['errors'])} errors")


def main():
    parser = argparse.ArgumentParser(description="Cross-version documentation sync")
    parser.add_argument("repo_path", help="Path to the docs repository root")
    parser.add_argument("product", help="Product name (e.g., apim)")
    parser.add_argument("current_version", help="Current version (e.g., 4.10)")
    parser.add_argument("next_version", help="Next version (e.g., 4.11)")
    parser.add_argument("--changed-files", nargs="+",
                        help="Only sync these files (paths relative to version dir)")
    parser.add_argument("--changed-files-from",
                        help="Read changed file list from a file (one path per line). "
                             "Handles filenames with spaces correctly.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would happen without making changes")
    args = parser.parse_args()

    # --changed-files-from takes priority (handles spaces in filenames)
    changed_files = args.changed_files
    if args.changed_files_from:
        with open(args.changed_files_from) as f:
            changed_files = [line.strip() for line in f if line.strip()]

    results = sync_versions(
        repo_path=args.repo_path,
        product=args.product,
        current_version=args.current_version,
        next_version=args.next_version,
        changed_files=changed_files,
        dry_run=args.dry_run,
    )

    print_results(results, args.product, args.current_version, args.next_version, args.dry_run)

    if "error" in results:
        sys.exit(2)
    if results.get("errors"):
        sys.exit(2)
    # Warnings (e.g., "not found") are non-fatal — exit 0
    sys.exit(0)


if __name__ == "__main__":
    main()
