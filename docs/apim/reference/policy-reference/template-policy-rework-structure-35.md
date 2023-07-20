---
description: >-
  This page provides the technical details of the Transform Query Parameters
  policy
---

# Transform Query Parameters

## Overview

Functional and implementation information for the JSON-to-XML policy is organized into the following sections:

* [Configuration](template-policy-rework-structure-35.md#configuration)
* [Compatibility](template-policy-rework-structure-35.md#compatibility-matrix)
* [Changelogs](template-policy-rework-structure-35.md#changelogs)

{% hint style="warning" %}
This example will work for [v2 APIs and v4 proxy APIs.](../../overview/gravitee-api-definitions-and-execution-engines.md)

Currently, this policy can **not** be applied at the message level.
{% endhint %}

You can use the `transformqueryparams` policy to override incoming HTTP request query parameters. You can override the HTTP query parameters by:

* Clearing all existing query parameters
* Adding to or updating the list of query parameters
* Removing query parameters individually

The query parameter values of the incoming request are accessible via the `{#request.params['query_parameter_name']}` construct

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

{% code title="Sample Configuration" %}
```json
"transform-queryparams": {
    "addQueryParameters": [
        {
            "name": "myParam",
            "value": "{#request.id}"
        }
    ],
    "removeQueryParameters": [
        "secretParam"
    ]
}
```
{% endcode %}

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into [phases](broken-reference) that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the Transform Query Parameters policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="188.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

## Compatibility

The [changelog for each version of APIM](../../releases-and-changelog/changelog/) provides a list of policies included in the default distribution.&#x20;

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-transformqueryparams/blob/master/CHANGELOG.md" %}
