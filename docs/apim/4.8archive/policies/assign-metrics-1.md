---
hidden: true
---

# Assign Metrics

{% hint style="warning" %}
**This feature requires** [**Gravitee's Enterprise Edition**](../../4.6/overview/gravitee-apim-enterprise-edition/)**.**
{% endhint %}

## Overview

You can use the `assign-metrics` policy to push extra metrics in addition to the natively provided request metrics.

These metrics can then be used from analytics dashboards to create custom widgets and, optionally, apply aggregations based on their value.

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs, v4 HTTP proxy APIs, and v4 message APIs. It cannot be applied to v4 TCP proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="HTTP proxy API example" %}
To display your request distribution based on a particular HTTP header in your dashboards, create the custom metric shown below:

```json
"assign-metrics": {
    "metrics": [
        {
            "name": "myCustomHeader,
            "value": "{#request.headers['X-MyCustomHeader'] != null ? #request.headers['X-MyCustomHeader'][0] : null}"
        }
    ]
}
```
{% endtab %}

{% tab title="Message API example" %}
An example of this policy applied at the message level is shown below:

```json
{
    "id": "subscribe-assign-metrics",
    "name": "subscribe-assign-metrics",
    "apiVersion": "1.0",
    "definitionVersion": "4.0.0",
    "type": "message",
    "analytics": {},
    "description": "subscribe-assign-metrics",
    "listeners": [
        {
            "type": "http",
            "paths": [
                {
                    "path": "/subscribe-assign-metrics"
                }
            ],
            "entrypoints": [
                {
                    "type": "sse",
                    "configuration": {
                        "heartbeatIntervalInMs": 5000,
                        "metadataAsComment": false,
                        "headersAsComment": true
                    }
                }
            ]
        }
    ],
    "endpointGroups": [
        {
            "name": "default",
            "type": "mock",
            "endpoints": [
                {
                    "name": "default",
                    "type": "mock",
                    "weight": 1,
                    "inheritConfiguration": false,
                    "configuration": {
                        "messageInterval": 500,
                        "messageContent": "custom-metric",
                        "messageCount": 12
                    }
                }
            ]
        }
    ],
    "flows": [
        {
            "name": "test-flow",
            "enabled": true,
            "selectors": [
                {
                    "type": "channel",
                    "operation": ["SUBSCRIBE"],
                    "channel": "/",
                    "channel-operator": "STARTS_WITH"
                }
            ],
            "request": [],
            "response": [],
            "subscribe": [
                {
                    "name": "Assign metrics",
                    "description": "",
                    "enabled": true,
                    "policy": "policy-assign-metrics",
                    "configuration": {
                        "metrics": [
                            {
                                "name": "content",
                                "value": "{#message.content}"
                            },
                            {
                                "name": "recordable",
                                "value": "{#message.attributes['message.recordable']}"
                            },
                            {
                                "name": "static",
                                "value": "value"
                            }
                        ]
                    }
                }
            ],
            "publish": []
        }
    ]
}
```
{% endtab %}
{% endtabs %}

## Configuration

You can enable or disable the policy with policy identifier `policy-assign-metrics`.

### Phases

The phases checked below are supported by the `assign-metrics` policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>true</td><td>onResponse</td><td>true</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>true</td></tr><tr><td>onResponseContent</td><td>true</td><td>onMessageResponse</td><td>true</td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `assign-metrics` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>1.x</td><td>Up to 3.1.7</td></tr><tr><td>2.x</td><td>3.18 to 3.20</td></tr><tr><td>3.x</td><td>4.0+</td></tr></tbody></table>
