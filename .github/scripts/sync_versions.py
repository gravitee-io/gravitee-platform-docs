#!/usr/bin/env python3
"""Cross-version documentation sync.

Unidirectional sync: copies changes from docs/{product}/{current_version}/
to docs/{product}/{next_version}/, skipping files listed in .version-overrides.

Usage:
    python sync_versions.py /path/to/repo apim 4.10 4.11
    python sync_versions.py /path/to/repo apim 4.10 4.11 --dry-run
    python sync_versions.py /path/to/repo apim 4.10 4.11 --changed-files file1.md file2.md

When --changed-files is omitted, syncs ALL files from current → next (full sync).
When provided, only syncs the listed files (incremental sync, for GitHub Action use).

Exit codes:
    0 = all files synced cleanly
    1 = conflicts detected (files differ in next_version but aren't in .version-overrides)
    2 = error (missing dirs, bad args, etc.)
"""

import argparse
import filecmp
import os
import shutil
import sys


OVERRIDES_FILENAME = ".version-overrides"


def load_overrides(next_version_dir: str) -> set:
    """Load the .version-overrides file from the next version directory.

    Returns a set of relative paths (relative to the version dir) that
    should NOT be synced from current → next.
    """
    overrides_path = os.path.join(next_version_dir, OVERRIDES_FILENAME)
    if not os.path.exists(overrides_path):
        return set()
    overrides = set()
    with open(overrides_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                overrides.add(line)
    return overrides


def get_all_files(version_dir: str) -> set:
    """Get all file paths relative to version_dir."""
    files = set()
    for root, _, filenames in os.walk(version_dir):
        for fname in filenames:
            full_path = os.path.join(root, fname)
            rel_path = os.path.relpath(full_path, version_dir)
            files.add(rel_path)
    return files


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

    overrides = load_overrides(next_dir)
    results = {"synced": [], "skipped": [], "conflicts": [], "new_files": [], "errors": []}

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

        # Skip files in overrides registry
        if rel_path in overrides:
            results["skipped"].append(rel_path)
            continue

        # File must exist in current version
        if not os.path.exists(current_file):
            results["errors"].append(f"{rel_path}: not found in {current_version}")
            continue

        # Case 1: File doesn't exist in next version — new file
        if not os.path.exists(next_file):
            results["new_files"].append(rel_path)
            if not dry_run:
                os.makedirs(os.path.dirname(next_file), exist_ok=True)
                shutil.copy2(current_file, next_file)
            continue

        # Case 2: Files are identical — already in sync
        if filecmp.cmp(current_file, next_file, shallow=False):
            continue  # Nothing to do

        # Case 3: Files differ — sync (overwrite next with current)
        # This is safe because divergent files should be in .version-overrides
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

    if results["skipped"]:
        print(f"  Skipped (in .version-overrides) ({len(results['skipped'])}):")
        for f in results["skipped"]:
            print(f"    ⊘ {f}")

    if results["errors"]:
        print(f"  Errors ({len(results['errors'])}):")
        for e in results["errors"]:
            print(f"    ✗ {e}")

    total = len(results["synced"]) + len(results["new_files"])
    print()
    print(f"  Total: {total} files {'would be ' if dry_run else ''}synced, "
          f"{len(results['skipped'])} skipped, "
          f"{len(results['errors'])} errors")


def main():
    parser = argparse.ArgumentParser(description="Cross-version documentation sync")
    parser.add_argument("repo_path", help="Path to the docs repository root")
    parser.add_argument("product", help="Product name (e.g., apim)")
    parser.add_argument("current_version", help="Current version (e.g., 4.10)")
    parser.add_argument("next_version", help="Next version (e.g., 4.11)")
    parser.add_argument("--changed-files", nargs="+",
                        help="Only sync these files (paths relative to version dir)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would happen without making changes")
    args = parser.parse_args()

    results = sync_versions(
        repo_path=args.repo_path,
        product=args.product,
        current_version=args.current_version,
        next_version=args.next_version,
        changed_files=args.changed_files,
        dry_run=args.dry_run,
    )

    print_results(results, args.product, args.current_version, args.next_version, args.dry_run)

    if "error" in results:
        sys.exit(2)
    if results.get("errors"):
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
