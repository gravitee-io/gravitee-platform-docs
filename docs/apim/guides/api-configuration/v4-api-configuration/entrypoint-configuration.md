---
description: This article walks through how to configure v4 API entrypoints
---

# Entrypoint configuration

## Introduction

In Gravitee, Gateway entrypoints define the protocol and configuration settings by which the API consumer accesses the Gateway API. The Gateway entrypoint dictates how the backend API is exposed through the gateway.

After you've created your Gateway API and selected your entrypoint(s), you can configure them on the API's page.  This article walks through that process for configuring v4 Message API entrypoints and v4 Proxy API entrypoints.

## Configure v4 message API entrypoints

{% hint style="warning" %}
**Enterprise only**

As of Gravitee 4.0, the ability to create APIs with message API entrypoints is an Enterprise Edition capability. To learn more about Gravitee Enterprise, and what's included in various enterprise packages, please:

* [Refer to the EE vs OSS documentation](../../../overview/introduction-to-gravitee-api-management-apim/ee-vs-oss.md)
* [Book a demo](http://127.0.0.1:5000/o/8qli0UVuPJ39JJdq9ebZ/s/rYZ7tzkLjFVST6ex6Jid/)
* [Check out the pricing page](https://www.gravitee.io/pricing)
{% endhint %}

v4 APIs support the following entrypoints:

* HTTP GET: exposes a backend resource via the HTTP GET method
* HTTP POST: exposes a backend resource via the HTTP POST method
* WebSocket: exposes a backend resource via a WebSocket stream
* Webhooks: exposes a backend resource via a Webhooks subscription
* Server-sent events (SSE): exposes a backend resource via a unidirectional, SSE stream

To access Entrypoint configuration, head to the APIs page and select your API. Then, under **Entrypoints,** select **General.**

Depending on which Entrypoint your API utilizes, entrypoint configuration may differ. Please refer to the following sections that cover configuration details for each.

## HTTP GET

If you chose **HTTP GET** as an entrypoint, you will be brought to a page where you can configure:

* **Context path:** the URL of your API. For example, if your URL is `[https://apim-master-gateway.team-apim.gravitee.dev/myAPI]`, then `[/myAPI]` is the context path.
* **Virtual hosts:** enabling virtual hosts requires you to define your **virtual host** and optionally enable **override access**.
* **HTTP GET characteristics**
  * **Limit messages count:** defines the maximum number of messages to retrieve via HTTP GET. The default is 500. To set a custom limit, enter a numeric value in the **Limit messages count** text field.
  * **Limit messages duration:** defines the maximum duration, in milliseconds, to wait to retrieve the expected number of messages (See **Limit messages count**). The effective number of retrieved messages could be less than expected if maximum duration is reached before all messages are retrieved. To set a custom limit, enter a numeric value in the **Limit messages duration** text field.
  * **HTTP GET permissions:** allow or disallow **Allow sending messages headers to client in payload** and **Allow sending messages metadata to client in payload** by toggling these actions ON or OFF.

## HTTP POST

If you chose **HTTP POST** as an entrypoint, you will be brought to a page where you can configure:

* **Context path:** the URL of your API. For example, if your URL is `[https://apim-master-gateway.team-apim.gravitee.dev/myAPI]`, then `[/myAPI]` is the context path.
* **Virtual hosts:** enabling virtual hosts requires you to define your **virtual host** and optionally enable **override access**.
* **HTTP POST permissions:** allow or disallow add request Headers to the generated message by toggling **Allow add request Headers to the generated message** ON or OFF.

## WebSocket

If you chose **WebSocket** as an entrypoint, you will be brought to a page where you can configure:

* **Context path:** the URL of your API. For example, if your URL is `[https://apim-master-gateway.team-apim.gravitee.dev/myAPI]`, then `[/myAPI]` is the context path.
* **Virtual hosts:** enabling virtual hosts requires you to define your **virtual host** and optionally enable **override access**.
* **WebSocket configuration**
  * **Publisher configuration:** choose to either enable or disable the publication capability by toggling **Enable the publication capability** ON or OFF. Disabling it assumes that the application will never be able to publish any message.
  * **Subscriber configuration:** choose to enable or disable the subscription capability by toggling **Enable the subscription capability** ON or OFF. Disabling it assumes that the application will never receive any message.

## Webhooks

If you chose **Webhook** as an entrypoint, you will be brought to a page where you can configure:

* **HTTP Options**
  * **Connect timeout:** the maximum time, in milliseconds, to connect to the Webhook. Either enter a numeric value or use the arrows to the right of the text field.
  * **Read timeout:** the maximum time, in milliseconds, allotted for the Webhook to complete the request (including response). Either enter a numeric value or use the arrows to the right of the text field.
  * **Idle timeout:** the maximum time, in milliseconds, a connection will stay in the pool without being used. Once this time has elapsed, the unused connection will be closed, freeing the associated resources. Either enter a numeric value or use the arrows to the right of the text field.
* **Proxy options**
  * Choose whether to use a proxy for client connections by toggling **Use proxy** ON or OFF. If enabled, you will need to select from the proxy types in the **Proxy type** drop-down:
    * HTTP proxy
    * SOCKS4
    * SOCKS5
  * Choose whether to use the proxy configured at system level by toggling **Use system proxy** ON or OFF. If enabled, you will need to define:
    * Proxy host: enter your proxy host in the **Proxy host** text field.
    * Proxy port: enter your proxy port in the **Proxy port** text field.
    * (Optional) Proxy username: enter your proxy username in the **Proxy username** text field.
    * (Optional) Proxy password: enter your proxy password in the **Proxy password** text field.

A [**SOCKS proxy**](https://hailbytes.com/how-to-use-socks4-and-socks5-proxy-servers-for-anonymous-web-browsing/) is a type of proxy server that uses the SOCKS protocol to tunnel traffic through an intermediary server.

Also, when using Webhooks as an entrypoint, you can set up both dead letter queues for storing undelivered messages and secure callbacks. When configuring DLQ with webhook, you redirect all the messages that the webhook rejects to another location, such as a Kafka topic.

{% hint style="info" %}
**UI Limitations**

As of Gravtiee APIM 4.0, you can only configure DLQs and secure callbacks for your Webhook via the API definition. Support for configuration in the Gravitee APIM Console is planned for future releases.
{% endhint %}

### Set up your dead letter queue

To enable DLQ, declare another endpoint that will be used to configure the dlq object in the webhook entrypoint definition:

```
{
    "type": "webhook-advanced",
    "dlq": {
        "endpoint": "dlq-endpoint"
    },
    "configuration": {}
}
```

The endpoint used for the dead letter queue:

* Must support PUBLISH mode
* Should be based on a broker that can persist messages, such as Kafka.

Once configured and deployed, any message rejected with a 4xx error response by the Webhook will be automatically sent to the DLQ endpoint and the consumption of messages will continue.

#### Combining DLQ with the retry policy

If you set up a DLQ, you can utilize the Gravitee Retry policy in order to "retry" delivery of undelivered messages from the DLQ. For more information on the Retry policy, please refer to the Retry policy policy reference.

### Set up secure callbacks

Callbacks can be secured using basic authentication, JWT, and OAuth2.

To secure a callback, add an `auth` object to the configuration section of your API definition. The following example shows how to configure basic authentication:

```
{
    "configuration": {
        "entrypointId": "webhook-advanced",
        "callbackUrl": "https://example.com",
        "auth": {
            "type": "basic",
            "basic": {
                "username": "username",
                "password": "a-very-secured-password"
            }
        }
    }
}
```

To use JWT, the `auth` object should look like this:

```
        "auth": {
            "type": "token",
            "token": {
                "value": "eyJraWQiOiJk..."
            }
        }
```

To use OAuth2, the `auth` object should look like this:

```
        "auth": {
            "type": "oauth2",
            "oauth2": {
                "endpoint": "https://auth.gravitee.io/my-domain/oauth/token",
                "clientId": "a-client-id",
                "clientSecret": "a-client-secret",
                "scopes": ["roles"]
            }
        }
```

## Server-Sent Events

If you chose **SSE** as an entrypoint, you will be brought to a page where you can configure:

* **Context path:** the URL of your API. For example, if your URL is `[https://apim-master-gateway.team-apim.gravitee.dev/myAPI]`, then `[/myAPI]` is the context path.
* **Virtual hosts:** enabling virtual hosts requires you to define your **virtual host** and optionally enable **override access**.
* **SSE characteristics and permissions**
  * **Heartbeat intervals:** define the interval in which heartbeats are sent to the client by entering a numeric value into the **Define the interval in which heartbeats** **are sent to client** text field or by using the arrow keys. Intervals must be greater than or equal to 2000ms. Each heartbeat will be sent as an empty comment: `''`.
  * Choose to allow or disallow sending message metadata to the client as SSE comments by toggling **Allow sending messages metadata to client as SSE comments** ON or OFF.
  * Choose to allow or disallow sending message headers to the client as SSE comments by toggling **Allow sending messages headers to client as SSE comments** ON or OFF.

{% hint style="info" %}
You can also add an Entrypoint to your API by selecting **Add an entrypoint.** From here, you will simply need to configure the entrypoint using the details specific to that entrypoint (see exapandable sections above).

When you are done configuring your entrypoints, make sure to select **Save changes.**
{% endhint %}

## Configure v4 Proxy API entrypoints

To alter v4 Proxy API entrypoints, select your API, and then select **General** underneath the **Entrypoints** category in the left-hand nav.&#x20;

<figure><img src="../../../.gitbook/assets/2023-07-18_10-50-48.png" alt=""><figcaption><p>v4 proxy API entrypoint configuration</p></figcaption></figure>

From here, you can alter existing entrypoints by changing the context path, add a new entrypoint by selecting the **Add context path** button and then adding a new context path, and/or deleting existing entrypoints by selecting the <img src="../../../.gitbook/assets/Screen Shot 2023-07-18 at 10.51.56 AM.png" alt="" data-size="line"> icon that correlates to the entrypoint that you want to delete.&#x20;

When you are done, make sure to redeploy the API for your changes to take effect.
