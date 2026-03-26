---
description: An overview about RabbitMQ.
---

# RabbitMQ

## Overview

This article details the [configuration](rabbitmq.md#configuration) and [implementation](rabbitmq.md#implementation) of the **RabbitMQ** endpoint.

## Configuration

The **RabbitMQ** endpoint allows the Gateway to open up a persistent connection and/or call a backend RabbitMQ resource, as long as that RabbitMQ resource communicates over AMQP 0-9-1 protocol. If you choose this endpoint, you will need to configure the settings in the following sections.

### 1. Initial settings

1. **Server host:** Define the host of your RabbitMQ resource.
2. **Server port:** Define the port that RabbitMQ is using.
3. **Virtual host:** Define the virtual host to use.

### 2. Role

You can tell the Gravitee Gateway's RabbitMQ client to act as a producer, a consumer, or both a producer and consumer. Choose **Use Consumer**, **Use Producer**, or **Use Consumer and Producer** from the drop-down menu to do one of the following:

* **Use Producer:** Tells the Gateway RabbitMQ client to be prepared to produce messages and send them to the RabbitMQ broker that you define as your endpoint
* **Use Consumer:** Tells the Gateway RabbitMQ client to be prepared to consume messages from the RabbitMQ broker that you define as your endpoint
* **Use Producer and Consumer:** Tells the Gateway RabbitMQ client to both **Use Producer** and **Use Consumer**

### 3. Initial security settings

You will define more Gravitee Gateway-specific security settings later on, but this is where you define your RabbitMQ-specific authentication flow. Gravitee supports **Authentication with SSL**.

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

### 4. Role settings

If you chose **Use Producer** or **Use Producer and Consumer**, you must define the settings that the Gravitee Gateway RabbitMQ client will rely on for producing messages to your backend RabbitMQ topic/broker.

If you chose **Use Consumer** or **Use Producer and Consumer**, you must define the settings that the Gravitee Gateway RabbitMQ client will rely on for consuming messages from your backend RabbitMQ topic/broker.

{% tabs %}
{% tab title="Producer" %}
Define the following:

1. **Exchange name**
2. **Exchange type**
3. Enable or disable [**Durable**](https://www.rabbitmq.com/tutorials/amqp-concepts.html#exchanges)**:** Durable exchanges survive broker restart.
4. Enable or disable [**Auto Delete**](https://www.rabbitmq.com/tutorials/amqp-concepts.html#exchanges)**:** Deletes the exchange when last queue is unbound from it.
5. **Routing Key**
{% endtab %}

{% tab title="Second Tab" %}
Define the following:

1. **Exchange name**
2. **Exchange type**
3. Enable or disable [**Durable**](https://www.rabbitmq.com/tutorials/amqp-concepts.html#exchanges)**:** Durable exchanges survive broker restart.
4. Enable or disable [**Auto Delete**](https://www.rabbitmq.com/tutorials/amqp-concepts.html#exchanges)**:** Deletes the exchange when last queue is unbound from it.
5. **Routing Key**
{% endtab %}
{% endtabs %}

## Implementation

### Subscribe

On each incoming request, the RabbitMQ endpoint retrieves information from the request to create a dedicated consumer that will persist until the request terminates. Subscription relies on **Connection name**, **Exchange**, **Queue**, **Routing key**, and **QoS**.

{% tabs %}
{% tab title="Connection name" %}
A connection name is generated for the consumer per the format `gio-apim-consumer-<first part of uuid>`, e.g., `gio-apim-consumer-a0eebc99`.
{% endtab %}

{% tab title="Exchange" %}
The endpoint will declare the exchange with the options provided by the configuration at the API level. The exchange name can be overridden with the attribute `rabbitmq.exchange`**.**

If the provided exchange options are incompatible with the existing exchange found on RabbitMQ, the request will be interrupted with an error.
{% endtab %}

{% tab title="Queue" %}
The request's client identifier will be used to create a queue per the format `gravitee/gio-gateway/<clientIdentifier>`**.**

The created queue will have different options depending on the QoS applied on the entrypoint:

**None:** `durable = false` and `autoDelete = true`

**Auto:** `durable = true` and `autoDelete = false`

**Other not supported:** If the queue already exists, the messages will be load-balanced between both clients.
{% endtab %}

{% tab title="Routing key" %}
In order to route the proper messages to the queue, a routing key from the API configuration is used to create the binding between the exchange and the queue. The routing key can be overridden with the attribute `rabbitmq.routingKey`.
{% endtab %}

{% tab title="QoS" %}
**None:** Applies a strategy with high throughput, low latency, no durability, and no reliability.

* The broker disregards a message as soon as it sends it to the consumer.
* Only use this mode if downstream subscribers can consume messages at a rate exceeding the flow of inbound messages. Otherwise, messages will accumulate in the JVM process memory, leading to out-of-memory errors.
* This mode uses auto-ack when registering the RabbitMQ Consumer.

**Auto:** Applies a strategy that balances performance and quality.

* When the entrypoint supports manual ack, the strategy will use it. Otherwise, it will use auto-ack from the RabbitMQ Reactor library.
* Messages are acknowledged upon arrival in the `Flux#doOnNext` callback to promote a message flow that downstream subscribers can manage.
* This mode does not use auto-ack when registering the RabbitMQ Consumer. Instead, `consumeAutoAck` means messages are automatically acknowledged by the library in one the Flux hooks.
{% endtab %}
{% endtabs %}

### Publish

A shared producer is created by the endpoint and reused for all requests with that same configuration.

All request messages will be published in the exchange using the routing key. It is not possible to select the exchange or routing key based on message attributes. Only request attributes are supported.

Publication relies on **Connection name**, **Exchange**, and **Routing key**.

{% tabs %}
{% tab title="Connection name" %}
A connection name is generated for the producer per the format `gio-apim-producer-<first part of uuid>`, e.g., `gio-apim-producer-a0eebc99`.
{% endtab %}

{% tab title="Exchange" %}
The endpoint will declare the exchange with the options provided by the configuration at the API level. The exchange name can be overridden with the attribute `rabbitmq.exchange`**.**

If the provided exchange options are incompatible with the existing exchange found on RabbitMQ, the request will be interrupted with an error.
{% endtab %}

{% tab title="Routing key" %}
To route the correct messages to the queue, a routing key from the API configuration is used to create the binding between the exchange and the queue.

The routing key can be overridden via the attribute `rabbitmq.routingKey`.
{% endtab %}
{% endtabs %}
