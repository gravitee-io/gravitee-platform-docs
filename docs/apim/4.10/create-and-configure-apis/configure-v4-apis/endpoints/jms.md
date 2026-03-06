### Overview

The JMS Endpoint Plugin enables Gravitee APIM to connect to JMS-compliant message brokers as backend endpoints. It supports both producer (send) and consumer (receive) operations across multiple JMS providers including ActiveMQ Classic, ActiveMQ Artemis, IBM MQ, and Solace. This is an Enterprise feature requiring a valid license (pack: `apim-connectors-advanced`, feature ID: `apim-en-endpoint-jms`).

### Key Concepts

#### JMS API Versions

The plugin supports three JMS API versions: `V1_1` (JMS 1.1), `V2` (JMS 2.0), and `V3` (Jakarta JMS 3.0). The version must match the JMS provider library deployed at runtime. JMS 2.0+ enables asynchronous send operations with automatic fallback to synchronous send for older versions or providers that don't support async.

#### Connection Sharing

Connection behavior varies by destination type and configuration. Queue consumers always use a shared connection. Topic subscriptions use shared connections for non-durable topics without a client ID, but switch to exclusive connections when a client ID is provided or when durable subscriptions are enabled. For durable topics without an explicit client ID, the plugin auto-generates a UUID.

#### Provider Configuration Models

The plugin supports two configuration models: **provider-specific** (ActiveMQ Classic, ActiveMQ Artemis, IBM MQ, Solace) with dedicated properties, and **generic JNDI-based** for other JMS providers. Provider-specific configurations use direct connection factory instantiation, while the generic model performs JNDI lookups using a configurable properties file format.

### Prerequisites

Before configuring a JMS endpoint, ensure the following requirements are met:

* Gravitee APIM version 4.x or later
* Valid Enterprise license with `apim-connectors-advanced` pack
* JMS provider client libraries placed in `./plugins/jms/ext/` directory (not bundled with plugin)
* Network connectivity to target JMS broker
* Broker credentials (if authentication is required)

### Gateway Configuration

#### Endpoint Type

Set the endpoint `type` property to `jms` when configuring API endpoints.

#### Connection Factory Configuration

| Property | Description | Example |
|:---------|:------------|:--------|
| `connectionFactory.connectionFactoryClassName` | Fully qualified class name of the JMS ConnectionFactory (mandatory) | `org.apache.activemq.ActiveMQConnectionFactory` |
| `connectionFactory.apiVersion` | JMS API version: `V1_1`, `V2`, or `V3` (mandatory) | `V2` |

#### ActiveMQ Classic Provider

| Property | Description | Example |
|:---------|:------------|:--------|
| `connectionFactory.brokerUrl` | Connection URL with optional query parameters (mandatory) | `tcp://localhost:61616?property=value` |
| `connectionFactory.useCompression` | Enable message compression (default: `false`) | `true` |
| `connectionFactory.customProperties` | Additional key-value properties passed to the connection factory | `[{"key": "maxConnections", "value": "10"}]` |

#### ActiveMQ Artemis Provider

| Property | Description | Example |
|:---------|:------------|:--------|
| `connectionFactory.brokerUrl` | Connection URL with optional query parameters (mandatory) | `tcp://localhost:61616?property=value` |
| `connectionFactory.compressionLevel` | Compression level 0-9, higher = stronger compression (default: `0`) | `6` |

#### IBM MQ Provider

| Property | Description | Example |
|:---------|:------------|:--------|
| `connectionFactory.hostname` | Hostname or IP address of the MQ broker (mandatory) | `mq.example.com` |
| `connectionFactory.port` | Port number on which the MQ broker is listening (mandatory) | `1414` |
| `connectionFactory.channel` | MQ client channel name (mandatory) | `DEV.APP.SVRCONN` |
| `connectionFactory.queueManager` | Queue manager name (mandatory) | `QM1` |
| `connectionFactory.customProperties` | Additional key-value properties passed to the connection factory | `[{"key": "CCSID", "value": "1208"}]` |

#### Solace Provider

| Property | Description | Example |
|:---------|:------------|:--------|
| `connectionFactory.brokerUrl` | Connection URL (mandatory) | `smf://solace.example.com:55555` |
| `connectionFactory.messageVpn` | Solace Message VPN logical namespace (mandatory) | `default` |
| `connectionFactory.customProperties` | Additional key-value properties passed to the connection factory | `[{"key": "Solace_JMS_VPN", "value": "vpn1"}]` |

#### Generic Provider (JNDI)

| Property | Description | Example |
|:---------|:------------|:--------|
| `connectionFactory.jndiLookupName` | JNDI object name to look up (default: `ConnectionFactory`) | `jms/MyConnectionFactory` |
| `connectionFactory.jndiConfig` | JNDI properties in `jndi.properties` format (mandatory) | See JNDI Configuration Format below |
| `connectionFactory.customProperties` | Key-value pairs that override/append to JNDI configuration (supports EL) | `[{"key": "queue.MyQueue", "value": "example.MyQueue"}]` |

**JNDI Configuration Format:**

```properties
java.naming.factory.initial=org.apache.activemq.jndi.ActiveMQInitialContextFactory
java.naming.provider.url=tcp://localhost:61616
connectionFactoryNames=ConnectionFactory
queue.MyQueue=example.MyQueue
topic.MyTopic=example.MyTopic
```

#### Security Configuration

| Property | Description | Example |
|:---------|:------------|:--------|
| `sharedConfigurationOverride.security.auth.username` | Authentication username (supports EL and secrets) | `admin` or `{#secrets['jms.username']}` |
| `sharedConfigurationOverride.security.auth.password` | Authentication password (supports EL and secrets) | `{#secrets['jms.password']}` |

#### Producer Configuration

| Property | Description | Example |
|:---------|:------------|:--------|
| `sharedConfigurationOverride.producer.enabled` | Enable producer capability (default: `false`) | `true` |
| `sharedConfigurationOverride.producer.destinationType` | Destination type: `QUEUE` or `TOPIC` (mandatory if enabled) | `QUEUE` |
| `sharedConfigurationOverride.producer.destinationName` | Name of the queue or topic (mandatory if enabled) | `demo.queue` |
| `sharedConfigurationOverride.producer.targetMessageType` | Message type to produce: `TEXT` or `BYTES` (default: `TEXT`) | `TEXT` |
| `sharedConfigurationOverride.producer.messageIdPrefix` | Prefix to append to message IDs | `api-` |

#### Dynamic Configuration

All string properties support Expression Language (EL) expressions for runtime evaluation. Configuration can be overridden using context attributes set via the assign-attribute policy. Attribute keys must start with `gravitee.attributes.endpoint.jms` followed by the property path (e.g., `gravitee.attributes.endpoint.jms.producer.destinationName`).

### Creating a JMS Endpoint

1. Set the endpoint type to `jms` and select the appropriate provider (ActiveMQ Classic, Artemis, IBM MQ, Solace, or Generic).
2. Specify the `connectionFactoryClassName` and `apiVersion`.
3. Configure provider-specific properties such as `brokerUrl` for ActiveMQ or `hostname`, `port`, `channel`, and `queueManager` for IBM MQ.
4. Enable producer and/or consumer capabilities in `sharedConfigurationOverride` and specify destination type and name.
5. Add authentication credentials under `security.auth` if required.
6. Deploy the corresponding JMS provider client libraries to `./plugins/jms/ext/` before starting the gateway.

### Configuring Client ID for Topic Subscriptions

1. Set the context attribute `gravitee.attribute.jms.clientId` using the assign-attribute policy to provide an explicit client ID.
2. If no attribute is set, the plugin uses the request client identifier if available.
3. For durable subscriptions without an explicit client ID, the plugin auto-generates a UUID.

Non-durable topic subscriptions without a client ID use a shared connection, while all other scenarios (explicit client ID or durable subscription) use an exclusive connection.

### Restrictions

* Requires Gravitee APIM version 4.x or later
* Enterprise feature requiring valid license with `apim-connectors-advanced` pack (feature ID: `apim-en-endpoint-jms`)
* JMS provider client libraries must be manually deployed to `./plugins/jms/ext/` directory (not bundled)
* JNDI lookup names are validated against a protocol whitelist (`tcp`, `ssl`, `tls`, `smf`, `smfs`, `amqp`, `amqps`); disallowed protocols include `ldap`, `rmi`, `iiop`, `ldaps`, `dns`, `corba`, `nis`, `http`, `https`
* Durable subscriptions are only supported for topic destinations
* Asynchronous send requires JMS 2.0+ and provider support; older versions fall back to synchronous send
* Queue consumers always use shared connections regardless of client ID configuration
* 
