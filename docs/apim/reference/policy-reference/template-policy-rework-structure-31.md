---
description: This page provides the technical details of the Retry policy
---

# Retry

## Overview

Functional and implementation information for the JSON-to-XML policy is organized into the following sections:

* [Configuration](template-policy-rework-structure-31.md#configuration)
* [Compatibility Matrix](template-policy-rework-structure-31.md#compatibility-matrix)
* [Errors](template-policy-rework-structure-31.md#errors)
* [Changelogs](template-policy-rework-structure-31.md#changelogs)

{% hint style="warning" %}
This example will work for [v2 APIs and v4 proxy APIs.](../../overview/gravitee-api-definitions-and-execution-engines.md)

Currently, this policy can **not** be applied at the message level.
{% endhint %}

You can use the `retry` policy to replay requests when experiencing backend connection issues or if the response meets a given _condition_.

If the retry takes too long, relative to the `timeout` value, the request stops and returns status code `502`.

{% hint style="info" %}
To replay a request with a payload, the gateway stores it in memory. We recommend you avoid applying it to requests with a large payload.
{% endhint %}

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

{% code title="Sample Configuration" %}
```json
{
  "retry": {
    "condition": "{#response.status > 500}",
    "maxRetries": 3,
    "timeout": 1000
  }
}

```
{% endcode %}

### Reference

<table><thead><tr><th>Property</th><th data-type="checkbox">Required</th><th>Description</th><th>Default</th><th>Example</th></tr></thead><tbody><tr><td>condition</td><td>true</td><td>Condition to test to determine whether or not to retry the request (supports Expression Language)</td><td>-</td><td>{#response.status > 500}</td></tr><tr><td>maxRetries</td><td>true</td><td>Number of retries before failing (502 - Bad Gateway)</td><td>1</td><td>-</td></tr><tr><td>delay</td><td>false</td><td>Time between each attempt</td><td>0</td><td>-</td></tr><tr><td>timeout</td><td>true</td><td>Time after which an operation is considered a failure</td><td>1000</td><td>-</td></tr><tr><td>lastResponse</td><td>false</td><td>Returns the last attempt response, even if it failed regarding the configured condition. In timeout case, <code>502</code> is returned.</td><td>false</td><td>-</td></tr></tbody></table>

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into [phases](broken-reference) that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the Retry policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="188.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

## Compatibility matrix

The [changelog for each version of APIM](../../releases-and-changelog/changelog/) provides a list of policies included in the default distribution. The chart below summarizes this information in relation to the `json-xml` policy.

| Plugin version | Supported APIM versions |
| -------------- | ----------------------- |
| 2.x and upper  | 3.10.x to latest        |
| Up to 1.x      | Up to 3.9.x             |

## Errors

<table data-full-width="false"><thead><tr><th width="171">HTTP status code</th><th width="387">Reason</th></tr></thead><tbody><tr><td><code>502</code></td><td><p>Received in the following cases:</p><ul><li>No response satisfies the condition after <code>maxRetries</code></li><li>Technical errors when calling the backend (for example, connection refused, timeout)</li></ul></td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-retry/blob/master/CHANGELOG.md" %}
