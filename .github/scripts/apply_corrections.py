import os
import sys

corrections_file = os.path.join(os.getcwd(), ".github/corrections/corrections.txt")
print(f"📄 Looking for corrections file at: {corrections_file}")

# Debug: Check if corrections file exists
if not os.path.exists(corrections_file):
    print("❌ Error: No corrections file found. Please upload the reviewed corrections.")
    sys.exit(1)

# Debug: Print corrections file content
print("📄 Corrections file contents:")
with open(corrections_file, "r", encoding="utf-8") as f:
    lines = f.readlines()
    print("".join(lines))  # Print entire corrections file for debugging

approved_corrections = []
for i in range(0, len(lines), 4):  # Every correction is stored in 4 lines
    if "File:" in lines[i] and "**Original:**" in lines[i+1] and "**Suggested:**" in lines[i+2]:
        file_info = lines[i].replace("File: ", "").strip()
        original = lines[i+1].replace("**Original:** ", "").strip()
        suggested = lines[i+2].replace("**Suggested:** ", "").strip()
        approval = lines[i+3].strip().lower()

        print(f"🔍 Checking: {file_info} | Original: {original} | Suggested: {suggested} | Approved: {approval}")

        if approval == "yes":
            approved_corrections.append((file_info, original, suggested))

# Debug: Print approved corrections
print(f"✅ Approved Corrections Found: {len(approved_corrections)}")
if not approved_corrections:
    print("❌ No approved corrections found. Exiting.")
    sys.exit(1)

for file_path, original, suggested in approved_corrections:
    if not os.path.exists(file_path):
        print(f"⚠️ Skipping: {file_path} (file not found)")
        continue

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if original not in content:
        print(f"⚠️ Warning: '{original}' not found in {file_path}. Skipping replacement.")
        continue

    updated_content = content.replace(original, suggested)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(updated_content)

print(f"✅ Successfully applied {len(approved_corrections)} approved corrections.")
