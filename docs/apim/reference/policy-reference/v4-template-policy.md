---
description: Sample structure for policy documentation
---

# Template Policy

{% hint style="warning" %}
**This feature requires** [**Gravitee's Enterprise Edition**](../../overview/introduction-to-gravitee-api-management-apim/ee-vs-oss.md)**.**
{% endhint %}

## Overview

The `json-xml` policy transforms JSON payloads to XML before either sending the payload to the backend system or returning it to the client.

{% hint style="warning" %}
For transforming XML content to JSON, please see the `xml-json` policy.
{% endhint %}

### Proxy API example

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

### Message API example

{% hint style="warning" %}
ONLY INCLUDE THIS SECTION IF MESSAGES ARE SUPPORTED. Otherwise, use the example structure and hint shown for [basic authentication](basic-authentication.md#example)
{% endhint %}

Otherwise provide an example:

For message APIs, the JSON-to-XML policy is used to transform the message `content` in either the `publish` or `subscribe` phase.

For example, you can create a message API with an HTTP GET entrypoint and a mock endpoint. Suppose the endpoint is configured to return the message content as follows:

{% code title="Default message" %}
```json
{ \"id\": \"1\", \"name\": \"bob\", \"v\": 2 }
```
{% endcode %}

Then adding a JSON-to-XML policy on the subscribe phase will return the payload to the client via the HTTP GET entrypoint like so (the number of messages returned will vary by the number of messages specified in the Mock endpoint):

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

The output is the typical return structure for the HTTP GET entrypoint with each message `content` field being transformed from JSON to XML.

{% hint style="info" %}
For the HTTP GET entrypoint specifically, the entire payload can be returned as XML by adding the `"Accept": "application/json"` header to the GET request. In this case, the message content is transformed into [CDATA](https://www.w3.org/TR/REC-xml/#sec-cdata-sect) and is therefore not treated as marked-up content for the purpose of the entrypoint using the `Accept` header.
{% endhint %}

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies through the Policy Studio in the Management Console or interacting directly with the Management API.

{% tabs %}
{% tab title="Management Console" %}
<mark style="color:yellow;">We should wait to make these once the v4 Policy Studio is finalized</mark>
{% endtab %}

{% tab title="Managment API" %}
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
{% endtab %}
{% endtabs %}

### Reference

<table data-full-width="true"><thead><tr><th width="175">Property</th><th width="108" data-type="checkbox">Required</th><th width="298">Description</th><th width="97" data-type="select">Type</th><th width="132">Options</th><th>Default</th></tr></thead><tbody><tr><td>name</td><td>false</td><td>Provide a descriptive name for your policy</td><td></td><td>N/a</td><td>N/a</td></tr><tr><td>description</td><td>false</td><td>Provide a description for your policy</td><td></td><td>N/a</td><td>N/a</td></tr><tr><td>rootElement</td><td>true</td><td>XML root element name that encloses content.</td><td></td><td>N/a</td><td>root</td></tr><tr><td>scope</td><td>true</td><td>The execution scope</td><td></td><td>REQUEST, RESPONSE</td><td>REQUEST</td></tr></tbody></table>

### Phases

Policies can be applied to the request or the response of a gateway API transaction. Depending on the [version of the gateway API](../../overview/gravitee-api-definitions-and-execution-engines.md#policy-execution-phases-and-execution-order), the request and response are broken up into what are known as _phases_. Each policy has different compatibility with the available phases:

{% tabs %}
{% tab title="v4 API definition" %}
v4 APIs have the following phases:

* `onRequest`: This phase is executed before invoking the backend services for both proxy and message APIs. Policies can act on the headers and the content for proxy APIs.
* `onMessageRequest`: This phase occurs after the `onRequest` phase and allows policies to act on each incoming message before being sent to the backend service. This only applies to message APIs.
* `onResponse`: This phase is executed after invoking the backend services for both proxy and message APIs. Policies can act on the headers and the content for proxy APIs.
* `onMessageResponse`: This phase after the `onResponse` phase and allows policies to act on each outgoing message before being sent to the client application. This only applies to message APIs.

This policy is compatible with the following v4 API phases:

<table data-full-width="false"><thead><tr><th width="138" data-type="checkbox">onRequest</th><th width="134" data-type="checkbox">onResponse</th><th data-type="checkbox">onMessageRequest</th><th data-type="checkbox">onMessageResponse</th></tr></thead><tbody><tr><td>true</td><td>true</td><td>true</td><td>true</td></tr></tbody></table>
{% endtab %}

{% tab title="v2 API definition" %}
v2 APIs have the following phases:

* `onRequest`: This phase only allows policies to work on request headers. It never accesses the request body.
* `onRequestContent`: This phase always occurs after the `onRequest` phase. It allows policies to work at the content level and access the request body.
* `onResponse`: This phase only allows policies to work on response headers. It never accesses the response body.
* `onResponseContent`: This phase always occurs after the `onResponse` phase. It allows policies to work at the content level and access the response body.

This policy supports the following phases:

<table><thead><tr><th width="134" data-type="checkbox">onRequest</th><th width="144" data-type="checkbox">onResponse</th><th width="191" data-type="checkbox">onRequestContent</th><th data-type="checkbox">onResponseContent</th></tr></thead><tbody><tr><td>false</td><td>false</td><td>true</td><td>true</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

## Compatibility matrix

In the [changelog for each version of APIM](../../releases-and-changelog/changelog/), we provide a list of policies included in the default distribution. The chart below summarizes this information in relation to the `json-xml` policy.

<table data-full-width="false"><thead><tr><th width="161.33333333333331">Plugin Version</th><th width="242">Supported APIM versions</th><th>Included in APIM default distribution</th></tr></thead><tbody><tr><td>2.2</td><td>>=3.20</td><td>>=3.21</td></tr><tr><td>2.1</td><td>^3.0</td><td>>=3.0 &#x3C;3.21</td></tr><tr><td>2.0</td><td>^3.0</td><td>N/a</td></tr></tbody></table>

## Installation and deployment

Each version of APIM includes a number of policies by default. If the policy is not included in the default distribution or you would like to use a different version of the policy, you can modify the plugin.

{% hint style="warning" %}
Please ensure the policy version you select is compatible with your version of APIM.
{% endhint %}

To do so, follow these steps:

1. Download the plugin archive (a `.zip` file) from [the plugins download page](https://download.gravitee.io/#graviteeio-apim/plugins/)
2. Add the file into the `plugins` folder for both the gateway and management API

{% hint style="info" %}
**Location of `plugins` folder**

The location of the `plugins` folder varies depending on your installation. By default, it is in ${GRAVITEE\_HOME/plugins}. This can be modified in [the `gravitee.yaml` file.](../../getting-started/configuration/the-gravitee-api-gateway/environment-variables-system-properties-and-the-gravitee.yaml-file.md#configure-the-plugins-repository)

Most installations will contain the `plugins` folder in`/gravitee/apim-gateway/plugins` for the gateway and `/gravitee/apim-management-api/plugins` for the management API.
{% endhint %}

3. Remove any existing plugins of the same name.
4. Restart your APIM nodes

## Errors

### Overview

<table data-full-width="true"><thead><tr><th width="225">Phase</th><th width="171">HTTP status code</th><th width="244">Error template key</th><th>Description</th></tr></thead><tbody><tr><td>onRequest</td><td><code>400</code></td><td>JSON_INVALID_PAYLOAD</td><td>Request payload cannot be transformed properly to XML</td></tr><tr><td>onResponse</td><td><code>500</code></td><td>JSON_INVALID_PAYLOAD</td><td>Response payload cannot be transformed properly to XML</td></tr><tr><td>onMessageRequest</td><td><code>400</code></td><td>JSON_INVALID_MESSAGE_PAYLOAD</td><td>Incoming message cannot be transformed properly to XML</td></tr><tr><td>onMessageResponse</td><td><code>500</code></td><td>JSON_INVALID_MESSAGE_PAYLOAD</td><td>Outgoing message cannot be transformed properly to XML</td></tr></tbody></table>

### Nested objects

To limit the processing time in the case of a nested object, the default max depth of a nested object has been set to 1000. This default value can be overridden using the environment variable `gravitee_policy_jsonxml_maxdepth`.

## Changelog

### 2.2

#### What's New?

* Blazingly fast
* Full chatgpt and neuralink integration for quick API mastery

#### Bug fixes

* Fix crashes related to nested objects

#### Breaking Changes

* Only supports APIM versions >4.0

### 2.1

#### What's New?

* Blazingly fast
* Full chatgpt and neuralink integration for quick API mastery

#### Bug fixes

* Fix crashes related to nested objects

#### Breaking Changes

* Only supports APIM versions >4.0
