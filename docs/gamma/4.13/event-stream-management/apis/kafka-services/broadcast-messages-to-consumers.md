---
hidden: false
noIndex: false
description: Send a one-off message to the subscribers of a Kafka Service, or to the members of its subscribed applications, from Event Stream Management. Follow the steps to broadcast it.
---

# Broadcast messages to consumers

A broadcast sends a one-off message about a Kafka Service to the people who consume it, for example to announce maintenance or a plan change. It goes out as a portal notification or by email.

## Prerequisites

* Permission to send messages about the Kafka Service. Without it, the **Broadcasts** item doesn't appear in the Kafka Service sidebar.

## Send a broadcast

1. From the Gamma console, open **Event Stream Management**.
2. In the **APIs** group of the sidebar, click **Kafka Services**.
3. Click the name of the Kafka Service.
4. In the **Consumers** group of the Kafka Service sidebar, click **Broadcasts**.
5. Complete the following fields:

<table>
    <thead>
        <tr>
            <th width="160">Field</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Title</strong></td>
            <td>Optional. The title of the message.</td>
        </tr>
        <tr>
            <td><strong>Message</strong></td>
            <td>Required. The text of the message.</td>
        </tr>
        <tr>
            <td><strong>Recipients</strong></td>
            <td>Required. <strong>API subscribers</strong> addresses the subscribers of the Kafka Service. The console also offers one option per application role, for example <strong>Members with the Owner role on subscribed applications</strong>, which addresses the members that hold that role on the applications subscribed to the Kafka Service.</td>
        </tr>
        <tr>
            <td><strong>Channel</strong></td>
            <td><strong>Portal</strong> sends the message as a portal notification. <strong>Email</strong> sends it by email. The default is <strong>Portal</strong>.</td>
        </tr>
    </tbody>
</table>

6. Click **Send message**.

The message goes out at once, without a confirmation step. The page doesn't keep a history of broadcasts. Once the message is sent, the **Title** and **Message** fields clear.

## Verification

To verify that the broadcast was sent, follow these steps:

1. Check the confirmation under the form. It reads **Message sent**, with the number of recipients that the message was delivered to.
2. If the number is 0, check the recipients. For example, **API subscribers** reaches no one on a Kafka Service without subscriptions.
