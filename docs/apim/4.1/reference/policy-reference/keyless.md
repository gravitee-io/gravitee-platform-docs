---
description: This page provides the technical details of the Keyless policy
---

# Keyless

## Overview

This security policy does not block any requests as it considers them as valid by default.

It sets multiple attributes during policy execution, as follows:

* `application`: Anonymous application value, which is equal to `1`.
* `user-id`: Internet Protocol (IP) address of the client or last proxy that sent the request.

Functional and implementation information for the `keyless` policy is organized into the following sections:

* [Examples](keyless.md#examples)
* [Configuration](keyless.md#configuration)
* [Compatibility Matrix](keyless.md#compatibility-matrix)
* [Errors](keyless.md#errors)
* [Changelogs](keyless.md#changelogs)

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs and v4 proxy APIs. It cannot be applied to v4 message APIs.
{% endhint %}

{% tabs %}
{% tab title="Proxy API example" %}
Sample policy configuration:

```json
{
    "id": "my-api",
    "name": "my-api",
    "gravitee": "2.0.0",
    "proxy": {
        "context_path": "/test",
        "endpoints": [
            {
                "name": "default",
                "target": "http://localhost:8080/team",
                "http": {
                    "connectTimeout": 3000,
                    "readTimeout": 60000
                }
            }
        ]
    },
    "flows": [
        {
            "name": "flow-1",
            "methods": ["GET"],
            "enabled": true,
            "path-operator": {
                "path": "/",
                "operator": "STARTS_WITH"
            },
            "pre": [
                {
                    "name": "Key less",
                    "description": "",
                    "enabled": true,
                    "policy": "key-less",
                    "configuration": {}
                }
            ],
            "post": []
        }
    ],
    "resources": []
}
```
{% endtab %}
{% endtabs %}

## Configuration

### Phases

The phases checked below are supported by the `keyless` policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="137" data-type="checkbox">Compatible?</th><th width="199.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `keyless` policy:

| Plugin version | Supported APIM versions |
| -------------- | ----------------------- |
| 1.x            | Up to 3.20              |
| 3.x            | 4.0+                    |

## Errors

This policy cannot fail as it does not carry out any validation.

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-keyless/blob/master/CHANGELOG.md" %}
