---
description: Configuration guide for configure webhook subscriptions.
---

# Configure Webhook Subscriptions

{% hint style="warning" %}
This feature is in tech preview.
{% endhint %}

## Prerequisites

* Enable the New Developer Portal. For more information about enabling the New Developer Portal, see [configure-the-new-portal.md](configure-the-new-portal.md "mention").

## Configure webhook subscriptions

1.  From the Developer Portal's catalog, navigate to the webhook that you want to configure.

    <figure><img src="../../.gitbook/assets/image (299) (1).png" alt=""><figcaption></figcaption></figure>
2.  Click **Learn More**.

    <figure><img src="../../.gitbook/assets/805EA5C8-A387-48A8-962F-8BAF3149889F (1).jpeg" alt=""><figcaption></figcaption></figure>
3.  Click **Subscribe**.

    <figure><img src="../../.gitbook/assets/E4E7D948-D35F-4E44-A370-DF4E3D384B10_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
4.  Click the plan that you want to subscribe to, and then click **Next**.

    <figure><img src="../../.gitbook/assets/622A15C9-2CBA-4959-9F9E-6F5CF8A8B548 (1).jpeg" alt=""><figcaption></figcaption></figure>
5.  Select the application that you want to use to subscribe to the API, and then click **Next**.

    <figure><img src="../../.gitbook/assets/35DBD082-6975-44A2-90E6-DD6C5F5BBA59 (1).jpeg" alt=""><figcaption></figcaption></figure>
6.  In the **Configure Consumer** page, complete the following steps:

    1. (Optional) In the **Channel** field, select the channel that sends events to your callback URL.
    2. In the **Callback URL** field, enter the full URL of the publicly available HTTP(S) endpoint that receives the message payloads. For example, `https://api.myservice.com/webhooks/orders`.
    3. (Optional) In the **Headers** section, enter the custom HTTP headers to include in your calls.
    4. From the **Retry** drop-down menu, select when the API should retry sending the message when an error occurs with the target. For example, if the callback URL is unreachable.
    5. From the **Security configuration** drop-down menu, select the configuration to connect to the callback URL. The default is **No security**.
    6. (Optional) In the **SSL** section, enable **Verify host** and **Trust all**.

    <figure><img src="../../.gitbook/assets/image (300) (1).png" alt=""><figcaption></figcaption></figure>
7.  Click **Next**.

    <figure><img src="../../.gitbook/assets/E64B2895-B6B3-43C2-BE7A-DD162CC6E029 (1).jpeg" alt=""><figcaption></figcaption></figure>
8. In the **Add a comment** field, enter a message to explain why you want to subscribe to the API.
9.  Click **Subscribe**.

    <figure><img src="../../.gitbook/assets/11C5B4EE-F95D-4A58-A9FC-51BD9FF03EC1 (1).jpeg" alt=""><figcaption></figcaption></figure>

## Verification

Once you subscribe to an API, the Developer Portal displays the description details. For example:

<figure><img src="../../.gitbook/assets/image (301) (1).png" alt=""><figcaption></figcaption></figure>
