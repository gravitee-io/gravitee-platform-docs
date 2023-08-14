---
description: This page provides the technical details of the Assign Attributes policy
---

# Assign Attributes

## Overview

Functional and implementation information for the JSON-to-XML policy is organized into the following sections:

* [Examples](assign-attributes.md#examples)
* [Configuration](assign-attributes.md#configuration)
* [Compatibility Matrix](assign-attributes.md#compatibility-matrix)
* [Errors](assign-attributes.md#errors)
* [Changelogs](assign-attributes.md#changelogs)

## Examples

You can use the `assign-attributes` policy to set variables such as request attributes and other execution context attributes.

You can use it to retrieve initial request attributes after `Transform headers` or `Transform query parameters` policies and reuse them in other policies (`Dynamic routing`, for example).

{% tabs %}
{% tab title="Proxy API example" %}
{% hint style="warning" %}
The proxy API example also applies to v2 APIs. This policy can also be used at the message level for v4 APIs.
{% endhint %}

Let’s say we want to inject request attributes into the context attributes:

```
"assign-attributes": {
    "attributes": [
        {
            "name": "initialContentTypeHeader,
            "value": "{#request.headers['Content-Type']}"
        },
        {
            "name": "initialFooParamHeader,
            "value": "{#request.params['foo']}"
        }
    ]
}
```

To extract the request attributes you can use the following syntax:

Get the content-type header:

```
{#context.attributes['initialContentTypeHeader']}
```

Get the foo query param:

```
{#context.attributes['initialFooParamHeader']}
```

**Request objects**

You can also be more general and put complex objects into the context attributes:

```
"assign-attributes": {
    "attributes": [
        {
            "name": "initialRequest,
            "value": "{#request}"
        }
    ]
}
```

To extract the request attributes you can use the following syntax:

Get the content-type header:

```
{#context.attributes['initialRequest'].headers['content-type']}
```

Get the foo query param:

```
{#context.attributes['initialRequest'].params['foo']}
```
{% endtab %}

{% tab title="Message API example" %}
Let’s say we want to inject attributes into the message:

```
"assign-attributes": {
    "attributes": [
        {
            "name": "initialContentTypeHeader,
            "value": "{#message.headers['Content-Type']}"
        },
        {
            "name": "initialFooMetadataHeader,
            "value": "{#message.metadata['foo']}"
        }
    ]
}
```

To extract the message attributes you can use the following syntax:

Get the content-type header:

```
{#message.attributes['initialContentTypeHeader']}
```

Get the foo metadata:

```
{#message.attributes['initialFooMetadataHeader']}
```
{% endtab %}
{% endtabs %}

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into [phases](broken-reference/) that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the Assign Attributes policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="188.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>true</td><td>onResponse</td><td>true</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>true</td></tr><tr><td>onResponseContent</td><td>true</td><td>onMessageResponse</td><td>true</td></tr></tbody></table>

## Compatibility matrix

The [changelog for each version of APIM](../../releases-and-changelogs/changelogs/) provides a list of policies included in the default distribution. The chart below summarizes this information in relation to the `assign-attributes` policy.

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>&#x3C;= 1.x</td><td>All</td></tr></tbody></table>

## Errors

<table data-full-width="false"><thead><tr><th width="210">Phase</th><th width="171">HTTP status code</th><th width="387">Error template key</th></tr></thead><tbody><tr><td>onRequest</td><td><code>500</code></td><td>An error occurred while setting request attributes in the execution context</td></tr><tr><td>onResponse</td><td><code>500</code></td><td>An error occurred while setting request attributes in the execution context</td></tr><tr><td>onRequestContent</td><td><code>500</code></td><td>An error occurred while setting request attributes in the execution context</td></tr><tr><td>onResponseContent</td><td><code>500</code></td><td>An error occurred while setting request attributes in the execution context</td></tr><tr><td>onMessageRequest</td><td><code>500</code></td><td>An error occurred while setting request attributes in the execution context</td></tr><tr><td>onMessageResponse</td><td><code>500</code></td><td>An error occurred while setting request attributes in the execution context</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-assign-attributes/blob/master/CHANGELOG.md" %}
