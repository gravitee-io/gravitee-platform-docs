---
description: >-
  Send one-way announcements about changes or maintenance to the consumers of
  an API proxy.
hidden: false
noIndex: false
---

# Broadcast messages to consumers

The **Broadcasts** page sends announcements to your API consumers. A broadcast is a one-way message to specified recipients that informs them of changes or updates, for example a maintenance window.

To open the page, follow these steps:

1. Click **API Proxies** in the module sidebar.
2. Select your API proxy.
3. Click **Broadcasts** in the API proxy sidebar.

Sending a broadcast requires the `api-message-c` permission.

<!-- TODO: Screenshot of the Compose broadcast form -->

<figure><img src="../../../.gitbook/assets/PLACEHOLDER-gamma-api-broadcasts-compose.png" alt=""><figcaption><p>The Compose broadcast form</p></figcaption></figure>

## Send a broadcast

To send a broadcast, follow these steps:

1. Click **Compose broadcast**.
2. Select a **Channel**: **Portal Notifications**, **Email**, or **POST HTTP Message**.
3. Select one or more **Recipients**. The options are application roles, and the message reaches the consumers of this API holding the selected roles.
4. Fill in the channel-specific fields:
   * For **Portal Notifications** and **Email**, enter a **Title**.
   * For **POST HTTP Message**, enter the target **URL** (an `http` or `https` address), and optionally turn on **Use system proxy**.
5. Enter the **Message**, up to 250 characters. A counter under the field shows the remaining characters.
6. Click **Send**.

After the send, a success banner reports how many recipients the broadcast reached, and offers to compose another one.

## Verification

To verify a broadcast is working as expected, follow these steps:

1. Send a broadcast on the **Portal Notifications** channel to a role held by a test user.
2. Sign in to the Developer Portal as that user. The notification carries the title and message you entered.

<!-- TODO: Screenshot of the received portal notification -->

<figure><img src="../../../.gitbook/assets/PLACEHOLDER-gamma-api-broadcast-received.png" alt=""><figcaption><p>A received broadcast</p></figcaption></figure>
