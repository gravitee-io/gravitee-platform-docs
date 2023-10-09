---
description: This page provides the technical details of the Transform Headers policy
---

# Transform Headers

## Overview

You can use the `transform-headers` policy to override HTTP headers in incoming requests or outbound responses. You can override the HTTP headers by:

* Adding to or updating the list of headers
* Removing headers individually
* Defining a whitelist == Compatibility with APIM

Functional and implementation information for the `transform-headers` policy is organized into the following sections:

* [Examples](transform-headers.md#examples)
* [Configuration](transform-headers.md#configuration)
* [Compatibility Matrix](transform-headers.md#compatibility-matrix)
* [Changelogs](transform-headers.md#changelogs)

## Examples

{% hint style="warning" %}
This policy can be applied to all Gravitee APIs: v2 APIs, v4 proxy APIs, and v4 message APIs.&#x20;
{% endhint %}

{% hint style="info" %}
The policy configuration for a v2 API using the legacy execution engine must include the `scope`. If the policy is applied to a v4 API or a v2 API using the emulated reactive engine, the configuration does not include `scope`.
{% endhint %}

{% tabs %}
{% tab title="v2 API example" %}
```json
"transform-headers": {
    "addHeaders": [
        {
            "name": "X-Gravitee-Request-Id",
            "value": "{#request.id}"
        }
    ],
    "removeHeaders": [
        "X-Gravitee-TransactionId"
    ],
    "whitelistHeaders": [
        "Content-Type",
        "Content-Length"
    ],
    "scope": "REQUEST"
}
```

Add a header from the request’s payload:

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

{% tab title="Proxy API example" %}
```json
"transform-headers": {
    "addHeaders": [
        {
            "name": "X-Gravitee-Request-Id",
            "value": "{#request.id}"
        }
    ],
    "removeHeaders": [
        "X-Gravitee-TransactionId"
    ],
    "whitelistHeaders": [
        "Content-Type",
        "Content-Length"
    ],
}
```

Add a header from the request’s payload:

```json
"transform-headers": {
    "addHeaders": [
        {
            "name": "X-Product-Id",
            "value": "{#jsonPath(#request.content, '$.product.id')}"
        }
    ]
}
```
{% endtab %}

{% tab title="Message API example" %}
```json
"transform-headers": {
    "addHeaders": [
        {
            "name": "X-Gravitee-Message-Id",
            "value": "{#message.id}"
        }
    ],
    "removeHeaders": [
        "X-Gravitee-TransactionId"
    ],
    "whitelistHeaders": [
        "Content-Type",
        "Content-Length"
    ],
}
```

Add a header from the message’s payload:

```json
"transform-headers": {
    "addHeaders": [
        {
            "name": "X-Product-Id",
            "value": "{#jsonPath(#message.content, '$.product.id')}"
        }
    ]
}
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
