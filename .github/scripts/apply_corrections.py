import os
import json

# ✅ Load reviewed corrections
corrections_file = "corrections.json"

if not os.path.exists(corrections_file):
    print("❌ No corrections file found. Make sure to review corrections first.")
    exit(1)

with open(corrections_file, "r", encoding="utf-8") as f:
    corrections = json.load(f)

# ✅ Apply only approved corrections
for correction in corrections:
    file_path = correction["file"]
    original = correction["original"]
    suggested = correction["suggested"]

    # Skip if the file no longer exists
    if not os.path.exists(file_path):
        print(f"⚠️ Skipping {file_path} (file not found)")
        continue

    # Read the file content
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Apply correction
    modified_lines = []
    change_applied = False
    for line in lines:
        if original in line and not change_applied:  # Ensure we only apply once
            modified_lines.append(line.replace(original, suggested))
            change_applied = True
        else:
            modified_lines.append(line)

    # Write back the modified content
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(modified_lines)

    print(f"✅ Applied correction in {file_path}")

print("🚀 All approved corrections have been applied successfully.")
