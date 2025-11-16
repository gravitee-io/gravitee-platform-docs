---
description: This page contains the technical details of the MQTT5 endpoint plugin
---

# MQTT5

{% hint style="warning" %}
**This feature requires** [**Gravitee's Enterprise Edition**](../../../../../../overview/gravitee-apim-enterprise-edition/README.md)**.**
{% endhint %}

## Overview

Use this endpoint to publish and/or subscribe messages to a MQTT 5.x broker such as HiveMQ or Mosquito. Refer to the following sections for additional details.

* [Compatibility matrix](mqtt5.md#user-content-compatibility-matrix)
* [Endpoint identifier](mqtt5.md#user-content-endpoint-identifier)
* [Endpoint configuration](mqtt5.md#user-content-endpoint-configuration)
* [Supplemental information](mqtt5.md#user-content-a-word-on)

## Compatibility matrix <a href="#user-content-compatibility-matrix" id="user-content-compatibility-matrix"></a>

| Plugin version | APIM version    |
| -------------- | --------------- |
| 1.x and up     | 4.0.x to latest |

## Endpoint identifier <a href="#user-content-endpoint-identifier" id="user-content-endpoint-identifier"></a>

To use this plugin, declare the following `mqtt5` identifier while configuring your API endpoints.

## Endpoint configuration <a href="#user-content-endpoint-configuration" id="user-content-endpoint-configuration"></a>

### General configuration <a href="#user-content-general-configuration" id="user-content-general-configuration"></a>

#### **Endpoint-level configuration**

<table><thead><tr><th width="133">Attributes</th><th width="89">Default</th><th width="118">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td>serverHost</td><td>N/A</td><td>Yes</td><td>Define the host of the MQTT broker.</td></tr><tr><td>serverPort</td><td>N/A</td><td>Yes</td><td>Define the port of the MQTT broker.</td></tr></tbody></table>

### Shared Configuration <a href="#user-content-shared-configuration" id="user-content-shared-configuration"></a>

<table><thead><tr><th width="208">Attributes</th><th width="131">Default</th><th width="116">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td>sessionExpiryInterval</td><td>86400 (24h)</td><td>No</td><td>The expiry interval, in seconds, of the persistent session. Default is 24h, -1 means no expiry.</td></tr></tbody></table>

#### **Security**

Security options are available under the `security` attribute configuration.

#### **Authentication**

Available under `security.auth`:

<table><thead><tr><th width="129">Attributes</th><th width="88">Default</th><th width="115">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td>username</td><td>N/A</td><td>No</td><td>The username to use for the authentication.</td></tr><tr><td>password</td><td>N/A</td><td>No</td><td>The password to use for the authentication.</td></tr></tbody></table>

#### **SSL**

Available under `security.ssl`:

<table><thead><tr><th width="212">Attributes</th><th width="90">Default</th><th width="116">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td>truststore.type</td><td>N/A</td><td>Yes</td><td>Truststore type can be PKCS12, JKS, or PEM.</td></tr><tr><td>truststore.path</td><td>N/A</td><td>No</td><td>The path from which the truststore is loaded.</td></tr><tr><td>truststore.content</td><td>N/A</td><td>No</td><td>The content in base64 from which the keystore is loaded.</td></tr><tr><td>truststore.password</td><td>N/A</td><td>No</td><td>The password used to load the truststore.</td></tr><tr><td>keystore.type</td><td>N/A</td><td>No</td><td>Keystore type can be PKCS12, JKS, or PEM.</td></tr><tr><td>keystore.path</td><td>N/A</td><td>No</td><td>The path from which the keystore is loaded.</td></tr><tr><td>keystore.content</td><td>N/A</td><td>No</td><td>The content in base64 from which the keystore is loaded.</td></tr><tr><td>keystore.password</td><td>N/A</td><td>No</td><td>The password used to load the keystore.</td></tr><tr><td>keystore.certPath</td><td>N/A</td><td>No</td><td>The path from which the certificate is loaded.</td></tr><tr><td>keystore.certContent</td><td>N/A</td><td>No</td><td>The content in base64 from which the certificate is loaded.</td></tr><tr><td>keystore.keyPath</td><td>N/A</td><td>No</td><td>The path from which the key is loaded.</td></tr><tr><td>keystore.keyContent</td><td>N/A</td><td>No</td><td>The content in base64 from which the key is loaded.</td></tr><tr><td>keystore.keyPassword</td><td>N/A</td><td>No</td><td>The password used to read the key.</td></tr></tbody></table>

#### **Consumer configuration**

<table><thead><tr><th width="127">Attributes</th><th width="87">Default</th><th width="117">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td>enabled</td><td>false</td><td>No</td><td>Allow enabling or disabling of the consumer capability.</td></tr><tr><td>topic</td><td>N/A</td><td>Yes</td><td>Refers to a UTF-8 string that the broker uses to filter messages for each connected client.</td></tr></tbody></table>

{% hint style="warning" %}
Gravitee's management of shared subscriptions allows parallel requests to consume messages. MQTT5 does not allow last-retained message delivery for shared subscriptions.
{% endhint %}

#### **Producer configuration**

<table><thead><tr><th width="219">Attributes</th><th width="93">Default</th><th width="121">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td>enabled</td><td>false</td><td>No</td><td>Allow enabling or disabling of the producer capability.</td></tr><tr><td>topic</td><td>N/A</td><td>Yes</td><td>Refers to a UTF-8 string that the broker uses to filter messages for each connected client.</td></tr><tr><td>retained</td><td>false</td><td>No</td><td>Define if the retain flag must be set to publish every message.</td></tr><tr><td>responseTopic</td><td>N/A</td><td>No</td><td>The response topic represents the topic(s) on which the responses from the receivers of the message are expected.</td></tr><tr><td>messageExpiryInterval</td><td>-1</td><td>No</td><td>This interval defines the period of time that the broker stores the publish message for any matching subscribers that are not currently connected. When no message expiry interval is set, the broker must store the message for matching subscribers indefinitely. When the <code>retained=true</code> option is set on the PUBLISH message, this interval also defines how long a message is retained on a topic.</td></tr></tbody></table>

### Examples <a href="#user-content-examples" id="user-content-examples"></a>

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

## Supplemental information <a href="#user-content-a-word-on" id="user-content-a-word-on"></a>

### MQTT5 vs Gravitee <a href="#user-content-mqtt5-vs-gravitee" id="user-content-mqtt5-vs-gravitee"></a>

The Gateway acts as a protocol mediator and includes an abstraction layer to provide the API consumer with the same experience for every supported backend technology (MQTT, Kafka, etc.).

Gravitee implements MQTT5 shared subscriptions to ensure that the Gateway can handle multiple concurrent requests. This is subject to the following limitations:

* Latest retain message is not supported by shared subscriptions and so not transmitted when subscribing
* The NoLocal MQTT5 feature is not supported by shared subscriptions
* Some MQTT5 server implementations such as HiveMQ are able to deliver messages that were received when a client was disconnected. Others, such as Mosquitto, are not.

### HTTP polling <a href="#user-content-http-polling" id="user-content-http-polling"></a>

The Gravitee HTTP GET entrypoint connector allows HTTP polling by API consumers. The MQTT5 connector uses shared subscriptions to avoid losing messages sent between 2 HTTP polls. In this case, the first HTTP poll creates the shared subscription that enables the subsequent HTTP poll to consume the pending messages.

MQTT5 isn’t designed to support persisting pending messages for long periods. Consumers performing HTTP polling with long disconnection periods may lose messages.

If concurrent HTTP poll requests originate from the same consumer application, the messages will be spread across the HTTP poll.

HTTP GET does not offer particular QoS, and it is not possible to consume messages from a particular point in time. Message consumption is entirely dependent on MQTT5 server capabilities, and message loss or duplication may occur.

### Server-sent events <a href="#user-content-server-side-event" id="user-content-server-side-event"></a>

It is possible to stream the messages from a MQTT5 topic in real time using the SSE entrypoint. A consumer can run several SSE calls to distribute the workload across multiple instances. All the messages will be shared between instances.

SSE does not offer particular QoS and, in case of network failure or issues on the client side, messages may be acknowledged but never received.

### Webhook <a href="#user-content-webhook" id="user-content-webhook"></a>

Webhook is the only entrypoint offering the `AT-MOST-ONCE` or `AT-LEAST-ONCE` QoS capability. Webhook subscriptions run in the background on the Gateway and make a call to an external HTTP URL for each message consumed. The message is acknowledged only if the call is successful (e.g., 2xx response from the remote service).

### Other entrypoints <a href="#user-content-other-entrypoints" id="user-content-other-entrypoints"></a>

The MQTT5 endpoint can be used with any entrypoint that supports messages. For example, it is possible to publish or consume messages using the WebSocket entrypoint or publish messages with the HTTP POST entrypoint.

### Recommendations <a href="#user-content-recommendations" id="user-content-recommendations"></a>

Below are recommendations to increase stability when consuming messages with HTTP GET and MQTT5:

* Configure a `sessionExpiryInterval` to retain messages for sufficient intervals between HTTP polls.
* Ensure that messages to consume are published with a proper `messageExpiryInterval` and `qos`. A `messageExpiryInterval` set to 0 or a `qos` set to `AT_MOST_ONCE` may expire the message before the consumer can perform another HTTP poll to consume it.
