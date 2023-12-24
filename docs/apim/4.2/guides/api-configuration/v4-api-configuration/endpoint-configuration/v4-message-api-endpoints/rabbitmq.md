# RabbitMQ

## Overview

This article details the [configuration](rabbitmq.md#configuration) and [implementation](rabbitmq.md#implementation) of the **RabbitMQ** endpoint.

## Configuration

The **RabbitMQ** endpoint allows the Gateway to open up a persistent connection and/or call a backend RabbitMQ resource, as long as that RabbitMQ resource communicates over AMQP 0-9-1 protocol. If you choose this endpoint, you will need to configure the following:

* **Server host:** Define the host of your RabbitMQ resource.
* **Server port:** Define the port that RabbitMQ is using.
* **Virtual host:** Define the virtual host to use.
* How the Gateway will interact with RabbitMQ by instructing the Gravitee Gateway to act as either a producer, a consumer, or both a producer and consumer:
  * **Use Producer:** Tells the Gateway Gateway to be prepared to produce messages and send them to RabbitMQ that you define as your endpoint.
  * **Use Consumer:** Tells the Gateway to be prepared to consume messages from RabbitMQ that you define as your endpoint.
  * **Use Producer and Consumer:** Tells the Gateway to be able to use both **Use Producer** and **Use Consumer** settings.
* **Authentication:** Define the **username** and **password** for RabbitMQ authentication.
* **SSL Options:**
  * **Verify Host:** Enable host name verification.
  * **Truststore:** Select from **None**, **PEM with path**, **PEM with content**, **JKS with path**, **JKS with content**, **PKCS12 with path**, or **PKCS12 with content** and supply the required content/path and password.
  * **KeyStore:** Select from **None**, **PEM with path**, **PEM with content**, **JKS with path**, **JKS with content**, **PKCS12 with path**, or **PKCS12 with content** and supply the required content/path and password.
* **Producer** settings (if you chose **Use Producer** or **Use Producer and Consumer**): Define the settings that the Gravitee Gateway Kafka client will rely on for producing messages to your backend Kafka topic/broker. You will need to define:
  * **Exchange name**
  * **Exchange type**
  * Enable or disable [**Durable**](https://www.rabbitmq.com/tutorials/amqp-concepts.html#exchanges)**:** Durable exchanges survive broker restart.
  * Enable or disable [**Auto Delete**](https://www.rabbitmq.com/tutorials/amqp-concepts.html#exchanges)**:** Deletes the exchange when last queue is unbound from it.
  * **Routing Key**
* **Consumer** settings (if you chose **Use Consumer** or **Use Producer and Consumer**): Define the settings that the Gravitee Gateway Kafka client will rely on for consuming messages from your backend Kafka topic/broker. You will need to define:
  * **Exchange name**
  * **Exchange type**
  * Enable or disable [**Durable**](https://www.rabbitmq.com/tutorials/amqp-concepts.html#exchanges)**:** Durable exchanges survive broker restart.
  * Enable or disable [**Auto Delete**](https://www.rabbitmq.com/tutorials/amqp-concepts.html#exchanges)**:** Deletes the exchange when last queue is unbound from it.
  * **Routing Key**

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

* The broker disregards a message as soon as it sends it to the consumer.&#x20;
* Only use this mode if downstream subscribers can consume messages at a rate exceeding the flow of inbound messages. Otherwise, messages will accumulate in the JVM process memory, leading to out-of-memory errors.&#x20;
* This mode uses auto-ack when registering the RabbitMQ Consumer.

**Auto:** Applies a strategy that balances performance and quality.

* When the entrypoint supports manual ack, the strategy will use it. Otherwise, it will use auto-ack from the RabbitMQ Reactor library.
* Messages are acknowledged upon arrival in the `Flux#doOnNext` callback to promote a message flow that downstream subscribers can manage.&#x20;
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
