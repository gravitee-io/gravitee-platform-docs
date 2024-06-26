# Kafka

## Overview

This page discusses the [configuration](kafka.md#configuration) and [implementation](kafka.md#implementation) of the **Kafka** endpoint

## Configuration

The **Kafka** endpoint allows the Gateway to open up a persistent connection and/or call a backend Kafka broker via a Kafka client set up by the Gravitee Gateway. If you chose this endpoint, you will need to configure the settings in the following sections.

### 1. Role

You can tell the Gravitee Gateway's Kafka client to act as a producer, a consumer, or both a producer and consumer. Choose **Use Consumer**, **Use Producer**, or **Use Consumer and Producer** from the drop-down menu to do one of the following:

* **Use Producer:** Tells the Gateway Kafka client to be prepared to produce messages and send them to the Kafka broker that you define as your endpoint
* **Use Consumer:** Tells the Gateway Kafka client to be prepared to consume messages from the Kafka broker that you define as your endpoint
* **Use Producer and Consumer:** Tells the Gateway Kafka client to both **Use Producer** and **Use Consumer**

### **2. Bootstrap servers**

You must define a comma-separated list of host/port pairs to use for establishing the initial connection to the Kafka cluster. This list only pertains to the initial hosts used to discover the full set of servers. The client will make use of all servers irrespective of which servers the list designates for bootstrapping.&#x20;

### 3. Initial security settings

You will define more Gravitee Gateway-specific security settings later on, but this is where you define your Kafka-specific authentication flow. Gravitee supports **PLAINTEXT**, **SASL\_PLAINTEXT**, **SASL\_SSL**, and **SSL** protocols.

{% tabs %}
{% tab title="PLAINTEXT" %}
No further security configuration is necessary.
{% endtab %}

{% tab title="SASL" %}
Define the following:

1. **SASL mechanism:** Used for client connections. This will be GSSAPI, OAUTHBEARER, PLAIN, SCRAM\_SHA-256, or SCRAM-SHA-512.
2. **SASL JAAS Config:** The JAAS login context parameters for SASL connections in the format used by JAAS configuration files.
{% endtab %}

{% tab title="SSL" %}
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

### 4. Role settings

If you chose **Use Producer** or **Use Producer and Consumer**, you need to define the settings that the Gravitee Gateway Kafka client will rely on for producing messages to your backend Kafka topic/broker.&#x20;

If you chose **Use Consumer** or **Use Producer and Consumer**, you need to define the settings that the Gravitee Gateway Kafka client will rely on for consuming messages from your backend Kafka topic/broker.

{% tabs %}
{% tab title="Producer" %}
Define the following:

1. **Topics:** The topic that the broker uses to filter messages for each connected client.
2. **Compression type:** Choose the compression type for all data generated by the producer. The options are **none**, **gzip**, **snappy**, **lz4**, or **zstd**. Anything else will throw an exception to the consumer.
{% endtab %}

{% tab title="Consumer" %}
Define the following:

1. **Encode message Id:** Toggle this ON or OFF to encode message IDs in base64.
2. **Auto offset reset:** Use the **Auto offset reset** drop-down menu to configure what happens when there is no initial offset in Kafka, or if the current offset no longer exists on the server:
   * **Earliest:** Automatically reset the offset to the earliest offset.
   * **Latest:** Automatically reset the offset to the latest offset.
   * **None:** Throw an exception to the consumer if no previous offset is found for the consumer's group.
   * **Anything else:** Throw an exception to the consumer.
3. Choose **Specify List of Topics** or **Specify Topic Expression**:
   * **Specify List of Topics:** The topic(s) from which your Gravitee Gateway client will consume messages.
   * **Specify Topic Expression:** A single Java regular expression to consume only messages from Kafka topics that match the expression.
{% endtab %}
{% endtabs %}

## Implementation

### Common to subscribe and publish

Properties can be accessed from a Kafka cluster programmatically using [Gravitee Expression Language](../../../../gravitee-expression-language.md) (EL). To extract message metadata with EL, use the syntax `{#message.metadata.[]}`, e.g., `{#message.metadata.key}`. Supported attributes are `key`, `topic`, `partition`, and `offset`.

### Subscribe

For each incoming request, the Kafka endpoint retrieves information from the request to create a dedicated consumer that will persist until the request terminates. Subscription relies on **ConsumerGroup**, **ClientId**, **Topic**, **AutoOffsetReset**, and **Offset selection**.

{% tabs %}
{% tab title="ConsumerGroup" %}
The consumer group is computed from the request's client identifier and used to load-balance consumption. Kafka doesn't offer a way to manually create a consumer group; a consumer group can only be created through a new consumer instance. See the [Kafka documentation](https://docs.confluent.io/platform/current/clients/consumer.html#concepts) for more information.
{% endtab %}

{% tab title="ClientId" %}
A client ID is generated for the consumer per the format `gio-apim-consumer-<first part of uuid>`, e.g., `gio-apim-consumer-a0eebc99`.
{% endtab %}

{% tab title="Topic" %}
A topic is retrieved from the API configuration and can be overridden with the attribute `gravitee.attribute.kafka.topics`**.**
{% endtab %}

{% tab title="AutoOffsetReset" %}
The `auto-offset-reset` of the API is managed at the endpoint level and cannot be overridden by request.
{% endtab %}

{% tab title="Offset selection" %}
By default, the consumer that is created will either resume from where it left off or use the `auto-offset-reset` configuration to position itself at the beginning or end of the topic.&#x20;

Offsets are determined by partitions, resulting in numerous possible mappings. To mitigate the inherent complexity of offset selection, Gravitee has introduced a mechanism to target a specific position on a Kafka topic.&#x20;

Given a compatible entrypoint (SSE, HTTP GET), and by using At-Most-Once or At-Least-Once QoS, it is possible to specify a last event ID. The format is encoded by default and follows the pattern:

```yaml
<topic1>@<partition11>#<offset11>,<partition12>#<offset12>;<topic2>@<partition21>#<offset21>,<partition22>#<offset22>...
```

For example, `my-topic@1#0,2#0`.
{% endtab %}
{% endtabs %}

### Publish

A shared producer is created by the endpoint and reused for all requests with that same configuration. Publication relies on **ClientId**, **Topic**, and **Partitioning**.

{% tabs %}
{% tab title="ClientId" %}
The client ID is generated for the producer per the format `gio-apim-producer-<first part of uuid>`, e.g., `gio-apim-producer-a0eebc99`.
{% endtab %}

{% tab title="Topic" %}
A topic is retrieved from the API configuration and can be overridden, either on the request for all messages or directly on the message, with the attribute `gravitee.attribute.kafka.topics`.
{% endtab %}

{% tab title="Partitioning" %}
The only supported method for targeting a specific partition is to define a key and rely on the built-in partitioning mechanism. Kafka's default partitioner strategy uses the key to compute the associated partition: `hash(key) % nm of partition`.&#x20;

Repeated use of the same key on each message guarantees that messages are relegated to the same partition and order is maintained. Gravitee doesn't support overriding this mechanism to manually set the partition.&#x20;

To set a key on a message, the attribute `gravitee.attribute.kafka.recordKey` must be added to the message.
{% endtab %}
{% endtabs %}
