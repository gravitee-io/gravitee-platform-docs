# Assign Attributes

## Overview

You can use the `assign-attributes` policy to set variables such as request attributes and other execution context attributes.

You can use it to retrieve initial request attributes after `Transform headers` or `Transform query parameters` policies and reuse them in other policies (`Dynamic routing`, for example).

## Basic Usage

With this policy, you can do things like inject an attribute that will dynamically determine if the content passed in the request is in JSON format:

```json
"assign-attributes": {
  "attributes": [
    {
      "name": "isJson",
      "value": "'application/json'.equals(#request.headers['Content-Type'])"
    }
  ]
}
```

You can use the syntax `{#context.attributes['isJson']}` in subsequent policies to extract the result.

You can also inject complex objects into the context attributes:

```json
"assign-attributes": {
  "attributes": [
    {
      "name": "initialRequest",
      "value": "{#request}"
    }
  ]
}
```

To extract request attributes and get the Content-Type header you can use the following syntax:

```json
{#context.attributes['initialRequest'].headers['Content-Type']}
```

If you are using the policy in a message API, you can use the policy on the publish and subscribe phases to set attributes. You can access data at the message level with expressions like `{#message.headers['my-header'][0]}`. This can be used, for example, to set an attribute based on the message headers in a Kafka record.

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs, v4 HTTP proxy APIs, and v4 message APIs. It cannot be applied to v4 TCP proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="V2 API definition" %}
```json
{
  "name": "Assign Attributes v2",
  "flows" : [
    {
      "id" : "93998bb2-2612-4dcb-998b-b226121dcb64",
      "name" : "",
      "path-operator" : {
        "path" : "/",
        "operator" : "STARTS_WITH"
      },
      "condition": "",
      "consumers": [ ],
      "methods": [ ],
      "pre": [ 
        {
          "name" : "Assign attributes",
          "description" : "",
          "enabled" : true,
          "policy" : "policy-assign-attributes",
          "configuration" : {
            "scope":"REQUEST",
            "attributes": [
              {
                "name":"my-attribute",
                "value":"{#request.headers['Content-Type']}"
              }
            ]
          }
        }
      ],
      "post" : [ ],
      "enabled" : true
    } 
  ]
  ...
}
```
{% endtab %}

{% tab title="V4 API definition" %}
```json
{
  "api": {
    "name": "Assign Attributes",    
    "flows": [
      {
        "name": "",
        "enabled": true,
        "selectors": [
          {
            "type": "HTTP",
            "path": "/",
            "pathOperator": "EQUALS",
            "methods": []
          }
        ],
        "request": [
          {
            "name": "Assign attributes",
            "enabled": true,
            "policy": "policy-assign-attributes",
            "configuration": {
              "scope": "REQUEST",
              "attributes": [
                {
                  "name": "my-attribute",
                  "value": "{#request.headers['Content-Type']}"
                }
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

{% tab title="V2 API CRD" %}
```yaml
apiVersion: "gravitee.io/v1alpha1"
kind: "ApiDefinition"
metadata:
  name: "assign-attributes-v2-gko-api"
spec:
  name: "Assign Attributes V2 GKO API",
  flows:
  - name: "common-flow"
    path-operator:
      path: "/"
      operator: "STARTS_WITH"
    enabled: true
    pre:
    - name: "Assign attributes"
      description: "Assign an attribute"
      enabled: true
      policy: "policy-assign-attributes"
      configuration:
        scope: "REQUEST"
        attributes:
        - name: "my-attribute"
          value: "{#request.headers['Content-Type']}"
...
```
{% endtab %}

{% tab title="V4 API CRD" %}
```yaml
apiVersion: "gravitee.io/v1alpha1"
kind: "ApiV4Definition"
metadata:
  name: "assign-attributes-v4-gko-api"
spec:
  name: "Assign Attributes V4 GKO API"
  flows:
    - name: "common-flow"
      enabled: true
      selectors:
      - type: "HTTP"
        path: "/"
        pathOperator: "EQUALS"
      request:
      - name: "Assign attributes"
        enabled: true
        policy: "policy-assign-attributes"
        configuration:
          scope: "REQUEST"
          attributes:
          - name: "my-attribute"
            value: "{#request.headers['Content-Type']}"
...
```
{% endtab %}
{% endtabs %}

## Configuration

### Phases

The phases checked below are supported by the `assign-attributes` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="196.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>true</td><td>onResponse</td><td>true</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>true</td></tr><tr><td>onResponseContent</td><td>true</td><td>onMessageResponse</td><td>true</td></tr></tbody></table>

### Options

You can configure the `assign-attributes` policy with the following options:

<table><thead><tr><th width="134">Property</th><th>Required</th><th width="171">Description</th><th width="86">Type</th><th>Default</th></tr></thead><tbody><tr><td>scope</td><td>only for v4 proxy APIs</td><td>The execution scope (<code>request</code> or <code>response</code>)</td><td>string</td><td><code>REQUEST</code></td></tr><tr><td>attributes</td><td>X</td><td>List of attributes</td><td>See table below</td><td></td></tr></tbody></table>

### Attributes

You can configure the `assign-attributes` policy with the following attributes:

<table><thead><tr><th width="134">Property</th><th>Required</th><th width="171">Description</th><th width="86">Type</th><th>Default</th></tr></thead><tbody><tr><td>name</td><td>X</td><td>Attribute name</td><td>string</td><td></td></tr><tr><td>value</td><td>X</td><td>Attribute value (can be EL)</td><td>string</td><td></td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `assign-attributes` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>Up to 1.x</td><td>All</td></tr><tr><td>From 2.x</td><td>4.0+</td></tr></tbody></table>

## Errors

<table data-full-width="false"><thead><tr><th width="210">Phase</th><th width="171">HTTP status code</th><th width="387">Error template key</th></tr></thead><tbody><tr><td>onRequest</td><td><code>500</code></td><td>An error occurred while setting request attributes in the execution context</td></tr><tr><td>onResponse</td><td><code>500</code></td><td>An error occurred while setting request attributes in the execution context</td></tr><tr><td>onRequestContent</td><td><code>500</code></td><td>An error occurred while setting request attributes in the execution context</td></tr><tr><td>onResponseContent</td><td><code>500</code></td><td>An error occurred while setting request attributes in the execution context</td></tr><tr><td>onMessageRequest</td><td><code>500</code></td><td>An error occurred while setting request attributes in the execution context</td></tr><tr><td>onMessageResponse</td><td><code>500</code></td><td>An error occurred while setting request attributes in the execution context</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-assign-attributes/blob/master/CHANGELOG.md" %}
