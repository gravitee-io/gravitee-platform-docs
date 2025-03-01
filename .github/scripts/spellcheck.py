import re
import os
import language_tool_python
import signal

# ✅ Load ignore list
ignore_list = {line.strip().lower(): line.strip() for line in open(".github/spellcheck-ignore.txt", encoding="utf-8")}

# ✅ Initialize LanguageTool with fail-safe
try:
    tool = language_tool_python.LanguageTool('en-US')
except Exception as e:
    print(f"⚠️ Error initializing LanguageTool: {e}")
    tool = None

timeout_log = ".github/spellcheck-timeouts.log"

def detect_comment(line, inside_code, inside_block):
    if re.match(r'^\s*```', line):
        return not inside_code, inside_block, False
    if inside_code:
        return inside_code, inside_block, bool(re.match(r'^\s*(#|//|\*)', line))
    if re.search(r'/\*', line):
        return inside_code, True, False
    if re.search(r'\*/', line):
        return inside_code, False, False
    return inside_code, inside_block, False

def apply_spellcheck(sentence):
    return " ".join([ignore_list.get(word.lower(), word) for word in sentence.split()])

def apply_grammar(sentence):
    if not tool:
        return sentence
    def timeout_handler(signum, frame):
        raise TimeoutError("LanguageTool check() took too long!")
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(10)
    try:
        matches = tool.check(sentence)
        signal.alarm(0)
    except TimeoutError:
        print(f"⚠️ Timeout: Skipping {sentence}")
        with open(timeout_log, "a") as log:
            log.write(sentence + "\n")
        return sentence
    return sentence

# ✅ Process files
for root, _, files in os.walk("."):
    for file in files:
        if file.endswith((".md", ".txt", ".py", ".js", ".java", ".cpp", ".ts")):
            path = os.path.join(root, file)
            lines = open(path, encoding="utf-8").readlines()
            inside_code, inside_block = False, False
            with open("corrections.txt", "w") as f:
                for line in lines:
                    orig = line.strip()
                    inside_code, inside_block, is_comment = detect_comment(line, inside_code, inside_block)
                    if inside_code and not is_comment or inside_block or not orig:
                        continue
                    corrected = apply_grammar(apply_spellcheck(orig))
                    f.write(f"Original: {orig}\nSuggested: {corrected}\n\n")
