import os
import re
import json
from spellchecker import SpellChecker
from gingerit.gingerit import GingerIt  # ✅ NEW: Use GingerIt for grammar

# Load spellcheck ignore list
ignore_list = {line.strip().lower(): line.strip() for line in open(".github/spellcheck-ignore.txt", "r", encoding="utf-8")}

# ✅ Initialize spellchecker and grammar checker
spell = SpellChecker()
grammar_parser = GingerIt()  # ✅ NEW: Use GingerIt

def is_comment(line, inside_code_block):
    """Detects whether a line is inside a code block or is a comment."""
    if re.match(r'^\s*```', line):  
        return not inside_code_block, False
    return inside_code_block, bool(re.match(r'^\s*(#|//|\*)', line))

def is_code_or_url(line):
    """Skips lines containing URLs, file paths, or inline code."""
    return bool(re.search(r'https?://\S+|`.*?`|www\.\S+', line))

def apply_spellcheck(sentence):
    """Applies spellcheck while preserving words in the ignore list."""
    words = sentence.split()
    corrected_words = [ignore_list.get(word.lower(), word) if word.lower() in ignore_list else spell.correction(word) or word for word in words]
    return " ".join(corrected_words)

def apply_grammar(sentence):
    """Applies grammar correction using GingerIt."""
    corrected = grammar_parser.parse(sentence)  # ✅ Using GingerIt
    return corrected["result"] if "result" in corrected else sentence

# ✅ Process files
corrections = []
for root, _, files in os.walk("."):
    for file in files:
        if file.endswith((".md", ".txt", ".py", ".js", ".java", ".cpp", ".ts")):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            inside_code = False
            modified_lines = []
            
            for line in lines:
                orig = line.strip()
                inside_code, is_comment = is_comment(line, inside_code)
                
                if inside_code and not is_comment or not orig or is_code_or_url(orig):
                    modified_lines.append(line)
                    continue
                
                # Apply spellcheck and grammar correction
                spellchecked = apply_spellcheck(orig)
                grammatically_corrected = apply_grammar(spellchecked)

                if orig != grammatically_corrected:
                    corrections.append({"original": orig, "suggested": grammatically_corrected, "file": path})
                
                modified_lines.append(grammatically_corrected + "\n")

            with open(path, "w", encoding="utf-8") as f:
                f.writelines(modified_lines)

# ✅ Save corrections for review
with open("corrections.json", "w", encoding="utf-8") as f:
    json.dump(corrections, f, indent=4)

print("✅ Spellcheck & Grammar Review Complete. Download `corrections.json` to review changes.")
