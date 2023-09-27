---
description: >-
  This page provides the technical details of the Transform Query Parameters
  policy
---

# Transform Query Parameters

## Overview

You can use the `transformqueryparams` policy to override incoming HTTP request query parameters. You can override the HTTP query parameters by:

* Clearing all existing query parameters
* Adding to or updating the list of query parameters
* Removing query parameters individually

The query parameter values of the incoming request are accessible via the `{#request.params['query_parameter_name']}` construct.

Functional and implementation information for the `transformqueryparams` policy is organized into the following sections:

* [Examples](transform-query-parameters.md#examples)
* [Configuration](transform-query-parameters.md#configuration)
* [Compatibility Matrix](transform-query-parameters.md#compatibility-matrix)
* [Changelogs](transform-query-parameters.md#changelogs)

## Examples

{% hint style="warning" %}
This policy can be applied to [v2 APIs and v4 proxy APIs.](../../overview/gravitee-api-definitions-and-execution-engines/) Currently, this policy can **not** be applied at the message level.
{% endhint %}

{% tabs %}
{% tab title="Proxy API example" %}
The example below shows how to add the ID of the incoming request to the outgoing request:

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
{% endtab %}
{% endtabs %}

## Configuration

### Phases

The phases checked below are supported by the `transformqueryparams` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="133" data-type="checkbox">Compatible?</th><th width="200.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `transformqueryparams` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>1.x</td><td>All</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-transformqueryparams/blob/master/CHANGELOG.md" %}
