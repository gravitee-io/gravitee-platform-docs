---
hidden: false
noIndex: false
description: Get notified by email or by webhook when events happen on a Message API in Event Stream Management, and choose the events of your console notifications. Follow the steps to choose the channels and the events.
---

# Configure notifications

A notification sends a message through a channel when an event happens on a Message API, for example when a subscription is created. Each notification pairs one channel with the events that trigger it.

## Open the notifications

1. From the Gamma console, open **Event Stream Management**.
2. In the sidebar, click **Message APIs**.
3. Click the name of the Message API.
4. In the **Monitoring** group of the Message API sidebar, click **Notifications**.

The page counts the **Console notifiers**, **Email notifiers**, and **Webhook notifiers**, and lists the notifications under **Configured notifications**, with their name, their channel, their number of events, and their target.

The **Console Notification** row holds your own console notifications for the Message API. Its events can change, and it can't be deleted.

## Add a notification

1. Click **Add notification**.
2. In **Name**, enter a name for the notification.
3. In **Channel**, select **Default Email Notifier** or **Default Webhook Notifier**.
4. Enter the target:
    * For an email channel, enter the addresses in `Email address(es)`.
    * For a webhook channel, enter the URL in **Webhook URL**. Optional: Turn on **Use system proxy**.
5. Under **Events**, select the events that send the notification. The events are grouped by category.
6. Click **Add notification**.

The console saves the notification and confirms with **Notification saved**.

## Change or delete a notification

Open the actions menu of the notification's row:

* **Edit events** changes the events, the target, and the proxy setting of the notification. The channel can't change.
* **Delete** removes the notification.

On the **Console Notification** row, events that come from one of your groups show as selected and can't be cleared.

Your role on the Message API decides which of these actions you see. Adding, editing, and deleting a notification each depend on their own permission.

## Verification

To verify a notification, follow these steps:

1. Reload the **Notifications** page.
2. Check that the notification is listed with the channel, the number of events, and the target you expect.
