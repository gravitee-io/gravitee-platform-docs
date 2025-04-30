---
hidden: true
---

# Transform Headers

## Overview

You can use the `transform-headers` policy to override HTTP headers in incoming requests or outbound responses. You can override the HTTP headers by:

* Adding to or updating the list of headers
* Removing headers individually
* Defining a whitelist
* Converting HTTP-based headers into Message Headers (specifically for publishing messages to Event Brokers using Protocol Mediation)

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs, v4 HTTP proxy APIs, and v4 message APIs. It cannot be applied to v4 TCP proxy APIs.
{% endhint %}

{% hint style="info" %}
The policy configuration for a v2 API using the legacy execution engine must include the `scope`. If the policy is applied to a v4 API or a v2 API using the emulated reactive engine, the configuration does not include `scope`.
{% endhint %}

{% tabs %}
{% tab title="v2 API definition" %}
```json
{
  "name": "Transform headers v2 API",
  "flows": [
    {
      "name": "common-flow",
      "path-operator": {
        "path": "/",
        "operator": "STARTS_WITH"
      },
      "pre": [
        {
          "name": "Transform Headers",
          "enabled": true,
          "policy": "transform-headers",
          "configuration": {
            "scope": "REQUEST",
            "whitelistHeaders": [
              ""
            ],
            "addHeaders": [
              {
                "name": "added-header",
                "value": "added-value"
              }
            ],
            "removeHeaders": [
              "removed-header"
            ]
          }
        }
      ],
      "enabled": true
    }
  ],
  ...
}
```

The below snippet shows how you can add a header from the request’s payload:

```json
"transform-headers": {
    "addHeaders": [
        {
            "name": "X-Product-Id",
            "value": "{#jsonPath(#request.content, '$.product.id')}"
        }
    ]
    "scope": "REQUEST_CONTENT"
}
```
{% endtab %}

{% tab title="v4 API definition" %}
```json
{
  "api": {
    "name": "Transform headers v4 proxy",
    "flows": [
      {
        "name": "common-flow",
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
            "name": "Transform Headers",
            "enabled": true,
            "policy": "transform-headers",
            "configuration": {
              "whitelistHeaders": [],
              "addHeaders": [
                {
                  "name": "add-header",
                  "value": "add-value"
                },
                {
                  "name": "X-Gravitee-Request-Id",
                  "value": "{#request.id}"
                }
              ],
              "scope": "REQUEST",
              "removeHeaders": [
                "remove-header"
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
  name: "transform-headers-v2-api"
spec:
  name: "Transform headers v2 API"
  flows:
  - name: "common-flow"
    enabled: true
    path-operator:
      path: "/"
      operator: "STARTS_WITH"
    pre:
    - name: "Transform Headers"
      enabled: true
      policy: "transform-headers"
      configuration:
        whitelistHeaders:
        - ""
        addHeaders:
        - name: "added-header"
          value: "added-value"
        scope: "REQUEST"
        removeHeaders:
        - "removed-header"
```
{% endtab %}

{% tab title="v4 API CRD" %}
```yaml
apiVersion: "gravitee.io/v1alpha1"
kind: "ApiV4Definition"
metadata:
  name: "transform-headers-v4-proxy"
spec:
  name: "Transform headers v4 proxy"
  flows:
  - name: "common-flow"
    enabled: true
    selectors:
    - type: "HTTP"
      path: "/"
      pathOperator: "EQUALS"
    request:
    - name: "Transform Headers"
      enabled: true
      policy: "transform-headers"
      configuration:
        scope: "REQUEST"
        whitelistHeaders: []
        addHeaders:
        - name: "add-header"
          value: "add-value"
        - name: "X-Gravitee-Request-Id"
          value: "{#request.id}"
        removeHeaders:
        - "remove-header"
```
{% endtab %}
{% endtabs %}

## Configuration

### Phases

The phases checked below are supported by the `transform-headers` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="204.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>true</td><td>onResponse</td><td>true</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>true</td></tr><tr><td>onResponseContent</td><td>true</td><td>onMessageResponse</td><td>true</td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `transform-headers` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>1.x</td><td>3.x</td></tr><tr><td>3.x</td><td>4.0+</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-transform-headers/blob/master/CHANGELOG.md" %}
