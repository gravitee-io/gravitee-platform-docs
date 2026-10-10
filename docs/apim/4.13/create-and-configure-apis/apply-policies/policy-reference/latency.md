---
description: The Latency policy adds artificial delay to a request or a response in API Management 4.13. Learn how to configure the delay.
metaLinks:
  alternates:
    - latency.md
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

To read the time to wait from the request, set `dynamicTime`. The following configuration reads it, in seconds, from the `X-Latency` request header:

```json
{
    "name": "Latency policy",
    "description": "",
    "enabled": true,
    "policy": "latency",
    "configuration": {
        "dynamicTime": "{#request.headers['X-Latency'][0]}",
        "timeUnit": "SECONDS"
    }
}
```

{% hint style="warning" %}
The policy doesn't cap the time that `dynamicTime` returns. If the expression reads a value that the client sends, such as a header or a query parameter, make sure the value is controlled and bounded.
{% endhint %}

## Configuration

### Phases

The phases checked below are supported by the `latency` policy:

<table data-full-width="false">
    <thead>
        <tr>
            <th width="209">v2 Phases</th>
            <th width="139" data-type="checkbox">Compatible?</th>
            <th width="199.41136671177264">v4 Phases</th>
            <th data-type="checkbox">Compatible?</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>onRequest</code></td>
            <td>true</td>
            <td><code>onRequest</code></td>
            <td>true</td>
        </tr>
        <tr>
            <td><code>onResponse</code></td>
            <td>true</td>
            <td><code>onResponse</code></td>
            <td>true</td>
        </tr>
        <tr>
            <td><code>onRequestContent</code></td>
            <td>false</td>
            <td><code>onMessageRequest</code></td>
            <td>true</td>
        </tr>
        <tr>
            <td><code>onResponseContent</code></td>
            <td>false</td>
            <td><code>onMessageResponse</code></td>
            <td>true</td>
        </tr>
    </tbody>
</table>

### Options

You can configure the `latency` policy with the following options:

<table>
    <thead>
        <tr>
            <th width="116">Property</th>
            <th width="105" data-type="checkbox">Required</th>
            <th width="274">Description</th>
            <th width="100">Type</th>
            <th>Default</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>time</code></td>
            <td>false</td>
            <td>Time to wait, in the unit set by <code>timeUnit</code></td>
            <td>integer</td>
            <td>100</td>
        </tr>
        <tr>
            <td><code>dynamicTime</code></td>
            <td>false</td>
            <td>Gravitee Expression Language expression that returns the time to wait, in the unit set by <code>timeUnit</code>. When it's set, the policy ignores <code>time</code>, even if the expression fails. In the <code>onMessageRequest</code> and <code>onMessageResponse</code> phases, the expression is evaluated for each message.</td>
            <td>string</td>
            <td>-</td>
        </tr>
        <tr>
            <td><code>timeUnit</code></td>
            <td>false</td>
            <td>Time unit ( <code>"MILLISECONDS"</code> or <code>"SECONDS"</code>)</td>
            <td>string</td>
            <td><code>"MILLISECONDS"</code></td>
        </tr>
    </tbody>
</table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `latency` policy.

| Plugin version | APIM version |
| -------------- | ------------ |
| Up to 1.3.x    | Up to 3.9.x  |
| 1.4.x          | Up to 3.20   |
| 2.x            | 4.x+         |
| 3.x            | 4.7.x+       |

APIM 4.12.22 and later bundle version 3.1.0 of the policy. Support for the `onResponse` phase and the `dynamicTime` option was added in version 3.1.0.

## Errors

When the policy can't resolve the time from `dynamicTime` in the `onRequest` or `onResponse` phase, the request fails with the following error:

<table data-full-width="false">
    <thead>
        <tr>
            <th>HTTP status code</th>
            <th>Message</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>500</code></td>
            <td><code>Invalid latency time</code></td>
        </tr>
    </tbody>
</table>

In the `onMessageRequest` and `onMessageResponse` phases, the same error interrupts the message flow instead.

The `latency` policy raises one error key:

| Key                    | Raised when                                                                                                                                                   |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `LATENCY_INVALID_TIME` | The `dynamicTime` expression fails, returns no value, or returns a number lower than 0, for example because the header it reads is missing or isn't a number. |

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-latency/blob/master/CHANGELOG.md" %}
