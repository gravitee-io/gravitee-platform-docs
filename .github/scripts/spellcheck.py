import os
import re
import language_tool_python

# Load ignore list
ignore_list = {}
ignore_file = ".github/spellcheck-ignore.txt"
if os.path.exists(ignore_file):
    with open(ignore_file, "r", encoding="utf-8") as f:
        for line in f:
            word = line.strip()
            ignore_list[word.lower()] = word  # Preserve case

# Initialize LanguageTool
tool = language_tool_python.LanguageTool('en-US')

def is_code_or_url(line):
    return bool(re.search(r'https?://\S+|`.*?`|www\.\S+', line))

def apply_spellcheck(sentence):
    return " ".join([ignore_list.get(word.lower(), word) for word in sentence.split()])

def apply_grammar(sentence):
    matches = tool.check(sentence)
    corrections = []
    for match in matches:
        if match.replacements and match.context.lower() not in ignore_list:
            corrections.append((match.offset, match.context, match.replacements[0]))
    for offset, original, replacement in sorted(corrections, key=lambda x: -x[0]):
        if offset + len(original) <= len(sentence):
            sentence = sentence[:offset] + replacement + sentence[offset + len(original):]
    return sentence

# Collect corrections
corrections = []
for root, _, files in os.walk("."):
    for file in files:
        if file.endswith((".md", ".txt", ".py", ".js", ".java", ".cpp", ".ts")):
            path = os.path.join(root, file)
            lines = open(path, "r", encoding="utf-8").readlines()

            for line in lines:
                orig = line.strip()
                if not orig or is_code_or_url(orig):
                    continue
                
                spellchecked = apply_spellcheck(orig)
                corrected = apply_grammar(spellchecked)

                if corrected != orig:
                    corrections.append(f"File: {path}\nOriginal: {orig}\nSuggested: {corrected}\n\n")

# Write all corrections to a file for manual review
review_file = "corrections_review.txt"
with open(review_file, "w", encoding="utf-8") as f:
    f.writelines(corrections)

print(f"Corrections written to {review_file}. Review and upload back for approval.")
