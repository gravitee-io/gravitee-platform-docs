import os
import sys
import subprocess

def get_changed_files(repo_path):
    # In a PR context (with actions/checkout fetch-depth: 0),
    # we compare against origin/main to find all files changed in the PR.
    try:
        # Check if origin/main exists, otherwise fallback to main
        refs_result = subprocess.run(
            ["git", "show-ref", "refs/remotes/origin/main"],
            cwd=repo_path, capture_output=True, text=True
        )
        base = "origin/main" if refs_result.returncode == 0 else "main"
        
        result = subprocess.run(
            ["git", "diff", "--name-only", f"{base}...HEAD"],
            cwd=repo_path, capture_output=True, text=True, check=True
        )
        return set(line.strip() for line in result.stdout.split('\n') if line.strip())
    except subprocess.CalledProcessError as e:
        print(f"Error getting changed files: {e.stderr}")
        # Fallback to local diff if ref is missing
        try:
            res2 = subprocess.run(["git", "diff", "--name-only", "HEAD^1"], cwd=repo_path, capture_output=True, text=True)
            return set(line.strip() for line in res2.stdout.split('\n') if line.strip())
        except Exception:
            return set()

def main():
    if len(sys.argv) < 5:
        print("Usage: python lint_overrides.py <repo_path> <product> <current_version> <next_version>")
        sys.exit(1)

    repo_path = sys.argv[1]
    product = sys.argv[2]
    current_version = sys.argv[3]
    next_version = sys.argv[4]

    next_prefix = f"docs/{product}/{next_version}/"
    current_prefix = f"docs/{product}/{current_version}/"

    changed_files = get_changed_files(repo_path)
    if not changed_files:
        print("No files changed or unable to determine diff. Skipping lint.")
        sys.exit(0)
    
    # Filter files for current and next versions
    changed_in_next = set(f for f in changed_files if f.startswith(next_prefix))
    changed_in_current = set(f for f in changed_files if f.startswith(current_prefix))

    if not changed_in_next:
        print(f"No files changed in {next_prefix}. Skipping lint.")
        sys.exit(0)

    # Read overrides for next_version
    overrides_file = os.path.join(repo_path, next_prefix, ".version-overrides")
    file_overrides = set()
    dir_prefixes = []
    if os.path.exists(overrides_file):
        with open(overrides_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    if line.startswith("docs/"):
                        if line.startswith(next_prefix):
                            clean_line = line[len(next_prefix):]
                        else:
                            clean_line = line
                    else:
                        clean_line = line
                        
                    if clean_line.endswith("/"):
                        dir_prefixes.append(clean_line)
                    else:
                        file_overrides.add(clean_line)

    errors = []
    
    for f in changed_in_next:
        rel_path = f[len(next_prefix):]
        
        # Skip the overrides file itself
        if rel_path == ".version-overrides":
            continue
            
        # Check if it was also changed in the current version
        if f"{current_prefix}{rel_path}" in changed_in_current:
            continue
            
        # Check if it is protected by an override
        is_overridden = False
        if rel_path in file_overrides:
            is_overridden = True
        else:
            for prefix in dir_prefixes:
                if rel_path.startswith(prefix):
                    is_overridden = True
                    break
                    
        if is_overridden:
            continue
            
        # It's a divergent edit without an override!
        errors.append(rel_path)
        
    if errors:
        print(f"::error::Found {len(errors)} version divergence(s) in {next_prefix} without overrides.")
        print("The following files were modified in the newer version but NOT in the older version,")
        print("and they are NOT listed in .version-overrides. This means the sync bot will")
        print("overwrite or delete your changes on the next run!\n")
        
        for err in errors:
            print(f"❌ {err}")
            
        print(f"\nFIX: If these are {next_version}-specific changes, add their paths to {next_prefix}.version-overrides.")
        print(f"     If these are global changes, please apply your edits to the {current_version} version instead.")
        sys.exit(1)
    else:
        print(f"All divergent edits in {next_prefix} are properly protected by overrides. Pass.")

if __name__ == "__main__":
    main()
