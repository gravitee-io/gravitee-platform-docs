import os
import json

corrections_file = "corrections.json"

if not os.path.exists(corrections_file):
    print("❌ Error: Corrections file not found. Ensure you've reviewed and uploaded the file.")
    exit(1)

# Load corrections from JSON
with open(corrections_file, "r", encoding="utf-8") as f:
    corrections = json.load(f)

if not corrections:
    print("✅ No corrections to apply.")
    exit(0)

approved_changes = {}

# ✅ Process each correction
for entry in corrections:
    original = entry["original"]
    suggested = entry["suggested"]
    file_path = entry["file"]

    # ✅ Allow manual approval
    decision = ""
    while decision not in ["yes", "no", "exit"]:
        decision = input(f"File: {file_path}\nOriginal: {original}\nSuggested: {suggested}\nApprove this change? (yes/no/exit): ").strip().lower()

    if decision == "yes":
        approved_changes.setdefault(file_path, []).append((original, suggested))
    elif decision == "exit":
        print("⏸️ Review paused. You can re-run the script later.")
        exit(0)

# ✅ Apply approved changes to files
for file_path, changes in approved_changes.items():
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    modified = False
    for original, corrected in changes:
        if original in content:
            content = content.replace(original, corrected)
            modified = True

    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

print("✅ Approved corrections applied successfully.")
