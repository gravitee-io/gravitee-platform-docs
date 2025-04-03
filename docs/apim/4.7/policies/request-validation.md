---
description: This page provides the technical details of the Request Validation policy
hidden: true
---

# Request Validation

## Overview

You can use the `request-validation` policy to validate an incoming HTTP request according to defined rules. A rule is defined for an input value. This input value supports Expression Language expressions and is validated against constraint rules. By default, if none of the rules can be validated, the policy returns a `400` status code.

Functional and implementation information for the `request-validation` policy is organized into the following sections:

* [Examples](request-validation.md#examples)
* [Configuration](request-validation.md#configuration)
* [Compatibility Matrix](request-validation.md#compatibility-matrix)
* [Errors](request-validation.md#errors)
* [Changelogs](request-validation.md#changelogs)

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs and v4 HTTP proxy APIs. It cannot be applied to v4 message APIs or v4 TCP proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="HTTP proxy API example" %}
Sample policy configuration:

```json
"policy-request-validation": {
    "rules": [
        {
            "constraint": {
                "parameters": [
                    ".*\\\\.(txt)$"
                ],
                "type": "PATTERN"
            },
            "input": "{#request.pathInfos[2]}"
        }
    ],
    "status": "400"
}
```
{% endtab %}
{% endtabs %}

## Configuration

The `request-validation` policy supports the following constraint rules:

<table><thead><tr><th width="162.5">Constraint</th><th>Description</th></tr></thead><tbody><tr><td><code>NOT_NULL</code></td><td>Input value is required</td></tr><tr><td><code>MIN</code></td><td> Input value is a number and its value is greater than or equal to a given parameter</td></tr><tr><td><code>MAX</code></td><td>Input value is a number and its value is lower than or equal to a given parameter</td></tr><tr><td><code>MAIL</code></td><td>Input value is valid according to the mail pattern</td></tr><tr><td><code>DATE</code></td><td>Input value is valid according to the date format pattern given as a parameter</td></tr><tr><td><code>PATTERN</code></td><td>Input value is valid according to the pattern given as a parameter</td></tr><tr><td><code>SIZE</code></td><td>Input value length is between two given parameters</td></tr><tr><td><code>ENUM</code></td><td>Field value included in ENUM</td></tr></tbody></table>

### Phases

The phases checked below are supported by the `request-validation` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="196.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

The `request-validation` policy can be configured with the following options:

<table><thead><tr><th width="128">Property</th><th data-type="checkbox">Required</th><th width="216">Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>scope</td><td>true</td><td>Phase when the policy is executed</td><td>Policy scope</td><td>ON_REQUEST</td></tr><tr><td>status</td><td>true</td><td>HTTP status code send to the consumer in case of validation issues</td><td>HTTP status code</td><td>400</td></tr><tr><td>rules</td><td>true</td><td>Rules to apply to incoming request</td><td>List of rules</td><td>-</td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `request-validation` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>1.x</td><td>All</td></tr></tbody></table>

## Errors

<table><thead><tr><th width="198.5">HTTP status code</th><th>Message</th></tr></thead><tbody><tr><td><code>400</code></td><td>Incoming HTTP request can not be validated.</td></tr></tbody></table>

You can use the response template feature to override the default response provided by the policy. These templates must be defined at the API level (see the API Console **Response Templates** option in the API **Proxy** menu).

The error keys sent by this policy are as follows:

| Key                          | Parameters |
| ---------------------------- | ---------- |
| REQUEST\_VALIDATION\_INVALID | violations |

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-request-validation/blob/master/CHANGELOG.md" %}
