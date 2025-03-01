import os
import re

# ✅ Read approved corrections
corrections = []
with open("corrections.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(0, len(lines), 4):  # Each entry is 4 lines (Original, Suggested, Approval, Blank)
    if i + 2 >= len(lines):  # Ensure there are enough lines to process
        break
    original = lines[i].strip().replace("Original: ", "")
    suggested = lines[i + 1].strip().replace("Suggested: ", "")
    decision = lines[i + 2].strip().lower()

    if decision == "yes":
        corrections.append((original, suggested))

# ✅ Apply approved corrections to files
for root, _, files in os.walk("."):
    for file in files:
        if file.endswith((".md", ".txt", ".py", ".js", ".java", ".cpp", ".ts")):
            path = os.path.join(root, file)

            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            modified_content = content
            for original, suggested in corrections:
                # Replace only full-word matches
                modified_content = re.sub(rf'\b{re.escape(original)}\b', suggested, modified_content)

            # Write back only if changes were made
            if modified_content != content:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(modified_content)

print("✅ Approved corrections applied successfully.")
