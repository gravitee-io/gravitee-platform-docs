---
description: An overview about resource filtering.
---

# Resource Filtering

## Overview

You can use the `resource-filtering` policy to filter REST resources. By applying this filter, you can restrict or allow access to a specific resource determined by a path and a method (or an array of methods).

This policy is mainly used in plan configuration, to limit subscriber access to specific resources only.

## Basic Usage

A typical usage would be to allow access to all paths (`/**`) but in read-only mode (GET method).

```json
"resource-filtering" : {
    "whitelist":[
        {
            "pattern":"/**",
            "methods": ["GET"]
        }
    ]
}
```

#### "Deny access to all, except allowed users"

Another typical use case is to deny access to all, except specifically allowed users. In this scenario, we want to generically deny all access to any endpoint within the API, but allow specific users to specific paths/methods of the API. The below screenshot and policy configuration code describes our above scenario.

We have added the Resource Filtering policy to our JWT plan, and defined a Trigger condition on the policy: `{#context.attributes['jwt.claims']['scope'].contains('getInventory') == false}`.

If the authenticated client (i.e.: the access token) does not have the custom claim named `scope`, or the custom claim does not contain the value `getInventory`, then the policy is triggered and every endpoint path (`/**`) will be blacklisted, and the client will receive a <mark style="color:red;">`403`</mark> or <mark style="color:red;">`405`</mark> response status.

However, if the client's access token includes a custom claim `scope`, and it contains `getInventory`, then the Resource Filtering is NOT applied, and the client is allowed access to any specific endpoint path (within this API).

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs and v4 HTTP proxy APIs. It cannot be applied to v4 message APIs or v4 TCP proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="V2 API definition" %}
```json
{
  "name": "Resource Filtering v2",
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
          "name" : "Resource filtering",
          "description" : "Allow access to all paths",
          "enabled" : true,
          "policy" : "policy-resource-filtering",
          "configuration" : {
             "whitelist": [
              {
                "methods": ["GET"],
                "pattern": "/**"
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
    "name": "Resource Filtering",    
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
            "name": "Resource Filtering",
            "enabled": true,
            "policy": "resource-filtering",
            "configuration": {
              "blacklist": [
                {
                  "methods": [
                    "CONNECT",
                    "DELETE",
                    "GET",
                    "HEAD",
                    "OPTIONS",
                    "PATCH",
                    "POST",
                    "PUT",
                    "TRACE"
                  ],
                  "pattern": "/**"
                }
              ],
              "whitelist": []
            },
            "condition": "{#context.attributes['jwt.claims']['scope'].contains('getInventory') == false}"
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
  name: "resource-filtering-v2-gko-api"
spec:
  name: "Resource Filtering V2 GKO API",
  flows:
  - name: "common-flow"
    path-operator:
      path: "/"
      operator: "STARTS_WITH"
    enabled: true
    pre:
    - name: "Resource filtering"
      description: "Allow access to all paths"
      enabled: true
      policy: "policy-resource-filtering"
      configuration:
        whitelist:
        - methods:
          - "GET"
          pattern: "/**"
    ]
...
```
{% endtab %}

{% tab title="V4 API CRD" %}
```yaml
apiVersion: "gravitee.io/v1alpha1"
kind: "ApiV4Definition"
metadata:
  name: "resource-filtering-v4-gko-api"
spec:
  name: "Resource Filtering V4 GKO API"
  flows:
    - name: "common-flow"
      enabled: true
      selectors:
      - type: "HTTP"
        path: "/"
        pathOperator: "EQUALS"
      request:
      - name: "Resource Filtering"
        enabled: true
        policy: "resource-filtering"
        configuration:
           blacklist:
          - methods:
            - "CONNECT"
            - "DELETE"
            - "GET"
            - "HEAD"
            - "OPTIONS"
            - "PATCH"
            - "POST"
            - "PUT"
            - "TRACE"
            pattern: "/**"
          whitelist: []
        condition: "{#context.attributes['jwt.claims']['scope'].contains('getInventory') == false}"
...
```
{% endtab %}
{% endtabs %}

## Configuration

The implementation of the `resource-filtering` policy supports Ant-style path patterns, where URL mapping matches URLs using the following rules:

* `?` matches one character
* `*` matches zero or more characters
* `**` matches zero or more directories in a path

### Phases

The phases checked below are supported by the `resource-filtering` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="135" data-type="checkbox">Compatible?</th><th width="203.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

The `resource-filtering` policy can be configured with the following options:

<table><thead><tr><th width="156">Property</th><th data-type="checkbox">Required</th><th width="243">Description</th><th width="155">Type</th><th>Default</th></tr></thead><tbody><tr><td>whitelist</td><td>false</td><td>List of allowed resources</td><td>array of <a href="https://docs.gravitee.io/apim/3.x/apim_policies_resource_filtering.html#gravitee-policy-resource-filtering-resource"><code>resources</code></a></td><td>-</td></tr><tr><td>blacklist</td><td>false</td><td>List of restricted resources</td><td>array of <a href="https://docs.gravitee.io/apim/3.x/apim_policies_resource_filtering.html#gravitee-policy-resource-filtering-resource"><code>resources</code></a></td><td>-</td></tr></tbody></table>

{% hint style="info" %}
You can’t apply whitelisting and blacklisting to the same resource. Whitelisting takes precedence over blacklisting.
{% endhint %}

A resource is defined as follows:

<table><thead><tr><th width="122">Property</th><th data-type="checkbox">Required</th><th width="230">Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>pattern</td><td>true</td><td>An <a href="https://docs.gravitee.io/apim/3.x/apim_policies_resource_filtering.html#gravitee-policy-resource-filtering-ant">Ant-style path pattern</a> (<a href="http://ant.apache.org/">Apache Ant</a>).</td><td>string</td><td>-</td></tr><tr><td>methods</td><td>false</td><td>List of HTTP methods for which filter is applied.</td><td>array of HTTP methods</td><td>All HTTP methods</td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `resource-filtering` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>1.x</td><td>All</td></tr></tbody></table>

## Errors

| HTTP status code | Message                                                                   |
| ---------------- | ------------------------------------------------------------------------- |
| `403`            | Access to the resource is forbidden according to resource-filtering rules |
| `405`            | Method not allowed while accessing this resource                          |

You can use the response template feature to override the default responses provided by the policy. These templates must be defined at the API level (see the API Console **Response Templates** option in the API **Proxy** menu).

The error keys sent by this policy are as follows:

<table><thead><tr><th width="428.5">Key</th><th>Parameters</th></tr></thead><tbody><tr><td>RESOURCE_FILTERING_FORBIDDEN</td><td>path - method</td></tr><tr><td>RESOURCE_FILTERING_METHOD_NOT_ALLOWED</td><td>path - method</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-resource-filtering/blob/master/CHANGELOG.md" %}
