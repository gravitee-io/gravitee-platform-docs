# How-To Guide: Running the Automated Spellcheck & PR Creation Workflow

## 1. Trigger the Workflow
1. Navigate to the **GitHub repository**.
2. Go to the **"Actions"** tab.
3. Find the workflow named **"Automated Spellcheck & PR Creation"**.
4. Click **"Run workflow"**.

## 2. Review & Debug
- The workflow will install dependencies and execute spellchecking.
- If no issues are found, it will **exit without making changes**.
- If corrections are needed, it will apply them **directly** to the affected files.

## 3. Reviewing the Pull Request
1. Once the workflow completes, a **PR is automatically created**.
2. Go to the **"Pull Requests"** tab in the repository.
3. Locate the PR titled **"Automated Spellcheck & Grammar Fixes"**.
4. Review the changes in the **Files Changed** tab.
5. If all corrections look good, **merge the PR**.

## 4. Troubleshooting
| Issue | Possible Cause | Solution |
|--------|--------------|----------|
| **Workflow does not trigger** | The workflow is not manually triggered | Ensure you click "Run workflow" in GitHub Actions |
| **PR not created** | No spelling errors found | Check logs in the Actions tab to confirm |
| **Unexpected word replacements** | The word is inside a link or code block | Check the ignore conditions in the script |
| **Merge conflicts in PR** | The `spellcheck-auto-fixes` branch is outdated | Manually rebase and resolve conflicts before merging |

## 5. How to Manually Rebase and Resolve Merge Conflicts
If a merge conflict occurs when pushing to `spellcheck-auto-fixes`, follow these steps:

```sh
git checkout spellcheck-auto-fixes
git fetch origin main
git rebase origin/main
# Resolve conflicts manually
git add .
git rebase --continue
git push origin spellcheck-auto-fixes --force