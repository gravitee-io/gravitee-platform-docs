---
description: This page provides the technical details of the Request Validation policy
---

# Request Validation

## Overview

Functional and implementation information for the JSON-to-XML policy is organized into the following sections:

* [Configuration](template-policy-rework-structure-33.md#configuration)
* [Compatibility](template-policy-rework-structure-33.md#compatibility-matrix)
* [Errors](template-policy-rework-structure-33.md#errors)
* [Changelogs](template-policy-rework-structure-33.md#changelogs)

{% hint style="warning" %}
This example will work for [v2 APIs and v4 proxy APIs.](../../overview/gravitee-api-definitions-and-execution-engines.md)

Currently, this policy can **not** be applied at the message level.
{% endhint %}

You can use the `request-validation` policy to validate an incoming HTTP request according to defined rules. A rule is defined for an input value. This input value supports Expression Language expressions and is validated against constraint rules.

Constraint rules can be:

* `NOT_NULL` — Input value is required
* `MIN` — Input value is a number and its value is greater than or equal to a given parameter
* `MAX` — Input value is a number and its value is lower than or equal to a given parameter
* `MAIL` — Input value is valid according to the mail pattern
* `DATE` — Input value is valid according to the date format pattern given as a parameter
* `PATTERN` — Input value is valid according to the pattern given as a parameter
* `SIZE` — Input value length is between two given parameters
* `ENUM` — Field value included in ENUM

By default, if none of the rules can be validated, the policy returns a `400` status code.

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

{% code title="Sample Configuration" %}
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
{% endcode %}

### Reference

<table><thead><tr><th>Property</th><th data-type="checkbox">Required</th><th>Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>scope</td><td>true</td><td>Phase when the policy is executed</td><td>Policy scope</td><td>ON_REQUEST</td></tr><tr><td>status</td><td>true</td><td>HTTP status code send to the consumer in case of validation issues</td><td>HTTP status code</td><td>400</td></tr><tr><td>rules</td><td>true</td><td>Rules to apply to incoming request</td><td>List of rules</td><td>-</td></tr></tbody></table>

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into [phases](broken-reference) that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the JSON-to-XML policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="188.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

## Compatibility matrix

The [changelog for each version of APIM](../../releases-and-changelog/changelog/) provides a list of policies included in the default distribution. The chart below summarizes this information in relation to the `json-xml` policy.

<table data-full-width="false"><thead><tr><th width="161.33333333333331">Plugin Version</th><th width="242">Supported APIM versions</th><th>Included in APIM default distribution</th></tr></thead><tbody><tr><td>2.2</td><td>>=3.20</td><td>>=3.21</td></tr><tr><td>2.1</td><td>^3.0</td><td>>=3.0 &#x3C;3.21</td></tr><tr><td>2.0</td><td>^3.0</td><td>N/a</td></tr></tbody></table>

## Errors

#### HTTP status code

| Code  | Message                                     |
| ----- | ------------------------------------------- |
| `400` | Incoming HTTP request can not be validated. |

#### Default response override

You can use the response template feature to override the default response provided by the policy. These templates must be defined at the API level (see the API Console **Response Templates** option in the API **Proxy** menu).

#### Error keys

The error keys sent by this policy are as follows:

| Key                          | Parameters |
| ---------------------------- | ---------- |
| REQUEST\_VALIDATION\_INVALID | violations |

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-request-validation/blob/master/CHANGELOG.md" %}
