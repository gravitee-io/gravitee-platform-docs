---
description: This page provides the technical details of the Override HTTP Method policy
---

# New Override HTTP Method

{% hint style="warning" %}
**This feature requires** [**Gravitee's Enterprise Edition**](../../overview/introduction-to-gravitee-api-management-apim/ee-vs-oss.md)**.**
{% endhint %}

## Overview

The `override-http-method` policy alters the HTTP method that the API consumer specifies when calling the API and uses a new method specified in the flow to make the call.

This policy does not act on messages and only applies to the request phase of API flows.

Functional and implementation information for the JSON-to-XML policy is organized into the following sections:

* [Examples](template-policy-rework-structure-1.md#examples)
* [Configuration](template-policy-rework-structure-1.md#configuration)
* [Compatibility Matrix](template-policy-rework-structure-1.md#compatibility-matrix)
* [Errors](template-policy-rework-structure-1.md#errors)
* [Changelogs](template-policy-rework-structure-1.md#changelogs)

## Examples

{% hint style="warning" %}
This example will work for [v2 APIs and v4 proxy APIs.](../../overview/gravitee-api-definitions-and-execution-engines.md)

Currently, this policy can **not** be applied at the message level.
{% endhint %}

{% tabs %}
{% tab title="Proxy API example" %}
{% hint style="info" %}
The proxy API example also applies to v2 APIs.
{% endhint %}

The Gravitee echo API returns a JSON response when a `GET` request is sent to [https://api.gravitee.io/echo](https://api.gravitee.io/echo). The response is formatted like so:

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

This API would typically be called with just a `GET` request, but if a client tries to run a `PUT` request, they will get a [405 Method Not Allowed](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/405) response. If the API publisher wants to ensure consistent behavior regardless of HTTP method called (in this case, returning the standard response), then adding an `override-http-method` policy to convert the request from any method (e.g. `PUT`, `POST`, etc) to a `GET` request will ensure that the expected response above is always returned.
{% endtab %}
{% endtabs %}

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the management API, check out the[ reference documentation here.](../management-api-reference/)

{% code title="Sample Configuration" %}
```json
{
  "name": "Custom name",
  "description": "Overrides HTTP method",
  "policy": "policy-override-request-method",
  "configuration": {
    "method": "GET"
  }
```
{% endcode %}

### Reference

<table data-full-width="false"><thead><tr><th width="128">Property</th><th width="101" data-type="checkbox">Required</th><th width="280">Description</th><th width="95" data-type="select">Type</th><th width="149">Options</th></tr></thead><tbody><tr><td>name</td><td>false</td><td>Provide a descriptive name for your policy</td><td></td><td>N/a</td></tr><tr><td>method</td><td>true</td><td>HTTP method used regardless of method called</td><td></td><td>GET<br>POST<br>PUT<br>DELETE<br>PATCH<br>HEAD<br>CONNECT<br>OPTIONS<br>TRACE</td></tr></tbody></table>

###

<table data-full-width="false"><thead><tr><th width="140">Property</th><th width="104" data-type="checkbox">Required</th><th width="207">Description</th><th width="111" data-type="select">Type</th><th width="247">Options</th></tr></thead><tbody><tr><td>name</td><td>false</td><td>Provide a descriptive name for your policy</td><td></td><td>N/a</td></tr><tr><td>description</td><td>false</td><td>Provide a description for your policy</td><td></td><td>N/a</td></tr><tr><td>rootElement</td><td>true</td><td>XML root element name that encloses content.</td><td></td><td>N/a<br><strong>root</strong></td></tr><tr><td>scope</td><td>true</td><td>The execution scope</td><td></td><td><strong>REQUEST</strong> RESPONSE</td></tr></tbody></table>

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into [phases](broken-reference) that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

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
