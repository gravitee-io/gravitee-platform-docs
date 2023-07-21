---
description: This page provides the technical details of the Mock policy
---

# Mock

## Overview

Functional and implementation information for the Mock policy is organized into the following sections:

* [Examples](template-policy-rework-structure-24.md#examples)
* [Configuration](template-policy-rework-structure-24.md#configuration)
* [Compatibility Matrix](template-policy-rework-structure-24.md#compatibility-matrix)
* [Changelogs](template-policy-rework-structure-24.md#changelogs)

## Examples

You can use the `mock` policy to create mock responses when a consumer calls one of your services. This means you do not have to provide a functional backend as soon as you create your API, giving you more time to think about your API contract.

You can think of the policy as a contract-first approach — you are able to create a fully-functional API without needing to write a single line of code to handle consumer calls.

Internally, this policy replaces the default HTTP invoker with a mock invoker. There are no more HTTP calls between the gateway and a remote service or backend.

{% hint style="info" %}
The Mock policy will **not** cause the other policies to be skipped, regardless of its location in the flow.
{% endhint %}

When defining the response body content, you can use Expression Language to provide a dynamic mock response.

{% tabs %}
{% tab title="Proxy API example" %}
{% hint style="warning" %}
This example will work for [v2 APIs and v4 proxy APIs.](../../overview/gravitee-api-definitions-and-execution-engines.md)

Currently, this policy can **not** be applied at the message level.
{% endhint %}

Note that you don’t need to provide the `Content-Type` header, since the Mock policy can automatically detect the content type.

#### Body content example (XML)

```
<user id="{#request.paths[3]}">
    <firstname>{#properties['firstname_' + #request.paths[3]]}</firstname>
	<lastname>{#properties['lastname_' + #request.paths[3]]}</lastname>
	<age>{(T(java.lang.Math).random() * 60).intValue()}</age>
	<createdAt>{(new java.util.Date()).getTime()}</createdAt>
</user>
```

#### Body content example (JSON)

```
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

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

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

### Reference

<table><thead><tr><th>Property</th><th data-type="checkbox">Required</th><th>Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>status</td><td>true</td><td>HTTP Status Code</td><td>integer</td><td></td></tr><tr><td>headers</td><td>true</td><td>HTTP Headers</td><td>Array of HTTP headers</td><td></td></tr><tr><td>content</td><td>true</td><td>HTTP Body content</td><td>string</td><td></td></tr></tbody></table>

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into [phases](broken-reference) that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the Mock policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="188.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

## Compatibility matrix

The [changelog for each version of APIM](../../releases-and-changelog/changelog/) provides a list of policies included in the default distribution. The chart below summarizes this information in relation to the `json-xml` policy.

<table data-full-width="false"><thead><tr><th width="161.33333333333331">Plugin Version</th><th width="242">Supported APIM versions</th></tr></thead><tbody><tr><td>&#x3C;=1.x</td><td>All</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-mock/blob/master/CHANGELOG.md" %}
