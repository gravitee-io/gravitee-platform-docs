---
description: An overview about v4 Message API Entrypoints.
---

# v4 Message API Entrypoints

## Overview

{% hint style="warning" %}
**Enterprise only**

As of Gravitee 4.3, the ability to create APIs with message API entrypoints is an Enterprise Edition capability. To learn more about Gravitee Enterprise Edition and what's included in various enterprise packages, please:

* [Refer to the EE vs OSS documentation](../../../../../../overview/gravitee-apim-enterprise-edition/)
* [Book a demo](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/rYZ7tzkLjFVST6ex6Jid/)
* [Check out the pricing page](https://www.gravitee.io/pricing)
{% endhint %}

v4 APIs support the following entrypoints:

* **HTTP GET:** Exposes a backend resource via the HTTP GET method
* **HTTP POST:** Exposes a backend resource via the HTTP POST method
* **WebSocket:** Exposes a backend resource via a WebSocket stream
* **Webhook:** Exposes a backend resource via a Webhooks subscription
* **Server-sent events (SSE):** Exposes a backend resource via a unidirectional SSE stream

## Configuration

To access your entrypoint configuration, go to the **API** page in the Console, select your API, then select **Entrypoints** from the inner the left nav.

At the top right of the page, you can choose to enable or disable virtual hosts. Enabling virtual hosts requires you to define your virtual host and optionally enable override access.

<figure><img src="../../../../../../../../../.gitbook/assets/configure v4 message entrypoints (1).png" alt=""><figcaption><p>v4 message API entrypoint configuration</p></figcaption></figure>

Next, depending on which entrypoint(s) your API utilizes, specific entrypoint configuration may differ. Click on the tiles below for the configuration details of each specific entrypoint.

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td></td><td>HTTP GET</td><td></td><td><a href="http-get.md">http-get.md</a></td></tr><tr><td></td><td>HTTP POST</td><td></td><td><a href="http-post.md">http-post.md</a></td></tr><tr><td></td><td>WebSocket</td><td></td><td><a href="websocket.md">websocket.md</a></td></tr><tr><td></td><td>Webhook</td><td></td><td><a href="webhook.md">webhook.md</a></td></tr><tr><td></td><td>Server-sent events</td><td></td><td><a href="server-sent-events.md">server-sent-events.md</a></td></tr></tbody></table>

You can also add an entrypoint to your API by clicking **Add an entrypoint**. Configuration is entrypoint-specific (see the tiles above).

When you are done configuring your entrypoints, click **Save changes.**
