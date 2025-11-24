---
description: An overview about latency.
---

# Latency

## Overview

You can use the `latency` policy to add latency to either the request or the response. For example, if you configure the policy on the request with a latency of 100ms, the Gateway waits 100ms before routing the request to the backend service.

This policy is particularly useful in two scenarios:

* Testing: adding latency allows you to test client applications when APIs are slow to respond.
* Monetization: a longer latency can be added to free plans to encourage clients to move to a better (or paid) plan.

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs, v4 HTTP proxy APIs, and v4 message APIs. It cannot be applied to v4 TCP proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="HTTP proxy API example" %}
Example policy configuration for a proxy API:

```json
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
```
{% endtab %}

{% tab title="Message API example" %}
Example subscription configuration for a message API:

```json
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
