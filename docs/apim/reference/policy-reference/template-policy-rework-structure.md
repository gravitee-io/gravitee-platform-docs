---
description: This page provides the technical details of the JSON-to-XML policy
---

# Template Policy - Rework Structure

{% hint style="warning" %}
**This feature requires** [**Gravitee's Enterprise Edition**](../../overview/introduction-to-gravitee-api-management-apim/ee-vs-oss.md)**.**
{% endhint %}

## Overview

Functional and implementation information for the JSON-to-XML policy is organized into the following sections:

* [Examples](template-policy-rework-structure.md#examples)
* [Configuration](template-policy-rework-structure.md#configuration)
* [Compatibility Matrix](template-policy-rework-structure.md#compatibility-matrix)
* [Errors](template-policy-rework-structure.md#errors)
* [Changelogs](template-policy-rework-structure.md#changelogs)

## Examples

The JSON-to-XML policy transforms JSON payloads to XML before either sending the payload to the backend system or returning it to the client. To transform XML content to JSON, please see the JSON-to-XML policy.

{% tabs %}
{% tab title="Proxy API example" %}
{% hint style="info" %}
The proxy API example also applies to v2 APIs.
{% endhint %}

For proxy APIs, the JSON-to-XML policy is most commonly used for transforming JSON data before returning it to the client in the `response` phase.

For example, the Gravitee echo API returns a JSON response when a `GET` request is sent to [https://api.gravitee.io/echo](https://api.gravitee.io/echo). The response is formatted like so:

{% code title="Default response" %}
```json
{
    "bodySize": 0,
    "headers": {
        "Accept": "*/*",
        "Host": "api.gravitee.io",
        "User-Agent": "{{user-agent-info}}",
        "X-Gravitee-Request-Id": "{{generated-request-id}}",
        "X-Gravitee-Transaction-Id": "{{generated-trx-id}}",
        "accept-encoding": "deflate, gzip"
    },
    "query_params": {}
}
```
{% endcode %}

Adding a JSON-to-XML policy on the `response` phase for a proxy API will transform the response output to:

{% code title="Transformed response" %}
```xml
<root>
  <headers>
    <Accept>*/*</Accept>
    <Host>api.gravitee.io</Host>
    <User-Agent>{{user-agent-info}}</User-Agent>
    <X-Gravitee-Request-Id>{{generated-request-id}}</X-Gravitee-Request-Id>
    <X-Gravitee-Transaction-Id>{{generated-trx-id}}</X-Gravitee-Transaction-Id>
    <accept-encoding>deflate, gzip</accept-encoding>
  </headers>
  <query_params/>
  <bodySize>0</bodySize>
</root>
```
{% endcode %}
{% endtab %}

{% tab title="Message API example" %}
{% hint style="warning" %}
ONLY INCLUDE THIS SECTION IF MESSAGES ARE SUPPORTED. Otherwise, use a single example section with one of the following two hints:
{% endhint %}

{% hint style="warning" %}
This example will work for [v2 APIs and v4 proxy APIs.](../../overview/gravitee-api-definitions-and-execution-engines.md)

Currently, this policy can **not** be applied at the message level.
{% endhint %}

{% hint style="warning" %}
This example will work for [v2 APIs, v4 proxy APIs, and for the initial connection request of v4 message APIs](../../overview/gravitee-api-definitions-and-execution-engines.md).

Currently, this policy can **not** be applied at the message level.
{% endhint %}

**Otherwise, provide a message example:**

For message APIs, the JSON-to-XML policy is used to transform the message `content` in either the `publish` or `subscribe` phase.

For example, you can create a message API with an HTTP GET entrypoint and a mock endpoint. Suppose the endpoint is configured to return the message content as follows:

{% code title="Default message" %}
```json
{ \"id\": \"1\", \"name\": \"bob\", \"v\": 2 }
```
{% endcode %}

Adding a JSON-to-XML policy on the subscribe phase will return the payload to the client via the HTTP GET entrypoint as follows (the number of messages returned will vary by the number of messages specified in the Mock endpoint):

{% code title="Transformed messages" %}
```xml
{
    "items": [
        {
            "content": "<root><id>1</id><name>bob</name><v>2</v></root>",
            "id": "0"
        },
        {
            "content": "<root><id>1</id><name>bob</name><v>2</v></root>",
            "id": "1"
        },
        {
            "content": "<root><id>1</id><name>bob</name><v>2</v></root>",
            "id": "2"
        },
        {
            "content": "<root><id>1</id><name>bob</name><v>2</v></root>",
            "id": "3"
        }
    ],
    "pagination": {
        "nextCursor": "3"
    }
}
```
{% endcode %}

The output is the typical return structure for the HTTP GET entrypoint with each message `content` field transformed from JSON to XML.

{% hint style="info" %}
For the HTTP GET entrypoint specifically, the entire payload can be returned as XML by adding the `"Accept": "application/json"` header to the GET request. In this case, the message content is transformed into [CDATA](https://www.w3.org/TR/REC-xml/#sec-cdata-sect) and is therefore not treated as marked-up content for the purpose of the entrypoint using the `Accept` header.
{% endhint %}
{% endtab %}
{% endtabs %}

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

{% code title="Sample Configuration" %}
```json
{
  "name": "Custom name",
  "description": "Converts data from JSON to XML",
  "policy": "json-xml",
  "configuration": {
    "scope": "RESPONSE",
    "rootElement": "root"
  }
}
```
{% endcode %}

### Reference

<table data-full-width="false"><thead><tr><th width="140">Property</th><th width="104" data-type="checkbox">Required</th><th width="207">Description</th><th width="111" data-type="select">Type</th><th width="247">Options</th></tr></thead><tbody><tr><td>name</td><td>false</td><td>Provide a descriptive name for your policy</td><td></td><td>N/a</td></tr><tr><td>description</td><td>false</td><td>Provide a description for your policy</td><td></td><td>N/a</td></tr><tr><td>rootElement</td><td>true</td><td>XML root element name that encloses content.</td><td></td><td>N/a<br><strong>root</strong></td></tr><tr><td>scope</td><td>true</td><td>The execution scope</td><td></td><td><strong>REQUEST</strong> RESPONSE</td></tr></tbody></table>

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into phases that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the JSON-to-XML policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="188.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>false</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>true</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>true</td></tr><tr><td>onResponseContent</td><td>true</td><td>onMessageResponse</td><td>true</td></tr></tbody></table>

## Compatibility matrix

The [changelog for each version of APIM](../../releases-and-changelog/changelog/) provides a list of policies included in the default distribution. The chart below summarizes this information in relation to the `json-xml` policy.

<table data-full-width="false"><thead><tr><th width="161.33333333333331">Plugin Version</th><th width="242">Supported APIM versions</th><th>Included in APIM default distribution</th></tr></thead><tbody><tr><td>2.2</td><td>>=3.20</td><td>>=3.21</td></tr><tr><td>2.1</td><td>^3.0</td><td>>=3.0 &#x3C;3.21</td></tr><tr><td>2.0</td><td>^3.0</td><td>N/a</td></tr></tbody></table>

## Errors

<table data-full-width="false"><thead><tr><th width="210">Phase</th><th width="171">HTTP status code</th><th width="387">Error template key</th></tr></thead><tbody><tr><td>onRequest</td><td><code>400</code></td><td><strong>JSON_INVALID_PAYLOAD:</strong> Request payload cannot be transformed properly to XML</td></tr><tr><td>onResponse</td><td><code>500</code></td><td><strong>JSON_INVALID_PAYLOAD:</strong><br>Response payload cannot be transformed properly to XML</td></tr><tr><td>onMessageRequest</td><td><code>400</code></td><td><strong>JSON_INVALID_MESSAGE_PAYLOAD:</strong> Incoming message cannot be transformed properly to XML</td></tr><tr><td>onMessageResponse</td><td><code>500</code></td><td><strong>JSON_INVALID_MESSAGE_PAYLOAD:</strong> Outgoing message cannot be transformed properly to XML</td></tr></tbody></table>

### Nested objects

To limit the processing time in the case of a nested object, the default max depth of a nested object has been set to 1000. This default value can be overridden using the environment variable `gravitee_policy_jsonxml_maxdepth`.

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-json-xml/blob/master/CHANGELOG.md" %}
