
# PR Merge Notifier GitHub Action

This GitHub Actions workflow sends a Slack notification whenever a pull request is merged into the `main` branch of the repository. It constructs a detailed message including PR title, author, commit information, a diff link, and a list of changed files.

## Trigger

The workflow is triggered when a pull request is **closed** (`pull_request: types: [closed]`). It only continues if:

- The pull request was actually **merged**.
- The pull request was merged into the `main` branch.

This is controlled by the `if` condition on the job:
```yaml
if: >
  github.event.pull_request.merged == true &&
  github.event.pull_request.base.ref == 'main'
```

## Job: `notify-slack`

Runs on: `ubuntu-latest`

### Step 1: Checkout Code
```yaml
uses: actions/checkout@v3
with:
  fetch-depth: 0
```
This ensures the workflow has access to the full Git history, necessary to compute the previous commit (`fetch-depth: 0`).

### Step 2: Build Slack Payload

- Computes:
  - `CURRENT_SHA`: SHA of the merge commit.
  - `PREVIOUS_SHA`: SHA of the commit just before the merge.
- Generates:
  - `DIFF_URL`: Comparison link between the previous and current commit.
  - `COMMIT_URL`: Direct link to the merge commit.
- Extracts changed files using `git diff --name-only` and filters for `.md` files only.
- Generates direct GitHub links for each changed `.md` file.
- Assembles a Slack-friendly payload using `jq`, structured like:
```
:tada: Pull request merged to `main`!
*Title:* <PR URL|PR Title>
*Author:* GitHub Actor
*Commit:* Commit URL
*Diff:* Diff URL
*Changed files:*
• Link1
• Link2
...
```

### Step 3: Send Slack Notification

```yaml
uses: slackapi/slack-github-action@v1.24.0
```
Sends the generated JSON payload to the Slack webhook defined in the `SLACK_WEBHOOK_URL` secret.

## Notes

- Only `.md` file changes are recorded in the final Slack message.
- `jq` is used to construct a well-formatted JSON message for Slack from shell-generated text.

