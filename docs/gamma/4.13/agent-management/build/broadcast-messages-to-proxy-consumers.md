---
hidden: false
noIndex: false
description: Send a one-way announcement to the consumers of an LLM Proxy, MCP Proxy, or A2A Proxy about a change, an update, or a maintenance window. Follow the steps to compose one.
---

# Broadcast messages to proxy consumers

Each LLM Proxy, MCP Proxy, and A2A Proxy detail view includes a **Broadcasts** page that sends announcements to the consumers of the proxy. A broadcast is a one-way message to the recipients you select, for example to announce a deprecation, a breaking change, or a maintenance window.

## Open the Broadcasts page

1. From the Gamma console sidebar, select **Agent Management**.
2. Under **Secure**, select **LLM Proxies**, **MCP Proxies**, or **A2A Proxies**.
3. Select the proxy whose consumers you want to reach.
4. Under **Consumer Access**, select **Broadcasts**.

<!-- TODO: Screenshot of the Broadcasts page before a broadcast is composed -->

<figure><img src="../../.gitbook/assets/PLACEHOLDER-gamma-aim-broadcasts.png" alt=""><figcaption><p>The Broadcasts page</p></figcaption></figure>

Until you compose a broadcast, the page shows an introduction to broadcasts instead of the form.

The **Broadcasts** item appears in the proxy sidebar only when you're allowed to read broadcasts. The **Compose broadcast** button appears only when you're allowed to send them. Without the send permission, the page shows **You do not have permission to send broadcast messages for this API.**

## Send a broadcast

To send a broadcast, follow these steps:

1. Click **Compose broadcast**.
2. Select a **Channel**: **Portal Notifications**, **Email**, or **POST HTTP Message**. The channel defaults to **Portal Notifications**.
3. For **Portal Notifications** and **Email**, select one or more **Recipients**, and then enter a **Title**. The **Recipients** list offers the following options:
   * **API subscribers**. The users who subscribed to the proxy.
   * One option per application role defined in your organization, such as **Members with the OWNER role on applications subscribed to this API**. The message reaches the members holding that role on the applications with an accepted subscription to the proxy.
4. For **POST HTTP Message**, enter the target **URL** as a full `http://` or `https://` address. To send headers with the request, click **Add header** and enter a name and a value for each one. Optionally, turn on **Use system proxy**.
5. Enter the **Message**, up to 4,000 characters. A counter under the field shows the remaining characters.
6. Click **Send**. The button stays disabled until the form is valid.

<!-- TODO: Screenshot of the Compose broadcast form with the Portal Notifications channel selected -->

<figure><img src="../../.gitbook/assets/PLACEHOLDER-gamma-aim-broadcast-compose.png" alt=""><figcaption><p>The Compose broadcast form</p></figcaption></figure>

Switching the channel clears the fields that belong to the previous channel, so a title entered for a portal notification doesn't travel with an HTTP broadcast.

After the send, the page shows **Broadcast sent** and offers **Compose another broadcast**. When at least one recipient was reached, the confirmation reports how many. The count depends on the channel:

* For **Portal Notifications**, the count is the number of users matched by the selected recipients.
* For **Email**, the count is the number of matched users that have an email address. Users without one are skipped.
* For **POST HTTP Message**, the count is always 1, because the message is posted to a single URL.

If the send fails, the form shows the error above the **Cancel** and **Send** buttons and keeps what you entered.

An HTTP broadcast is refused when the webhook notifier is disabled with `notifiers.webhook.enabled: false` in the `gravitee.yml` of the Management API. When `notifiers.webhook.whitelist` lists one or more URLs, a broadcast to a URL outside that list is refused as well.

## Verification

To verify a broadcast is working as expected, follow these steps:

1. Send a broadcast on the **Portal Notifications** channel to **API subscribers**.
2. Under **Monitoring**, select **Audit Logs**. The trail lists a **MESSAGE_SENT** event with your user as the **Actor**.
