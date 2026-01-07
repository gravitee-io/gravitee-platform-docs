---
description: Configuration guide for webhook.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/bGmDEarvnV52XdcOiV8o/create-and-configure-apis/configure-v4-apis/entrypoints/webhook
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
| 4.x            | 4.6 to 4..8  |

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
