import os
import re
import json
import sys

try:
    from gingerit.gingerit import GingerIt
    from pyspellchecker import SpellChecker
    from sentence_splitter import SentenceSplitter
except ImportError:
    print("❌ Error: Required modules not found. Ensure the virtual environment is activated.")
    sys.exit(1)

parser = GingerIt()
spell = SpellChecker()
splitter = SentenceSplitter(language='en')

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
        return result.get("result", sentence)
    except Exception as e:
        print(f"⚠️ Warning: Grammar check failed for: {sentence}\nError: {e}")
        return sentence  # Return original if correction fails

# Process files
corrections = []
valid_extensions = {".md", ".txt", ".py", ".js", ".java", ".cpp", ".ts"}
for root, _, files in os.walk("."):
    for file in files:
        if not any(file.endswith(ext) for ext in valid_extensions):
            continue  # Skip unknown files

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
