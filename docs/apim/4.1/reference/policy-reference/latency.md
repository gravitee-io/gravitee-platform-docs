---
description: This page provides the technical details of the Latency policy
---

# Latency

## Overview

You can use the `latency` policy to add latency to either the request or the response. For example, if you configure the policy on the request with a latency of 100ms, the Gateway waits 100ms before routing the request to the backend service.

This policy is particularly useful in two scenarios:

* Testing: adding latency allows you to test client applications when APIs are slow to respond.
* Monetization: a longer latency can be added to free plans to encourage clients to move to a better (or paid) plan.

Functional and implementation information for the `latency` policy is organized into the following sections:

* [Examples](latency.md#examples)
* [Configuration](latency.md#configuration)
* [Compatibility Matrix](latency.md#compatibility-matrix)
* [Errors](latency.md#errors)
* [Changelogs](latency.md#changelogs)

## Examples

{% hint style="warning" %}
The proxy API example also applies to v2 APIs. This policy can also be applied at the message level for v4 APIs.
{% endhint %}

{% tabs %}
{% tab title="Proxy APIs" %}
Example policy configuration for a proxy API:

```json
{
    "id": "my-proxy-api",
    "name": "my-proxy-api",
    "apiVersion": "1.0",
    "definitionVersion": "4.0.0",
    "type": "proxy",
    "listeners": [
        {
            "type": "http",
            "paths": [
                {
                    "path": "/test"
                }
            ],
            "entrypoints": [
                {
                    "type": "http-proxy"
                }
            ]
        }
    ],
    "endpointGroups": [
        {
            "name": "default-group",
            "type": "http-proxy",
            "endpoints": [
                {
                    "name": "default",
                    "type": "http-proxy",
                    "weight": 1,
                    "inheritConfiguration": false,
                    "configuration": {
                        "target": "http://localhost:8080/endpoint"
                    }
                }
            ]
        }
    ],
    "flows": [
        {
            "name": "flow-1",
            "enabled": true,
            "request": [
                {
                    "name": "Latency policy",
                    "description": "",
                    "enabled": true,
                    "policy": "latency",
                    "configuration": {
                        "time": 2,
                        "timeUnit": "SECONDS"
                    }
                }
            ],
            "response": [],
            "subscribe": [],
            "publish": []
        }
    ],
    "analytics": {
        "enabled ": true
    }
}
```
{% endtab %}

{% tab title="Message APIs" %}
Example subscription configuration for a message API:

```json
{
    "id": "my-message-subscribe-api",
    "name": "my-message-subscribe-api",
    "apiVersion": "1.0",
    "definitionVersion": "4.0.0",
    "type": "message",
    "listeners": [
        {
            "type": "http",
            "paths": [
                {
                    "path": "/test"
                }
            ],
            "entrypoints": [
                {
                    "type": "sse",
                    "configuration": {
                        "headersAsComment": true
                    }
                }
            ]
        }
    ],
    "endpointGroups": [
        {
            "name": "default-group",
            "type": "mock",
            "endpoints": [
                {
                    "name": "default",
                    "type": "mock",
                    "weight": 1,
                    "inheritConfiguration": false,
                    "configuration": {
                        "messageContent": "{ \"message\": \"hello\" }",
                        "messageCount": 1
                    }
                }
            ]
        }
    ],
    "flows": [
        {
            "name": "flow-1",
            "enabled": true,
            "subscribe": [
                {
                    "name": "Latency policy",
                    "description": "",
                    "enabled": true,
                    "policy": "latency",
                    "configuration": {
                        "time": 2,
                        "timeUnit": "SECONDS"
                    }
                }
            ],
            "request": [],
            "response": [],
            "publish": []
        }
    ],
    "analytics": {
        "enabled ": true
    }
}
```
{% endtab %}
{% endtabs %}

## Configuration

### Phases

The phases checked below are supported by the `latency` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="199.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>true</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>true</td></tr></tbody></table>

### Options

You can configure the `latency` policy with the following options:

<table><thead><tr><th width="116">Property</th><th width="105" data-type="checkbox">Required</th><th width="274">Description</th><th width="100">Type</th><th>Default</th></tr></thead><tbody><tr><td>time</td><td>false</td><td>Time to wait (<code>ms</code>)</td><td>integer</td><td>100</td></tr><tr><td>timeUnit</td><td>false</td><td>Time unit ( <code>"MILLISECONDS"</code> or <code>"SECONDS"</code>)</td><td>string</td><td><code>"MILLISECONDS"</code></td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `latency` policy.

| Plugin version | APIM version |
| -------------- | ------------ |
| Up to 1.3.x    | Up to 3.9.x  |
| 1.4.x          | Up to 3.20   |
| 2.x            | 4.x+         |

## Errors

<table data-full-width="false"><thead><tr><th>HTTP status code</th><th>Message</th></tr></thead><tbody><tr><td><code>500</code></td><td>Server error</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-latency/blob/master/CHANGELOG.md" %}
