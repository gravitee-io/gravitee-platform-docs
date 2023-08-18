---
description: This page provides the technical details of the Assign Metrics policy
---

# Assign Metrics

{% hint style="warning" %}
**This feature requires** [**Gravitee's Enterprise Edition**](../../overview/introduction-to-gravitee-api-management-apim/ee-vs-oss.md)**.**
{% endhint %}

## Overview

You can use the `assign-metrics` policy to push extra metrics in addition to the natively provided request metrics.

These metrics can then be used from analytics dashboards to create custom widgets and, optionally, apply aggregations based on their value.

Functional and implementation information for the `assign-metrics` policy is organized into the following sections:

* [Examples](assign-metrics.md#examples)
* [Configuration](assign-metrics.md#configuration)
* [Compatibility Matrix](assign-metrics.md#compatibility-matrix)

## Examples

{% hint style="info" %}
This proxy API example also applies to v2 APIs. Currently, this policy can **not** be applied at the message level for v4 APIs.
{% endhint %}

{% tabs %}
{% tab title="Proxy API example" %}
To display your request distribution based on a particular HTTP header in your dashboards, create the custom metric shown below.

```
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
{% endtabs %}

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

You can enable or disable the policy with policy identifier `policy-assign-metrics`.

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into [phases](broken-reference/) that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines/). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the `assign-metrics` policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>true</td><td>onResponse</td><td>true</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>true</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

## Compatibility matrix

The [changelog for each version of APIM](../../releases-and-changelogs/changelogs/) provides a list of policies included in the default distribution. The chart below summarizes this information in relation to the `assign-metrics` policy.

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>1.x</td><td>Up to 3.1.7</td></tr><tr><td>2.x</td><td>3.18 to 3.20</td></tr><tr><td>3.x</td><td>4.0+</td></tr></tbody></table>
