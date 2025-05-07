
# 📘 GitHub Actions Workflow: `gitbook-sync-notifier.yml`

This guide explains the GitHub Actions workflow used to send Slack notifications when `.md` files in the `docs/` directory are changed in the `main` branch. It includes a fix to ensure only Markdown files are monitored.

---

## 🧾 Summary

- **Trigger:** Push events on the `main` branch.
- **Purpose:** Notify Slack when `.md` files under `docs/` are modified.
- **Exclusions:** Ignores pull request merge commits.
- **Output:** A Slack message with commit info and links to changed files.

---

## ⚙️ Workflow Steps

### 🔹 Trigger

```yaml
on:
  push:
    branches:
      - main
```

Triggers on any push to the `main` branch.

---

### 🔹 Setup & Checkout

```yaml
jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Setting up job
        run: echo "Setting up job"

      - name: Checkout code
        uses: actions/checkout@v3
        with:
          fetch-depth: 0
```

- `fetch-depth: 0` is used to retrieve the full Git history, required to compare SHAs.

---

### 🔹 Commit Filter

```yaml
      - name: Get commit message
        run: |
          MESSAGE="${{ github.event.head_commit.message }}"
          if [[ "$MESSAGE" =~ ^Merge\ pull\ request ]]; then
            echo "This is a PR merge. Skipping."
            echo "send=false" >> "$GITHUB_ENV"
          else
            echo "This is NOT a PR merge. Proceeding."
            echo "send=true" >> "$GITHUB_ENV"
          fi
```

Skips Slack notifications for pull request merge commits.

---

### 🔹 Build Slack Message

```yaml
      - name: Build Slack payload
        if: env.send == 'true'
        run: |
          CURRENT_SHA="${{ github.sha }}"
          PREVIOUS_SHA=$(git rev-parse "$CURRENT_SHA^1")

          FILE_LIST=$(git diff --name-only "$PREVIOUS_SHA" "$CURRENT_SHA" | grep '^docs/.*\.md$' || true)

          if [[ -z "$FILE_LIST" ]]; then
            echo "No docs/ .md files changed. Skipping notification."
            echo "send=false" >> "$GITHUB_ENV"
            exit 0
          fi
```

✅ **FIXED LINE:**
```bash
FILE_LIST=$(git diff --name-only "$PREVIOUS_SHA" "$CURRENT_SHA" | grep '^docs/.*\.md$' || true)
```

Only includes `.md` files in `docs/`.

```bash
          FILE_LINKS=""
          while read -r FILE; do
            LINK="• https://github.com/gravitee-io/gravitee-platform-docs/blob/main/$FILE"
            FILE_LINKS="${FILE_LINKS}${LINK}\n"
          done <<< "$FILE_LIST"

          DIFF_URL="https://github.com/gravitee-io/gravitee-platform-docs/compare/$PREVIOUS_SHA...$CURRENT_SHA"
          COMMIT_URL="https://github.com/gravitee-io/gravitee-platform-docs/commit/$CURRENT_SHA"

          echo -e ":book: GitBook Sync Detected!\nRepository: gravitee-io/gravitee-platform-docs\nBranch: main\nAuthor: ${{ github.actor }}\nCommit: $COMMIT_URL\nMessage: $MESSAGE\nDiff: $DIFF_URL\nChanged files:\n$FILE_LINKS" > slack_message.txt

          jq -Rs '{ text: . }' slack_message.txt > payload.json
```

Builds and formats the Slack message with commit details and a list of changed files.

---

### 🔹 Send Slack Message

```yaml
      - name: Send Slack notification
        if: env.send == 'true'
        uses: slackapi/slack-github-action@v1.24.0
        with:
          payload-file-path: payload.json
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

Uses Slack’s GitHub Action to send the notification.

---

## ✅ Key Change Summary

**Old:**
```bash
FILE_LIST=$(git diff --name-only "$PREVIOUS_SHA" "$CURRENT_SHA" | grep '^docs/' || true)
```

**New:**
```bash
FILE_LIST=$(git diff --name-only "$PREVIOUS_SHA" "$CURRENT_SHA" | grep '^docs/.*\.md$' || true)
```

This ensures that only `.md` files under `docs/` are considered.

---

## 📌 Final Notes

- Ensure that your Slack webhook URL is stored securely in `SLACK_WEBHOOK_URL` secret.
- This workflow improves signal-to-noise ratio by excluding PR merges and non-Markdown file changes.
