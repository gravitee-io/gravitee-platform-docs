---
description: This page provides the technical details of the JSON-to-JSON policy
---

# JSON to JSON

## Overview

Functional and implementation information for the JSON-to-XML policy is organized into the following sections:

* [Examples](template-policy-rework-structure-15.md#examples)
* [Configuration](template-policy-rework-structure-15.md#configuration)
* [Errors](template-policy-rework-structure-15.md#errors)
* [Changelogs](template-policy-rework-structure-15.md#changelogs)

## Examples

You can use the `json-to-json` policy to apply a transformation (or mapping) on the request and/or response and/or message content.

This policy is based on the [JOLT](https://github.com/bazaarvoice/jolt) library.

In APIM, you need to provide the JOLT specification in the policy configuration.

{% hint style="info" %}
You can use APIM EL in the JOLT specification.
{% endhint %}

At request/response level, the policy will do nothing if the processed request/response does not contain JSON. This policy checks the `Content-Type` header before applying any transformation.

At message level, the policy will do nothing if the processed message has no content. It means that the message will be re-emitted as is\


{% tabs %}
{% tab title="Proxy API example" %}
{% hint style="info" %}
The proxy API example also applies to v2 APIs.
{% endhint %}

For this input:

Input

```
{
    "_id": "57762dc6ab7d620000000001",
    "name": "name",
    "__v": 0
}
```

And this JOLT specification:

```
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

```
{
    "id": "57762dc6ab7d620000000001",
    "name": "name"
}
```

\

{% endtab %}

{% tab title="Message API example" %}
For this input:

Input

```
{
    "_id": "57762dc6ab7d620000000001",
    "name": "name",
    "__v": 0
}
```

And this JOLT specification:

```
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

```
{
    "id": "57762dc6ab7d620000000001",
    "name": "name"
}
```
{% endtab %}
{% endtabs %}

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

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

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into [phases](broken-reference) that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the JSON-to-XML policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="188.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>false</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>true</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>true</td></tr><tr><td>onResponseContent</td><td>true</td><td>onMessageResponse</td><td>true</td></tr></tbody></table>

## Errors

<table data-full-width="false"><thead><tr><th width="210">Phase</th><th width="171">HTTP status code</th><th width="387">Error template key</th></tr></thead><tbody><tr><td>onRequestContent</td><td><code>500</code></td><td>Bad specification file or transformation cannot be executed properly</td></tr><tr><td>onResponseContent</td><td><code>500</code></td><td>Bad specification file or transformation cannot be executed properly</td></tr><tr><td>onMessageRequest</td><td><code>400</code></td><td><strong>JSON_INVALID_MESSAGE_PAYLOAD:</strong> Incoming message cannot be transformed properly to XML</td></tr><tr><td>onMessageResponse</td><td><code>500</code></td><td><strong>JSON_INVALID_MESSAGE_PAYLOAD:</strong> Outgoing message cannot be transformed properly to XML</td></tr></tbody></table>

### Nested objects

To limit the processing time in the case of a nested object, the default max depth of a nested object has been set to 1000. This default value can be overridden using the environment variable `gravitee_policy_jsonxml_maxdepth`.

## Changelogs

\{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-json-xml/blob/master/CHANGELOG.md" %\}
