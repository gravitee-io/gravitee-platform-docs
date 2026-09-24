---
hidden: false
noIndex: false
description: Review the history of changes made to a Message API in Event Stream Management, with who made each change and the patch it applied. Follow the steps to filter the audit logs.
---

# Review audit logs

The audit logs of a Message API record changes made to it, such as updates to its definition. Each entry shows when the change happened, who made it, the event, the object it targets, and the patch it applied.

## Prerequisites

* A license that includes the `apim-audit-trail` feature. Without it, the **Audit Logs** item of the sidebar shows a lock icon.
* Permission to read the audit logs of the Message API.

## Review the audit logs

1. From the Gamma console, open **Event Stream Management**.
2. In the sidebar, click **Message APIs**.
3. Click the name of the Message API.
4. In the **Monitoring** group of the Message API sidebar, click **Audit Logs**.

The list shows the **Date**, **User**, **Event**, and **Target** of each change. To see the change itself, click the view icon in the **Patch** column. The row expands to show the JSON patch.

## Filter the audit logs

* In the event filter, select one event type. The list shows the raw event names, for example `API_UPDATED`.
* In **Date range**, pick a start date and an end date.

To clear the filters, click **Reset**.

## Verification

To verify that the audit logs record your changes, follow these steps:

1. Change a setting of the Message API, for example its description.
2. Open **Audit Logs**.
3. Check that the newest entry shows your change.
