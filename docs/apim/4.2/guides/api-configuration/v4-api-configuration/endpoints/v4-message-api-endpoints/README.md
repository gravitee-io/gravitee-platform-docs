---
description: An overview about v4 Message API Endpoints.
---

# v4 Message API Endpoints

## Overview

{% hint style="warning" %}
**Enterprise-only**

The ability to create APIs with message API endpoints is an Enterprise Edition capability. To learn more about Gravitee Enterprise Edition and what's included in various enterprise packages:

* [Refer to the EE vs OSS documentation](../../../../../overview/gravitee-apim-enterprise-edition/README.md)
* [Book a demo](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/rYZ7tzkLjFVST6ex6Jid/)
* [Check out the pricing page](https://www.gravitee.io/pricing)
{% endhint %}

v4 message APIs currently support the following endpoints:

* **Kafka**: Enables the Gravitee API Gateway to establish a persistent connection with a Kafka topic as a backend resource or target.
* **MQTT 5**: Enables the Gravitee API Gateway to establish a persistent connection with an MQTT topic as a backend resource or target.
* **RabbitMQ**: Enables the Gravitee API Gateway to establish a persistent connection with RabbitMQ as a backend resource or target. This will only work if you are using RabbitMQ and the AMQP 0-9-1 protocol. Because this endpoint supports the AMQP 0-9-1 protocol, it may support other event brokers and message queues that communicate over the AMQP 0-9-1 protocol. However, Gravitee does not guarantee or officially support these implementations.
* **Solace**: Enables the Gravitee API Gateway to establish a persistent connection with Solace as a backend resource or target.
* **Mock**: Enables the Gateway to simulate responses from a server for testing API implementations.

## Configuration and Implementation

To access endpoint configuration:

1. Select **APIs** from the left nav
2. Select your API
3. Select **Backend services** from the Endpoints section of the inner left nav

The integrations Gravitee uses to enable Kafka, MQTT, RabbitMQ, and Solace endpoints for v4 API definitions rely on the following terminology and functionality:

* **Request-Id**: A Universally Unique Identifier (UUID) generated for any new request. This can be overridden using `X-Gravitee-Request-Id`as a Header or Query parameter.
* **Transaction-Id**: A UUID generated for any new request. This can be overridden using `X-Gravitee-Transaction-Id`as a Header or Query parameter.
* **Client-Identifier**: Inferred from the subscription attached to the request. It is either the subscription ID, or, with a Keyless plan, a hash of the remote address. The **Client-Identifier** can be provided by the client via the header `X-Gravitee-Client-Identifier`. In this case, the value used by Gravitee will be the original inferred value suffixed with the provided overridden value.

Click on the tiles below for specific configuration and implementation details.

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td></td><td>Kafka</td><td></td><td><a href="kafka.md">kafka.md</a></td></tr><tr><td></td><td>MQTT5</td><td></td><td><a href="mqtt5.md">mqtt5.md</a></td></tr><tr><td></td><td>Solace</td><td></td><td><a href="solace.md">solace.md</a></td></tr><tr><td></td><td>RabbitMQ</td><td></td><td><a href="rabbitmq.md">rabbitmq.md</a></td></tr><tr><td></td><td>Mock</td><td></td><td><a href="../../endpoint-configuration/v4-message-api-endpoints/mock.md">mock.md</a></td></tr></tbody></table>

{% hint style="info" %}
For more detailed information on Gravitee endpoints, see the [Endpoint Reference](../../../../../reference/endpoint-reference/README.md) documentation.
{% endhint %}
