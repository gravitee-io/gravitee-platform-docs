---
description: This page provides the technical details of the Assign Attributes policy
---

# Assign Attributes

## Overview

You can use the `assign-attributes` policy to set variables such as request attributes and other execution context attributes.

You can use it to retrieve initial request attributes after `Transform headers` or `Transform query parameters` policies and reuse them in other policies (`Dynamic routing`, for example).

Functional and implementation information for the `assign-attributes` policy is organized into the following sections:

* [Examples](assign-attributes.md#examples)
* [Configuration](assign-attributes.md#configuration)
* [Compatibility Matrix](assign-attributes.md#compatibility-matrix)
* [Errors](assign-attributes.md#errors)
* [Changelogs](assign-attributes.md#changelogs)

## Examples

{% hint style="warning" %}
This policy can be applied to all Gravitee APIs: v2 APIs, v4 proxy APIs, and v4 message APIs.
{% endhint %}

{% tabs %}
{% tab title="Proxy API example" %}
To inject an attribute that will dynamically determine if the content is in JSON format:

```
"assign-attributes": {
    "attributes": [
        {
            "name": "isJson,
            "value": "'application/json'.equals(#request.headers['Content-Type'])"
        }
    ]
}
```

To extract the request attribute and get the format of the content you can use the following syntax:

```
{#context.attributes['isJson']}
```

**Request objects**

You can also be more general and inject complex objects into the context attributes:

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

To extract request attributes and get the Content-Type header you can use the following syntax:

```
{#context.attributes['initialRequest'].headers['Content-Type']}
```
{% endtab %}

{% tab title="Message API example" %}
To inject an attribute that will dynamically determine if the content is in JSON format:

```
"assign-attributes": {
    "attributes": [
        {
            "name": "isJson,
            "value": "'application/json'.equals(#message.headers['Content-Type'])"
        }
    ]
}
```

To extract the message attribute and get the format of the content you can use the following syntax:

```
{#message.attributes['isJson']}
```

**Message objects**

You can also be more general and inject complex objects into the message attributes:

```
"assign-attributes": {
    "attributes": [
        {
            "name": "initialMessage,
            "value": "{#message}"
        }
    ]
}
```

To extract message attributes and get the Content-Type header you can use the following syntax:

```
{#message.attributes['initialMessage'].headers['Content-Type']}
```

To assign an attribute to the content of a message:

```
"assign-attributes": {
    "attributes": [
        {
            "name": "messageContent,
            "value": "{#message.content}"
        }
    ]
}
```
{% endtab %}
{% endtabs %}

## Configuration

### Phases

The phases checked below are supported by the `assign-attributes` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="188.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>true</td><td>onResponse</td><td>true</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>true</td></tr><tr><td>onResponseContent</td><td>true</td><td>onMessageResponse</td><td>true</td></tr></tbody></table>

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
