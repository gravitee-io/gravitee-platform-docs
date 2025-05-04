
import os
import json
import pandas as pd
from pathlib import Path
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = Path("docs/apim")

def load_docs(base_dir):
    version_docs = defaultdict(list)
    allowed_versions = ["4.0", "4.1", "4.2", "4.3", "4.4", "4.5", "4.6", "4.7", "4.7x"]
    for version_name in allowed_versions:
        version_dir = base_dir / version_name
        if not version_dir.exists():
            print(f"Skipping missing version: {version_name}")
            continue
        for md_file in version_dir.rglob("*.md"):
            try:
                with open(md_file, "r", encoding="utf-8") as f:
                    content = f.read()
                relative_path = md_file.relative_to(base_dir).as_posix()
                title = content.strip().splitlines()[0].strip("# ").strip()
                version_docs[version_name].append({
                    "path": relative_path,
                    "title": title,
                    "content": content
                })
            except Exception as e:
                print(f"Error reading {md_file}: {e}")
    return version_docs

version_docs = load_docs(BASE_DIR)
sorted_versions = sorted(version_docs.keys())
redirects = {"renamed": [], "moved": [], "vanished": []}

for i in range(len(sorted_versions) - 1):
    v1, v2 = sorted_versions[i], sorted_versions[i + 1]
    docs_v1, docs_v2 = version_docs[v1], version_docs[v2]

    if not docs_v1 or not docs_v2:
        continue

    v1_texts = [doc["content"] for doc in docs_v1]
    v2_texts = [doc["content"] for doc in docs_v2]

    vectorizer = TfidfVectorizer().fit(v1_texts + v2_texts)
    v1_matrix = vectorizer.transform(v1_texts)
    v2_matrix = vectorizer.transform(v2_texts)

    sim_matrix = cosine_similarity(v1_matrix, v2_matrix)

    matched_v2_indices = set()
    for idx1, sim_row in enumerate(sim_matrix):
        best_idx2 = sim_row.argmax()
        best_score = sim_row[best_idx2]
        doc1 = docs_v1[idx1]
        doc2 = docs_v2[best_idx2]

        if best_score >= 0.9 and best_idx2 not in matched_v2_indices:
            matched_v2_indices.add(best_idx2)
            if doc1["path"] == doc2["path"]:
                continue
            elif doc1["title"] == doc2["title"]:
                redirects["moved"].append({
                    "from_version": v1, "to_version": v2,
                    "from_path": doc1["path"], "to_path": doc2["path"],
                    "score": round(best_score, 3)
                })
            else:
                redirects["renamed"].append({
                    "from_version": v1, "to_version": v2,
                    "from_path": doc1["path"], "to_path": doc2["path"],
                    "score": round(best_score, 3)
                })
        else:
            redirects["vanished"].append({
                "from_version": v1, "to_version": v2,
                "from_path": doc1["path"], "reason": "No strong content match"
            })

Path("redirect_outputs").mkdir(exist_ok=True)

pd.DataFrame(redirects["renamed"]).to_csv("redirect_outputs/content_based_redirects_renamed.csv", index=False)
pd.DataFrame(redirects["moved"]).to_csv("redirect_outputs/content_based_redirects_moved.csv", index=False)
pd.DataFrame(redirects["vanished"]).to_csv("redirect_outputs/content_based_redirects_vanished.csv", index=False)

with open("redirect_outputs/content_based_redirects_all.json", "w", encoding="utf-8") as f:
    json.dump(redirects, f, indent=2)

with open("redirect_outputs/_redirects", "w", encoding="utf-8") as f:
    for entry in redirects["renamed"] + redirects["moved"]:
        from_path = f"/{entry['from_version']}/{entry['from_path'].split('/', 1)[-1]}"
        to_path = f"/{entry['to_version']}/{entry['to_path'].split('/', 1)[-1]}"
        f.write(f"{from_path} {to_path} 301!\n")

with open("redirect_outputs/nginx_redirects.conf", "w", encoding="utf-8") as f:
    for entry in redirects["renamed"] + redirects["moved"]:
        from_path = f"/{entry['from_version']}/{entry['from_path'].split('/', 1)[-1]}"
        to_path = f"/{entry['to_version']}/{entry['to_path'].split('/', 1)[-1]}"
        f.write(f"rewrite ^{from_path}$ {to_path} permanent;\n")

cloudflare_rules = []
for entry in redirects["renamed"] + redirects["moved"]:
    from_path = f"/{entry['from_version']}/{entry['from_path'].split('/', 1)[-1]}"
    to_path = f"/{entry['to_version']}/{entry['to_path'].split('/', 1)[-1]}"
    cloudflare_rules.append({
        "source": from_path, "target": to_path, "status": 301
    })

with open("redirect_outputs/cloudflare_redirects.json", "w", encoding="utf-8") as f:
    json.dump(cloudflare_rules, f, indent=2)

summary_md = '''
# 🔁 Content-Based Redirect Mapping – Output Summary

This summary lists all generated redirect files for maintaining URL integrity across APIM documentation versions.

---

## 📊 CSV Downloads

- `content_based_redirects_renamed.csv`: Renamed pages based on content similarity.
- `content_based_redirects_moved.csv`: Pages moved to a different path with identical content.
- `content_based_redirects_vanished.csv`: Pages with no strong content match in the next version.

---

## 🧩 JSON Mapping

- `content_based_redirects_all.json`: Combined JSON containing all redirect categories.

---

## 📁 Redirect Files

- `_redirects`: Netlify-style redirects.
- `nginx_redirects.conf`: NGINX rewrite rules.
- `cloudflare_redirects.json`: Cloudflare Page Rules in JSON format.
'''

with open("redirect_outputs/content_based_redirect_summary.md", "w", encoding="utf-8") as f:
    f.write(summary_md.strip())
