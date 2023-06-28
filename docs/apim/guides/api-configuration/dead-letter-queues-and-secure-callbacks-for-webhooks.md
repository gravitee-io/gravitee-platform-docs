---
description: >-
  This article walks through how to configure Dead letter queues for Webhooks
  subscriptions
---

# Dead letter queues and secure callbacks for Webhooks

## Introduction

If using the Webhooks entrypoint, you can:

* Set up dead letter queueus for undelivered message storage
* Configure secure callbacks

The dead letter queue (DLQ) functionality makes it possible to push undelivered messages to external storage. When configuring DLQ with the Webhooks entrypoint, you redirect all the messages that the Webhook rejects to another location, such as a Kafka topic.

By default, without DLQ, any error returned by the Webhook will stop the consumption of the messages.

Callbacks can be secured using basic authentication, JWT, and OAuth2.

This article walks through how to configure a dead letter queue and secure callbacks using the Gravitee v4 API definition.

## Set up your dead letter queue

To enable DLQ, declare another endpoint that will be used to configure the dlq object in the webhook entrypoint definition:

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

* Must support PUBLISH mode
* Should be based on a broker that can persist messages, such as Kafka.

Once configured and deployed, any message rejected with a 4xx error response by the Webhook will be automatically sent to the DLQ endpoint and the consumption of messages will continue.

### Combining DLQ with the retry policy

If you set up a DLQ, you can utilize the Gravitee Retry policy in order to "retry" delivery of undelivered messages from the DLQ. For more information on the Retry policy, please refer to the Retry policy policy reference.

## Set up secure callbacks

Callbacks can be secured using basic authentication, JWT, and OAuth2.

To secure a callback, add an `auth` object to the configuration section of your API definition. The following example shows how to configure basic authentication:

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

To use JWT, the `auth` object should look like this:

```
        "auth": {
            "type": "token",
            "token": {
                "value": "eyJraWQiOiJk..."
            }
        }
```

To use OAuth2, the `auth` object should look like this:

```
        "auth": {
            "type": "oauth2",
            "oauth2": {
                "endpoint": "https://auth.gravitee.io/my-domain/oauth/token",
                "clientId": "a-client-id",
                "clientSecret": "a-client-secret",
                "scopes": ["roles"]
            }
        }
```
