---
description: This page contains the technical details of the RabbitMQ endpoint plugin
---

# RabbitMQ

{% hint style="warning" %}
**This feature requires** [**Gravitee's Enterprise Edition**](../../../../../../overview/gravitee-apim-enterprise-edition/README.md)**.**
{% endhint %}

## Overview

Use this endpoint to publish and/or subscribe messages to a RabbitMQ broker.&#x20;

* [Quality of Service](rabbitmq.md#user-content-quality-of-service)
* [Compatibility matrix](rabbitmq.md#user-content-compatibility-matrix)
* [Endpoint identifier](rabbitmq.md#user-content-endpoint-identifier)
* [Endpoint configuration](rabbitmq.md#user-content-endpoint-configuration)

## Quality of Service <a href="#user-content-quality-of-service" id="user-content-quality-of-service"></a>

<table><thead><tr><th width="108.99999999999997">QoS</th><th width="140">Delivery</th><th>Description</th></tr></thead><tbody><tr><td>None</td><td>Unwarranted</td><td>Messages are acked automatically</td></tr><tr><td>Auto</td><td>1,0 or n</td><td>Messages are acked by entrypoint if supported</td></tr></tbody></table>

## Compatibility matrix <a href="#user-content-compatibility-matrix" id="user-content-compatibility-matrix"></a>

| Plugin version | APIM version |
| -------------- | ------------ |
| 1.x            | 4.x          |

## Endpoint identifier <a href="#user-content-endpoint-identifier" id="user-content-endpoint-identifier"></a>

To use this plugin, declare the following `rabbitmq` identifier while configuring your API endpoints.

## Endpoint configuration <a href="#user-content-endpoint-configuration" id="user-content-endpoint-configuration"></a>

### General configuration <a href="#user-content-general-configuration" id="user-content-general-configuration"></a>

<table><thead><tr><th width="142">Attributes</th><th width="97">Default</th><th width="124">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td>serverHost</td><td>N/A</td><td>Yes</td><td>Define the host of the RabbitMQ</td></tr><tr><td>serverPort</td><td>N/A</td><td>Yes</td><td>Define the port of the RabbitMQ</td></tr></tbody></table>

### Shared Configuration <a href="#user-content-shared-configuration" id="user-content-shared-configuration"></a>

#### **Security configuration**

<table><thead><tr><th width="234">Attributes</th><th width="92">Default</th><th width="117">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td>auth.username</td><td>N/A</td><td>Yes</td><td>Define the user to authenticate to RabbitMQ</td></tr><tr><td>auth.password</td><td>N/A</td><td>Yes</td><td>Define the password to authenticate to RabbitMQ</td></tr><tr><td>ssl.hostnameVerifier</td><td>Yes</td><td>No</td><td>Enable host name verification</td></tr><tr><td>ssl.truststore.type</td><td>NONE</td><td>No</td><td>The type of truststore (NONE, JKS, PKCS12, PEM). Use NONE if you don’t need to define a truststore.</td></tr><tr><td>ssl.truststore.path</td><td>N/A</td><td>No</td><td>The location of the truststore file in the Gateway filesystem</td></tr><tr><td>ssl.truststore.content</td><td>N/A</td><td>No</td><td>The base64 encoded content of the truststore file (or the actual certificates if the truststore type is PEM)</td></tr><tr><td>ssl.truststore.password</td><td>N/A</td><td>No</td><td>The password to decrypt the truststore</td></tr><tr><td>ssl.keystore.type</td><td>NONE</td><td>No</td><td>The type of keystore (NONE, JKS, PKCS12, PEM). Use NONE if you don’t need to define a keystore.</td></tr><tr><td>ssl.keystore.path</td><td>N/A</td><td>No</td><td>The location of the keystore file in the Gateway filesystem</td></tr><tr><td>ssl.keystore.content</td><td>N/A</td><td>No</td><td>The base64 encoded content of the keystore file (or the actual certificates if the keystore type is PEM)</td></tr><tr><td>ssl.keystore.password</td><td>N/A</td><td>No</td><td>The password to decrypt the keystore</td></tr><tr><td>ssl.keystore.certPath</td><td>N/A</td><td>No</td><td>The path to cert file (.PEM) in the Gateway filesystem. Only relevant if the keystore type is PEM.</td></tr><tr><td>ssl.keystore.certContent</td><td>N/A</td><td>No</td><td>The certificate PEM content. Only relevant if the keystore type is PEM.</td></tr><tr><td>ssl.keystore.keyPath</td><td>N/A</td><td>No</td><td>The path to private key file (.PEM) in the Gateway filesystem. Only relevant if the keystore type is PEM.</td></tr><tr><td>ssl.keystore.keyContent</td><td>N/A</td><td>No</td><td>The private key PEM content. Only relevant if the keystore type is PEM.</td></tr></tbody></table>

#### **Producer configuration**

<table><thead><tr><th width="204">Attributes</th><th width="99">Default</th><th width="121">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td>enabled</td><td>false</td><td>No</td><td>Enable or disable the producer capability</td></tr><tr><td>routingKey</td><td></td><td>Yes</td><td>The routing key used to route messages to queues</td></tr><tr><td>exchange.name</td><td></td><td>Yes</td><td>The exchange name</td></tr><tr><td>exchange.type</td><td></td><td>Yes</td><td>The exchange type</td></tr><tr><td>exchange.durable</td><td></td><td>Yes</td><td>The exchange durable flag</td></tr><tr><td>exchange.autoDelete</td><td></td><td>Yes</td><td>The exchange autoDelete flag</td></tr></tbody></table>

#### **Consumer configuration**

<table><thead><tr><th width="207">Attributes</th><th width="91">Default</th><th width="119">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td>enabled</td><td>false</td><td>No</td><td>Enable or disable the consumer capability</td></tr><tr><td>routingKey</td><td></td><td>Yes</td><td>The routing key used to route messages to queues</td></tr><tr><td>exchange.name</td><td></td><td>Yes</td><td>The exchange name</td></tr><tr><td>exchange.type</td><td></td><td>Yes</td><td>The exchange type</td></tr><tr><td>exchange.durable</td><td></td><td>Yes</td><td>The exchange durable flag</td></tr><tr><td>exchange.autoDelete</td><td></td><td>Yes</td><td>The exchange autoDelete flag</td></tr></tbody></table>

### **Examples**

#### **Produce messages**

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

#### **Consume messages**

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

#### **TLS configuration with file**

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

#### **mTLS configuration with file**

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
