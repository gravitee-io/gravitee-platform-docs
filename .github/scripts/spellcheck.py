import os
import json
import re

try:
    from gingerit.gingerit import GingerIt
except ImportError:
    print("❌ Error: `gingerit` module is missing. Install it with `pip install gingerit`.")
    exit(1)

parser = GingerIt()

# Load ignore list
ignore_list = {}
ignore_file = ".github/spellcheck-ignore.txt"
if os.path.exists(ignore_file):
    with open(ignore_file, "r", encoding="utf-8") as f:
        ignore_list = {word.strip().lower(): word.strip() for word in f.readlines()}

def is_code_or_url(line):
    return bool(re.search(r'https?://\S+|`.*?`|www\.\S+', line))

def correct_grammar(sentence):
    try:
        result = parser.parse(sentence)
        return result["result"] if "result" in result else sentence
    except Exception:
        print(f"⚠️ Warning: Timeout checking grammar for: {sentence}")
        return sentence

# Process files
corrections = []
for root, _, files in os.walk("."):
    for file in files:
        if file.endswith((".md", ".txt", ".py", ".js", ".java", ".cpp", ".ts")):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            for line in lines:
                original = line.strip()
                if not original or is_code_or_url(original):
                    continue
                
                corrected = correct_grammar(original)
                if original != corrected:
                    corrections.append({"original": original, "suggested": corrected})

# Save corrections to file
os.makedirs(".github/corrections", exist_ok=True)
corrections_path = ".github/corrections/corrections.txt"
with open(corrections_path, "w", encoding="utf-8") as f:
    for correction in corrections:
        f.write(f"**Original:** {correction['original']}\n")
        f.write(f"**Suggested:** {correction['suggested']}\n")
        f.write("Approve? (yes/no)\n\n")

print(f"✅ {len(corrections)} corrections generated. Review in `corrections.txt` and upload the approved version.")
