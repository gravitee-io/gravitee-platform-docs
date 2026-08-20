---
hidden: false
noIndex: false
description: Send console, email, or webhook alerts when API events occur, such as a deployment or a subscription change. Follow the steps to add a notification.
---

# Configure notifications

The **Notifications** page alerts you when key API events occur, for example deployments, subscription changes, or policy errors. Each notification pairs a channel with a set of API events that trigger it.

To open the page, complete the following steps:

1. Click **API Proxies** in the module sidebar.
2. Select your API proxy.
3. Click **Notifications** in the API proxy sidebar.

<!-- TODO: Screenshot of the Notifications page with configured notifiers -->

<figure><img src="../../../.gitbook/assets/PLACEHOLDER-gamma-api-notifications-page.png" alt=""><figcaption><p>The Notifications page</p></figcaption></figure>

The page shows the **Console notifiers**, **Email notifiers**, and **Webhook notifiers** counters, and a table with the **Name**, **Channel**, **Events**, and **Target** columns. An **Actions** column is added when you can edit or delete a notification.

The **Console notifiers** counter shows `1` for every API, because each API has a console notification whether or not any event is subscribed to it. The **Email notifiers** and **Webhook notifiers** counters show how many notifications of each channel are configured.

The table is grouped under the **Configured notifications** card. The **Events** column shows `None` when no event is subscribed, or a count such as `1 event`. The **Target** column shows the email address for an email notification or the URL for a webhook notification, and a dash for the console notification, which has no target. The table always lists the console notification, so it is never empty.

If you haven't yet created an email or webhook notification, a **Why configure notifications?** card precedes the **Configured notifications** table. The card explains that you can be alerted on deployments, subscription requests, or policy errors without polling the dashboard. It also covers routing alerts to the console, email, or webhooks, and filtering by event type to reduce alert fatigue.

To create, edit, or delete notifications, you need the `api-notification-c`, `api-notification-u`, or `api-notification-d` permission. If you hold none of these permissions, the **Add notification** button and the **Actions** column aren't shown.

## Add a notification

To add an email or webhook notification, complete the following steps:

1. Click **Add notification**.
2. Enter a **Name**.
3. Select a **Channel**. The channel sets the target field: `Email address(es)` for the **Email** channel, or **Webhook URL** for the **Webhook** channel.
4. For a webhook, optionally enable **Use system proxy** to route webhook calls through the gateway's configured system proxy.
5. Under **Events**, select the API events that send a notification. Events are grouped by category.
6. Click **Add notification**.

{% hint style="info" %}
The **Console** channel isn't created from this form. Edit the console notification from the notifications list to choose which events appear in the console.
{% endhint %}

## Edit or delete a notification

To change a notification, open its **Actions** menu in the table, and then click **Edit events**. You can then adjust its target or its selected events. The channel of an existing notification can't be changed.

To delete a notification, open its **Actions** menu in the table, and then click **Delete**. The **Delete notification** dialog warns that the notification is permanently deleted, and the action can't be undone.

## Verification

To verify a notification is working as expected, complete the following steps:

1. Add a notification for an event you control, for example an API deployment event.
2. Trigger the event by deploying the API.
3. Confirm that the notification arrives on the configured channel.

You can also return to the **Notifications** page. Confirm that the new notification appears in the **Configured notifications** table with the matching channel, and that the **Email notifiers** or **Webhook notifiers** counter has increased.

<!-- TODO: Screenshot of a received notification for a triggered API event -->

<figure><img src="../../../.gitbook/assets/PLACEHOLDER-gamma-api-notification-received.png" alt=""><figcaption><p>A received notification</p></figcaption></figure>
