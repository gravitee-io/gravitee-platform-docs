import re
import os
import language_tool_python

# ✅ Load ignore list
ignore_list = {}
with open(".github/spellcheck-ignore.txt", "r", encoding="utf-8") as f:
    for line in f:
        word = line.strip()
        ignore_list[word.lower()] = word  # Preserve case sensitivity

# ✅ Load LanguageTool
try:
    tool = language_tool_python.LanguageTool('en-US')
except Exception:
    print("Error: LanguageTool failed to initialize. Skipping grammar check.")
    tool = None

# ✅ Function to check if a line is inside a code block or comment
def is_comment(line, inside_code_block, inside_block_comment):
    if re.match(r'^\s*```', line):  
        return not inside_code_block, inside_block_comment, False
    if inside_code_block:
        return inside_code_block, inside_block_comment, bool(re.match(r'^\s*(#|//|\*)', line))
    if re.search(r'/\*', line):  # Start of multi-line block comment
        return inside_code_block, True, False
    if re.search(r'\*/', line):  # End of multi-line block comment
        return inside_code_block, False, False
    return inside_code_block, inside_block_comment, False

# ✅ Function to check if a line contains a URL or file path
def is_code_or_url(line):
    return bool(re.search(r"https?://\S+|`.*?`|www\.\S+", line))  # Properly escaped

# ✅ Function to apply spellchecking
def apply_spellcheck(sentence):
    words = sentence.split()
    return " ".join([ignore_list.get(word.lower(), word) for word in words])

# ✅ Function to apply grammar corrections safely
def apply_grammar(sentence):
    if not tool:
        return sentence
    try:
        matches = tool.check(sentence)
    except Exception:
        return sentence
    
    corrections = []
    for match in matches:
        if match.replacements and match.context.lower() not in ignore_list:
            corrections.append((match.offset, match.context, match.replacements[0]))

    # Apply corrections in reverse order to prevent offset shifting
    for offset, original, replacement in sorted(corrections, key=lambda x: -x[0]):
        if offset + len(original) <= len(sentence):
            sentence = sentence[:offset] + replacement + sentence[offset + len(original):]

    return sentence

# ✅ Process each file
changes = []
for root, _, files in os.walk("."):
    for file in files:
        if file.endswith((".md", ".txt", ".py", ".js", ".java", ".cpp", ".ts")):
            path = os.path.join(root, file)
            lines = open(path, "r", encoding="utf-8").readlines()
            inside_code, inside_block_comment = False, False

            for line in lines:
                orig = line.strip()
                inside_code, inside_block_comment, is_comment = is_comment(line, inside_code, inside_block_comment)

                # ✅ Skip non-editable lines
                if inside_code and not is_comment or inside_block_comment or not orig or is_code_or_url(orig):
                    continue

                # ✅ Apply spellcheck & grammar correction
                fixed = apply_spellcheck(orig)
                corrected = apply_grammar(fixed)

                # ✅ Prevent punctuation issues
                corrected = corrected.replace("..", ".").replace(",.", ".").replace(" ,", ",")

                if corrected != orig:
                    changes.append((path, orig, corrected))

# ✅ Create review file
if changes:
    with open("spellcheck_review.md", "w", encoding="utf-8") as f:
        f.write("# Spellcheck & Grammar Fixes Review\n\n")
        for i, (file, original, corrected) in enumerate(changes):
            f.write(f"### Change {i+1}\n")
            f.write(f"**File:** `{file}`\n")
            f.write(f"**Original:** `{original}`\n")
            f.write(f"**Suggested:** `{corrected}`\n")
            f.write("Approve? (yes/no)\n\n")
