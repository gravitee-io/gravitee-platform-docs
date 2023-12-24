---
description: This page contains the technical details of the RabbitMQ endpoint plugin
---

# RabbitMQ

### Description <a href="#user-content-description" id="user-content-description"></a>

#### Quality Of Service <a href="#user-content-quality-of-service" id="user-content-quality-of-service"></a>

| QoS  | Delivery    | Description                                    |
| ---- | ----------- | ---------------------------------------------- |
| None | Unwarranted | Messages are acked automatically.              |
| Auto | 1,0 or n    | Messages are acked by entrypoint if supported. |

### Compatibility matrix <a href="#user-content-compatibility-matrix" id="user-content-compatibility-matrix"></a>

| Plugin version | APIM version |
| -------------- | ------------ |
| 1.x            | 4.x          |

### Endpoint identifier <a href="#user-content-endpoint-identifier" id="user-content-endpoint-identifier"></a>

In order to use this version, you have to declare the following identifier `rabbitmq` while configuring your API endpoints.

### Endpoint configuration <a href="#user-content-endpoint-configuration" id="user-content-endpoint-configuration"></a>

#### General configuration <a href="#user-content-general-configuration" id="user-content-general-configuration"></a>

| Attributes | Default | Mandatory | Description                      |
| ---------- | ------- | --------- | -------------------------------- |
| serverHost | N/A     | Yes       | Define the host of the RabbitMQ. |
| serverPort | N/A     | Yes       | Define the port of the RabbitMQ. |

#### Shared Configuration <a href="#user-content-shared-configuration" id="user-content-shared-configuration"></a>

**Security configuration**

| Attributes               | Default | Mandatory | Description                                                                                                   |
| ------------------------ | ------- | --------- | ------------------------------------------------------------------------------------------------------------- |
| auth.username            | N/A     | Yes       | Define the user to authenticate to RabbitMQ.                                                                  |
| auth.password            | N/A     | Yes       | Define the password to authenticate to RabbitMQ.                                                              |
| ssl.hostnameVerifier     | Yes     | No        | Enable host name verification.                                                                                |
| ssl.truststore.type      | NONE    | No        | The type of truststore (NONE, JKS, PKCS12, PEM). Use NONE if you don’t need to define a truststore.           |
| ssl.truststore.path      | N/A     | No        | The location of the truststore file in the Gateway filesystem.                                                |
| ssl.truststore.content   | N/A     | No        | The base64 encoded content of the truststore file (or the actual certificates if the truststore type is PEM). |
| ssl.truststore.password  | N/A     | No        | The password to decrypt the truststore.                                                                       |
| ssl.keystore.type        | NONE    | No        | The type of keystore (NONE, JKS, PKCS12, PEM). Use NONE if you don’t need to define a keystore.               |
| ssl.keystore.path        | N/A     | No        | The location of the keystore file in the Gateway filesystem.                                                  |
| ssl.keystore.content     | N/A     | No        | The base64 encoded content of the keystore file (or the actual certificates if the keystore type is PEM).     |
| ssl.keystore.password    | N/A     | No        | The password to decrypt the keystore.                                                                         |
| ssl.keystore.certPath    | N/A     | No        | The path to cert file (.PEM) in the Gateway filesystem. Only relevant if the keystore type is PEM.            |
| ssl.keystore.certContent | N/A     | No        | The certificate PEM content. Only relevant if the keystore type is PEM.                                       |
| ssl.keystore.keyPath     | N/A     | No        | The path to private key file (.PEM) in the Gateway filesystem. Only relevant if the keystore type is PEM.     |
| ssl.keystore.keyContent  | N/A     | No        | The private key PEM content. Only relevant if the keystore type is PEM.                                       |

**Producer configuration**

| Attributes          | Default | Mandatory | Description                                          |
| ------------------- | ------- | --------- | ---------------------------------------------------- |
| enabled             | false   | No        | Allow enabling or disabling the producer capability. |
| routingKey          |         | Yes       | The routing key used to route message to queues.     |
| exchange.name       |         | Yes       | The exchange name.                                   |
| exchange.type       |         | Yes       | The exchange type.                                   |
| exchange.durable    |         | Yes       | The exchange durable flag.                           |
| exchange.autoDelete |         | Yes       | The exchange autoDelete flag.                        |

**Consumer configuration**

| Attributes          | Default | Mandatory | Description                                          |
| ------------------- | ------- | --------- | ---------------------------------------------------- |
| enabled             | false   | No        | Allow enabling or disabling the consumer capability. |
| routingKey          |         | Yes       | The routing key used to route message to queues.     |
| exchange.name       |         | Yes       | The exchange name.                                   |
| exchange.type       |         | Yes       | The exchange type.                                   |
| exchange.durable    |         | Yes       | The exchange durable flag.                           |
| exchange.autoDelete |         | Yes       | The exchange autoDelete flag.                        |

**Examples**

**Produce messages**

```
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

**Consume messages**

```
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

**TLS configuration with file**

```
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

**mTLS configuration with file**

```
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
