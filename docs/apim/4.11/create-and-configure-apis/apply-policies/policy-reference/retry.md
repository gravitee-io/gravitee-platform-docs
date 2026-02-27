---
description: An overview about retry.
metaLinks:
  alternates:
    - retry.md
---

# Retry

## Overview

You can use the `retry` policy to replay requests when experiencing backend connection issues or if the response meets a given _condition_.

If the retry takes too long, relative to the `timeout` value, the request stops and returns status code `502`.

{% hint style="info" %}
To replay a request with a payload, the Gateway stores it in memory. We recommend you avoid applying it to requests with a large payload.
{% endhint %}

## Examples

{% hint style="warning" %}
This policy can only be applied to v2 APIs and v4 HTTP proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="HTTP proxy API example" %}
Sample policy configuration:

```json
{
  "retry": {
    "condition": "{#response.status > 500}",
    "maxRetries": 3,
    "timeout": 1000
  }
}
```
{% endtab %}
{% endtabs %}

## Configuration

### Phases

The phases checked below are supported by the `retry` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="202.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

The `retry` policy can be configured with the following options:

<table><thead><tr><th width="163">Property</th><th data-type="checkbox">Required</th><th width="296">Description</th><th>Default</th><th>Example</th></tr></thead><tbody><tr><td>condition</td><td>true</td><td>Condition to test to determine whether or not to retry the request (supports Expression Language)</td><td>-</td><td>{#response.status > 500}</td></tr><tr><td>maxRetries</td><td>true</td><td>Number of retries before failing (502 - Bad Gateway)</td><td>1</td><td>-</td></tr><tr><td>delay</td><td>false</td><td>Time between each attempt</td><td>0</td><td>-</td></tr><tr><td>timeout</td><td>true</td><td>Time after which an operation is considered a failure</td><td>1000</td><td>-</td></tr><tr><td>lastResponse</td><td>false</td><td>Returns the last attempt response, even if it failed regarding the configured condition. In timeout case, <code>502</code> is returned.</td><td>false</td><td>-</td></tr></tbody></table>

You can enable or disable the policy with policy identifier `retry`.

## Compatibility matrix

The following is the compatibility matrix for APIM and the `retry` policy:

| Plugin version | Supported APIM versions |
| -------------- | ----------------------- |
| 2.x            | All                     |

## Errors

<table data-full-width="false"><thead><tr><th width="194.5">HTTP status code</th><th width="387">Reason</th></tr></thead><tbody><tr><td><code>502</code></td><td><ul><li>No response satisfies the condition after <code>maxRetries</code></li><li>Technical errors when calling the backend (for example, connection refused, timeout)</li></ul></td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-retry/blob/master/CHANGELOG.md" %}
