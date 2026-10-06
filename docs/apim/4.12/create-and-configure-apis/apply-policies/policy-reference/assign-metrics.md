---
description: The Assign Metrics policy pushes extra metrics alongside the native request metrics in API Management 4.12. Learn how to configure it.
metaLinks:
  alternates:
    - assign-metrics.md
---

# Assign Metrics

{% hint style="warning" %}
**This feature requires** [**Gravitee's Enterprise Edition**](../../../introduction/enterprise-edition.md)**.**
{% endhint %}

## Overview

You can use the `assign-metrics` policy to push extra metrics in addition to the natively provided request metrics.

These metrics can then be used from analytics dashboards to create custom widgets and, optionally, apply aggregations based on their value.

Each metric has a name and a value. The Gateway evaluates the value with Gravitee Expression Language and records the result as a string. When the expression resolves to nothing, the Gateway records no metric for it.

This policy is applicable to the following API types:

* v2 APIs
* v4 HTTP proxy APIs
* v4 message APIs
* v4 LLM proxy APIs
* v4 MCP proxy APIs
* v4 A2A proxy APIs

**Note:** The `assign-metrics` policy isn't supported by v4 TCP proxy APIs or v4 native Kafka APIs.

## Metrics on LLM proxy APIs

On a v4 [LLM proxy](../../../ai-agent-management/llm-proxy/README.md) API, the endpoint publishes token counts and costs as it reads the LLM response body, which happens after the response phase of the flow has run. So that a metric can read those values, the policy evaluates response-phase metrics once the response body has been read in full, instead of when the response phase starts. This applies to streamed and non-streamed LLM responses alike. Every other API type evaluates response-phase metrics when the response phase runs, unchanged.

Deferring the evaluation doesn't change how often a metric is evaluated or how the response reaches the client. Each metric is evaluated once per request, and the Gateway relays the response chunk by chunk as it did before. If the response stream fails part way through, the Gateway still records each metric from the values published up to that point.

The following context attributes are available to a response-phase metric on an LLM proxy API:

<table>
    <thead>
        <tr>
            <th width="330">Context attribute</th>
            <th>Value</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>llmproxy.usage.sent.token</code></td>
            <td>Input token count read from the LLM response</td>
        </tr>
        <tr>
            <td><code>llmproxy.usage.received.token</code></td>
            <td>Output token count read from the LLM response</td>
        </tr>
        <tr>
            <td><code>llmproxy.usage.sent.cost</code></td>
            <td>Cost of the input tokens, set only when the endpoint resolves a price for the model</td>
        </tr>
        <tr>
            <td><code>llmproxy.usage.received.cost</code></td>
            <td>Cost of the output tokens, set only when the endpoint resolves a price for the model</td>
        </tr>
        <tr>
            <td><code>llmproxy.usage.price.unavailable</code></td>
            <td><code>true</code> when the LLM response reports usage and the endpoint can't resolve a price for the model</td>
        </tr>
    </tbody>
</table>

The `llmproxy.model` context attribute holds the model the client asked for, which the LLM proxy reads from the request. The model named in the LLM response is reported by the built-in `keyword_llm-proxy_model` metric rather than by a context attribute. When the response names no model, that metric falls back to the model the request targeted.

## Examples

The following examples show the policy configured on three of the API types it supports.

### HTTP proxy API example

To display your request distribution based on a particular HTTP header in your dashboards, create the custom metric shown below:

```json
"assign-metrics": {
    "metrics": [
        {
            "name": "myCustomHeader",
            "value": "{#request.headers['X-MyCustomHeader'] != null ? #request.headers['X-MyCustomHeader'][0] : null}"
        }
    ]
}
```

### LLM proxy API example

To record the token counts an LLM reported and the model the client requested, add the metrics below to the response phase of an LLM proxy API flow:

```json
"assign-metrics": {
    "metrics": [
        {
            "name": "inputTokens",
            "value": "{#context.attributes['llmproxy.usage.sent.token']}"
        },
        {
            "name": "outputTokens",
            "value": "{#context.attributes['llmproxy.usage.received.token']}"
        },
        {
            "name": "requestedModel",
            "value": "{#context.attributes['llmproxy.model']}"
        }
    ]
}
```

### Message API example

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

## Configuration

You can enable or disable the policy with policy identifier `policy-assign-metrics`.

### Phases

The phases checked below are supported by the `assign-metrics` policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>true</td><td>onResponse</td><td>true</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>true</td></tr><tr><td>onResponseContent</td><td>true</td><td>onMessageResponse</td><td>true</td></tr></tbody></table>

On v4 LLM proxy, MCP proxy, and A2A proxy APIs, the policy runs in the request and response phases. These API types have no message phases.

## Compatibility matrix

The following is the compatibility matrix for APIM and the `assign-metrics` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>1.x</td><td>Up to 3.17</td></tr><tr><td>2.x</td><td>3.18 to 3.20</td></tr><tr><td>3.x</td><td>4.0 and later</td></tr><tr><td>4.x</td><td>4.8 and later</td></tr><tr><td>5.x</td><td>4.10 and later</td></tr></tbody></table>

APIM 4.12.18 and later bundle plugin version 5.0.0. Support for LLM proxy and A2A proxy APIs was added in plugin version 5.0.0, and support for MCP proxy APIs in plugin version 4.1.0.
