---
description: This page contains the technical details of the SSE entrypoint plugin
---

# Server-sent Events

{% hint style="warning" %}
**This feature requires** [**Gravitee's Enterprise Edition**](../../overview/gravitee-apim-enterprise-edition/)**.**
{% endhint %}

## Overview

This Advanced version of the SSE plugin adds enterprise features to the OSS version of the SSE entrypoint. Refer to the following sections for additional details.

* [Quality of Service](server-sent-events.md#user-content-quality-of-service)
* [Compatibility matrix](server-sent-events.md#compatibility-matrix)
* [Entrypoint identifier](server-sent-events.md#user-content-plugin-identifier)
* [Entrypoint configuration](server-sent-events.md#user-content-configuration)

## Quality of Service <a href="#user-content-quality-of-service" id="user-content-quality-of-service"></a>

The Advanced version of the SSE plugin offers improved QoS.

<table><thead><tr><th width="172.99999999999997">QoS</th><th width="132">Delivery</th><th>Description</th></tr></thead><tbody><tr><td>None</td><td>Unwarranted</td><td>Already supported by OSS</td></tr><tr><td>Balanced</td><td>0, 1 or n</td><td>Already supported by OSS</td></tr><tr><td>At-Best</td><td>0, 1 or n</td><td>Support <code>Last-Event-ID</code> to improve QoS</td></tr><tr><td>At-Most-Once</td><td>0 or 1</td><td>Support <code>Last-Event-ID</code> to improve QoS</td></tr><tr><td>At-Least-Once</td><td>1 or n</td><td>Support <code>Last-Event-ID</code> to improve QoS</td></tr></tbody></table>

## Compatibility matrix

| Plugin version | APIM version |
| -------------- | ------------ |
| 1.x            | 3.19.x       |
| 2.x            | 3.20.x       |
| 3.x            | 3.21.x       |

## Entrypoint identifier <a href="#user-content-plugin-identifier" id="user-content-plugin-identifier"></a>

To use this Advanced version of the plugin, either:

* Declare the following `sse-advanced` identifier while configuring your API entrypoints
* Simply update your existing API, due to the compatibility of the Advanced and OSS configurations

## Entrypoint configuration <a href="#user-content-configuration" id="user-content-configuration"></a>

When creating a new API, configure this plugin with the following parameters:

```json
{
    "name": "apiv4-sse",
    "apiVersion": "1.0",
    "definitionVersion": "4.0.0",
    "type": "async",
    "description": "apiv4 with SSE entrypoint",
    "listeners": [
        {
            "type": "http",
            "paths": [
                {
                    "path": "/test-sse"
                }
            ],
            "entrypoints": [
                {
                    "type": "sse-advanced",
                    "configuration": {
                        "metadataAsComment": false, # Allow sending messages metadata to client as SSE comments. Each metadata will be sent as an extra line following ':key=value' format
                        "headersAsComment": false # Allow sending messages headers to client as SSE comments. Each header will be sent as an extra line following ':key=value' format
                    }
                }
            ]
        }
    ],
    ...
}
```
