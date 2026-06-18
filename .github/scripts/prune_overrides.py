import os
import sys

def main():
    if len(sys.argv) < 5:
        print("Usage: python prune_overrides.py <repo_path> <product> <current_version> <next_version>")
        sys.exit(1)

    repo_path = sys.argv[1]
    product = sys.argv[2]
    current_version = sys.argv[3]
    next_version = sys.argv[4]

    next_dir = os.path.join(repo_path, "docs", product, next_version)
    current_dir = os.path.join(repo_path, "docs", product, current_version)
    overrides_file = os.path.join(next_dir, ".version-overrides")

    if not os.path.exists(overrides_file):
        print(f"No overrides file found at {overrides_file}")
        sys.exit(0)

    with open(overrides_file, "r") as f:
        lines = f.read().splitlines()

    new_lines = []
    pruned_count = 0

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            new_lines.append(line)
            continue

        # Paths in .version-overrides can be either relative to the version directory (e.g. "guides/foo.md")
        # or absolute from the repo root (e.g. "docs/apim/4.12/guides/foo.md").
        # The sync script typically handles relative paths, but we support both.
        if stripped.startswith("docs/"):
            # If it's absolute, check if it starts with the next version prefix
            prefix = f"docs/{product}/{next_version}/"
            if stripped.startswith(prefix):
                rel_path = stripped[len(prefix):]
            else:
                # Malformed entry or applies to a different product/version? We'll leave it alone.
                new_lines.append(line)
                continue
        else:
            rel_path = stripped

        # Check existence
        path_in_next = os.path.join(next_dir, rel_path)
        path_in_current = os.path.join(current_dir, rel_path)

        exists_in_next = os.path.exists(path_in_next)
        exists_in_current = os.path.exists(path_in_current)

        if exists_in_next:
            # File exists in next version — valid override
            new_lines.append(line)
        elif exists_in_current:
            # File does NOT exist in next, but DOES exist in current.
            # This is an intentional "tombstone" override to prevent the sync bot
            # from recreating the file in next.
            new_lines.append(line)
        else:
            # File does NOT exist in next AND does NOT exist in current.
            # This is a dead link (orphaned entry). Prune it.
            pruned_count += 1
            print(f"Pruned orphaned override: {stripped}")

    if pruned_count > 0:
        # Write back cleanly
        with open(overrides_file, "w") as f:
            f.write("\n".join(new_lines) + "\n")
        print(f"Successfully pruned {pruned_count} entries from {overrides_file}.")
    else:
        print(f"No orphaned entries found in {overrides_file}.")

if __name__ == "__main__":
    main()
