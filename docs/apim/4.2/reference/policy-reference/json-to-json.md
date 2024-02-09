---
description: This page provides the technical details of the JSON to JSON policy
---

# JSON to JSON

## Overview

You can use the `json-to-json` policy to apply a transformation (or mapping) on the request and/or response and/or message content.

This policy is based on the [JOLT](https://github.com/bazaarvoice/jolt) library.

In APIM, you need to provide the JOLT specification in the policy configuration.

{% hint style="info" %}
You can use APIM EL in the JOLT specification.
{% endhint %}

At request/response level, the policy will do nothing if the processed request/response does not contain JSON. This policy checks the `Content-Type` header before applying any transformation.

At message level, the policy will do nothing if the processed message has no content. It means that the message will be re-emitted as is.

Functional and implementation information for the `json-to-json` policy is organized into the following sections:

* [Examples](json-to-json.md#examples)
* [Configuration](json-to-json.md#configuration)
* [Compatibility Matrix](json-to-json.md#compatibility-matrix)
* [Errors](json-to-json.md#errors)
* [Changelogs](json-to-json.md#changelogs)

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs, v4 HTTP proxy APIs, and v4 message APIs. It cannot be applied to v4 TCP proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="HTTP proxy API example" %}
For this input:

```json
{
    "_id": "57762dc6ab7d620000000001",
    "name": "name",
    "__v": 0
}
```

And this JOLT specification:

```java
[
  {
    "operation": "shift",
    "spec": {
      "_id": "id",
      "*": {
        "$": "&1"
      }
    }
  },
  {
    "operation": "remove",
    "spec": {
      "__v": ""
    }
  }
]
```

The output is as follows:

```json
{
    "id": "57762dc6ab7d620000000001",
    "name": "name"
}
```
{% endtab %}

{% tab title="Message API example" %}
For this input:

```json
{
    "_id": "57762dc6ab7d620000000001",
    "name": "name",
    "__v": 0
}
```

And this JOLT specification:

```java
[
  {
    "operation": "shift",
    "spec": {
      "_id": "id",
      "*": {
        "$": "&1"
      }
    }
  },
  {
    "operation": "remove",
    "spec": {
      "__v": ""
    }
  }
]
```

The output is as follows:

```json
{
    "id": "57762dc6ab7d620000000001",
    "name": "name"
}
```
{% endtab %}
{% endtabs %}

## Configuration

Sample policy configuration is shown below:

{% code title="Sample Configuration" %}
```json
{
    "json-to-json": {
        "scope": "REQUEST",
        "specification": "[{ \"operation\": \"shift\", \"spec\": { \"_id\": \"id\", \"*\": { \"$\": \"&1\" } } }, { \"operation\": \"remove\", \"spec\": { \"__v\": \"\" } }]"
    }
}
```
{% endcode %}

### Options

The `json-to-json` policy can be configured with the following options:

<table><thead><tr><th width="210">Property</th><th width="165">Required</th><th width="238">Description</th><th width="83">Type</th><th>Default</th></tr></thead><tbody><tr><td>scope</td><td>only for legacy execution engine</td><td>The execution scope (<code>request</code> or <code>response</code>)</td><td>string</td><td><code>REQUEST</code></td></tr><tr><td>specification</td><td>X</td><td><p>The <a href="http://jolt-demo.appspot.com/">JOLT</a> specification to apply on a given content.</p><p>Can contain EL.</p></td><td>string</td><td></td></tr><tr><td>overrideContentType</td><td></td><td>Override the Content-Type to <code>application/json</code></td><td>string</td><td><code>true</code></td></tr></tbody></table>

### Phases

The phases checked below are supported by the `json-to-json` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="199.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>true</td><td>onResponse</td><td>true</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>true</td></tr><tr><td>onResponseContent</td><td>true</td><td>onMessageResponse</td><td>true</td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `json-to-json` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>1.x</td><td>Up to 3.19.x</td></tr><tr><td>2.x</td><td>3.20.x</td></tr><tr><td>3.x</td><td>4.0+</td></tr></tbody></table>

## Errors

Legacy execution engine:

<table data-full-width="false"><thead><tr><th width="171">Code</th><th width="387">Message</th></tr></thead><tbody><tr><td><code>500</code></td><td>Bad specification file or transformation cannot be executed properly</td></tr></tbody></table>

Reactive execution engine:&#x20;

<table data-full-width="false"><thead><tr><th width="98.5">Code</th><th width="302">Error template key</th><th>Description</th></tr></thead><tbody><tr><td><code>500</code></td><td>INVALID_JSON_TRANSFORMATION</td><td>Unable to apply JOLT transformation to payload</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-json-xml/blob/master/CHANGELOG.md" %}
