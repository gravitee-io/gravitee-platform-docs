---
description: This page contains the technical details of the Webhook entrypoint plugin
---

# Webhook

Enterprise feature

### Description <a href="#user-content-description" id="user-content-description"></a>

| Plugin version | APIM version |
| -------------- | ------------ |
| 1.x            | 3.21.x       |

This _Advanced_ version aims to add _Enterprise features_ to the Webhook endpoint in OSS version such as:

* dead letter queue
* secured callback

#### Plugin identifier <a href="#user-content-plugin-identifier" id="user-content-plugin-identifier"></a>

In order to use this _Advanced_ version, you only have to declare the following identifier `webhook-advanced` while configuring your API entrypoints. You could also update existing API, thanks to compatibility of the _Advanced_ version configuration with the _OSS_ version

#### Quality Of Service <a href="#user-content-quality-of-service" id="user-content-quality-of-service"></a>

| QoS           | Delivery    | Description                                 |
| ------------- | ----------- | ------------------------------------------- |
| None          | Unwarranted | Performance matters over delivery guarantee |
| Auto          | 0 or n      | Performance matters over delivery guarantee |
| At-Most-Once  | 0 or 1      | Delivery guarantee matters over performance |
| At-Least-Once | 1 or n      | Delivery guarantee matters over performance |

#### Dead Letter Queue (DLQ) <a href="#user-content-dead-letter-queue-dlq" id="user-content-dead-letter-queue-dlq"></a>

Dead letter is the ability to push undelivered messages to an external storage. When configuring DLQ with webhook, you can basically redirect all messages rejected by the webhook to another location such as a kafka topic.

By default, without DLQ, any error returned by the webhook will stop the consumption of the messages.

Enabling DLQ requires to declare another endpoint that will be used to configure the `dlq` section of the webhook entrypoint definition:

```
{
    "type": "webhook-advanced",
    "dlq": {
        "endpoint": "dlq-endpoint"
    },
    "configuration": {}
}
```

The endpoint used for the dead letter queue:

* Must support `PUBLISH` mode
* Should be based on a broker capable to persist messages. Kafka is a good choice.

Once configured and deployed, any message rejected with a 4xx error response by the webhook will be automatically sent to the dlq endpoint and the consumption of messages will continue.

### Configuration <a href="#user-content-configuration" id="user-content-configuration"></a>

The configuration is provided when creating the subscription.

```
{
    "configuration": {
        "entrypointId": "webhook-advanced",
        "callbackUrl": "https://example.com"
    }
}
```

#### Http options <a href="#user-content-http-options" id="user-content-http-options"></a>

It is possible to tune the underlying http client used to perform the calls to the webhook url.

| Attributes               | Default | Mandatory | Description                                                                                                                                                                                                                                               |
| ------------------------ | ------- | --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| connectTimeout           | 3000    | Yes       | Maximum time to connect to the backend in milliseconds.                                                                                                                                                                                                   |
| readTimeout              | 10000   | Yes       | Maximum time given to the backend to complete the request (including response) in milliseconds.                                                                                                                                                           |
| idleTimeout              | 60000   | Yes       | Maximum time a connection will stay in the pool without being used in milliseconds. Once the timeout has elapsed, the unused connection will be closed, allowing to free the eventual associated resources.                                               |
| maxConcurrentConnections | 5       | Yes       | Maximum pool size for connections. It basically represents the maximum number of concurrent requests at a time. Max value is 20. Currency is automatically set to 1 when using qos AT\_LEAST\_ONCE or AT\_MOST\_ONCE in order to ensure message delivery. |

#### Secured callbacks <a href="#user-content-secured-callbacks" id="user-content-secured-callbacks"></a>

Security information can be provided when creating the subscription. Currently, we support:

* Basic
* Token (JWT)
* OAuth2

**Basic authentication example**

```
{
    "configuration": {
        "entrypointId": "webhook-advanced",
        "callbackUrl": "https://example.com",
        "auth": {
            "type": "basic",
            "basic": {
                "username": "username",
                "password": "a-very-secured-password"
            }
        }
    }
}
```

**Token JWT authentication example**

```
{
    "configuration": {
        "entrypointId": "webhook-advanced",
        "callbackUrl": "https://example.com",
        "auth": {
            "type": "token",
            "token": {
                "value": "eyJraWQiOiJk..."
            }
        }
    }
}
```

**OAuth2 authentication example**

```
{
    "configuration": {
        "entrypointId": "webhook-advanced",
        "callbackUrl": "https://example.com",
        "auth": {
            "type": "oauth2",
            "oauth2": {
                "endpoint": "https://auth.gravitee.io/my-domain/oauth/token",
                "clientId": "a-client-id",
                "clientSecret": "a-client-secret",
                "scopes": ["roles"]
            }
        }
    }
}
```
