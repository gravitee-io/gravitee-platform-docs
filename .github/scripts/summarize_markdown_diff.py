#!/usr/bin/env python3

import sys
import os
import re
from collections import Counter

def extract_title(content):
    """Extract first H1 as title."""
    match = re.search(r'^# (.+)', content, re.MULTILINE)
    return match.group(1).strip() if match else "Untitled"

def summarize_text(text, max_sentences=3):
    """Simple frequency-based summarizer."""
    sentences = re.split(r'(?<=[.!?]) +', text)
    words = re.findall(r'\w+', text.lower())
    freq = Counter(words)
    ranked = sorted(sentences, key=lambda s: sum(freq.get(w.lower(), 0) for w in s.split()), reverse=True)
    return ' '.join(ranked[:max_sentences])

def count_images(text):
    """Counts Markdown image links."""
    return len(re.findall(r'!\[.*?\]\(.*?\)', text))

def count_words(text):
    """Counts number of words in text."""
    return len(re.findall(r'\w+', text))

def process_file(filepath, diff_content):
    if not os.path.exists(filepath):
        return  # File was deleted or doesn't exist in this branch

    with open(filepath, 'r', encoding='utf-8') as f:
        full_content = f.read()

    title = extract_title(full_content)

    added_lines = [line[1:] for line in diff_content.splitlines() if line.startswith('+') and not line.startswith('+++')]
    added_content = '\n'.join(added_lines)

    image_count = count_images(added_content)
    word_count = count_words(added_content)

    if image_count < 3 and word_count < 100:
        return  # Not significant enough

    summary = summarize_text(added_content)

    page_url = f"https://github.com/gravitee-io/gravitee-platform-docs/blob/main/{filepath}"
    print(f"### {title}\n{page_url}\n\n{summary}\n")

if __name__ == "__main__":
    for arg in sys.argv[1:]:
        file_path, diff_path = arg.split('::')
        if os.path.exists(diff_path):
            with open(diff_path, 'r', encoding='utf-8') as f:
                diff = f.read()
            process_file(file_path, diff)
