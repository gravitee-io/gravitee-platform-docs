---
description: This article discusses the implementation details of v4 API endpoints
---

# Endpoint implementation

## Overview

Gravitee supports several different message brokers. This page describes the integrations Gravitee uses to enable Kafka, MQTT, RabbitMQ, and Solace endpoints for v4 API definitions. These rely on the following terminology and functionality:

* **Request-Id**: A Universally Unique Identifier (UUID) generated for any new request. This can be overridden using `X-Gravitee-Request-Id`as a Header or Query parameter.
* **Transaction-Id**: A UUID generated for any new request. This can be overridden using `X-Gravitee-Transaction-Id`as a Header or Query parameter.
* **Client-Identifier**: Inferred from the subscription attached to the request. It is either the subscription ID, or, with a Keyless plan, a hash of the remote address. The **Client-Identifier** can be provided by the client via the header `X-Gravitee-Client-Identifier`. In this case, the value used by Gravitee will be the original inferred value suffixed with the provided overridden value.

## Kafka

<details>

<summary>Subscribe</summary>

For each incoming request, a consumer is created and will persist until the request terminates. The Kafka endpoint retrieves information from the request to create a dedicated consumer characterized by:

**ConsumerGroup**

The consumer group is computed from the request's client identifier and is used to load-balance consumption. Kafka doesn't offer a way to manually create a consumer group; a consumer group can only be created through a new consumer instance. See the [Kafka documentation](https://docs.confluent.io/platform/current/clients/consumer.html#concepts) for more information.

**ClientId**

A client ID is generated for the consumer with the format `gio-apim-consumer-<first part of uuid>`, e.g., `gio-apim-consumer-a0eebc99`.

**Topics**

A topic is retrieved from the API configuration and can be overridden with the attribute `gravitee.attribute.kafka.topics`**.**

**AutoOffsetReset**

The `auto-offset-reset` of the API is managed at the endpoint level and cannot be overridden by request.

**Offset selection**

By default, the consumer that is created will either resume from where it left off or use the `auto-offset-reset` configuration to position itself at the beginning or end of the topic.&#x20;

Offsets are determined by partitions, which results in numerous possible mappings. Due to the inherent complexity of offset selection, Gravitee has introduced a mechanism to target a specific position on a Kafka topic.&#x20;

Given a compatible entrypoint (SSE, HTTP GET) and by using at-most-once or at-least-once QoS, it is possible to specify a last event ID. The format is encoded by default but follows the pattern:

```yaml
<topic1>@<partition11>#<offset11>,<partition12>#<offset12>;<topic2>@<partition21>#<offset21>,<partition22>#<offset22>...
```

For example, `my-topic@1#0,2#0`.

</details>

<details>

<summary>Publish</summary>

A shared producer is created by the endpoint and reused for all requests that have the same configuration. A shared producer is characterized by:

**ClientId**

The client ID of the producer is generated with the format `gio-apim-producer-<first part of uuid>`, e.g., `gio-apim-producer-a0eebc99`.

**Topics**

A topic is retrieved from the API configuration and can be overridden, either on the request for all messages or directly on the message, with the attribute `gravitee.attribute.kafka.topics`.

**Partitioning**

The only supported method for targeting a specific partition is to define a key and rely on the built-in partitioning mechanism. Kafka's default partitioner strategy uses the key to compute the associated partition: `hash(key) % nm of partition`.&#x20;

Repeated use of the same key on each message guarantees that messages are relegated to the same partition and order is maintained. Gravitee doesn't support overriding this mechanism to manually set the partition.&#x20;

To set a key on a message, the attribute `gravitee.attribute.kafka.recordKey` must be added to the message.

</details>

## MQTT



<details>

<summary>Common to Subscribe and Publish</summary>

On each incoming request, an MQTT client is created and will persist until the request is terminated. This behavior applies to both Subscribe and Publish modes, as does the following:

**MQTT Client Identifier**

The identifier for the MQTT Client is generated with the format `gio-apim-client-<first part of uuid>`, e.g., `gio-apim-client-a0eebc99`.

**Session Expiry Interval**

The default value is 86,400 seconds. If the value in the configuration is less than or equal to -1, no session expiry is set.

</details>

<details>

<summary>Subscribe</summary>

On each incoming request, the common client ([Common](https://gravitee.slab.com/posts/endpoints-implementation-details-65woom0y#hqy85-common)) is used to subscribe to a shared topic. The MQTT endpoint retrieves information from the request to configure the subscription. Subscription is characterized by:

**Shared subscription**

A shared subscription is created from the incoming request with the format `$share/<clientIdentifier>/<topic>`. This allows multiple clients using the same subscription to consume the same topic in parallel. In order to distinguish all clients using the same subscription, the client identifier must be overridden.

**Topic**

The topic is retrieved from the API configuration and can be overridden with the attribute `gravitee.attribute.mqtt5.topic`**.**

**QoS**

When the entrypoint supports manual ack, the strategy will use it. Otherwise, it will use auto-ack.

</details>

<details>

<summary>Publish</summary>

On each incoming request, the common client ([Common](https://gravitee.slab.com/posts/endpoints-implementation-details-65woom0y#hqy85-common)) is used to publish messages on a topic. This publication is done with MQTT at-least-once QoS, without expiration. Publication is characterized by:

**Topic**

The topic is retrieved from the API configuration and can be overridden, either on the request or the message, with the attribute `gravitee.attribute.mqtt5.topic`.

**Message Expiry Interval**

By default, there is no expiry. The value can be configured in the API definition.

</details>

## Solace

<details>

<summary>Common to Subscribe and Publish</summary>

On each incoming request, the endpoint searches an internal cache for an existing Solace messaging service for the API configuration. If not found, the endpoint will create a new one from the API configuration.

</details>

<details>

<summary>Subscribe</summary>

On each incoming request, the common messaging service ([Common](https://gravitee.slab.com/posts/endpoints-implementation-details-65woom0y#h3go9-common)) is used to create a dedicated message receiver. Subscription is characterized by:

### Message Receiver

The Solace endpoint consumes messages based on the QoS:

**None**

When the QoS is None, a Direct Message Receiver is created and a shared queue is named following the format `gravitee-gio-gateway-<clientIdentifier>`.

This allows multiple clients using the same subscription to consume the same topic in parallel. In order to distinguish all clients using the same subscription, the client identifier must be overridden.

**Auto / At least Once / At Most Once**

A Persistent Message Receiver is created to keep track of messages.

When the entrypoint supports manual ack, the endpoint will use it. Otherwise, the endpoint will use auto-ack for every message received in addition to a Durable Non Exclusive queue that follows the naming format `gravitee/gio-gateway/<clientIdentifier>`.

### Topic

The topic is retrieved from the API configuration and cannot be overridden via attributes.

</details>

### Subscribe





<details>

<summary>Publish</summary>



</details>

### Publish

As for subscribe mode, on each incoming request, the endpoint searches from an internal cache an existing Solace messaging service for the API configuration, otherwise, it will create a new one from the API configuration.

A Direct Message Publisher is created for the request with a backpressure reject mode limited to 10 messages.

#### Topic

The topic is retrieved from the API configuration, and cannot be overridden with attributes.

## RabbitMQ

### Subscribe

On each incoming request, a consumer is created and will live until the request ends.

The RabbitMQ endpoint retrieves information from the request to create a dedicated consumer:

#### Connection Name

The connection name of the consumer is generated and follows the format: `gio-apim-consumer-<first part of uuid>` for example `gio-apim-consumer-a0eebc99`

#### Exchange

The endpoint will declare the exchange with the option provided by the configuration at the API level. The exchange name can be overridden with the attribute `rabbitmq.exchange`**.**

If the exchange options provided are incompatible with the existing exchange found on Rabbit, the request will be interrupted with an error.

#### Queue

A queue will be created using the client identifier of the request following this format: `gravitee/gio-gateway/<clientIdentifier>`**.**

The created queue will have different options depending on the QoS applied on the entrypoint:

* None:
  * durable = false
  * autoDelete = true
* Auto
  * durable = true
  * autoDelete = false
* **Other not supported**

If the queue already exists, the messages would be load-balanced between both clients.

#### RoutingKey

In order to route the right messages to the queue, a routing key is used from the API configuration to create the binding between the exchange and the queue.

The routing key can be overridden with the attribute `rabbitmq.routingKey`

#### QoS

* None

Strategy applying a high throughput, low latency, no durability, and no reliability.

> The broker forgets about a message as soon as it has sent it to the consumer. Use this mode if downstream subscribers are very fast, at least faster than the flow of inbound messages. Messages will pile up in the JVM process memory if subscribers are not able to cope with the flow of messages, leading to out-of-memory errors. Note this mode uses the auto-acknowledgment mode when registering the RabbitMQ Consumer.

* Auto

Strategy balancing between performances and quality.

When the entrypoint supports manual ack, the strategy will use it. Otherwise, it will use auto ack coming from the RabbitMQ Reactor library:

> _With this mode, messages are acknowledged right after their arrival, in the Flux#doOnNext callback. This can help to cope with the flow of messages, avoiding the downstream subscribers to be overwhelmed. Note this mode does not use the auto-acknowledgment mode when registering the RabbitMQ Consumer. In this case, consumeAutoAck means messages are automatically acknowledged by the library in one the Flux hooks._

### Publish

A shared producer is created by the endpoint and reused for all requests matching the same configuration.

All messages of the request will be published in the exchange using the routing key. It is not possible to select an exchange or a routing key depending on the message attributes, only request attributes are supported.

#### Connection Name

The connection name of the consumer is generated and follows the format: `gio-apim-consumer-<first part of uuid>` for example `gio-apim-producer-a0eebc99`

#### Exchange

The endpoint will declare the exchange with the option provided by the configuration at the API level. The exchange name can be overridden with the attribute `rabbitmq.exchange`**.**

If the exchange options provided are incompatible with the existing exchange found on Rabbit, the request will be interrupted with an error.

#### RoutingKey

In order to route the right messages to the queue, A routing key is used from the API configuration and used to create the binding between the exchange and the queue.

The routing key can be overridden with the attribute `rabbitmq.routingKey.`
