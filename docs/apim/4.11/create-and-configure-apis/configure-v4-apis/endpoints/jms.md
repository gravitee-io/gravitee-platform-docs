### Overview

The JMS endpoint connector enables Gravitee APIM to produce and consume messages from JMS-compliant message brokers. It supports both queue (point-to-point) and topic (publish-subscribe) messaging patterns with configurable authentication, compression, and JNDI lookup. This feature is part of the `apim-connectors-advanced` license pack and was introduced in gravitee-node versions 7.26.0 and 8.0.0-alpha.11.

### Prerequisites

Before configuring a JMS endpoint, ensure the following requirements are met:

* Gravitee APIM version 4.x or later
* Valid license for `apim-connectors-advanced` pack (includes `apim-en-endpoint-jms` feature)
* JMS provider client library placed in `./plugins/jms/ext/` directory at runtime
* Network connectivity to the target JMS broker

{% hint style="warning" %}
The JMS endpoint plugin does not bundle JMS provider client libraries. You must place the required JMS provider library in `./plugins/jms/ext/` at runtime.
{% endhint %}

### Connection Factory Configuration

The connection factory establishes the connection to the JMS broker. Three configuration methods are supported:

* **Direct broker URL:** Specify the connection URL directly (e.g., `tcp://localhost:61616`)
* **Provider-specific properties:** Configure hostname, port, channel, queue manager, or message VPN
* **JNDI lookup:** Use JNDI to retrieve the connection factory with custom properties

The `apiVersion` property determines the JMS specification version:

* `V1_1`: Legacy `javax.jms` support
* `V2`: Enhanced `javax.jms` with async send
* `V3`: Latest `jakarta.jms` specification

#### Connection Factory Properties

| Property | Description | Example |
|:---------|:------------|:--------|
| `connectionFactory.connectionFactoryClassName` | Fully qualified class name of the JMS ConnectionFactory | `org.apache.activemq.ActiveMQConnectionFactory` |
| `connectionFactory.apiVersion` | JMS API version: `V1_1`, `V2`, or `V3` | `V2` |
| `connectionFactory.brokerUrl` | Connection URL with optional query parameters | `tcp://localhost:61616?property=value` |
| `connectionFactory.hostname` | Hostname or IP address of the MQ broker | `broker.example.com` |
| `connectionFactory.port` | Port number on which the MQ broker is listening | `61616` |
| `connectionFactory.channel` | MQ client channel name | `DEV.APP.SVRCONN` |
| `connectionFactory.queueManager` | Queue manager name | `QM1` |
| `connectionFactory.messageVpn` | Solace Message VPN (logical namespace) | `default` |
| `connectionFactory.useCompression` | Enable message compression | `false` |
| `connectionFactory.compressionLevel` | Compression level (0-9, higher = stronger) | `0` |
| `connectionFactory.jndiLookupName` | JNDI object name to look up | `ConnectionFactory` |
| `connectionFactory.jndiConfig` | JNDI properties in `jndi.properties` format | See JNDI example below |
| `connectionFactory.customProperties` | Additional key-value properties passed to the connection factory | `[{"key": "timeout", "value": "5000"}]` |

All configuration properties use the attribute prefix `gravitee.attributes.endpoint.jms`.

### Producer Configuration

Producer mode sends messages to a destination with configurable message type and optional message ID prefix.

| Property | Description | Example |
|:---------|:------------|:--------|
| `producer.enabled` | Enable producer capability | `true` |
| `producer.destinationType` | Destination type: `QUEUE` or `TOPIC` | `QUEUE` |
| `producer.destinationName` | Name of the queue or topic | `demo.queue` |
| `producer.targetMessageType` | Message type: `TEXT` or `BYTES` | `TEXT` |
| `producer.messageIdPrefix` | Prefix to append to message IDs | `api-` |

### Consumer Configuration

Consumer mode receives messages from a destination with support for durable subscriptions on topics and message ID prefix stripping.

| Property | Description | Example |
|:---------|:------------|:--------|
| `consumer.enabled` | Enable consumer capability | `true` |
| `consumer.destinationType` | Destination type: `QUEUE` or `TOPIC` | `TOPIC` |
| `consumer.destinationName` | Name of the queue or topic | `demo.topic` |
| `consumer.durableSubscription` | Enable durable subscription (topics only) | `false` |
| `consumer.messageIdPrefix` | Prefix to strip from received message IDs | `api-` |

### Security Configuration

| Property | Description | Example |
|:---------|:------------|:--------|
| `security.auth.username` | Authentication username (supports EL and secrets) | `admin` |
| `security.auth.password` | Authentication password (supports EL and secrets) | `{#secrets['jms-password']}` |

### Topic Client ID Resolution

Topic consumers use either shared or exclusive connections based on client ID and durability settings:

| Scenario | Connection Type |
|:---------|:----------------|
| Non-durable topic, no client ID | Shared connection |
| Non-durable topic, client ID provided | Exclusive connection |
| Durable topic, no client ID | Exclusive connection (UUID auto-generated) |
| Durable topic, client ID provided | Exclusive connection |

Client ID is resolved from the context attribute `gravitee.attribute.jms.clientId` (if set via policy) or the request client identifier. Queue consumers always use shared connections regardless of client ID.

### Creating a JMS Endpoint

Configure a JMS endpoint in the API definition by specifying the endpoint type as `jms` and providing connection factory details.

1. Set the `connectionFactoryClassName` to match your JMS provider (e.g., `org.apache.activemq.ActiveMQConnectionFactory` for ActiveMQ Classic).
2. Choose the appropriate `apiVersion` (`V2` for `javax.jms` or `V3` for `jakarta.jms`).
3. Provide connection details via `brokerUrl` or provider-specific properties (hostname, port, channel, queueManager).
4. Enable producer or consumer capabilities in `sharedConfigurationOverride` with the destination type and name.
5. Add authentication credentials under `security.auth` if required.

All string properties support EL expressions for dynamic configuration (e.g., `{#request.headers['destination'][0]}`).

#### Example: Produce Messages to Queue

#### Example: Consume Messages from Topic

### Configuring JNDI Lookup

To use JNDI for connection factory lookup, provide the JNDI configuration in `jndi.properties` format under `connectionFactory.jndiConfig`.

1. Specify the initial context factory class (e.g., `org.apache.activemq.jndi.ActiveMQInitialContextFactory`).
2. Set the provider URL to the broker connection string.
3. Define the connection factory name in `connectionFactoryNames`.
4. Optionally map queue and topic names using `queue.` and `topic.` prefixes.
5. Set `jndiLookupName` to the object name to retrieve (defaults to `ConnectionFactory`).

#### JNDI Configuration Format

```properties
java.naming.factory.initial=org.apache.activemq.jndi.ActiveMQInitialContextFactory
java.naming.provider.url=tcp://localhost:61616
connectionFactoryNames=ConnectionFactory
queue.MyQueue=example.MyQueue
topic.MyTopic=example.MyTopic
```

#### JNDI Lookup Protocol Restrictions

The JNDI lookup name is validated against allowed protocols: `tcp`, `ssl`, `tls`, `smf`, `smfs`, `amqp`, `amqps`.

Disallowed protocols (`ldap`, `rmi`, `iiop`, `http`, `https`, `dns`, `corba`, `nis`) will trigger validation errors:

* `"JNDI lookup name cannot be null or blank"` — when lookup name is null, empty, or whitespace
* `"JNDI lookup name contains disallowed protocol: {lookupName}"` — when protocol is not whitelisted

### Supported JMS Providers

| Provider | JMS 2.x Class Name | JMS 3.x Class Name |
|:---------|:-------------------|:-------------------|
| ActiveMQ Classic | `org.apache.activemq.ActiveMQConnectionFactory` | `org.apache.activemq.ActiveMQConnectionFactory` |
| ActiveMQ Artemis | `org.apache.activemq.artemis.jms.client.ActiveMQConnectionFactory` | `org.apache.activemq.artemis.jms.client.ActiveMQConnectionFactory` |
| IBM MQ | `com.ibm.mq.jms.MQConnectionFactory` | `com.ibm.mq.jakarta.jms.MQConnectionFactory` |
| Solace | `com.solacesystems.jms.SolConnectionFactory` | N/A |

### Restrictions

* Plugin version 1.x requires Gravitee APIM 4.x or later
* JMS provider client libraries are not bundled and must be placed in `./plugins/jms/ext/` at runtime
* JNDI lookup names are restricted to protocols: `tcp`, `ssl`, `tls`, `smf`, `smfs`, `amqp`, `amqps`
* Durable subscriptions are only supported for topic destinations
* Client ID attribute (`gravitee.attribute.jms.clientId`) is only used for topic destinations; queue consumers always use shared connections
* Compression level must be between 0 and 9
