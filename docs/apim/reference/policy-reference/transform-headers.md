---
description: This page provides the technical details of the Transform Headers policy
---

# Transform Headers

## Overview

Functional and implementation information for the JSON-to-XML policy is organized into the following sections:

* [Examples](transform-headers.md#examples)
* [Configuration](transform-headers.md#configuration)
* [Compatibility Matrix](transform-headers.md#compatibility-matrix)
* [Changelogs](transform-headers.md#changelogs)

## Examples

You can use the `transform-headers` policy to override HTTP headers in incoming requests or outbound responses. You can override the HTTP headers by:

* Adding to or updating the list of headers
* Removing headers individually
* Defining a whitelist == Compatibility with APIM

{% tabs %}
{% tab title="Proxy API example" %}
{% hint style="info" %}
The proxy API example also applies to v2 APIs.
{% endhint %}

```
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

```
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
{% endtabs %}

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into [phases](broken-reference/) that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines/). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the Transform Headers policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="188.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>true</td><td>onResponse</td><td>true</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>true</td></tr><tr><td>onResponseContent</td><td>true</td><td>onMessageResponse</td><td>true</td></tr></tbody></table>

## Compatibility matrix

The [changelog for each version of APIM](../../releases-and-changelogs/changelogs/) provides a list of policies included in the default distribution. The chart below summarizes this information in relation to the `json-xml` policy.

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>1.x</td><td>&#x3C;=3.x</td></tr><tr><td>>=2.x</td><td>>=4.x</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-transform-headers/blob/master/CHANGELOG.md" %}
