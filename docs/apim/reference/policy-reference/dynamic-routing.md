---
description: This page provides the technical details of the Dynamic Routing policy
---

# Dynamic Routing

## Overview

Functional and implementation information for the Dynamic Routing policy is organized into the following sections:

* [Examples](dynamic-routing.md#examples)
* [Configuration](dynamic-routing.md#configuration)
* [Errors](dynamic-routing.md#errors)
* [Changelogs](dynamic-routing.md#changelogs)

## Examples

The `dynamic-routing` policy is used to dispatch inbound calls to different targets / endpoints or to rewrite URIs.

This policy is particularly useful for creating API _Mashups_.

Another typical use case is defining this kind of routing:

* Requests from [`http://gateway/apis/store/12/info`](http://gateway/apis/store/12/info) are redirected to [`http://backend_store12/info`](http://backend\_store12/info)
* Requests from [`http://gateway/apis/store/45/info`](http://gateway/apis/store/45/info) are redirected to [`http://backend_store45/info`](http://backend\_store45/info)

{% tabs %}
{% tab title="Proxy API example" %}
{% hint style="warning" %}
This example will work for [v2 APIs and v4 proxy APIs.](../../overview/gravitee-api-definitions-and-execution-engines.md)

Currently, this policy can **not** be applied at the message level.
{% endhint %}

```
"dynamic-routing": {
    "rules": [
        {
            "pattern": "/v1/stores/(.*)",
            "url": "http://host2/stores/{#group[0]}"
        }
    ]
}
```

You can also select endpoints configured for your API by name using expression language:

```
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

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

You can configure multiple rules and their respective redirections relative to the initial request path. When you define rules, it is important to remember that the API `context-path` must not be part of the rule’s path. For example, if your `context-path` is `/myapi` and your call is `/myapi/123`, if you want to select `123` the regular expression is `/(.*)` (don’t forget the `/`).

### Regular expressions

Using regular expressions can be very useful when you want to capture some parts of the initial request path and reuse them to define the redirection.

For example, to capture the end of a path after `/v1/stores/`, the rule path is `/v1/stores/(.*)`. You can then use it in the `redirect to` property: `http://store_backend/stores/{#group[0]}`

You can also use named groups instead of indexed groups: `/api/(?<version>v[0-9]+)/stores.*` ⇒ `http://host1/products/api/{#groupName'version'}`

### Attributes

<table data-full-width="false"><thead><tr><th width="140">Name</th><th width="207">Description</th></tr></thead><tbody><tr><td>request.endpoint</td><td>The endpoint URL invoked by the gateway after dynamic routing</td></tr></tbody></table>

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into [phases](broken-reference) that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the Dynamic Routing policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

## Errors

<table data-full-width="false"><thead><tr><th width="210">Phase</th><th width="171">HTTP status code</th><th width="387">Message</th></tr></thead><tbody><tr><td>onRequest</td><td><code>400</code></td><td>When no rules match the inbound request</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-dynamic-routing/blob/master/CHANGELOG.md" %}
