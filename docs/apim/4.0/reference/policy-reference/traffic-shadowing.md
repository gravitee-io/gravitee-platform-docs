---
description: This page provides the technical details of the Traffic Shadowing policy
---

# Traffic Shadowing

## Overview

Traffic shadowing allows to asynchronously copy the traffic to another service. By using this policy, the requests are duplicated and sent to the target. The target is an endpoint defined at the API level. The request can be enriched with additional headers.

Functional and implementation information for the `traffic-shadowing` policy is organized into the following sections:

* [Examples](traffic-shadowing.md#examples)
* [Configuration](traffic-shadowing.md#configuration)
* [Compatibility Matrix](traffic-shadowing.md#compatibility-matrix)
* [Changelogs](traffic-shadowing.md#changelogs)

## Examples

{% hint style="warning" %}
This policy can be applied to [v2 APIs and v4 proxy APIs.](../../overview/gravitee-api-definitions-and-execution-engines/) Currently, this policy can **not** be applied at the message level.
{% endhint %}

{% tabs %}
{% tab title="Proxy API example" %}
```json
{
  "traffic-shadowing": {
    "target": "{#endpoints['target-endpoint']}",
    "headers": [
        {
            "name": "X-Gravitee-Request-Id",
            "value": "{#request.id}"
        }
    ]
  }
}
```
{% endtab %}
{% endtabs %}

## Configuration

### Phases

The phases checked below are supported by the `traffic-shadowing` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="138" data-type="checkbox">Compatible?</th><th width="211.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

The `traffic-shadowing` policy can be configured with the following options:

<table><thead><tr><th width="147">Property</th><th data-type="checkbox">Required</th><th width="228">Description</th><th width="87">Default</th><th>Example</th></tr></thead><tbody><tr><td>target</td><td>true</td><td>The target endpoint (supports EL).</td><td>-</td><td>{#endpoints['my-endpoint']}</td></tr><tr><td>headers</td><td>false</td><td>A list of HTTP headers.</td><td>-</td><td>-</td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `traffic-shadowing` policy:

| Plugin version | Supported APIM versions            |
| -------------- | ---------------------------------- |
| 2.x and upper  | 3.18.20, 3.19.9, 3.20.3 and upper. |

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-traffic-shadowing/blob/master/CHANGELOG.md" %}