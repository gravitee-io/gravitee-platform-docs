
# 🚀 GitHub Action: Gravitee APIM Redirect Mapping

This GitHub Action automates the generation of redirect rules for your versioned Gravitee APIM documentation. It compares markdown files across specified versions using full content similarity (TF-IDF + cosine) and outputs redirects in multiple formats.

---

## 📂 Included Files

This action includes:

- `.github/scripts/generate_redirects.py`  
  A Python script that:
  - Scans only specified APIM version folders (`4.0` through `4.7x`)
  - Compares markdown files using content similarity
  - Outputs renamed, moved, and vanished page mappings
  - Exports redirect files for Netlify, NGINX, Cloudflare, and more

- `.github/workflows/redirect-mapping.yml`  
  A GitHub Actions workflow that:
  - Runs on every push to `docs/apim/*.md` or manual trigger
  - Installs Python dependencies
  - Runs the redirect script
  - Uploads all redirect artifacts

---

## 🧰 How to Use

1. **Copy Files to Your Repo**
   - Place `generate_redirects.py` into `.github/scripts/`
   - Place `redirect-mapping.yml` into `.github/workflows/`

2. **Ensure Directory Structure**
   Your repo should contain documentation in this structure:
   ```
   docs/
     apim/
       4.0/
       4.1/
       ...
       4.7x/
   ```

3. **Trigger the Workflow**
   - **Manual:** Go to "Actions" tab → "Generate Redirect Mappings" → Run workflow
   - **Automatic:** Push changes to any markdown file inside `docs/apim/**`

---

## 📦 Output Artifacts

After each run, the following files are uploaded:

| File                                | Purpose                             |
|-------------------------------------|-------------------------------------|
| `content_based_redirects_renamed.csv`  | Pages renamed (by content match)    |
| `content_based_redirects_moved.csv`    | Pages moved (same content, new path)|
| `content_based_redirects_vanished.csv`| Pages removed or unmatched          |
| `content_based_redirects_all.json`    | Full redirect mapping in JSON       |
| `_redirects`                          | Netlify-compatible redirects        |
| `nginx_redirects.conf`               | NGINX rewrite rules                 |
| `cloudflare_redirects.json`         | Cloudflare Worker/Rules format      |
| `content_based_redirect_summary.md` | Human-readable summary              |

---

## ✅ Benefits

- Full content comparison — avoids false matches on duplicate titles
- Export-ready formats for static CDNs and reverse proxies
- Simple to integrate and rerun

---

For questions or improvements, feel free to fork and customize!
