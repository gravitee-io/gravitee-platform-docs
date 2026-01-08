---
description: An overview about mqtt5.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/bGmDEarvnV52XdcOiV8o/create-and-configure-apis/configure-v4-apis/endpoints/mqtt5
---

# MQTT5

## Overview

This page discusses the [configuration](mqtt5.md#configuration) and [implementation](mqtt5.md#implementation) of the **MQTT5** endpoint and includes a [reference](mqtt5.md#reference) section.

## Configuration

The **MQTT5** endpoint allows the Gateway to open up a persistent connection to and/or call a backend MQTT broker, as long as that broker is running on MQTT 5.x via an MQTT client set up by the Gravitee Gateway. Entering a host/port pair (and a list of topics for a producer) is required. Modifying any other configuration parameters is optional.

### 1. Server information

1. **Server host:** Define the serverHost for the MQTT broker that you are using as your endpoint.
2. **Server port:** Define the serverPort for the MQTT broker that you are using as your endpoint.

### 2. Role

You can tell the Gravitee Gateway's MQTT client to act as a producer, a consumer, or both a producer and consumer. Choose **Use Consumer**, **Use Producer**, or **Use Consumer and Producer** from the drop-down menu to do one of the following:

* **Use Producer:** Tells the Gateway MQTT client to be prepared to produce messages and send them to the MQTT broker that you define as your endpoint.
* **Use Consumer:** Tells the Gateway MQTT client to be prepared to consume messages from the MQTT broker that you define as your endpoint.
* **Use Producer and Consumer**: Tells the Gateway MQTT client to both **Use Producer** and **Use Consumer**.

### 3. Reconnect attempts

Specify an integer number (max 10) of reconnect attempts that the Gateway will initiate if the Gateway MQTT client disconnects from the MQTT broker.

### **4. Session expiry interval**

Define the period of time that the broker stores the session information of that particular MQTT client. When the session expiry interval is set to 0 or the CONNECT packet does not contain an expiry value, the session information is immediately removed from the broker when the client network connection closes.

### 5. Initial security settings

You will define more Gravitee Gateway-specific security settings later on, but this is where you define your MQTT-specific authentication flow. Gravitee supports **No security configuration**, **Authentication configuration**, **SSL configuration**, and **Authentication with SSL configuration**.

{% tabs %}
{% tab title="Authentication" %}
Gravitee uses TLS to support the **Username** and **Password** you define.
{% endtab %}

{% tab title="SSL" %}
**Hostname verifier:** Toggle to enable or disable hostname verification.

Define whichever of the following are relevant to your configuration.

**Truststore**

* **None**
* **PEM with content:** Enter binary content as base64.
* **PEM with path:** Enter the path to the truststore file.
* **JKS with content:** Enter binary content as base64 and the truststore password.
* **JKS with path:** Enter the truststore file path and password.
* **PKCS12 with content:** Enter binary content as base64 and the truststore password.
* **PKCS12 with path:** Enter the truststore file path and password

**Keystore**

* **None**
* **PEM with content:** Enter the certificate content and key content.
* **PEM with path:** Enter the certificate path and key path.
* **JKS with content:** Enter binary content as base64 and the keystore password.
* **JKS with path:** Enter the keystore file path and password.
* **PKCS12 with content:** Enter binary content as base64 and the keystore password.
* **PKCS12 with path:** Enter the keystore file path and password.
{% endtab %}
{% endtabs %}

### 6. Role settings

If you chose **Use Producer** or **Use Producer and Consumer**, you must define the settings that the Gravitee Gateway MQTT client will rely on to produce messages to your backend MQTT topic/broker.

If you chose **Use Consumer** or **Use Producer and Consumer**, you must define the settings that the Gravitee Gateway MQTT client will rely on to consume messages from your backend MQTT topic/broker.

{% tabs %}
{% tab title="Producer" %}
Define the following:

1. **Topic:** The UTF-8 string that the broker uses to filter messages for each connected client. The topic consists of one or more topic levels. Each topic level is separated by a forward slash (topic level separator).
2. **Retain settings:** Whether the retain flag must be set for every published message by toggling **Retained** ON or OFF. If enabled, the broker stores the last retained message.
3. **Message expiry interval:** Define the period of time that the broker stores the PUBLISH message for any matching subscribers that are not currently connected. When no message expiry interval is set, the broker must store the message for matching subscribers indefinitely. When the `retained=true` option is set on the PUBLISH message, the message expiry interval defines how long a message is retained on a topic.
4. **Response topic:** Define the topics on which the responses from the message receivers are expected.
{% endtab %}

{% tab title="Consumer" %}
Define the **Topic** from which the Gateway MQTT client will consume messages. **Topic** refers to an UTF-8 string that the broker uses to filter messages for each connected client and consists of one or more topic levels (separated by a forward slash).
{% endtab %}
{% endtabs %}

### Tenants

You can configure tenants to specify which users can proxy requests to this endpoint. Tenants ensure that certain groups of users receive information from only specific APIs. For more information about configuring tenants, see [tenants.md](../../../configure-and-manage-the-platform/gravitee-gateway/tenants.md "mention").

## Implementation

### Common to subscribe and publish

On each incoming request, an MQTT client is created and will persist until the request is terminated. This relies on **MQTT Client Identifier** and **Session Expiry Interval**.

{% tabs %}
{% tab title="MQTT Client Identifier" %}
The identifier for the MQTT Client is generated with the format `gio-apim-client-<first part of uuid>`, e.g., `gio-apim-client-a0eebc99`.
{% endtab %}

{% tab title="Session Expiry Interval" %}
The default value is 86,400 seconds. If the value in the configuration is less than or equal to -1, no session expiry is set.
{% endtab %}
{% endtabs %}

### Subscribe

On each incoming request, the [common client](mqtt5.md#common-to-subscribe-and-publish) is used to subscribe to a shared topic. The MQTT endpoint retrieves information from the request to configure the subscription. Subscription relies on **Shared subscription**, **Topic**, and **QoS**.

{% tabs %}
{% tab title="Shared subscription" %}
A shared subscription is created from the incoming request per the format `$share/<clientIdentifier>/<topic>`. This allows multiple clients using the same subscription to consume the same topic in parallel. In order to distinguish all clients using the same subscription, the client identifier must be overridden.
{% endtab %}

{% tab title="Topic" %}
The topic is retrieved from the API configuration and can be overridden with the attribute `gravitee.attribute.mqtt5.topic`**.**
{% endtab %}

{% tab title="QoS" %}
When the entrypoint supports manual ack, the strategy will use it. Otherwise, it will use auto-ack.
{% endtab %}
{% endtabs %}

### Publish

On each incoming request, the [common client](mqtt5.md#common-to-subscribe-and-publish) is used to publish messages on a topic. This publication is done with MQTT At-Least-Once QoS, without expiration. Publication relies on **Topic** and **Message Expiry Interval**.

{% tabs %}
{% tab title="Topic" %}
The topic is retrieved from the API configuration and can be overridden, either on the request or the message, with the attribute `gravitee.attribute.mqtt5.topic`.
{% endtab %}

{% tab title="Message Expiry Interval" %}
By default, there is no expiry. The value can be configured in the API definition.
{% endtab %}
{% endtabs %}

## Reference

Refer to the following sections for additional details.

### Compatibility matrix <a href="#user-content-compatibility-matrix" id="user-content-compatibility-matrix"></a>

| Plugin version | APIM version    |
| -------------- | --------------- |
| 1.x and up     | 4.0.x to latest |

### Endpoint identifier <a href="#user-content-endpoint-identifier" id="user-content-endpoint-identifier"></a>

To use this plugin, declare the `mqtt5` identifier when configuring your API endpoints.

### Endpoint configuration <a href="#user-content-endpoint-configuration" id="user-content-endpoint-configuration"></a>

#### General configuration <a href="#user-content-general-configuration" id="user-content-general-configuration"></a>

<table><thead><tr><th width="133">Attributes</th><th width="89">Default</th><th width="118">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td>serverHost</td><td>N/A</td><td>Yes</td><td>Define the host of the MQTT broker.</td></tr><tr><td>serverPort</td><td>N/A</td><td>Yes</td><td>Define the port of the MQTT broker.</td></tr></tbody></table>

#### Shared Configuration <a href="#user-content-shared-configuration" id="user-content-shared-configuration"></a>

<table><thead><tr><th width="208">Attributes</th><th width="131">Default</th><th width="116">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td>sessionExpiryInterval</td><td>86400 (24h)</td><td>No</td><td>The expiry interval, in seconds, of the persistent session. Default is 24h, -1 means no expiry.</td></tr></tbody></table>

{% tabs %}
{% tab title="Security" %}
Security options are available under the `security` attribute configuration.
{% endtab %}

{% tab title="Authentication" %}
Available under `security.auth`:

<table><thead><tr><th width="129">Attributes</th><th width="88">Default</th><th width="115">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td>username</td><td>N/A</td><td>No</td><td>The username to use for the authentication.</td></tr><tr><td>password</td><td>N/A</td><td>No</td><td>The password to use for the authentication.</td></tr></tbody></table>
{% endtab %}

{% tab title="SSL" %}
Available under `security.ssl`:

<table><thead><tr><th width="212">Attributes</th><th width="90">Default</th><th width="116">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td>truststore.type</td><td>N/A</td><td>Yes</td><td>Truststore type can be PKCS12, JKS, or PEM.</td></tr><tr><td>truststore.path</td><td>N/A</td><td>No</td><td>The path from which the truststore is loaded.</td></tr><tr><td>truststore.content</td><td>N/A</td><td>No</td><td>The content in base64 from which the keystore is loaded.</td></tr><tr><td>truststore.password</td><td>N/A</td><td>No</td><td>The password used to load the truststore.</td></tr><tr><td>keystore.type</td><td>N/A</td><td>No</td><td>Keystore type can be PKCS12, JKS, or PEM.</td></tr><tr><td>keystore.path</td><td>N/A</td><td>No</td><td>The path from which the keystore is loaded.</td></tr><tr><td>keystore.content</td><td>N/A</td><td>No</td><td>The content in base64 from which the keystore is loaded.</td></tr><tr><td>keystore.password</td><td>N/A</td><td>No</td><td>The password used to load the keystore.</td></tr><tr><td>keystore.certPath</td><td>N/A</td><td>No</td><td>The path from which the certificate is loaded.</td></tr><tr><td>keystore.certContent</td><td>N/A</td><td>No</td><td>The content in base64 from which the certificate is loaded.</td></tr><tr><td>keystore.keyPath</td><td>N/A</td><td>No</td><td>The path from which the key is loaded.</td></tr><tr><td>keystore.keyContent</td><td>N/A</td><td>No</td><td>The content in base64 from which the key is loaded.</td></tr><tr><td>keystore.keyPassword</td><td>N/A</td><td>No</td><td>The password used to read the key.</td></tr></tbody></table>
{% endtab %}

{% tab title="Consumer" %}
<table><thead><tr><th width="127">Attributes</th><th width="87">Default</th><th width="117">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td>enabled</td><td>false</td><td>No</td><td>Allow enabling or disabling of the consumer capability.</td></tr><tr><td>topic</td><td>N/A</td><td>Yes</td><td>Refers to a UTF-8 string that the broker uses to filter messages for each connected client.</td></tr></tbody></table>

{% hint style="warning" %}
Gravitee's management of shared subscriptions allows parallel requests to consume messages. MQTT5 does not allow last-retained message delivery for shared subscriptions.
{% endhint %}
{% endtab %}

{% tab title="Producer" %}
<table><thead><tr><th width="219">Attributes</th><th width="93">Default</th><th width="121">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td>enabled</td><td>false</td><td>No</td><td>Allow enabling or disabling of the producer capability.</td></tr><tr><td>topic</td><td>N/A</td><td>Yes</td><td>Refers to a UTF-8 string that the broker uses to filter messages for each connected client.</td></tr><tr><td>retained</td><td>false</td><td>No</td><td>Define if the retain flag must be set to publish every message.</td></tr><tr><td>responseTopic</td><td>N/A</td><td>No</td><td>The response topic represents the topic(s) on which the responses from the receivers of the message are expected.</td></tr><tr><td>messageExpiryInterval</td><td>-1</td><td>No</td><td>This interval defines the period of time that the broker stores the publish message for any matching subscribers that are not currently connected. When no message expiry interval is set, the broker must store the message for matching subscribers indefinitely. When the <code>retained=true</code> option is set on the PUBLISH message, this interval also defines how long a message is retained on a topic.</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

#### Example

The example below shows a full MQTT endpoint configuration:

```json
{
                    "name": "default",
                    "type": "mqtt5",
                    "weight": 1,
                    "inheritConfiguration": false,
                    "configuration": {
                        "serverHost": "localhost",
                        "serverPort": 9883
                    },
                    "sharedConfigurationOverride": {
                        "consumer" : {
                            "enabled": true,
                            "topic": "example"
                        },
                        "security" : {
                            "auth": {
                                "username": "user",
                                "password": "password"
                            },
                            "ssl" : {
                                "trustStore" : {
                                    "type" : "PKCS12",
                                    "path" : "/path/to/certs/hivemq-server.p12",
                                    "password" : "gravitee"
                                },
                                "keyStore" : {
                                    "type" : "PKCS12",
                                    "path" : "/path/to/certs/client.p12",
                                    "password" : "gravitee"
                                }
                            }
                        }
                    }
                }
```

### Supplemental information <a href="#user-content-a-word-on" id="user-content-a-word-on"></a>

<details>

<summary>MQTT5 vs Gravitee</summary>

The Gateway acts as a protocol mediator and includes an abstraction layer to provide the API consumer with the same experience for every supported backend technology (MQTT, Kafka, etc.).

Gravitee implements MQTT5 shared subscriptions to ensure that the Gateway can handle multiple concurrent requests. This is subject to the following limitations:

* Latest retain message is not supported by shared subscriptions and so not transmitted when subscribing
* The NoLocal MQTT5 feature is not supported by shared subscriptions
* Some MQTT5 server implementations such as HiveMQ are able to deliver messages that were received when a client was disconnected. Others, such as Mosquitto, are not.

</details>

<details>

<summary>HTTP polling</summary>

The Gravitee HTTP GET entrypoint connector allows HTTP polling by API consumers. The MQTT5 connector uses shared subscriptions to avoid losing messages sent between 2 HTTP polls. In this case, the first HTTP poll creates the shared subscription that enables the subsequent HTTP poll to consume the pending messages.

MQTT5 isn’t designed to support persisting pending messages for long periods. Consumers performing HTTP polling with long disconnection periods may lose messages.

If concurrent HTTP poll requests originate from the same consumer application, the messages will be spread across the HTTP poll.

HTTP GET does not offer particular QoS, and it is not possible to consume messages from a particular point in time. Message consumption is entirely dependent on MQTT5 server capabilities, and message loss or duplication may occur.

</details>

<details>

<summary>Server-sent events</summary>

It is possible to stream the messages from a MQTT5 topic in real time using the SSE entrypoint. A consumer can run several SSE calls to distribute the workload across multiple instances. All the messages will be shared between instances.

SSE does not offer particular QoS and, in case of network failure or issues on the client side, messages may be acknowledged but never received.

</details>

<details>

<summary>Webhook</summary>

Webhook is the only entrypoint offering the `AT-MOST-ONCE` or `AT-LEAST-ONCE` QoS capability. Webhook subscriptions run in the background on the Gateway and make a call to an external HTTP URL for each message consumed. The message is acknowledged only if the call is successful (e.g., 2xx response from the remote service).

</details>

<details>

<summary>Other entrypoints</summary>

The MQTT5 endpoint can be used with any entrypoint that supports messages. For example, it is possible to publish or consume messages using the WebSocket entrypoint or publish messages with the HTTP POST entrypoint.

</details>

<details>

<summary>Recommendations</summary>

Below are recommendations to increase stability when consuming messages with HTTP GET and MQTT5:

* Configure a `sessionExpiryInterval` to retain messages for sufficient intervals between HTTP polls.
* Ensure that messages to consume are published with a proper `messageExpiryInterval` and `qos`. A `messageExpiryInterval` set to 0 or a `qos` set to `AT_MOST_ONCE` may expire the message before the consumer can perform another HTTP poll to consume it.

</details>
