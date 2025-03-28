# RabbitMQ

## Overview

This article details the [configuration](rabbitmq.md#configuration) and [implementation](rabbitmq.md#implementation) of the **RabbitMQ** endpoint and includes a [reference](rabbitmq.md#reference) section.

## Configuration

The **RabbitMQ** endpoint allows the Gateway to open up a persistent connection and/or call a backend RabbitMQ resource, as long as that RabbitMQ resource communicates over AMQP 0-9-1 protocol. Entering a host and port is required. Modifying any other configuration parameters is optional.

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

You will define more Gravitee Gateway-specific security settings later on, but this is where you define your RabbitMQ-specific authentication flow. Gravitee supports SSL authentication.

1. Define the **username** and **password** for RabbitMQ authentication.
2. Choose whether to enable host name verification.&#x20;
3.  Use the drop-down menu to configure a truststore type

    * **None**
    * **PEM with content:** Enter binary content as base64.
    * **PEM with path:** Enter the path to the truststore file.
    * **JKS with content:** Enter binary content as base64 and the truststore password.
    * **JKS with path:** Enter the truststore file path and password.
    * **PKCS12 with content:** Enter binary content as base64 and the truststore password.
    * **PKCS12 with path:** Enter the truststore file path and password.

    and a keystore type

    * **None**
    * **PEM with content:** Enter the certificate content and key content.
    * **PEM with path:** Enter the certificate path and key path.
    * **JKS with content:** Enter binary content as base64 and the keystore password.
    * **JKS with path:** Enter the keystore file path and password.
    * **PKCS12 with content:** Enter binary content as base64 and the keystore password.
    * **PKCS12 with path:** Enter the keystore file path and password.

### 4. Role settings

If you chose **Use Producer** or **Use Producer and Consumer**, you must define the settings that the Gravitee Gateway RabbitMQ client will rely on for producing messages to your backend RabbitMQ topic/broker.&#x20;

If you chose **Use Consumer** or **Use Producer and Consumer**, you must define the settings that the Gravitee Gateway RabbitMQ client will rely on for consuming messages from your backend RabbitMQ topic/broker.&#x20;

{% tabs %}
{% tab title="Producer" %}
Define the following:

1. Enter the exchange name.
2. Enter the exchange type.
3. Choose whether to enable [durable exchanges](https://www.rabbitmq.com/tutorials/amqp-concepts.html#exchanges) that will survive broker restart.
4. Choose whether to enable [auto delete](https://www.rabbitmq.com/tutorials/amqp-concepts.html#exchanges) to delete the exchange when the last queue is unbound from it.
5. Enter the routing key.
{% endtab %}

{% tab title="Consumer" %}
Define the following:

1. Enter the exchange name.
2. Enter the exchange type.
3. Choose whether to enable [durable exchanges](https://www.rabbitmq.com/tutorials/amqp-concepts.html#exchanges) that will survive broker restart.
4. Choose whether to enable [auto delete](https://www.rabbitmq.com/tutorials/amqp-concepts.html#exchanges) to delete the exchange when the last queue is unbound from it.
5. Enter the routing key.
{% endtab %}
{% endtabs %}

### Tenants

You can configure tenants to specify which users can proxy requests to this endpoint. Tenants ensure that certain groups of users receive information from only specific APIs. For more information about configuring tenants, see [tenants.md](../../gravitee-gateway/tenants.md "mention").

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

## Reference

Refer to the following sections for additional details.

* [Quality of Service](rabbitmq.md#user-content-quality-of-service)
* [Compatibility matrix](rabbitmq.md#user-content-compatibility-matrix)
* [Endpoint identifier](rabbitmq.md#user-content-endpoint-identifier)
* [Endpoint configuration](rabbitmq.md#user-content-endpoint-configuration)

### Quality of Service <a href="#user-content-quality-of-service" id="user-content-quality-of-service"></a>

<table><thead><tr><th width="108.99999999999997">QoS</th><th width="140">Delivery</th><th>Description</th></tr></thead><tbody><tr><td>None</td><td>Unwarranted</td><td>Messages are acked automatically</td></tr><tr><td>Auto</td><td>1,0 or n</td><td>Messages are acked by entrypoint if supported</td></tr></tbody></table>

### Compatibility matrix <a href="#user-content-compatibility-matrix" id="user-content-compatibility-matrix"></a>

| Plugin version | APIM version |
| -------------- | ------------ |
| 1.x            | 4.x          |

### Endpoint identifier <a href="#user-content-endpoint-identifier" id="user-content-endpoint-identifier"></a>

To use this plugin, declare the `rabbitmq` identifier when configuring your API endpoints.

### Endpoint configuration <a href="#user-content-endpoint-configuration" id="user-content-endpoint-configuration"></a>

#### General configuration <a href="#user-content-general-configuration" id="user-content-general-configuration"></a>

<table><thead><tr><th width="142">Attributes</th><th width="97">Default</th><th width="124">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td>serverHost</td><td>N/A</td><td>Yes</td><td>Define the host of the RabbitMQ</td></tr><tr><td>serverPort</td><td>N/A</td><td>Yes</td><td>Define the port of the RabbitMQ</td></tr></tbody></table>

#### Shared Configuration <a href="#user-content-shared-configuration" id="user-content-shared-configuration"></a>

{% tabs %}
{% tab title="Security" %}
<table><thead><tr><th width="234">Attributes</th><th width="92">Default</th><th width="117">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td>auth.username</td><td>N/A</td><td>Yes</td><td>Define the user to authenticate to RabbitMQ</td></tr><tr><td>auth.password</td><td>N/A</td><td>Yes</td><td>Define the password to authenticate to RabbitMQ</td></tr><tr><td>ssl.hostnameVerifier</td><td>Yes</td><td>No</td><td>Enable host name verification</td></tr><tr><td>ssl.truststore.type</td><td>NONE</td><td>No</td><td>The type of truststore (NONE, JKS, PKCS12, PEM). Use NONE if you don’t need to define a truststore.</td></tr><tr><td>ssl.truststore.path</td><td>N/A</td><td>No</td><td>The location of the truststore file in the Gateway filesystem</td></tr><tr><td>ssl.truststore.content</td><td>N/A</td><td>No</td><td>The base64 encoded content of the truststore file (or the actual certificates if the truststore type is PEM)</td></tr><tr><td>ssl.truststore.password</td><td>N/A</td><td>No</td><td>The password to decrypt the truststore</td></tr><tr><td>ssl.keystore.type</td><td>NONE</td><td>No</td><td>The type of keystore (NONE, JKS, PKCS12, PEM). Use NONE if you don’t need to define a keystore.</td></tr><tr><td>ssl.keystore.path</td><td>N/A</td><td>No</td><td>The location of the keystore file in the Gateway filesystem</td></tr><tr><td>ssl.keystore.content</td><td>N/A</td><td>No</td><td>The base64 encoded content of the keystore file (or the actual certificates if the keystore type is PEM)</td></tr><tr><td>ssl.keystore.password</td><td>N/A</td><td>No</td><td>The password to decrypt the keystore</td></tr><tr><td>ssl.keystore.certPath</td><td>N/A</td><td>No</td><td>The path to cert file (.PEM) in the Gateway filesystem. Only relevant if the keystore type is PEM.</td></tr><tr><td>ssl.keystore.certContent</td><td>N/A</td><td>No</td><td>The certificate PEM content. Only relevant if the keystore type is PEM.</td></tr><tr><td>ssl.keystore.keyPath</td><td>N/A</td><td>No</td><td>The path to private key file (.PEM) in the Gateway filesystem. Only relevant if the keystore type is PEM.</td></tr><tr><td>ssl.keystore.keyContent</td><td>N/A</td><td>No</td><td>The private key PEM content. Only relevant if the keystore type is PEM.</td></tr></tbody></table>
{% endtab %}

{% tab title="Producer" %}
<table><thead><tr><th width="204">Attributes</th><th width="99">Default</th><th width="121">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td>enabled</td><td>false</td><td>No</td><td>Enable or disable the producer capability</td></tr><tr><td>routingKey</td><td></td><td>Yes</td><td>The routing key used to route messages to queues</td></tr><tr><td>exchange.name</td><td></td><td>Yes</td><td>The exchange name</td></tr><tr><td>exchange.type</td><td></td><td>Yes</td><td>The exchange type</td></tr><tr><td>exchange.durable</td><td></td><td>Yes</td><td>The exchange durable flag</td></tr><tr><td>exchange.autoDelete</td><td></td><td>Yes</td><td>The exchange autoDelete flag</td></tr></tbody></table>
{% endtab %}

{% tab title="Consumer" %}
<table><thead><tr><th width="207">Attributes</th><th width="91">Default</th><th width="119">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td>enabled</td><td>false</td><td>No</td><td>Enable or disable the consumer capability</td></tr><tr><td>routingKey</td><td></td><td>Yes</td><td>The routing key used to route messages to queues</td></tr><tr><td>exchange.name</td><td></td><td>Yes</td><td>The exchange name</td></tr><tr><td>exchange.type</td><td></td><td>Yes</td><td>The exchange type</td></tr><tr><td>exchange.durable</td><td></td><td>Yes</td><td>The exchange durable flag</td></tr><tr><td>exchange.autoDelete</td><td></td><td>Yes</td><td>The exchange autoDelete flag</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

#### **Examples**

{% tabs %}
{% tab title="Produce messages" %}
{% code title="Produce messages" %}
```json
{
  "name": "default",
  "type": "rabbitmq",
  "weight": 1,
  "inheritConfiguration": false,
  "configuration": {
    "serverHost": "server-host",
    "serverPort": 5672
  },
  "sharedConfigurationOverride": {
    "security": {
      "auth": {
        "username": "user",
        "password": "bitnami"
      }
    },
    "producer": {
      "enabled": true,
      "routingKey": "a.routing.key",
      "exchange": {
        "name": "an-exchange",
        "type": "topic",
        "durable": true,
        "autoDelete": false
      }
    }
  }
}
```
{% endcode %}
{% endtab %}

{% tab title="Consume messages" %}
{% code title="Consume messages" %}
```json
{
  "name": "default",
  "type": "rabbitmq",
  "weight": 1,
  "inheritConfiguration": false,
  "configuration": {
    "serverHost": "server-host",
    "serverPort": 5672
  },
  "sharedConfigurationOverride": {
    "security": {
      "auth": {
        "username": "user",
        "password": "bitnami"
      }
    },
    "consumer": {
      "enabled": true,
      "routingKey": "a.routing.key",
      "exchange": {
        "name": "an-exchange",
        "type": "topic",
        "durable": true,
        "autoDelete": false
      }
    }
  }
}
```
{% endcode %}
{% endtab %}

{% tab title="TLS config with file" %}
{% code title="TLS config with file" %}
```json
{
  "name": "default",
  "type": "rabbitmq",
  "weight": 1,
  "inheritConfiguration": false,
  "configuration": {
    "serverHost": "server-host",
    "serverPort": 5672
  },
  "sharedConfigurationOverride": {
    "security": {
      "auth": {
        "username": "user",
        "password": "bitnami"
      },
      "ssl": {
        "hostnameVerifier": true,
        "trustStore": {
            "type": "PKCS12",
            "path": "/opt/graviteeio-gateway/config/ssl/client.truststore.p12",
            "password": "my-secured-password"
        }
      }
    },
    "producer": {
      "enabled": true,
      "routingKey": "a.routing.key",
      "exchange": {
        "name": "an-exchange",
        "type": "topic",
        "durable": true,
        "autoDelete": false
      }
    }
  }
}
```
{% endcode %}
{% endtab %}

{% tab title="mTLS config with file" %}
{% code title="mTLS config with file" %}
```json
{
  "name": "default",
  "type": "rabbitmq",
  "weight": 1,
  "inheritConfiguration": false,
  "configuration": {
    "serverHost": "server-host",
    "serverPort": 5672
  },
  "sharedConfigurationOverride": {
    "security": {
      "auth": {
        "username": "user",
        "password": "bitnami"
      },
      "ssl": {
        "hostnameVerifier": true,
        "trustStore": {
            "type": "PKCS12",
            "path": "/opt/graviteeio-gateway/config/ssl/client.truststore.p12",
            "password": "my-secured-password"
        },
        "keyStore": {
            "type": "PKCS12",
            "path": "/opt/graviteeio-gateway/config/ssl/client.keystore.p12",
            "password": "my-secured-password"
        }
      }
    },
    "producer": {
      "enabled": true,
      "routingKey": "a.routing.key",
      "exchange": {
        "name": "an-exchange",
        "type": "topic",
        "durable": true,
        "autoDelete": false
      }
    }
  }
}
```
{% endcode %}
{% endtab %}
{% endtabs %}
