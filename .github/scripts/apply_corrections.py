import os

# Load reviewed corrections
review_file = "corrections_review.txt"

if not os.path.exists(review_file):
    print(f"No corrections found in {review_file}. Exiting.")
    exit(0)

# Read approved corrections
with open(review_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

corrections = []
file_map = {}

# Parse corrections from file
for i in range(0, len(lines), 4):  # Grouping every 4 lines as one correction set
    if "File:" in lines[i] and "Original:" in lines[i + 1] and "Suggested:" in lines[i + 2]:
        file_path = lines[i].split("File: ")[1].strip()
        original = lines[i + 1].split("Original: ")[1].strip()
        suggested = lines[i + 2].split("Suggested: ")[1].strip()

        if file_path not in file_map:
            file_map[file_path] = []
        file_map[file_path].append((original, suggested))

# Apply corrections to files
for file_path, changes in file_map.items():
    if not os.path.exists(file_path):
        print(f"File {file_path} not found. Skipping.")
        continue

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    for original, suggested in changes:
        content = content.replace(original, suggested)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Approved corrections have been applied.")
