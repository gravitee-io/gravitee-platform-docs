---
description: Configure a webhook subscription from the Developer Portal 4.8 catalog. Follow the steps to set it up for your application.
---

# Configure Webhook Subscriptions


## Prerequisites

* Enable the New Developer Portal. For more information about enabling the New Developer Portal, see [configure-the-new-portal.md](configure-the-new-portal.md "mention").

## Configure webhook subscriptions

1.  From the Developer Portal's catalog, navigate to the webhook that you want to configure.

    <figure><img src="../../.gitbook/assets/devportal-new-portal-configure-webh-299.png" alt="The developer portal catalogue, showing a welcome banner above a grid of API cards, most noting that their description is missing."><figcaption></figcaption></figure>
2.  Click **Learn More**.

    <figure><img src="../../.gitbook/assets/805EA5C8-A387-48A8-962F-8BAF3149889F.jpeg" alt="The developer portal catalogue filtered by a search term, showing six matching webhook API cards with the Learn more button on the first one highlighted."><figcaption></figcaption></figure>
3.  Click **Subscribe**.

    <figure><img src="../../.gitbook/assets/E4E7D948-D35F-4E44-A370-DF4E3D384B10_1_201_a.jpeg" alt="An API&#x27;s Details tab in the developer portal, noting that no details are available, with a Subscribe button and a sidebar showing the owner, last deployed date, version, and metadata."><figcaption></figcaption></figure>
4.  Click the plan that you want to subscribe to, and then click **Next**.

    <figure><img src="../../.gitbook/assets/622A15C9-2CBA-4959-9F9E-6F5CF8A8B548.jpeg" alt="The Choose a plan step of the developer portal subscription wizard, with a push plan selected over a keyless plan and the Next button highlighted."><figcaption></figcaption></figure>
5.  Select the application that you want to use to subscribe to the API, and then click **Next**.

    <figure><img src="../../.gitbook/assets/35DBD082-6975-44A2-90E6-DD6C5F5BBA59.jpeg" alt="The Choose an application step of the subscription wizard, showing three application cards with the first selected and the Next button highlighted."><figcaption></figcaption></figure>
6.  In the **Configure Consumer** page, complete the following steps:

    1. (Optional) In the **Channel** field, select the channel that sends events to your callback URL.
    2. In the **Callback URL** field, enter the full URL of the publicly available HTTP(S) endpoint that receives the message payloads. For example, `https://api.myservice.com/webhooks/orders`.
    3. (Optional) In the **Headers** section, enter the custom HTTP headers to include in your calls.
    4. From the **Retry** drop-down menu, select when the API should retry sending the message when an error occurs with the target. For example, if the callback URL is unreachable.
    5. From the **Security configuration** drop-down menu, select the configuration to connect to the callback URL. The default is **No security**.
    6. (Optional) In the **SSL** section, enable **Verify host** and **Trust all**.

    <figure><img src="../../.gitbook/assets/devportal-new-portal-configure-webh-300.png" alt="The Configure Consumer step of the subscription wizard, with an empty channel, a required callback URL, an empty headers table, no retry, no security, and trust store and key store set to none."><figcaption></figcaption></figure>
7.  Click **Next**.

    <figure><img src="../../.gitbook/assets/E64B2895-B6B3-43C2-BE7A-DD162CC6E029.jpeg" alt="The Configure Consumer step scrolled to the foot, showing the retry, security, and SSL options with the Next button highlighted."><figcaption></figcaption></figure>
8. In the **Add a comment** field, enter a message to explain why you want to subscribe to the API.
9.  Click **Subscribe**.

    <figure><img src="../../.gitbook/assets/11C5B4EE-F95D-4A58-A9FC-51BD9FF03EC1.jpeg" alt="The Checkout step of the subscription wizard, summarising the application and push plan beside a comment field, with the Subscribe button highlighted."><figcaption></figcaption></figure>

## Verification

Once you subscribe to an API, the Developer Portal displays the description details. For example:

<figure><img src="../../.gitbook/assets/devportal-new-portal-configure-webh-301.png" alt="The My Subscriptions tab of an API in the developer portal, showing the subscription&#x27;s application, plan, and timestamps beside an API access panel with a placeholder base URL and curl command, above the callback and retry configuration."><figcaption></figcaption></figure>
