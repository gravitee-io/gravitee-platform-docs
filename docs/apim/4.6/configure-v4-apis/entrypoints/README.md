---
description: An overview about entrypoints.
---

# Entrypoints

## Overview

You can choose to configure either [v4 proxy API entrypoints](./#proxy-api-entrypoints) or [v4 message API entrypoints](./#message-api-entrypoints).

## Proxy API entrypoints

To configure v4 proxy API entrypoints:

1. Select **APIs** from the left nav
2. Select your API
3. Select **Entrypoints** from the inner left nav

Refer to the following sections for step-by-step configuration details per proxy type.

### HTTP proxy APIs

Edit the entrypoint's settings under the **Entrypoints** tab.

<figure><img src="../../../../../.gitbook/assets/edit HTTP entrypoint.png" alt=""><figcaption><p>v4 HTTP proxy API entrypoint configuration</p></figcaption></figure>

You have the option to:

* Alter existing entrypoints by changing the context path
* Add a new entrypoint by clicking **Add context path** and adding a new context path
* Enable or disable virtual hosts. Enabling virtual hosts requires you to define your virtual host and optionally enable override access.

Redeploy the API for your changes to take effect.

### TCP proxy APIs

Edit the entrypoint's settings under the **Entrypoints** tab.

<figure><img src="../../../../../.gitbook/assets/tcp_entrypoints.png" alt=""><figcaption><p>v4 TCP proxy API entrypoint configuration</p></figcaption></figure>

You have the option to:

* Alter existing entrypoints by changing the host
* Add a new entrypoint by clicking **Add host** and adding a new host

Redeploy the API for your changes to take effect.

## Message API entrypoints

{% hint style="warning" %}
**Enterprise only**

As of Gravitee 4.3, the ability to create APIs with message API entrypoints is an [Enterprise Edition](../../overview/enterprise-edition.md) capability. To learn more about Gravitee Enterprise Edition and what's included in various enterprise packages, please:

* [Book a demo](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/rYZ7tzkLjFVST6ex6Jid/)
* [Check out the pricing page](https://www.gravitee.io/pricing)
{% endhint %}

v4 APIs support the following entrypoints:

* **HTTP GET:** Exposes a backend resource via the HTTP GET method
* **HTTP POST:** Exposes a backend resource via the HTTP POST method
* **WebSocket:** Exposes a backend resource via a WebSocket stream
* **Webhook:** Exposes a backend resource via a Webhooks subscription
* **Server-sent events (SSE):** Exposes a backend resource via a unidirectional SSE stream

## Procedure

To access your entrypoint configuration, go to the **API** page in the Console, select your API, then select **Entrypoints** from the inner the left nav.

At the top right of the page, you can choose to enable or disable virtual hosts. Enabling virtual hosts requires you to define your virtual host and optionally enable override access.

<figure><img src="../../../../../.gitbook/assets/configure v4 message entrypoints.png" alt=""><figcaption><p>v4 message API entrypoint configuration</p></figcaption></figure>

Entrypoint configuration depends on which entrypoint(s) your API utilizes. Click on the tiles below for the configuration details of each specific entrypoint.

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td></td><td><a href="http-get.md">HTTP GET</a></td><td></td><td><a href="broken-reference/">broken-reference</a></td></tr><tr><td></td><td><a href="http-post.md">HTTP POST</a></td><td></td><td><a href="broken-reference/">broken-reference</a></td></tr><tr><td></td><td><a href="websocket.md">WebSocket</a></td><td></td><td><a href="broken-reference/">broken-reference</a></td></tr><tr><td></td><td><a href="webhook.md">Webhook</a></td><td></td><td><a href="broken-reference/">broken-reference</a></td></tr><tr><td></td><td><a href="server-sent-events.md">Server-sent Events</a></td><td></td><td><a href="broken-reference/">broken-reference</a></td></tr></tbody></table>

You can also add an entrypoint to your API by clicking **Add an entrypoint**. Configuration is entrypoint-specific (see the tiles above).

When you are done configuring your entrypoints, click **Save changes.**
