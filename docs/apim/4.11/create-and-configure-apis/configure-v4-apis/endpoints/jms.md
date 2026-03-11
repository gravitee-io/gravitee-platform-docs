---
description: An overview about JMS.
metaLinks:
  alternates:
    - jms.md
---

# JMS

## Overview

This page discusses the [configuration](jms.md#configuration) and [implementation](jms.md#implementation) of the **JMS** endpoint and includes a [reference](jms.md#reference) section.

## Configuration

The **JMS** endpoint allows the Gravitee Gateway to produce and consume messages from JMS-compliant message brokers using web-friendly protocols such as HTTP or WebSocket. The Gateway mediates the protocol between the client and the backend. It supports both queue (point-to-point) and topic (publish-subscribe) messaging patterns.

{% hint style="warning" %}
The JMS endpoint plugin does not bundle JMS provider client libraries. Place the required JMS provider library in `./plugins/jms/ext/` at runtime.
{% endhint %}

### 1. Initial settings

Configure the connection factory to establish the connection to the JMS broker:

1. **Connection factory class name:** Enter the fully qualified class name of the JMS `ConnectionFactory` (for example, `org.apache.activemq.ActiveMQConnectionFactory`).
2. **JMS API version:** Select the JMS specification version:
   * `V1_1` — Legacy `javax.jms` support
   * `V2` — Enhanced `javax.jms` with async send
   * `V3` — Latest `jakarta.jms` specification
3. **Connection details:** Provide the connection details using one of these methods:

{% tabs %}
{% tab title="Direct broker URL" %}
Enter the broker URL directly (for example, `tcp://localhost:61616`).
{% endtab %}

{% tab title="Provider-specific properties" %}
Configure provider-specific properties such as hostname, port, channel, queue manager, or message VPN. The required properties depend on your JMS provider. For details, see the [supported providers](jms.md#supported-jms-providers) reference section.
{% endtab %}

{% tab title="JNDI lookup" %}
Use JNDI to retrieve the connection factory. Provide the following:

1. **JNDI lookup name:** The JNDI object name to look up (defaults to `ConnectionFactory`).
2. **JNDI configuration:** JNDI properties in `jndi.properties` format. For example:

```properties
java.naming.factory.initial=org.apache.activemq.jndi.ActiveMQInitialContextFactory
java.naming.provider.url=tcp://localhost:61616
connectionFactoryNames=ConnectionFactory
queue.MyQueue=example.MyQueue
topic.MyTopic=example.MyTopic
```

3. **Custom properties:** Optional key-value pairs that override or append to the JNDI configuration. Supports EL expressions.
{% endtab %}
{% endtabs %}

### 2. Role

Tell the Gravitee Gateway's JMS client to act as a producer, a consumer, or both a producer and consumer. Choose **Use Consumer**, **Use Producer**, or **Use Consumer and Producer** from the drop-down menu to do one of the following:

* **Use Producer:** Tells the Gateway JMS client to be prepared to produce messages and send them to the JMS broker that you define as your endpoint
* **Use Consumer:** Tells the Gateway JMS client to be prepared to consume messages from the JMS broker that you define as your endpoint
* **Use Producer and Consumer:** Tells the Gateway JMS client to both **Use Producer** and **Use Consumer**

### 3. Initial security settings

Enter the username and password for JMS broker authentication. Both fields support EL expressions and Gravitee secrets (for example, `{#secrets['jms-password']}`).

### 4. Role settings

If you chose **Use Producer** or **Use Producer and Consumer**, define the settings that the Gravitee Gateway JMS client relies on for producing messages to your backend JMS broker.

If you chose **Use Consumer** or **Use Producer and Consumer**, define the settings that the Gravitee Gateway JMS client relies on for consuming messages from your backend JMS broker.

{% tabs %}
{% tab title="Producer" %}
Define the following:

1. **Destination type:** Select `queue` or `topic`.
2. **Destination name:** Enter the name of the queue or topic.
3. **Target message type:** Select `TEXT` or `BYTES` (defaults to `TEXT`).
4. **Message ID prefix:** Optional. Enter a prefix to append to message IDs.
{% endtab %}

{% tab title="Consumer" %}
Define the following:

1. **Destination type:** Select `queue` or `topic`.
2. **Destination name:** Enter the name of the queue or topic.
3. **Durable subscription:** Enable durable subscription for topic destinations. This setting only applies to topics.
4. **Message ID prefix:** Optional. Enter a prefix to strip from received message IDs.
{% endtab %}
{% endtabs %}

## Implementation

### Topic client ID resolution

Topic consumers use either shared or exclusive connections based on client ID and durability settings:

| Scenario                              | Connection type                          |
| ------------------------------------- | ---------------------------------------- |
| Non-durable topic, no client ID       | Shared connection                        |
| Non-durable topic, client ID provided | Exclusive connection                     |
| Durable topic, no client ID           | Exclusive connection (UUID auto-generated) |
| Durable topic, client ID provided     | Exclusive connection                     |

The client ID is resolved from the context attribute `gravitee.attribute.jms.clientId` (if set via policy) or the request client identifier. Queue consumers always use shared connections regardless of client ID.

### Dynamic configuration

All string properties support EL expressions for dynamic configuration. For example:

```json
{
  "consumer": {
    "destinationName": "{#request.headers['destination'][0]}"
  }
}
```

Override configuration using context attributes (via the assign-attribute policy). Attributes use the prefix `gravitee.attributes.endpoint.jms` followed by the property path (for example, `gravitee.attributes.endpoint.jms.consumer.destinationName`).

## Reference

Refer to the following sections for additional details.

### Compatibility matrix

| Plugin version | APIM version  |
| -------------- | ------------- |
| 1.x            | 4.10.x to latest |

### Endpoint identifier

To use this plugin, declare the `jms` identifier when configuring your API endpoints.

### Supported JMS providers

| Provider         | JMS 2.x class name                                                | JMS 3.x class name                                                |
| ---------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------ |
| ActiveMQ Classic | `org.apache.activemq.ActiveMQConnectionFactory`                    | `org.apache.activemq.ActiveMQConnectionFactory`                    |
| ActiveMQ Artemis | `org.apache.activemq.artemis.jms.client.ActiveMQConnectionFactory` | `org.apache.activemq.artemis.jms.client.ActiveMQConnectionFactory` |
| IBM MQ           | `com.ibm.mq.jms.MQConnectionFactory`                               | `com.ibm.mq.jakarta.jms.MQConnectionFactory`                       |
| Solace           | `com.solacesystems.jms.SolConnectionFactory`                       | N/A                                                                |

### Endpoint configuration

#### Connection factory configuration

| Property | Description | Default | Required |
| -------- | ----------- | ------- | -------- |
| `connectionFactoryClassName` | Fully qualified class name of the JMS `ConnectionFactory` | N/A | Yes |
| `apiVersion` | JMS API version: `V1_1`, `V2`, or `V3` | N/A | Yes |
| `brokerUrl` | Connection URL with optional query parameters | N/A | No |
| `hostname` | Hostname or IP address of the MQ broker | N/A | No |
| `port` | Port number on which the MQ broker is listening | N/A | No |
| `channel` | MQ client channel name | N/A | No |
| `queueManager` | Queue manager name | N/A | No |
| `messageVpn` | Solace Message VPN | N/A | No |
| `useCompression` | Enable message compression | `false` | No |
| `compressionLevel` | Compression level (0-9, higher = stronger) | `0` | No |
| `jndiLookupName` | JNDI object name to look up | `ConnectionFactory` | No |
| `jndiConfig` | JNDI properties in `jndi.properties` format | N/A | No |
| `customProperties` | Additional key-value properties passed to the connection factory | `[]` | No |

#### Producer configuration

| Property | Description | Default | Required |
| -------- | ----------- | ------- | -------- |
| `producer.enabled` | Enable producer capability | `false` | No |
| `producer.destinationType` | Destination type: `queue` or `topic` | N/A | Yes (if enabled) |
| `producer.destinationName` | Name of the queue or topic | N/A | Yes (if enabled) |
| `producer.targetMessageType` | Message type: `TEXT` or `BYTES` | `TEXT` | No |
| `producer.messageIdPrefix` | Prefix to append to message IDs | N/A | No |

#### Consumer configuration

| Property | Description | Default | Required |
| -------- | ----------- | ------- | -------- |
| `consumer.enabled` | Enable consumer capability | `false` | No |
| `consumer.destinationType` | Destination type: `queue` or `topic` | N/A | Yes (if enabled) |
| `consumer.destinationName` | Name of the queue or topic | N/A | Yes (if enabled) |
| `consumer.durableSubscription` | Enable durable subscription (topics only) | `false` | No |
| `consumer.messageIdPrefix` | Prefix to strip from received message IDs | N/A | No |

#### Security configuration

| Property | Description | Default | Required |
| -------- | ----------- | ------- | -------- |
| `security.auth.username` | Authentication username (supports EL and secrets) | N/A | No |
| `security.auth.password` | Authentication password (supports EL and secrets) | N/A | No |

### JNDI lookup protocol restrictions

The JNDI lookup name is validated against the following allowed protocols: `tcp`, `ssl`, `tls`, `smf`, `smfs`, `amqp`, `amqps`.

Disallowed protocols (`ldap`, `rmi`, `iiop`, `http`, `https`, `dns`, `corba`, `nis`) trigger validation errors.

### Restrictions

* JMS provider client libraries are not bundled and must be placed in `./plugins/jms/ext/` at runtime
* JNDI lookup names are restricted to the protocols listed above
* Durable subscriptions are only supported for topic destinations
* The client ID attribute (`gravitee.attribute.jms.clientId`) is only used for topic destinations; queue consumers always use shared connections
* Compression level accepts values between 0 and 9
