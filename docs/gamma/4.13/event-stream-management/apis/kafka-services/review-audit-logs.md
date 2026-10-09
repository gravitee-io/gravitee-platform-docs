---
hidden: false
noIndex: false
description: Review the history of changes made to a Kafka Service in Event Stream Management, with who made each change and the patch it applied. Follow the steps to filter the audit logs.
---

# Review audit logs

The audit logs of a Kafka Service record changes made to it, such as updates to its definition or to its subscriptions. Each entry shows when the change happened, who made it, the event, the object it targets, and the patch it applied.

## Prerequisites

* A license that includes the `apim-audit-trail` feature. Without it, the **Audit Logs** item of the Kafka Service sidebar shows a lock icon.
* Permission to read the audit logs of the Kafka Service. Without it, the page shows that the feature is locked.

## Review the audit logs

1. From the Gamma console, open **Event Stream Management**.
2. In the **APIs** group of the sidebar, click **Kafka Services**.
3. Click the name of the Kafka Service.
4. In the **Monitoring** group of the Kafka Service sidebar, click **Audit Logs**.

The list shows the **Date**, **User**, **Event**, and **Target** of each change. To see the change itself, click the view icon in the **Patch** column. The row expands to show the JSON patch.

While the Kafka Service has no audit entry, the page explains what audit logs are for. Once entries exist, the info button next to **Audit Logs** shows that explanation again.

## Filter the audit logs

* In the event filter, select one event type. The list shows the raw event names, for example `API_UPDATED`.
* In **Date range**, pick a start date and an end date.

To clear the filters, click **Reset**.

## Verification

To verify that the audit logs record your changes, follow these steps:

1. Change a setting of the Kafka Service, for example its description.
2. Open **Audit Logs**.
3. Check that the newest entry shows your change.
