import os

# ✅ Load user-approved corrections
approved_corrections = {}
with open(".github/spellcheck_review.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(0, len(lines), 4):
    original = lines[i].strip().replace("Original: ", "")
    suggested = lines[i+1].strip().replace("Suggested: ", "")
    decision = lines[i+2].strip().lower()

    if decision == "yes":
        approved_corrections[original] = suggested

# ✅ Process files and apply approved corrections
for root, _, files in os.walk("."):
    for file in files:
        if file.endswith((".md", ".txt", ".py", ".js", ".java", ".cpp", ".ts")):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            for original, suggested in approved_corrections.items():
                content = content.replace(original, suggested)

            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

print("Approved corrections have been applied successfully!")
