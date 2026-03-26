---
description: This page contains the technical details of the Webhook entrypoint plugin
---

# Webhook

{% hint style="warning" %}
**This feature requires** [**Gravitee's Enterprise Edition**](../../overview/gravitee-apim-enterprise-edition/README.md)**.**
{% endhint %}

## Overview

This Advanced version of the Webhook plugin adds enterprise features to the OSS version of the Webhook entrypoint, including Dead Letter Queue and secured callback. Refer to the following sections for additional details.

* [Quality of Service](webhook.md#user-content-quality-of-service)
* [Compatibility matrix](webhook.md#compatibility-matrix)
* [Entrypoint identifier](webhook.md#user-content-plugin-identifier)
* [Entrypoint configuration](webhook.md#user-content-configuration)

## Quality of Service <a href="#user-content-quality-of-service" id="user-content-quality-of-service"></a>

The Advanced version of the Webhook plugin offers improved QoS.

<table><thead><tr><th width="169.99999999999997">QoS</th><th width="138">Delivery</th><th>Description</th></tr></thead><tbody><tr><td>None</td><td>Unwarranted</td><td>Performance matters over delivery guarantee</td></tr><tr><td>Auto</td><td>0 or n</td><td>Performance matters over delivery guarantee</td></tr><tr><td>At-Most-Once</td><td>0 or 1</td><td>Delivery guarantee matters over performance</td></tr><tr><td>At-Least-Once</td><td>1 or n</td><td>Delivery guarantee matters over performance</td></tr></tbody></table>

## Compatibility matrix <a href="#user-content-description" id="user-content-description"></a>

| Plugin version | APIM version |
| -------------- | ------------ |
| 1.x            | 3.21.x       |

## Entrypoint identifier <a href="#user-content-plugin-identifier" id="user-content-plugin-identifier"></a>

To use this Advanced version of the plugin, either:

* Declare the following `webhook-advanced` identifier while configuring your API entrypoints
* Simply update your existing API, due to the compatibility of the Advanced and OSS configurations

## Entrypoint configuration <a href="#user-content-configuration" id="user-content-configuration"></a>

When creating the Webhook subscription, the following configuration is provided:

```json
{
    "configuration": {
        "entrypointId": "webhook-advanced",
        "callbackUrl": "https://example.com"
    }
}
```

### HTTP options <a href="#user-content-http-options" id="user-content-http-options"></a>

The underlying HTTP client that performs the calls to the Webhook URL can be tuned via the following parameters.

<table><thead><tr><th width="173">Attributes</th><th width="94">Default</th><th width="121">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td>connectTimeout</td><td>3000</td><td>Yes</td><td>Maximum time to connect to the backend in milliseconds.</td></tr><tr><td>readTimeout</td><td>10000</td><td>Yes</td><td>Maximum time given to the backend to complete the request (including response) in milliseconds.</td></tr><tr><td>idleTimeout</td><td>60000</td><td>Yes</td><td>Maximum time a connection will stay in the pool without being used in milliseconds. Once the timeout has elapsed, the unused connection will be closed, freeing the associated resources.</td></tr><tr><td>maxConcurrentConnections</td><td>5</td><td>Yes</td><td>Maximum pool size for connections. This represents the maximum number of concurrent requests. Max value is 20. Value is automatically set to 1 when using QoS AT_LEAST_ONCE or AT_MOST_ONCE to ensure message delivery.</td></tr></tbody></table>

### Dead Letter Queue <a href="#user-content-secured-callbacks" id="user-content-secured-callbacks"></a>

Dead Letter Queue (DLQ) is the ability to push undelivered messages to an external storage. When configuring DLQ with Webhook, you can redirect all messages rejected by the Webhook to another location, such as a Kafka topic.

By default, without DLQ, any error returned by the Webhook will stop message consumption.&#x20;

Enabling DLQ requires declaring another endpoint that will be used to configure the `dlq` section of the Webhook entrypoint definition:

```json
{
    "type": "webhook-advanced",
    "dlq": {
        "endpoint": "dlq-endpoint"
    },
    "configuration": {}
}
```

The endpoint used for the DLQ:

* Must support `PUBLISH` mode
* Should be based on a broker capable of persisting messages, e.g., Kafka

Once configured and deployed, any message rejected by the Webhook with a 4xx error response will be automatically sent to the DLQ endpoint and message consumption will resume.

### Secured callbacks <a href="#user-content-secured-callbacks" id="user-content-secured-callbacks"></a>

Security information can be provided when creating the subscription. Examples of the currently supported authentication protocols are shown below.

{% tabs %}
{% tab title="Basic" %}
```json
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
{% endtab %}

{% tab title="Token JWT" %}
```json
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
{% endtab %}

{% tab title="OAuth2" %}
```json
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
{% endtab %}
{% endtabs %}
