---
description: >-
  Send console, email, or webhook notifications when API events occur, such as
  deployments or subscription changes.
hidden: false
noIndex: false
---

# Configure notifications

The **Notifications** page alerts you when key API events occur, for example deployments, subscription changes, or policy errors. Each notification pairs a channel with a set of API events that trigger it.

To open the page, follow these steps:

1. Click **API Proxies** in the module sidebar.
2. Select your API proxy.
3. Click **Notifications** in the API proxy sidebar.

<!-- TODO: Screenshot of the Notifications page with configured notifiers -->

<figure><img src="../../../.gitbook/assets/PLACEHOLDER-gamma-api-notifications-page.png" alt=""><figcaption><p>The Notifications page</p></figcaption></figure>

The page shows the **Console notifiers**, **Email notifiers**, and **Webhook notifiers** counters, and a table with the **Name**, **Channel**, **Events**, and **Target** columns.

The following permissions gate the actions on this page:

| Action                | Permission           |
| --------------------- | -------------------- |
| Add a notification    | `api-notification-c` |
| Edit a notification   | `api-notification-u` |
| Delete a notification | `api-notification-d` |

## Add a notification

To add an email or webhook notification, follow these steps:

1. Click **Add notification**.
2. Enter a **Name**.
3. Select a **Channel**. The channel sets the target field: `Email address(es)` for the **Email** channel, or **Webhook URL** for the **Webhook** channel.
4. For a webhook, optionally turn on **Use system proxy** to route webhook calls through the gateway's configured system proxy.
5. Under **Events**, select the API events that send a notification. Events are grouped by category.
6. Click **Add notification**.

{% hint style="info" %}
The **Console** channel isn't created from this form. Edit the console notification from the notifications list to choose which events appear in the console.
{% endhint %}

## Edit or delete a notification

To change a notification, open it from the table and adjust its target or its selected events. The channel of an existing notification can't be changed.

To delete a notification, use its **Actions** menu in the table. The **Delete notification** dialog warns that the notification is permanently deleted, and the action can't be undone.

## Verification

To verify a notification is working as expected, follow these steps:

1. Add a notification for an event you control, for example an API deployment event.
2. Trigger the event by deploying the API.
3. The notification arrives on the configured channel.

<!-- TODO: Screenshot of a received notification for a triggered API event -->

<figure><img src="../../../.gitbook/assets/PLACEHOLDER-gamma-api-notification-received.png" alt=""><figcaption><p>A received notification</p></figcaption></figure>
