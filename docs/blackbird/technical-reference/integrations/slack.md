---
noIndex: true
---

# Slack

Blackbird integrates with Slack to streamline your workflow and foster a collaborative environment where everyone is immediately informed of your mock and deployment statuses in Blackbird.

Key features include:

* **Mock and deployment start alerts** – Receive messages in Slack when mocks and deployments start to keep your team updated.
* **Mock and deployment completion alerts** – Receive messages in Slack when mocks and deployments finish to ensure you have visibility into successful or failed mocks and deployments.
* **Seamless collaboration** – Improve team collaboration by centralizing mock and deployment updates within your Slack workspace.

> **Note:** This integration is configured at the organization level. When enabled, all users in the organization will receive notifications in the designated Slack channel.

## Prerequisites

Before configuring the Slack integration, ensure you meet the following requirements:

* You have a Slack API token. For guidance on how to obtain a token, see [How to quickly get and use a Slack API bot token](https://api.slack.com/tutorials/tracks/getting-a-token) in the Slack documentation.
* You have access to the ID of the Slack channel that’s designated for alerts. Consider creating a specific channel (e.g., `#blackbird-alerts`) to help maintain visibility and reduce noise in other channels.

## Configure the Slack integration

After you meet the prerequisites, use the following procedure to configure the Slack integration.

**To configure the Slack integration:**

1. Log into the [Blackbird UI](https://blackbird.a8r.io).
2. In the left pane, choose **Settings** and then **Notifications**.
3. In the **Slack Integration** tile, choose **Configuration**.
4. In the **Slack Configuration** dialogue box, provide the Slack API token and the Slack Channel ID. For more information, see [Prerequisites](slack.md#prerequisites).
5. Choose the **Test Configuration** button to verify the token and ID. A message displays in the lower-right corner of your screen indicating whether the test succeeded or failed.
6. After a successful test, choose the **Save Configuration** button.

After the integration is configured, you can enable or disable notifications using the toggle in the Slack Integration tile.

> **Note:** Disabling notifications doesn't affect the configuration. It will only change when you edit it.
