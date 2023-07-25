---
description: This page provides the technical details of the Traffic Shadowing policy
---

# Traffic Shadowing

## Overview

Functional and implementation information for the JSON-to-XML policy is organized into the following sections:

* [Configuration](traffic-shadowing.md#configuration)
* [Compatibility Matrix](traffic-shadowing.md#compatibility-matrix)
* [Changelogs](traffic-shadowing.md#changelogs)

{% hint style="warning" %}
This policy can be applied to [v2 APIs and v4 proxy APIs.](../../overview/gravitee-api-definitions-and-execution-engines.md)

Currently, this policy can **not** be applied at the message level.
{% endhint %}

Traffic shadowing allows to asynchronously copy the traffic to another service. By using this policy, the requests are duplicated and sent to the target. The target is an endpoint defined at the API level. The request can be enriched with additional headers.

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

{% code title="Sample Configuration" %}
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
{% endcode %}

### Reference

<table><thead><tr><th>Property</th><th data-type="checkbox">Required</th><th>Description</th><th>Default</th><th>Example</th></tr></thead><tbody><tr><td>target</td><td>true</td><td>The target endpoint (supports EL).</td><td>-</td><td>{#endpoints['my-endpoint']}</td></tr><tr><td>headers</td><td>false</td><td>A list of HTTP headers.</td><td>-</td><td>-</td></tr></tbody></table>

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into [phases](broken-reference) that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the JSON-to-XML policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="188.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

## Compatibility matrix

The [changelog for each version of APIM](../../releases-and-changelog/changelog/) provides a list of policies included in the default distribution. The chart below summarizes this information in relation to the `traffic-shadowing` policy.

| Plugin version | Supported APIM versions            |
| -------------- | ---------------------------------- |
| 2.x and upper  | 3.18.20, 3.19.9, 3.20.3 and upper. |
| Up to 1.1.x    | Up to 3.14.x                       |

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-traffic-shadowing/blob/master/CHANGELOG.md" %}
