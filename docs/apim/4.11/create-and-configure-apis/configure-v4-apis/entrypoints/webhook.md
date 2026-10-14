---
description: Declare the webhook identifier to use the Webhook entrypoint on a v4 API Management 4.11 API. Follow the steps to configure it.
metaLinks:
  alternates:
    - webhook.md
---

# Webhook

## Entrypoint identifier <a href="#user-content-plugin-identifier" id="user-content-plugin-identifier"></a>

To use the plugin, declare the `webhook` identifier while configuring your API entrypoint.

## Entrypoint Configuration

If you chose **Webhook** as an entrypoint, you can modify the following configuration parameters.

1. Choose whether to interrupt message consumption if the request to the callback URL ends with a 5xx error.
2. Choose whether to interrupt message consumption if the request to the callback URL ends with an exception.
3. Define the maximum time, in milliseconds, to connect to the webhook.
4. Define the maximum time, in milliseconds, allotted for the webhook to complete the request (including response).
5. Define the maximum time, in milliseconds, a connection will stay in the pool without being used. Once this time has elapsed, the unused connection will be closed, freeing the associated resources.
6. Use the drop-down menu to select a proxy option: **No proxy**, **Use proxy configured at system level**, or **Use proxy for client connections**.
   * If you chose **Use proxy for client connections**, define the following:
     * **Proxy type:** Choose between HTTP, SOCKS4 and SOCKS5.
     * **Proxy host:** Enter your proxy host in the text field.
     * **Proxy port:** Enter your proxy port in the text field.
     * (Optional) **Proxy username:** Enter your proxy username in the text field.
     * (Optional) **Proxy password:** Enter your proxy password in the text field.

When you create the webhook entrypoint, the following configuration is added to the API definition:

```json
{
            "type": "webhook",
            "qos": "AUTO",
            "dlq": {
              "endpoint": "dlq-mocked default endpoint"
            },
            "configuration": {
              "interruptConsumptionOnServerError": true,
              "proxy": {
                "useSystemProxy": false,
                "enabled": false
              },
              "http": {
                "readTimeout": 10000,
                "idleTimeout": 60000,
                "connectTimeout": 3000,
                "maxConcurrentConnections": 5
              },
              "interruptConsumptionOnException": true
            }
          }
```

### Quality of Service <a href="#user-content-quality-of-service" id="user-content-quality-of-service"></a>

The Advanced version of the webhook plugin offers improved QoS. In the Console, use the drop-down menu to choose between the available options. QoS compatibility is detailed [here](../quality-of-service.md).

<table><thead><tr><th width="169.99999999999997">QoS</th><th width="138">Delivery</th><th>Description</th></tr></thead><tbody><tr><td>None</td><td>Unwarranted</td><td>Performance matters over delivery guarantee</td></tr><tr><td>Auto</td><td>0 or n</td><td>Performance matters over delivery guarantee</td></tr><tr><td>At-Most-Once</td><td>0 or 1</td><td>Delivery guarantee matters over performance</td></tr><tr><td>At-Least-Once</td><td>1 or n</td><td>Delivery guarantee matters over performance</td></tr></tbody></table>

### Compatibility matrix <a href="#user-content-description" id="user-content-description"></a>

| Plugin version | APIM version |
| -------------- | ------------ |
| 1.x            | 3.21.x       |
| 2.x            | 4.0 to 4.3   |
| 3.x            | 4.4 and 4.5  |
| 4.x            | 4.6 to 4.8   |
| 5.x            | 4.9.x        |
| 6.x            | 4.10.x       |
| 7.x            | 4.11.x       |

#### HTTP options <a href="#user-content-http-options" id="user-content-http-options"></a>

The underlying HTTP client that performs the calls to the webhook URL can be tuned with the following parameters.

<table><thead><tr><th width="173">Attributes</th><th width="94">Default</th><th width="121">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td>connectTimeout</td><td>3000</td><td>Yes</td><td>Maximum time to connect to the backend in milliseconds.</td></tr><tr><td>readTimeout</td><td>10000</td><td>Yes</td><td>Maximum time given to the backend to complete the request (including response) in milliseconds.</td></tr><tr><td>idleTimeout</td><td>60000</td><td>Yes</td><td>Maximum time a connection will stay in the pool without being used in milliseconds. Once the timeout has elapsed, the unused connection will be closed, freeing the associated resources.</td></tr><tr><td>maxConcurrentConnections</td><td>5</td><td>Yes</td><td>Maximum pool size for connections. This represents the maximum number of concurrent requests. Max value is 20. Value is automatically set to 1 when using QoS AT_LEAST_ONCE or AT_MOST_ONCE to ensure message delivery.</td></tr></tbody></table>

#### Dead Letter Queue <a href="#user-content-secured-callbacks" id="user-content-secured-callbacks"></a>

Dead Letter Queue (DLQ) is the ability to push undelivered messages to an external storage. When configuring DLQ with webhook, you can redirect all messages rejected by the Webhook to another location, such as a Kafka topic.

By default, without DLQ, any error returned by the webhook will stop message consumption.

* **To configure DLQ in the Console:** toggle **Dead Letter Queue** ON to define an external storage where each unsuccessfully pushed message will be stored and configure a replay strategy. Use the drop-down menu to select a pre-existing and supported endpoint or endpoint group to use for the DLQ.
*   **To enable DLQ via the API definition:** declare another endpoint that will be used to configure the DLQ object in the webhook entrypoint definition:

    ```json
    {
        "type": "webhook",
        "dlq": {
            "endpoint": "dlq-endpoint"
        },
        "configuration": {}
    }
    ```

    The endpoint used for the DLQ:

    * Must support `PUBLISH` mode
    * Should be based on a broker capable of persisting messages, e.g., Kafka

Once configured and deployed, any message rejected by the webhook with a 4xx error response will be automatically sent to the DLQ endpoint and message consumption will resume.

#### Secured callbacks

When you create a subscription, you can provide security information. These are the security types that are supported:&#x20;

* Basic
* Token (JWT)
* OAuth2

#### Dynamic callback path

{% hint style="info" %}
The dynamic callback path is available from APIM 4.11.10.
{% endhint %}

By default, every message of a subscription is pushed to the same **Callback URL**. To route each message to a different path, set the optional **Dynamic callback path** on the subscription. The gateway evaluates it for each message and appends the result to the callback URL.

The dynamic callback path supports [Gravitee Expression Language](../../../gravitee-expression-language.md) with the message context, so the path can be built from the message content, headers, or attributes. For example:

| Dynamic callback path | Message | Resulting call |
| --------------------- | ------- | -------------- |
| `/process-{#message.attributes['id']}` | Attribute `id` = `42` | `https://myapp.example.com/webhooks/process-42` |
| `/orders/{#message.headers['order-id'][0]}` | Header `order-id` = `A-17` | `https://myapp.example.com/webhooks/orders/A-17` |
| `/process/{#jsonPath(#message.content, '$.id')}` | Content `{"id": "123"}` | `https://myapp.example.com/webhooks/process/123` |

When you create the subscription through the Management API v2, set `callbackUrlPath` next to `callbackUrl` in `consumerConfiguration.entrypointConfiguration`:

```json
{
  "consumerConfiguration": {
    "entrypointId": "webhook",
    "entrypointConfiguration": {
      "callbackUrl": "https://myapp.example.com/webhooks",
      "callbackUrlPath": "/process-{#message.attributes['id']}"
    }
  }
}
```

The dynamic callback path follows these rules:

* Only the path changes. The scheme, host, and port of the callback URL stay the same for every message. The expression cannot change the host: if it evaluates to a full URL, such as `http://other-host:1234/x`, that URL is appended as a path.
* Path segments are joined with a single `/`, whether or not the callback URL ends with `/` or the evaluated path starts with `/`.
* A query string on the callback URL is kept and placed after the appended path. If the evaluated path has its own query string, both are merged. For example, `https://myapp.example.com/webhooks?token=abc` with `/process-42?retry=1` calls `https://myapp.example.com/webhooks/process-42?token=abc&retry=1`.
* If the expression evaluates to null or an empty string, the message is sent to the callback URL unchanged.
* If the expression fails to evaluate, the message is not sent to the webhook. It is sent to the Dead Letter Queue when one is configured. Without a Dead Letter Queue, the subscription stops consuming messages.

{% hint style="info" %}
When you use an expression in the dynamic callback path, configure a [Dead Letter Queue](#dead-letter-queue) so that a message whose expression fails does not stop the subscription.
{% endhint %}
