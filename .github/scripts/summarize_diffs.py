import sys
import os
import difflib
import re
import json
from pathlib import Path
from markdown import markdown
from bs4 import BeautifulSoup

def extract_title(md_content):
    for line in md_content.splitlines():
        if line.strip().startswith('#'):
            return line.strip().lstrip('#').strip()
    return "Untitled"

def word_count(text):
    return len(re.findall(r'\w+', text))

def image_count(md_content):
    return len(re.findall(r'!\[.*?\]\(.*?\)', md_content))

def summarize_diff(old, new):
    old_words = word_count(old)
    new_words = word_count(new)
    wc_diff = abs(new_words - old_words)

    old_imgs = image_count(old)
    new_imgs = image_count(new)
    img_diff = abs(new_imgs - old_imgs)

    new_lines = new.splitlines()
    diff = list(difflib.unified_diff(old.splitlines(), new_lines, lineterm=''))
    added_lines = [line[1:].strip() for line in diff if line.startswith('+') and not line.startswith('+++')]

    summary_text = ' '.join(added_lines)
    summary_html = markdown(summary_text)
    summary = BeautifulSoup(summary_html, "html.parser").get_text()
    summary = re.sub(r'\s+', ' ', summary).strip()
    if len(summary) > 400:
        summary = summary[:397] + '...'
    
    return {
        "significant": wc_diff >= 100 or img_diff >= 3,
        "summary": summary
    }

def main():
    base_dir = Path(sys.argv[1])
    sha_before = sys.argv[2]
    sha_after = sys.argv[3]
    repo_url = sys.argv[4]

    os.system(f'git checkout {sha_before}')
    old_files = {f for f in base_dir.rglob("*.md")}

    os.system(f'git checkout {sha_after}')
    new_files = {f for f in base_dir.rglob("*.md")}

    added = new_files - old_files
    existing = new_files & old_files

    results = []

    for f in added:
        content = f.read_text(encoding="utf-8")
        if word_count(content) >= 100 or image_count(content) >= 3:
            results.append({
                "title": extract_title(content),
                "link": f"{repo_url}/blob/main/{f.relative_to(base_dir)}",
                "summary": BeautifulSoup(markdown(content), "html.parser").get_text()[:400].strip()
            })

    for f in existing:
        old_content = os.popen(f'git show {sha_before}:{f}').read()
        new_content = f.read_text(encoding="utf-8")
        diff = summarize_diff(old_content, new_content)
        if diff["significant"]:
            results.append({
                "title": extract_title(new_content),
                "link": f"{repo_url}/blob/main/{f.relative_to(base_dir)}",
                "summary": diff["summary"]
            })

    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
