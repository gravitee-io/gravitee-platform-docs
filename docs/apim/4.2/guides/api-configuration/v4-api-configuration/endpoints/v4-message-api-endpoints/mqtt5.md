---
description: An overview about MQTT5.
---

# MQTT5

## Overview

This page discusses the [configuration](mqtt5.md#configuration) and [implementation](mqtt5.md#implementation) of the **MQTT5** endpoint

## Configuration

The **MQTT5** endpoint allows the Gateway to open up a persistent connection to and/or call a backend MQTT broker, as long as that broker is running on MQTT 5.x via an MQTT client set up by the Gravitee Gateway. If you chose this endpoint, you will need to configure the settings in the following sections.

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

You will define more Gravitee Gateway-specific security settings later on, but this is where you define your MQTT-specific authentication flow. Gravitee supports **Authentication**, **SSL**, and **Authentication with SSL**.

{% tabs %}
{% tab title="Authentication" %}
Gravitee uses TLS to support the **Username** and **Password** you define.
{% endtab %}

{% tab title="SSL" %}
**Hostname verifier:** Toggle to enable or disable hostname verification.

Define whichever of the following are relevant to your configuration.

**Truststore**

* **PEM with location:** Define the **location of your truststore file**.
* **PEM with certificates:** Define the trusted certificates in the format specified by 'ssl.truststore.type'.
* **JKS with location:** Define the **location of your truststore file** and the **SSL truststore password** for the truststore file.
* **JKS with certificates:** Define the trusted certificates in the format specified by 'ssl.truststore.type' and the **SSL truststore password** for the truststore file.
* **PKCS12 with location:** Define the **location of your truststore file** and the **SSL truststore password** for the truststore file.
* **PKCS12 with certificates:** Define the **trusted certificates** in the format specified by 'ssl.truststore.type' and the **SSL truststore password** for the truststore file.

**Keystore**

* **PEM with location:** Define the **SSL keystore certificate chain** and the location of your keystore file.
* **PEM with Key:** Define the **SSL keystore certificate chain** and the **SSL keystore private key** by defining the **Key** and the **Key password**.
* **JKS with location:** Define the **location of your keystore file** and the **SSL keystore password** for the keystore file.
* **JKS with Key:** Define the **SSL keystore private key** by defining the **Key** and the **Key password** and the **SSL keystore password** for the keystore file.
* **PKCS12 with location:** Define the **location of your keystore file** and the **SSL keystore password** for the keystore file.
* **PKCS12 with Key:** Define the **SSL keystore private key** by defining the **Key** and the **Key password** and the **SSL keystore password** for the keystore file.
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
Define the **Topic** from which the Gateway MQTT client will consume messages. **Topic** refers to an UTF-8 string that the broker uses to filter messages for each connected client and consists of one or more topic levels.
{% endtab %}
{% endtabs %}

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
