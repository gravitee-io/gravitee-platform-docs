# Summary of the Policy README Sync Workflow

## Overview

This GitHub Actions workflow automates the process of syncing policy README files from repositories in the Gravitee-io organization to a central documentation repository. The workflow detects changes in policy repositories and updates corresponding Markdown files in the docs repository. If changes are detected, a new branch is created with the updated documentation files. In our current setup, even if the pull request (PR) creation step “fails” (because you prefer to create the PR manually), the overall workflow passes.

## Key Files and Their Roles

### 1. `.github/workflows/sync-policy-readmes.yml`
- **Location:** `.github/workflows/` directory in the docs repository.
- **Purpose:**  
  - Defines the GitHub Actions workflow.
  - Configured to run manually via the `workflow_dispatch` event.
  - Sets necessary permissions (write access for repository contents and pull requests).
  - Contains steps to:
    - Check out the repository.
    - Set up Node.js.
    - Install dependencies.
    - Run the sync script (`sync-policy-readmes.js`).
    - Stage changes from the target docs folder.
    - Create a new branch and push the changes.
    - Attempt to create a pull request.
  - Uses `continue-on-error` for the PR creation step so that the workflow passes even if the PR isn’t automatically created.

### 2. `sync-policy-readmes.js`
- **Location:** Root of the docs repository.
- **Purpose:**
  - Uses the GitHub API to list all repositories in the Gravitee-io organization that have "policy" in their name.
  - For each matching repository:
    - Fetches the README file.
    - Extracts the title from the first Markdown header (or falls back to the repository name if no header is found).
    - Sanitizes the title (e.g., converts spaces to underscores and removes unwanted characters) to create a valid file name.
    - Writes or updates the corresponding Markdown file in the `docs/apim/4.6/policies/policy-reference` folder.
  - Logs progress and handles error cases (e.g., missing README or unexpected formats).

### 3. `package.json`
- **Location:** Root of the docs repository.
- **Purpose:**
  - Defines the project and its dependencies.
  - Specifies the dependency on `node-fetch` (version 2.x) used by `sync-policy-readmes.js` to make API requests.
  - Contains a start script (`npm start`) to run the sync script if needed.

### 4. `.gitignore`
- **Location:** Root of the docs repository.
- **Purpose:**
  - Excludes unwanted files (such as `node_modules/` and `package-lock.json`) from being committed.
  - Ensures that only the documentation changes (in the `docs/apim/4.6/policies/policy-reference` folder) are tracked by Git.

## Workflow Process Details

1. **Manual Trigger:**  
   The workflow is triggered manually via the GitHub Actions interface using the `workflow_dispatch` event. This allows for testing and on-demand updates.

2. **Repository Checkout and Setup:**  
   - The docs repository is checked out using a Personal Access Token (PAT) (`PAT_POLICY_BOT`).
   - Node.js (version 16) is set up, and dependencies are installed according to `package.json`.

3. **Running the Sync Script:**  
   - The `sync-policy-readmes.js` script is executed.
   - The script gathers README content from all policy repositories, processes it, and writes updated Markdown files into the designated documentation folder.

4. **Staging and Committing Changes:**  
   - Only changes in the `docs/apim/4.6/policies/policy-reference` folder are staged.
   - If differences are detected, a new branch (named with a timestamp) is created, and the changes are committed and pushed to the repository.

5. **Pull Request Creation (Optional):**  
   - The workflow attempts to create a pull request using the peter-evans/create-pull-request action.
   - If no differences are found or if the PR creation step “fails” (because you prefer to create the PR manually), the step is set to continue on error. This ensures that the overall workflow passes even if no PR is automatically opened.

## Outcome

- **Automated File Generation:**  
  The workflow successfully generates or updates Markdown files in the specified folder whenever policy repositories are updated.
- **Manual PR Creation:**  
  Since you prefer to create the pull request manually, the workflow is configured to pass even if the automatic PR step does not open one.
- **Clean and Focused Changes:**  
  With proper staging and the use of `.gitignore`, only the intended documentation changes are committed.
