---
description: This page contains the technical details of the MQTT5 endpoint plugin
---

# MQTT5

{% hint style="warning" %}
**This feature requires** [**Gravitee's Enterprise Edition**](../../overview/ee-vs-oss/)**.**
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

<table><thead><tr><th width="212">Attributes</th><th width="90">Default</th><th width="116">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td>trustore.type</td><td>N/A</td><td>Yes</td><td>Truststore type can be PKCS12, JKS, or PEM.</td></tr><tr><td>trustore.path</td><td>N/A</td><td>No</td><td>The path from which the truststore is loaded.</td></tr><tr><td>trustore.content</td><td>N/A</td><td>No</td><td>The content in base64 from which the keystore is loaded.</td></tr><tr><td>trustore.password</td><td>N/A</td><td>No</td><td>The password used to load the truststore.</td></tr><tr><td>keystore.type</td><td>N/A</td><td>No</td><td>Keystore type can be PKCS12, JKS, or PEM.</td></tr><tr><td>keystore.path</td><td>N/A</td><td>No</td><td>The path from which the keystore is loaded.</td></tr><tr><td>keystore.content</td><td>N/A</td><td>No</td><td>The content in base64 from which the keystore is loaded.</td></tr><tr><td>keystore.password</td><td>N/A</td><td>No</td><td>The password used to load the keystore.</td></tr><tr><td>keystore.certPath</td><td>N/A</td><td>No</td><td>The path from which the certificate is loaded.</td></tr><tr><td>keystore.certContent</td><td>N/A</td><td>No</td><td>The content in base64 from which the certificate is loaded.</td></tr><tr><td>keystore.keyPath</td><td>N/A</td><td>No</td><td>The path from which the key is loaded.</td></tr><tr><td>keystore.keyContent</td><td>N/A</td><td>No</td><td>The content in base64 from which the key is loaded.</td></tr><tr><td>keystore.keyPassword</td><td>N/A</td><td>No</td><td>The password used to read the key.</td></tr></tbody></table>

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

* Latest retain message is not transmitted when subscribing because it is not supported when using shared subscriptions
* NoLocal Mqtt feature is not supported by shared subscriptions.
* Some Mqtt5 server implementation such as HiveMq are able to deliver messages received when a client was disconnected. Others such as Mosquitto aren’t.

### HTTP polling <a href="#user-content-http-polling" id="user-content-http-polling"></a>

You can use gravitee http-get entrypoint connector to allow api consumers doing http polling. To avoid loosing messages that could have been sent between 2 http polls, Mqtt5 connector uses shared subscription.

The first http poll will create the shared subscription allowing subsequent http pool to consume the pending messages.

Mqtt5 isn’t made for persisting pending messages for a long period. Consumers that making http polling with long disconnection period may loose some messages.

In case of concurrent http poll requests coming from the same consumer application, the messages will be spread between the http poll.

Http get does not offer particular QoS, and it is not possible to consume messages from a particular point in time. Messages consumption is entirely depending on Mqtt5 server capabilities. Message loss or duplicates may happen.

#### Server Side Event <a href="#user-content-server-side-event" id="user-content-server-side-event"></a>

It is possible to stream the messages from a Mqtt5 topic in real time using SSE entrypoint. A consumer can run several sse calls in order to share the workload across multiple instances. All the messages will be shared between the instances.

Sse does not offer particular QoS and, in case of network failure or issue on the client side, that some messages may be acknowledged but never received.

#### Webhook <a href="#user-content-webhook" id="user-content-webhook"></a>

Webhook is the only entrypoint offering the `AT-MOST-ONCE` or `AT-LEAST-ONCE` qos capability. Webhook subscription are running in background on the gateway and basically make a call to an external http url for each message consume. The message is acknowledged only in case of success call (eg: 2xx response from the remote service).

#### Other entrypoints <a href="#user-content-other-entrypoints" id="user-content-other-entrypoints"></a>

Mqtt5 endpoint can be used with any type of entrypoint as long as it supports messages. It is for example possible to publish or consume messages using WebSocket entrypoint or simply publish messages with Http post entrypoint.

#### Recommendations <a href="#user-content-recommendations" id="user-content-recommendations"></a>

Here are some recommendations to increase stability when consuming messages with http get and mqtt5:

* Configure a `sessionExpiryInterval` to keep messages long time enough between http polls.
* Ensure that messages to consume are published with a proper `messageExpiryInterval` and `qos`. Having a `messageExpiryInterval` set to 0 or a `qos` set to `AT_MOST_ONCE` may expire the message before the consumer has a chance to make another http poll to consume it.
