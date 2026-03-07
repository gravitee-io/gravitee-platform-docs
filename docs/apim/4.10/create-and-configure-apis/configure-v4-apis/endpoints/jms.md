### Overview

The JMS endpoint connector enables Gravitee API Management to integrate with JMS-compliant message brokers as backend systems. It supports both producer (publish) and consumer (subscribe) operations across multiple JMS providers including ActiveMQ Classic, ActiveMQ Artemis, IBM MQ, and Solace. The connector supports JMS 1.1, 2.x, and 3.x (Jakarta) specifications.

{% hint style="warning" %}
The JMS endpoint connector is an Enterprise feature that requires the `apim-connectors-advanced` license pack.
{% endhint %}

### Key concepts

#### Destination types

JMS endpoints support two messaging patterns:

* **Queue**: Point-to-point messaging where each message is consumed by exactly one receiver.
* **Topic**: Publish-subscribe messaging where messages are broadcast to multiple subscribers. Durable subscriptions on topics persist messages for offline subscribers.

#### Quality of Service

The connector adapts message delivery guarantees based on QoS requirements:

| QoS Level | Delivery Guarantee | Acknowledgment Mode |
|:----------|:-------------------|:--------------------|
| None | Best effort | `DUPS_OK_ACKNOWLEDGE` |
| Auto | Adaptive | Based on requirements |
| At-Most-Once | 0 or 1 delivery | `AUTO_ACKNOWLEDGE` |
| At-Least-Once | 1 or more deliveries | `DUPS_OK_ACKNOWLEDGE` |

#### Connection sharing

Queue consumers always use shared connections. Topic consumers use shared or exclusive connections based on client ID and durability settings:

| Scenario | Connection Type |
|:---------|:----------------|
| Non-durable topic, no client ID | Shared connection |
| Non-durable topic, client ID provided | Exclusive connection |
| Durable topic, no client ID | Exclusive connection (UUID auto-generated) |
| Durable topic, client ID provided | Exclusive connection |

Client ID resolution follows this order:

1. Context attribute `gravitee.attribute.jms.clientId` (if set via policy)
2. Request client identifier (if available)

{% hint style="info" %}
The client ID attribute only affects topic destinations. Queue consumers always use shared connections.
{% endhint %}

### Prerequisites

Before configuring a JMS endpoint, ensure the following requirements are met:

* Gravitee APIM 4.x or later
* JMS provider client library placed in `{APIM_HOME}/plugins/jms/ext/`
* Network connectivity to the target message broker
* Valid credentials if broker requires authentication
* License feature `apim-en-endpoint-jms` (included in `apim-connectors-advanced` pack)

### Gateway configuration

#### Connection factory configuration

Configure the JMS connection factory using properties under the `gravitee.attributes.endpoint.jms` prefix:

| Property | Description | Example |
|:---------|:------------|:--------|
| `connectionFactoryClassName` | Fully qualified class name of the JMS ConnectionFactory (mandatory) | `org.apache.activemq.ActiveMQConnectionFactory` |
| `apiVersion` | JMS API version: `V1_1`, `V2`, or `V3` (mandatory) | `V2` |
| `brokerUrl` | Connection URL with optional query parameters | `tcp://localhost:61616?property=value` |
| `hostname` | Hostname or IP address of the MQ broker | `broker.example.com` |
| `port` | Port number on which the broker is listening | `61616` |
| `channel` | MQ client channel name | `DEV.APP.SVRCONN` |
| `queueManager` | Queue manager name | `QM1` |
| `messageVpn` | Solace Message VPN (logical namespace) | `default` |
| `useCompression` | Enable message compression (default: `false`) | `true` |
| `compressionLevel` | Compression level 0-9, higher = stronger (default: `0`) | `6` |
| `jndiLookupName` | JNDI object name to look up (default: `"ConnectionFactory"`) | `jms/ConnectionFactory` |
| `jndiConfig` | JNDI properties in `jndi.properties` format | `java.naming.factory.initial=...` |
| `customProperties` | Additional key-value pairs (supports EL) | `[{key: "property", value: "value"}]` |

#### Producer configuration

Enable and configure message publishing:

| Property | Description | Example |
|:---------|:------------|:--------|
| `producer.enabled` | Enable producer capability (default: `false`) | `true` |
| `producer.destinationType` | `QUEUE` or `TOPIC` (mandatory if enabled) | `QUEUE` |
| `producer.destinationName` | Name of the queue or topic (mandatory if enabled) | `orders.incoming` |
| `producer.targetMessageType` | `TEXT` or `BYTES` (default: `TEXT`) | `TEXT` |
| `producer.messageIdPrefix` | Prefix to append to message IDs | `api-` |

#### Consumer configuration

Enable and configure message consumption:

| Property | Description | Example |
|:---------|:------------|:--------|
| `consumer.enabled` | Enable consumer capability (default: `false`) | `true` |
| `consumer.destinationType` | `QUEUE` or `TOPIC` (mandatory if enabled) | `TOPIC` |
| `consumer.destinationName` | Name of the queue or topic (mandatory if enabled) | `events.notifications` |
| `consumer.durableSubscription` | Enable durable subscription for topics (default: `false`) | `true` |
| `consumer.messageIdPrefix` | Prefix to strip from received message IDs | `api-` |

#### Security configuration

Configure authentication credentials:

| Property | Description | Example |
|:---------|:------------|:--------|
| `security.auth.username` | Authentication username (supports EL and secrets) | `{#secrets['jms.username']}` |
| `security.auth.password` | Authentication password (supports EL and secrets) | `{#secrets['jms.password']}` |

### Creating a JMS endpoint

To create a JMS endpoint:

1. Install the JMS provider client library in `{APIM_HOME}/plugins/jms/ext/`.
2. Configure the endpoint type as `jms` in your API definition.
3. Set the mandatory `connectionFactoryClassName` and `apiVersion` properties.
4. Configure connection details using either `brokerUrl` or provider-specific properties (`hostname`, `port`, `channel`, `queueManager`, `messageVpn`).
5. Enable and configure `producer` or `consumer` capabilities with destination type and name.

Optionally, configure authentication credentials under `security.auth`. The endpoint will establish connections based on the destination type and client ID settings described in Key Concepts.

### Configuring JNDI lookup

For brokers requiring JNDI-based connection factory lookup:

1. Set `jndiLookupName` to the JNDI object name (default is `"ConnectionFactory"`).
2. Provide JNDI configuration via `jndiConfig` in `jndi.properties` format.
3. Ensure the lookup name uses allowed protocols (`tcp`, `ssl`, `tls`, `smf`, `smfs`, `amqp`, `amqps`) or is a simple JNDI name without protocol prefix.

{% hint style="danger" %}
The connector rejects lookup names containing disallowed protocols (`ldap`, `rmi`, `iiop`, `http`, `https`, `dns`, `corba`, `nis`) for security reasons.
{% endhint %}

### Restrictions

* Plugin version 1.x requires Gravitee APIM 4.x or later
* JMS provider client libraries are not bundled and must be installed separately in `{APIM_HOME}/plugins/jms/ext/`
* Durable subscriptions are only supported for `TOPIC` destinations
* Client ID attribute (`gravitee.attribute.jms.clientId`) only affects topic destinations; queue consumers always use shared connections
* JNDI lookup names must use whitelisted protocols or be simple names without protocol prefixes
* Authentication credentials support Expression Language (EL) and secrets but must be configured at endpoint level
* Compression level valid range is 0-9; values outside this range may cause errors
* Feature requires license pack `apim-connectors-advanced`

### Supported JMS providers

| Provider | JMS 2.x Class Name | JMS 3.x (Jakarta) Class Name |
|:---------|:-------------------|:-----------------------------|
| ActiveMQ Classic | `org.apache.activemq.ActiveMQConnectionFactory` | `org.apache.activemq.ActiveMQConnectionFactory` |
| ActiveMQ Artemis | `org.apache.activemq.artemis.jms.client.ActiveMQConnectionFactory` | `org.apache.activemq.artemis.jms.client.ActiveMQConnectionFactory` |
| IBM MQ | `com.ibm.mq.jms.MQConnectionFactory` | `com.ibm.mq.jakarta.jms.MQConnectionFactory` |
| Solace | `com.solacesystems.jms.SolConnectionFactory` | Not supported |
