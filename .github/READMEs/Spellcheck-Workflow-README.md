# Automated Spellcheck & PR Creation Workflow

## Overview
This GitHub Actions workflow automates spellchecking and grammar correction in a repository. 
It runs manually via `workflow_dispatch` and automatically applies corrections, ensuring that 
formatting and indentation are preserved. The corrected files are committed to a new branch, 
and a pull request (PR) is created for review.

---

## Workflow Details

### 1. Workflow Execution
- The workflow is triggered manually using `workflow_dispatch`.
- Runs on an `ubuntu-latest` runner.

### 2. Dependencies
The following dependencies are installed:
- **`codespell`**: Identifies and corrects common misspellings.
- **`fuzzywuzzy[speedup]`**: Improves spellcheck accuracy by finding the closest match to a word.
- **`sentence-splitter`**: Helps preserve sentence structure when applying corrections.

### 3. Spellcheck Execution
- The workflow first verifies if `.github/spellcheck-ignore.txt` exists, which contains words 
  to be ignored by `codespell`.
- `codespell` is run with:
  - **Ignore list:** `.github/spellcheck-ignore.txt`
  - **Skipping specific files:** `.git`, `.lock`, `.json`, `.yaml`, `.yml`, `.css`, `.html`
  - **Quiet level:** Reduces verbosity of output.

### 4. Applying Corrections
Each detected spelling error is analyzed and corrected while preserving formatting:

#### 4.1. Handling Context-Specific Phrases
- Certain phrases need **context-aware** corrections, such as:
  - `"identiy provider"` → `"identity provider"`
  - `"access toekn"` → `"access token"`
  - `"user authentification"` → `"user authentication"`
  - `"API getway"` → `"API gateway"`
- Only the incorrect word in the phrase is corrected instead of replacing the entire phrase.

#### 4.2. Edge Cases & Rules
The following special cases are handled:
- **Ignore links**:
  - Markdown links `[text](https://example.com)`
  - Ensures only the **link text** is corrected, not the URL.
- **Ignore capitalization mistakes in ignore list**:
  - If a word exists in `.github/spellcheck-ignore.txt` but with different capitalization, 
    it is corrected to match the exact case.
- **Ignore words inside code blocks or hint sections**:
  - Does not modify `{% tab title="Example" %}` or `{% hint style="info" %}`.
- **Ignore corrections where the word is surrounded by non-space characters**:
  - Example: `/vertx-`, `/vertx.`, `.vertx.` **will not be corrected**.
- **Preserve punctuation**:
  - Prevents cases where `word.` is replaced with `word` (removing punctuation incorrectly).
- **Preserve indentation**:
  - If a correction is applied, the original spacing/indentation is **preserved**.
- **Only replaces the first instance of a misspelled word in a line**:
  - Ensures words are not incorrectly replaced as substrings of other words.

### 5. Committing Changes & Creating PR
- If any corrections are applied:
  - A new branch (`spellcheck-auto-fixes`) is created.
  - Changes are committed with the message:  
    **"✅ Automated Spellcheck & Grammar Fixes"**.
  - The latest remote branch changes are pulled using `git pull --rebase` to avoid conflicts.
  - The branch is force-pushed to the remote repository.
  - A pull request is automatically created using `gh pr create`.

---

## Troubleshooting

| Issue | Possible Cause | Solution |
|--------|--------------|----------|
| **Workflow does not trigger** | The workflow is not manually triggered | Ensure you click "Run workflow" in GitHub Actions |
| **PR not created** | No spelling errors found | Check logs in the Actions tab to confirm |
| **Unexpected word replacements** | The word is inside a link or code block | Check the ignore conditions in the script |
| **Merge conflicts in PR** | The `spellcheck-auto-fixes` branch is outdated | Manually rebase and resolve conflicts before merging |

---

## Conclusion
This workflow ensures high-quality documentation by **automating spellchecking** while **preserving 
formatting and indentation**. It streamlines the process by **directly applying fixes** and 
**creating a PR for easy review**. 🚀
