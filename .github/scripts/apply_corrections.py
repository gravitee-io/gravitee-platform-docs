import os

corrections_file = ".github/corrections/corrections.txt"
if not os.path.exists(corrections_file):
    print("❌ Error: No corrections file found. Please upload the reviewed corrections.")
    exit(1)

approved_corrections = []
with open(corrections_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(0, len(lines), 3):
    original = lines[i].replace("**Original:** ", "").strip()
    suggested = lines[i+1].replace("**Suggested:** ", "").strip()
    approval = lines[i+2].strip().lower()

    if approval == "yes":
        approved_corrections.append((original, suggested))

# Apply changes
for root, _, files in os.walk("."):
    for file in files:
        if file.endswith((".md", ".txt", ".py", ".js", ".java", ".cpp", ".ts")):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            for original, suggested in approved_corrections:
                content = content.replace(original, suggested)

            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

print(f"✅ Applied {len(approved_corrections)} approved corrections.")
