---
description: An overview about ---.
hidden: true
---

# Transform Query Parameters

## Overview

You can use the `transformqueryparams` policy to override incoming HTTP request query parameters. You can override the HTTP query parameters by:

* Clearing all existing query parameters
* Adding to or updating the list of query parameters
* Removing query parameters individually

The query parameter values of the incoming request are accessible via the `{#request.params['query_parameter_name']}` construct.

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs and v4 HTTP proxy APIs. It cannot be applied to v4 message APIs or v4 TCP proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="v2 API definition" %}
```json
{
  "name": "Transform query parameters v2 API",
  "flows": [
    {
      "name": "common-flow",
      "path-operator": {
        "path": "/",
        "operator": "STARTS_WITH"
      },
      "pre": [
        {
          "name": "Transform Query Parameters",
          "description": "",
          "enabled": true,
          "policy": "transform-queryparams",
          "configuration": {
            "addQueryParameters": [
              {
                "name": "add-query-parameter",
                "value": "added-value",
                "appendToExistingArray": false
              },
              {
                "name": "add-dynamic-query-parameter",
                "value": "{#request.id}",
                "appendToExistingArray": false
              }
            ],
            "removeQueryParameters": [
              "remove-query-parameter"
            ]
          }
        }
      ],
      "post": [],
      "enabled": true
    }
  ],
  ...
}
```
{% endtab %}

{% tab title="v4 API definition" %}
```json
{
  "api": {
    "name": "Transform query parameters v4 proxy",
    "flows": [
      {
        "name": "common-flow",
        "enabled": true,
        "selectors": [
          {
            "type": "HTTP",
            "path": "/",
            "pathOperator": "EQUALS"
          }
        ],
        "request": [
          {
            "name": "Transform Query Parameters",
            "enabled": true,
            "policy": "transform-queryparams",
            "configuration": {
              "addQueryParameters": [
                {
                  "name": "add-query-parameter",
                  "value": "query-parameter-value",
                  "appendToExistingArray": false
                },
                {
                  "name": "add-dynamic-query-parameter",
                  "value": "{#request.id}",
                  "appendToExistingArray": false
                }
              ],
              "removeQueryParameters": [
                "remove-query-parameter"
              ]
            }
          }
        ]
      }
    ],
    ...
  }
  ...
}
```
{% endtab %}

{% tab title="v2 API CRD" %}
```yaml
apiVersion: "gravitee.io/v1alpha1"
kind: "ApiDefinition"
metadata:
  name: "transform-query-parameters-v2-api"
spec:
  name: "Transform query parameters v2 API"
  flows:
  - name: "common-flow"
    enabled: true
    path-operator:
      path: "/"
      operator: "STARTS_WITH"
    pre:
    - name: "Transform Query Parameters"
      enabled: true
      policy: "transform-queryparams"
      configuration:
        addQueryParameters:
        - name: "add-query-parameter"
          value: "added-value"
          appendToExistingArray: false
        - name: "add-dynamic-query-parameter"
          value: "{#request.id}"
          appendToExistingArray: false
        removeQueryParameters:
        - "remove-query-parameter"
  ...
```
{% endtab %}

{% tab title="v4 API CRD" %}
```yaml
apiVersion: "gravitee.io/v1alpha1"
kind: "ApiV4Definition"
metadata:
  name: "transform-query-parameters-v4-proxy"
spec:
  name: "Transform query parameters v4 proxy"
  flows:
  - name: "common-flow"
    enabled: true
    selectors:
    - type: "HTTP"
      path: "/"
      pathOperator: "EQUALS"
    request:
    - name: "Transform Query Parameters"
      enabled: true
      policy: "transform-queryparams"
      configuration:
        addQueryParameters:
        - name: "add-query-parameter"
          value: "query-parameter-value"
          appendToExistingArray: false
        - name: "add-dynamic-query-parameter"
          value: "{#request.id}"
          appendToExistingArray: false
        removeQueryParameters:
        - "remove-query-parameter"
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
