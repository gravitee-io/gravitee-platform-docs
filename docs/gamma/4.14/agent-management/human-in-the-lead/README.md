---
hidden: false
noIndex: false
description: The Human In the Lead group of the Agent Management sidebar holds the Inbox, Rules, Notifications, and History pages. Open the page you need.
---

# Human In the Lead

The **Human In the Lead** group of the Agent Management sidebar holds the **Inbox**, **Rules**, **Notifications**, and **History** pages, where you set up and take the decisions that MCP tool calls wait for.

* [**Decide on held tool calls**](decide-on-held-tool-calls.md). Approve a held call once or for a set time, reject it with a reason, and end a time-based approval early, from the **Inbox**.
* [**Require human approval for MCP tool calls**](../govern/require-human-approval-for-mcp-tool-calls.md). Turn on human approval for an MCP Proxy or MCP Studio, and create the rules on the **Rules** page that decide which calls wait, who decides them, and for how long.
* [**Set up approval notifications**](set-up-approval-notifications.md). Save email and webhook destinations on the **Notifications** page, and choose where each rule sends its notices.
* [**Review the decision history**](review-the-decision-history.md). Find past decisions and what became of each call on the **History** page, and export them.

Human In the Lead is part of Gravitee Enterprise. Without a license that includes it, the four items of the group carry an **Upgrade** badge and don't open. A page opened from a link reads **Human In the Lead is part of Gravitee Enterprise**, with a **Request an enterprise license** button.

## Who sees what

Each item of the **Human In the Lead** group appears only to users whose role can read it. For the permissions of each item, see [Roles and permissions](../get-started/roles-and-permissions.md).

* **Rules**: users see the rules that name them in **Rule access**. Administrators see every rule.
* **Inbox** and **History**: users see the approvals of the rules that name them in **Approval ownership**. Administrators see every approval and can end a time-based approval early.
* **Deciding**: only the users and groups in the **Approval ownership** of the rule approve or reject a call, administrators included.

## Audit log

The audit log of the environment records the following Human In the Lead events. For how to open and filter it, see [Review organization and environment audit logs](../../platform-management/review-audit-logs.md).

* Rules: `APPROVAL_RULE_CREATED`, `APPROVAL_RULE_UPDATED`, and `APPROVAL_RULE_DELETED`.
* Approvals: `APPROVAL_OPENED`, `APPROVAL_DECIDED`, `APPROVAL_RAN`, `APPROVAL_ENDED`, and `APPROVAL_EXPIRED`.
* Notices: `HITL_NOTICE_ATTEMPTED`, `HITL_NOTICE_GIVEN_UP`, and `HITL_NOTICE_REFUSED`.
* Saved notifications: `HITL_NOTIFICATION_CREATED`, `HITL_NOTIFICATION_UPDATED`, and `HITL_NOTIFICATION_DELETED`.
