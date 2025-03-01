import os

corrections_file = "corrections.txt"

if not os.path.exists(corrections_file):
    print("❌ Error: Corrections file not found. Ensure you've reviewed and uploaded the file.")
    exit(1)

# Read corrections from file
with open(corrections_file, "r", encoding="utf-8") as f:
    corrections = f.read().strip().split("\n\n")

if not corrections:
    print("✅ No corrections to apply.")
    exit(0)

approved_changes = {}

# ✅ Process each correction
for entry in corrections:
    lines = entry.strip().split("\n")
    if len(lines) < 2:
        continue

    original = lines[0].replace("Original: ", "").strip()
    suggested = lines[1].replace("Suggested: ", "").strip()

    # ✅ Allow manual approval
    decision = ""
    while decision not in ["yes", "no", "exit"]:
        decision = input(f"Original: {original}\nSuggested: {suggested}\nApprove this change? (yes/no/exit): ").strip().lower()

    if decision == "yes":
        approved_changes[original] = suggested
    elif decision == "exit":
        print("⏸️ Review paused. You can re-run the script later.")
        exit(0)

# ✅ Apply approved changes to all files
for root, _, files in os.walk("."):
    for file in files:
        if file.endswith((".md", ".txt", ".py", ".js", ".java", ".cpp", ".ts")):
            path = os.path.join(root, file)

            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            modified = False
            for original, corrected in approved_changes.items():
                if original in content:
                    content = content.replace(original, corrected)
                    modified = True

            if modified:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)

print("✅ Approved corrections applied successfully.")
