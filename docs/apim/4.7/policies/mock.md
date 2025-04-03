---
description: This page provides the technical details of the Mock policy
hidden: true
---

# Mock

## Overview

You can use the `mock` policy to create mock responses when a consumer calls one of your services. This means you do not have to provide a functional backend as soon as you create your API, giving you more time to think about your API contract.

You can think of the policy as a contract-first approach — you are able to create a fully-functional API without needing to write a single line of code to handle consumer calls.

Internally, this policy replaces the default HTTP invoker with a mock invoker. There are no more HTTP calls between the Gateway and a remote service or backend.

{% hint style="info" %}
The `mock` policy will **not** cause the other policies to be skipped, regardless of its location in the flow.
{% endhint %}

When defining the response body content, you can use [Gravitee Expression Language (EL)](../../4.6/guides/gravitee-expression-language.md) to provide a dynamic mock response.

Functional and implementation information for the `mock` policy is organized into the following sections:

* [Examples](mock.md#examples)
* [Configuration](mock.md#configuration)
* [Compatibility Matrix](mock.md#compatibility-matrix)
* [Changelogs](mock.md#changelogs)

## Examples

{% hint style="warning" %}
This policy can only be applied to v2 APIs. It cannot be applied to v4 message APIs or v4 proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="HTTP proxy API example" %}
Note that you don’t need to provide the `Content-Type` header, since the `mock` policy can automatically detect the content type.

**Body content example (XML)**

```xml
<user id="{#request.paths[3]}">
    <firstname>{#properties['firstname_' + #request.paths[3]]}</firstname>
	<lastname>{#properties['lastname_' + #request.paths[3]]}</lastname>
	<age>{(T(java.lang.Math).random() * 60).intValue()}</age>
	<createdAt>{(new java.util.Date()).getTime()}</createdAt>
</user>
```

**Body content example (JSON)**

```json
{
    "id": "{#request.paths[3]}",
    "firstname": "{#properties['firstname_' + #request.paths[3]]}",
    "lastname": "{#properties['lastname_' + #request.paths[3]]}",
    "age": {(T(java.lang.Math).random() * 60).intValue()},
    "createdAt": {(new java.util.Date()).getTime()}
}
```
{% endtab %}
{% endtabs %}

## Configuration

Sample policy configuration is shown below:

{% code title="Sample Configuration" %}
```json
"mock": {
    "status": "200",
    "headers": [
        {
            "name": "Content-Type",
            "value": "application/json"
        }, {
            "name": "Server",
            "value": "Gravitee.io"
        }
    ],
    "content": "<user id=\"{#request.paths[3]}\">\n\t<firstname>{#properties['firstname_' + #request.paths[3]]}</firstname>\n\t<lastname>{#properties['lastname_' + #request.paths[3]]}</lastname>\n\t<age>{(T(java.lang.Math).random() * 60).intValue()}</age>\n\t<createdAt>{(new java.util.Date()).getTime()}</createdAt>\n</user>"
}
```
{% endcode %}

### Phases

The phases checked below are supported by the `mock` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="204.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>false</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

The mock policy can be configured with the following options:

<table><thead><tr><th width="120">Property</th><th data-type="checkbox">Required</th><th width="183">Description</th><th width="149">Type</th><th>Default</th></tr></thead><tbody><tr><td>status</td><td>true</td><td>HTTP Status Code</td><td>integer</td><td></td></tr><tr><td>headers</td><td>true</td><td>HTTP Headers</td><td>Array of HTTP headers</td><td></td></tr><tr><td>content</td><td>true</td><td>HTTP Body content</td><td>string</td><td></td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `mock` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>Up to 1.x</td><td>All</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-mock/blob/master/CHANGELOG.md" %}
