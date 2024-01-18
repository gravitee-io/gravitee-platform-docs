---
description: This page contains the technical details of the SSE entrypoint plugin
---

# Server-sent Events

{% hint style="warning" %}
**This feature requires** [**Gravitee's Enterprise Edition**](../../overview/ee-vs-oss/)**.**
{% endhint %}

## Overview

This _Advanced_ version aims to add _Entreprise features_ to the SSE endpoint in OSS version such as:

#### Quality Of Service <a href="#user-content-quality-of-service" id="user-content-quality-of-service"></a>

Better Quality Of Service are becoming available with this _Advanced_ version.

| QoS           | Delivery    | Description                            |
| ------------- | ----------- | -------------------------------------- |
| None          | Unwarranted | Already supported by OSS               |
| Balanced      | 0, 1 or n   | Already supported by OSS               |
| At-Best       | 0, 1 or n   | Support `Last-Event-ID` to improve QoS |
| At-Most-Once  | 0 or 1      | Support `Last-Event-ID` to improve QoS |
| At-Least-Once | 1 or n      | Support `Last-Event-ID` to improve QoS |

| Plugin version | APIM version |
| -------------- | ------------ |
| 1.x            | 3.19.x       |
| 2.x            | 3.20.x       |
| 3.x            | 3.21.x       |

#### Plugin identifier <a href="#user-content-plugin-identifier" id="user-content-plugin-identifier"></a>

To use this Advanced version of the plugin, declare the following `sse-advanced` identifier while configuring your API entrypoints.

Alternatively, you could update your existing API, thanks to compatibility of the Advanced and OSS configurations.

#### Configuration <a href="#user-content-configuration" id="user-content-configuration"></a>

When creating a new API, you can configure the plugin with the following parameters:

```json
{
    "name": "apiv4-sse",
    "apiVersion": "1.0",
    "definitionVersion": "4.0.0",
    "type": "async",
    "description": "apiv4 with SSE entrpoint",
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
                        "metadataAsComment": false,
                        "headersAsComment": false
                    }
                }
            ]
        }
    ],
    ...
}
```

| Note | <p><strong>metadataAsComment</strong>: Allow sending messages metadata to client as SSE comments. Each metadata will be sent as extra line following ':key=value' format</p><p><strong>headersAsComment</strong>: Allow sending messages headers to client as SSE comments. Each header will be sent as extra line following ':key=value' format</p> |
| ---- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
