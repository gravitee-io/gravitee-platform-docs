import os
import re
import language_tool_python

# Load spellcheck ignore list
ignore_list = {}
ignore_file = ".github/spellcheck-ignore.txt"
if os.path.exists(ignore_file):
    with open(ignore_file, "r", encoding="utf-8") as f:
        for line in f:
            word = line.strip()
            ignore_list[word.lower()] = word  # Preserve case

# Load previously approved corrections
review_file = "corrections_review.txt"
approved_corrections = set()
if os.path.exists(review_file):
    with open(review_file, "r", encoding="utf-8") as f:
        approved_corrections = {line.strip() for line in f}

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

# Process each file and request approval for each correction
for root, _, files in os.walk("."):
    for file in files:
        if file.endswith((".md", ".txt", ".py", ".js", ".java", ".cpp", ".ts")):
            path = os.path.join(root, file)
            lines = open(path, "r", encoding="utf-8").readlines()
            new_lines = []

            for line in lines:
                orig = line.strip()
                
                # Skip URLs, code, or empty lines
                if not orig or is_code_or_url(orig):
                    new_lines.append(line)
                    continue
                
                # Apply spellcheck and grammar
                spellchecked = apply_spellcheck(orig)
                corrected = apply_grammar(spellchecked)
                
                # If there's a correction, prompt for approval
                if corrected != orig and corrected not in approved_corrections:
                    print(f"\nOriginal:  {orig}")
                    print(f"Suggested: {corrected}")
                    decision = input("Approve this change? (yes/no/exit): ").strip().lower()
                    
                    if decision == "yes":
                        new_lines.append(corrected + "\n")
                        approved_corrections.add(corrected)
                    elif decision == "exit":
                        print("Saving progress and exiting...")
                        with open(review_file, "w", encoding="utf-8") as f:
                            f.writelines([c + "\n" for c in approved_corrections])
                        exit(0)
                    else:
                        new_lines.append(line)
                else:
                    new_lines.append(line)

            # Write changes back
            with open(path, "w", encoding="utf-8") as f:
                f.writelines(new_lines)

# Save approved corrections
with open(review_file, "w", encoding="utf-8") as f:
    f.writelines([c + "\n" for c in approved_corrections])

print("Review complete. All approved changes have been applied.")
