---
description: An overview about ---.
hidden: true
---

# Dynamic Routing

## Overview

The `dynamic-routing` policy is used to dispatch inbound calls to different targets and endpoints or to rewrite URIs. This policy is particularly useful for creating API mashups.

Another typical use case is defining routing similar to the following:

* Requests from `http://gateway/apis/store/12/info` are redirected to `http://backend_store12/info`
* Requests from `http://gateway/apis/store/45/info` are redirected to `http://backend_store45/info`

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs and v4 HTTP proxy APIs. It cannot be applied to v4 message APIs or v4 TCP proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="HTTP proxy API example" %}
Sample policy configuration:

```json
"dynamic-routing": {
    "rules": [
        {
            "pattern": "/v1/stores/(.*)",
            "url": "http://host2/stores/{#group[0]}"
        }
    ]
}
```

You can also select endpoints configured for your API by name using Gravitee Expression Language:

```json
"dynamic-routing": {
    "rules": [
        {
            "pattern": "/v1/stores/(.*)",
            "url": "{#endpoints['default']}/{#group[0]}"
        }
    ]
}
```
{% endtab %}
{% endtabs %}

## Configuration

You can configure multiple rules and their respective redirections relative to the initial request path. When you define rules, it is important to remember that the API `context-path` must not be part of the rule’s path.

For example, if your `context-path` is `/myapi` and your call is `/myapi/123`, if you want to select `123`, the regular expression is `/(.*)` (don’t forget the `/`).

### Regular expressions

Using regular expressions can be very useful when you want to capture some parts of the initial request path and reuse them to define the redirection.

For example, to capture the end of a path after `/v1/stores/`, the rule path is `/v1/stores/(.*)`. You can then use it in the `redirect to` property: `http://store_backend/stores/{#group[0]}`

You can also use named groups instead of indexed groups: `/api/(?<version>v[0-9]+)/stores.*` ⇒ `http://host1/products/api/{#groupName'version'}`

### Phases

The phases checked below are supported by the `dynamic-routing` policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Attributes

The `dynamic-routing` policy can be configured with the following attributes:

<table data-full-width="false"><thead><tr><th width="140">Name</th><th width="207">Description</th></tr></thead><tbody><tr><td>request.endpoint</td><td>The endpoint URL invoked by the gateway after dynamic routing</td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `dynamic-routing` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>Up to 1.x</td><td>All</td></tr></tbody></table>

## Errors

<table data-full-width="false"><thead><tr><th width="210">Phase</th><th width="171">HTTP status code</th><th width="387">Message</th></tr></thead><tbody><tr><td>onRequest</td><td><code>400</code></td><td>When no rules match the inbound request</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-dynamic-routing/blob/master/CHANGELOG.md" %}
