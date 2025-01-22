---
description: This page provides the technical details of the Interrupt policy
hidden: true
---

# Interrupt

## Overview

The `Interrupt` policy can be used to break the entire request processing in case of a condition This is defined on the policy. By default, if no policy condition is defined, the policy will always break request processing.

Breaking the request processing means that no more policies will be executed and no endpoint will be called by the gateway.

By default, the policy will return a response payload to the consumer which contains the `message`.

If you want to override this standard response from the policy, you can define an `errorKey` which will be then be used to define a Response Template.

Functional and implementation information for the `Interrupt` policy is organized into the following sections:

* [Examples](interrupt.md#examples)
* [Configuration](interrupt.md#configuration)
* [Compatibility Matrix](interrupt.md#compatibility-matrix)
* [Errors](interrupt.md#errors)
* [Changelogs](interrupt.md#changelogs)

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs and v4 HTTP proxy APIs. It cannot be applied to v4 message APIs or v4 TCP proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="HTTP proxy API example" %}
Sample policy configuration:

```json
"policy-interrupt": {
    "errorKey": "MY_CUSTOM_KEY",
    "message": "You got a problem, sir!",
    "variables": [{
        "name": "custom-variable",
        "value": "{#request.headers['origin']}"
    }]
}
```
{% endtab %}
{% endtabs %}

## Configuration

### Phases

The phases checked below are supported by the `Interrupt` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="206.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>true</td><td>onResponse</td><td>true</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>true</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

The `Interrupt` policy can be configured with the following options:

<table><thead><tr><th width="143">Property</th><th width="115" data-type="checkbox">Required</th><th width="188">Description</th><th width="119">Type</th><th>Default</th></tr></thead><tbody><tr><td>errorKey</td><td>true</td><td>The error Key to use for defining a Response Template</td><td>string</td><td>-</td></tr><tr><td>message</td><td>true</td><td>Default response template</td><td>string</td><td>-</td></tr><tr><td>variables</td><td>false</td><td>The variables for Response Template purpose</td><td>List of variables</td><td>-</td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `Interrupt` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>1.x+</td><td>3.10.x+</td></tr></tbody></table>

## Errors

| Code  | Message                   |
| ----- | ------------------------- |
| `500` | Request processing broken |

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-interrupt/blob/master/CHANGELOG.md" %}
