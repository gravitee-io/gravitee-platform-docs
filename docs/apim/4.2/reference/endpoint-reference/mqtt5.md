---
description: This page contains the technical details of the MQTT5 endpoint plugin
---

# MQTT5

This is an Enterprise feature

### Description <a href="#user-content-description" id="user-content-description"></a>

This is a MQTT 5.x endpoint which allow subscribing or publishing messages to a MQTT 5.x broker such as HiveMQ or Mosquitto.

### Compatibility matrix <a href="#user-content-compatibility-matrix" id="user-content-compatibility-matrix"></a>

| Plugin version | APIM version    |
| -------------- | --------------- |
| 1.x and upper  | 4.0.x to latest |

### Endpoint identifier <a href="#user-content-endpoint-identifier" id="user-content-endpoint-identifier"></a>

In order to use this plugin, you only have to declare the following identifier `mqtt5` while configuring your API endpoints.

### Endpoint configuration <a href="#user-content-endpoint-configuration" id="user-content-endpoint-configuration"></a>

#### General configuration <a href="#user-content-general-configuration" id="user-content-general-configuration"></a>

**Endpoint level configuration**

| Attributes | Default | Mandatory | Description                         |
| ---------- | ------- | --------- | ----------------------------------- |
| serverHost | N/A     | Yes       | Define the host of the MQTT broker. |
| serverPort | N/A     | Yes       | Define the port of the MQTT broker. |

#### Shared Configuration <a href="#user-content-shared-configuration" id="user-content-shared-configuration"></a>

| Attributes            | Default     | Mandatory | Description                                                                                   |
| --------------------- | ----------- | --------- | --------------------------------------------------------------------------------------------- |
| sessionExpiryInterval | 86400 (24h) | No        | The expiry interval in seconds of the persistent session. Default is 24h, -1 means no expiry. |

**Security**

Security options are available under _security_ attribute configuration.

**Authentication**

Available under `security.auth` :

| Attributes | Default | Mandatory | Description                                 |
| ---------- | ------- | --------- | ------------------------------------------- |
| username   | N/A     | No        | The username to use for the authentication. |
| password   | N/A     | No        | The password to use for the authentication. |

**SSL**

Available under `security.ssl` :

| Attributes           | Default | Mandatory | Description                                                 |
| -------------------- | ------- | --------- | ----------------------------------------------------------- |
| trustore.type        | N/A     | Yes       | Truststore type could be either PKCS12, JKS or PEM.         |
| trustore.path        | N/A     | No        | The path from which the truststore is loaded.               |
| trustore.content     | N/A     | No        | The content in base64 from which the keystore is loaded.    |
| trustore.password    | N/A     | No        | The password used to load the truststore.                   |
| keystore.type        | N/A     | No        | Keystore type could be either PKCS12, JKS or PEM.           |
| keystore.path        | N/A     | No        | The path from which the keystore is loaded.                 |
| keystore.content     | N/A     | No        | The content in base64 from which the keystore is loaded.    |
| keystore.password    | N/A     | No        | The password used to load the keystore.                     |
| keystore.certPath    | N/A     | No        | The path from which the certificate is loaded.              |
| keystore.certContent | N/A     | No        | The content in base64 from which the certificate is loaded. |
| keystore.keyPath     | N/A     | No        | The path from which the key is loaded.                      |
| keystore.keyContent  | N/A     | No        | The content in base64 from which the key is loaded.         |
| keystore.keyPassword | N/A     | No        | The password used to read the key.                          |

**Consumer configuration**

| Attributes | Default | Mandatory | Description                                                                                  |
| ---------- | ------- | --------- | -------------------------------------------------------------------------------------------- |
| enabled    | false   | No        | Allow enabling or disabling the consumer capability.                                         |
| topic      | N/A     | Yes       | Refers to an UTF-8 string that the broker uses to filter messages for each connected client. |

| Important | Behind the scene, gravitee will manage shared subscription in order to allow parallel requests to consume messages. It is important to notice that Mqtt5 does not allow last retained message delivery with shared subscriptions. |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

**Producer configuration**

| Attributes            | Default | Mandatory | Description                                                                                                                                                                                                                                                                                                                                                                                            |
| --------------------- | ------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| enabled               | false   | No        | Allow enabling or disabling the producer capability.                                                                                                                                                                                                                                                                                                                                                   |
| topic                 | N/A     | Yes       | Refers to an UTF-8 string that the broker uses to filter messages for each connected client.                                                                                                                                                                                                                                                                                                           |
| retained              | false   | No        | Define if the retain flag must be set to every publish messages.                                                                                                                                                                                                                                                                                                                                       |
| responseTopic         | N/A     | No        | The response topic represents the topics on which the responses from the receivers of the message are expected.                                                                                                                                                                                                                                                                                        |
| messageExpiryInterval | -1      | No        | This interval defines the period of time that the broker stores the publish message for any matching subscribers that are not currently connected. When no message expiry interval is set, the broker must store the message for matching subscribers indefinitely. When the retained=true option is set on the PUBLISH message, this interval also defines how long a message is retained on a topic. |

#### Examples <a href="#user-content-examples" id="user-content-examples"></a>

Bellow you will find a full mqtt endpoint configuration example:

```
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

### A word on <a href="#user-content-a-word-on" id="user-content-a-word-on"></a>

#### Mqtt5 vs Gravitee <a href="#user-content-mqtt5-vs-gravitee" id="user-content-mqtt5-vs-gravitee"></a>

Gravitee gateway acts as a protocol mediator and comes with an abstraction to provide the same experience for the api consumer whatever the backend technology used (mqtt5, kafka, …​).

Mqtt5 shared subscriptions are used internally to ensure multiple concurrent requests can be handled by the gateway. This comes with the following limitations:

* Latest retain message is not transmitted when subscribing because it is not supported when using shared subscriptions
* NoLocal Mqtt feature is not supported by shared subscriptions.
* Some Mqtt5 server implementation such as HiveMq are able to deliver messages received when a client was disconnected. Others such as Mosquitto aren’t.

#### Http polling <a href="#user-content-http-polling" id="user-content-http-polling"></a>

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
