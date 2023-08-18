---
description: This page provides the technical details of the Interrupt policy
---

# Interrupt

## Overview

Functional and implementation information for the Interrupt policy is organized into the following sections:

* [Configuration](interrupt.md#configuration)
* [Compatibility Matrix](interrupt.md#compatibility-matrix)
* [Errors](interrupt.md#errors)
* [Changelogs](interrupt.md#changelogs)

{% hint style="info" %}
This policy can be applied to [v2 APIs and v4 proxy APIs.](../../overview/gravitee-api-definitions-and-execution-engines/)

Currently, this policy can **not** be applied at the message level.
{% endhint %}

The `Interrupt` policy can be used to break the entire request processing in case of a condition This is defined on the policy. By default, if no policy condition is defined, the policy will always break request processing.

Breaking the request processing means that no more policies will be executed and no endpoint will be called by the gateway.

By default, the policy will return a response payload to the consumer which contains the `message` (see the configuration section).

If you want to override this standard response from the policy, you can define an `errorKey` which will be then be used to define a Response Template.

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

{% code title="Sample Configuration" %}
```json
"policy-interrupt": {
    "errorKey": "MY_CUSTOM_KEY",
    "message": "You got a problem, sir !",
    "variables": [{
        "name": "custom-variable",
        "value": "{#request.headers['origin']}"
    }]
}
```
{% endcode %}

### Reference

<table><thead><tr><th>Property</th><th data-type="checkbox">Required</th><th>Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>errorKey</td><td>true</td><td>The error Key to use for defining a Response Template</td><td>string</td><td>-</td></tr><tr><td>message</td><td>true</td><td>Default response template</td><td>string</td><td>-</td></tr><tr><td>variables</td><td>false</td><td>The variables for Response Template purpose</td><td>List of variables</td><td>-</td></tr></tbody></table>

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into phases that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines/). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the JSON-to-XML policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="188.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>true</td><td>onResponse</td><td>true</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>true</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

## Compatibility matrix

The [changelog for each version of APIM](../../releases-and-changelogs/changelogs/) provides a list of policies included in the default distribution. The chart below summarizes this information in relation to the `json-xml` policy.

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>>=1.x</td><td>>=3.10.x</td></tr></tbody></table>

## Errors

| Code  | Message                   |
| ----- | ------------------------- |
| `500` | Request processing broken |

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-interrupt/blob/master/CHANGELOG.md" %}
