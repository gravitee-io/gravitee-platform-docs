---
description: This page provides the technical details of the JSON to XML policy
---

# JSON to XML

## Overview

The `json-xml` policy transforms JSON payloads to XML before either sending the payload to the backend system or returning it to the client.&#x20;

Functional and implementation information for the `json-xml` policy is organized into the following sections:

* [Examples](json-to-xml.md#examples)
* [Configuration](json-to-xml.md#configuration)
* [Compatibility Matrix](json-to-xml.md#compatibility-matrix)
* [Errors](json-to-xml.md#errors)
* [Changelogs](json-to-xml.md#changelogs)

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs, v4 HTTP proxy APIs, and v4 message APIs. It cannot be applied to v4 TCP proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="HTTP proxy API example" %}
For proxy APIs, the `json-xml` policy is most commonly used for transforming JSON data before returning it to the client in the `response` phase.

For example, the Gravitee echo API returns a JSON response when a `GET` request is sent to [https://api.gravitee.io/echo](https://api.gravitee.io/echo). The response is formatted as below:

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

Adding a `json-xml` policy on the response phase for a proxy API will transform the response output to:

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
For message APIs, the `json-xml` policy is used to transform the message content in either the publish or subscribe phase.

For example, you can create a message API with an HTTP GET entrypoint and a Mock endpoint. Suppose the endpoint is configured to return the message content as follows:

{% code title="Default message" %}
```json
{ \"id\": \"1\", \"name\": \"bob\", \"v\": 2 }
```
{% endcode %}

Adding a `json-xml` policy on the subscribe phase will return the payload to the client via the HTTP GET entrypoint as follows (the number of messages returned will vary by the number of messages specified in the Mock endpoint):

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

The output is the typical return structure for the HTTP GET entrypoint with each message content field transformed from JSON to XML.

{% hint style="info" %}
For the HTTP GET entrypoint specifically, the entire payload can be returned as XML by adding the `"Accept": "application/json"` header to the GET request. In this case, the message content is transformed into [CDATA](https://www.w3.org/TR/REC-xml/#sec-cdata-sect) and is therefore not treated as marked-up content for the purpose of the entrypoint using the `Accept` header.
{% endhint %}
{% endtab %}
{% endtabs %}

## Configuration

Sample policy configuration is shown below:

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

### Phases

The phases checked below are supported by the `json-xml` policy:

<table data-full-width="false"><thead><tr><th width="207">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>true</td><td>onResponse</td><td>true</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>true</td></tr><tr><td>onResponseContent</td><td>true</td><td>onMessageResponse</td><td>true</td></tr></tbody></table>

### Options

The `json-xml` policy can be configured with the following options:

<table data-full-width="false"><thead><tr><th width="140">Property</th><th width="177">Required</th><th width="256">Description</th><th width="111">Type</th><th width="247">Default</th></tr></thead><tbody><tr><td>scope</td><td>legacy engine only</td><td>The execution scope (<code>request</code> or <code>response</code>)</td><td>string</td><td><code>REQUEST</code></td></tr><tr><td>rootElement</td><td>X</td><td>Root element name that’s enclose content</td><td>string</td><td><code>root</code></td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `json-xml` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>1.x</td><td>3.x</td></tr><tr><td>3.x</td><td>4.0+</td></tr></tbody></table>

## Errors

<table data-full-width="false"><thead><tr><th width="210">Phase</th><th width="171">HTTP status code</th><th width="387">Error template key</th></tr></thead><tbody><tr><td>onRequest</td><td><code>400</code></td><td><strong>JSON_INVALID_PAYLOAD:</strong> Request payload cannot be transformed properly to XML</td></tr><tr><td>onResponse</td><td><code>500</code></td><td><strong>JSON_INVALID_PAYLOAD:</strong><br>Response payload cannot be transformed properly to XML</td></tr><tr><td>onMessageRequest</td><td><code>400</code></td><td><strong>JSON_INVALID_MESSAGE_PAYLOAD:</strong> Incoming message cannot be transformed properly to XML</td></tr><tr><td>onMessageResponse</td><td><code>500</code></td><td><strong>JSON_INVALID_MESSAGE_PAYLOAD:</strong> Outgoing message cannot be transformed properly to XML</td></tr></tbody></table>

### Nested objects

To limit the processing time in case of nested object, a default max depth of nested object has been defined to 100. This default value can be overridden using the environment variable `gravitee_policy_jsonxml_maxdepth`.

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-json-xml/blob/master/CHANGELOG.md" %}
