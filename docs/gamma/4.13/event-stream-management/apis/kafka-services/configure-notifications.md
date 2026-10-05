---
hidden: false
noIndex: false
description: Get notified by email or by webhook when events happen on a Kafka Service in Event Stream Management, and choose the events of your console notifications. Follow the steps to choose the channels and the events.
---

# Configure notifications

A notification sends a message through a channel when an event happens on a Kafka Service, for example when a subscription is created. Each notification pairs one channel with the events that trigger it.

Notifications report events of the Kafka Service's management, such as subscriptions and deployments. To be warned about the traffic and the connections of the Kafka Service, configure alerts instead. See [Configure alerts](configure-alerts.md).

## Open the notifications

1. From the Gamma console, open **Event Stream Management**.
2. In the **APIs** group of the sidebar, click **Kafka Services**.
3. Click the name of the Kafka Service.
4. In the **Monitoring** group of the Kafka Service sidebar, click **Notifications**.

The page counts the **Console notifiers**, **Email notifiers**, and **Webhook notifiers**, and lists the notifications under **Configured notifications**, with their **Name**, **Channel**, **Events**, and **Target**.

The notification on the console channel holds your own console notifications for the Kafka Service. Its events can change, and it can't be deleted. While it's the only notification, the page also explains what notifications are for. Once other notifications exist, the info button next to **Notifications** shows that explanation again.

## Add a notification

1. Click **Add notification**.
2. In **Name**, enter a name for the notification.
3. In **Channel**, select an email or a webhook notifier. The notifiers are the ones configured on your installation.
4. Enter the target:
    * For an email channel, enter the addresses in **Email address(es)**.
    * For a webhook channel, enter the URL in **Webhook URL**. Optional: Select **Use system proxy** to route the webhook calls through the configured system proxy.
5. Under **Events**, select the events that send the notification. The events are grouped by category.
6. Click **Add notification**.

The console saves the notification and confirms with **Notification saved**.

## Change or delete a notification

Open the actions menu of the notification's row:

* **Edit events** changes the events, the target, and the proxy setting of the notification. The name and the channel can't change. Click **Save**.
* **Delete** opens the **Delete notification `<name>`?** dialog. Click **Delete**. The console confirms with **Notification deleted**.

On the console notification, events that come from one of your groups show as selected and can't be cleared.

A notification that wasn't created from the console, for example one managed by the Gravitee Kubernetes Operator, is read-only and offers no **Edit events**.

Your role on the Kafka Service decides which of these actions you see. Adding, editing, and deleting a notification each depend on their own permission.

## Verification

To verify a notification, follow these steps:

1. Reload the **Notifications** page.
2. Check that the notification is listed with the channel, the number of events, and the target you expect.
