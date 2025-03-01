import re
import os
import language_tool_python

# ✅ Load spellcheck ignore list
ignore_list = {}
with open(".github/spellcheck-ignore.txt", "r", encoding="utf-8") as f:
    for line in f:
        word = line.strip()
        ignore_list[word.lower()] = word

# ✅ Initialize LanguageTool with proper handling
try:
    tool = language_tool_python.LanguageTool('en-US')
except Exception as e:
    print(f"Error initializing LanguageTool: {e}")
    tool = None

# ✅ Function to detect code blocks & comments
def check_comment_status(line, inside_code_block, inside_block_comment):
    if re.match(r'^\s*```', line):  
        return not inside_code_block, inside_block_comment, False
    if inside_code_block:
        return inside_code_block, inside_block_comment, bool(re.match(r'^\s*(#|//|\*)', line))
    if re.search(r'/\*', line):  # Start of multi-line block comment
        return inside_code_block, True, False
    if re.search(r'\*/', line):  # End of multi-line block comment
        return inside_code_block, False, False
    return inside_code_block, inside_block_comment, False

# ✅ Function to check if a line contains a URL or a file path
def is_code_or_url(line):
    return bool(re.search(r'https?://\S+|`.*?`|www\.\S+', line))

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

    # Apply corrections in reverse order to avoid offset issues
    for offset, original, replacement in sorted(corrections, key=lambda x: -x[0]):
        if offset + len(original) <= len(sentence):
            sentence = sentence[:offset] + replacement + sentence[offset + len(original):]

    return sentence

# ✅ Process each file
with open("corrections.txt", "w", encoding="utf-8") as f:
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith((".md", ".txt", ".py", ".js", ".java", ".cpp", ".ts")):
                path = os.path.join(root, file)
                lines = open(path, "r", encoding="utf-8").readlines()
                inside_code, inside_block_comment = False, False
                for line in lines:
                    orig = line.strip()
                    inside_code, inside_block_comment, is_comment = check_comment_status(line, inside_code, inside_block_comment)

                    # ✅ Skip grammar correction for code but apply to comments
                    if inside_code and not is_comment or inside_block_comment or not orig or is_code_or_url(orig):
                        continue

                    # ✅ Apply spellcheck
                    fixed = apply_spellcheck(orig)

                    # ✅ Apply grammar correction
                    corrected = apply_grammar(fixed)

                    # ✅ Prevent punctuation issues
                    corrected = corrected.replace("..", ".").replace(",.", ".").replace(" ,", ",")

                    if corrected != orig:
                        f.write(f"Original: {orig}\n")
                        f.write(f"Suggested: {corrected}\n")
                        f.write("Approve? (yes/no/exit): \n")
