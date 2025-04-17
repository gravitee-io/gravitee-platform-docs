---
hidden: true
---

# JSON Validation

## Overview

You can use the `json-validation` policy to validate JSON payloads. This policy uses [JSON Schema Validator](https://github.com/java-json-tools/json-schema-validator). It returns `400 BAD REQUEST` when request validation fails and `500 INTERNAL ERROR` when response validation fails, with a custom error message body. It can inject processing report messages into request metrics for analytics.

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs and both v4 HTTP proxy and v4 message APIs. It cannot be applied to v4 TCP proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="HTTP proxy API example" %}
Sample policy configuration:

```json
{
	"errorMessage": "Json payload invalid",
	"schema": "{\"title\": \"Person\", \"type\": \"object\", \"properties\": {\"name\": {\"type\": \"string\"}}, \"required\": [\"name\"]}",
	"validateUnchecked": false,
	"deepCheck": false,
	"straightResponseMode": false
}
```
{% endtab %}
{% endtabs %}

## Configuration

### Phases

The phases checked below are supported by the `json-validation` policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>false</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>true</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>true</td></tr><tr><td>onResponseContent</td><td>true</td><td>onMessageResponse</td><td>true</td></tr></tbody></table>

### Options

The `json-validation` policy can be configured with the following options:

<table><thead><tr><th width="227">Property</th><th width="112" data-type="checkbox">Required</th><th width="235">Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>scope</td><td>true</td><td>Policy scope from where the policy is executed</td><td>Policy scope</td><td>REQUEST_CONTENT</td></tr><tr><td>errorMessage</td><td>true</td><td>Custom error message in JSON format. Spel is allowed.</td><td>string</td><td>{"error":"Bad request"}</td></tr><tr><td>schema</td><td>true</td><td>Json schema.</td><td>string</td><td></td></tr><tr><td>deepCheck</td><td>false</td><td>Validate descendant even if JSON parent container is invalid</td><td>boolean</td><td>false</td></tr><tr><td>validateUnchecked</td><td>false</td><td>Unchecked validation means that conditions which would normally cause the processing to stop with an exception are instead inserted into the resulting report. Warning: this means that anomalous events like an unresolvable JSON Reference, or an invalid schema, are masked!.</td><td>boolean</td><td>false</td></tr><tr><td>straightRespondMode</td><td>false</td><td>Only for RESPONSE scope. Straight respond mode means that responses failed to validate still will be sent to user without replacement. Validation failures messages are still being written to the metrics for further inspection.</td><td>boolean</td><td>false</td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `json-validation` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>1.x</td><td>All</td></tr></tbody></table>

## Errors

<table data-full-width="false"><thead><tr><th width="210">Phase</th><th width="171">HTTP status code</th><th width="387">Error template key</th></tr></thead><tbody><tr><td>onRequestContent</td><td><code>400</code></td><td><p>Invalid payload</p><p>Invalid JSON schema</p><p>Invalid error message JSON format</p></td></tr><tr><td>onResponseContent</td><td><code>500</code></td><td><p>Invalid payload</p><p>Invalid JSON schema</p><p>Invalid error message JSON format</p></td></tr></tbody></table>

You can use the response template feature to override the default response provided by the policy. These templates must be defined at the API level (see the API Console **Response Templates** option in the API **Proxy** menu).

The policy sends the following error keys:

<table data-full-width="false"><thead><tr><th width="355.6456692913386">Key</th><th width="171">Parameters</th></tr></thead><tbody><tr><td>JSON_INVALID_PAYLOAD</td><td>-</td></tr><tr><td>JSON_INVALID_FORMAT</td><td>-</td></tr><tr><td>JSON_INVALID_RESPONSE_PAYLOAD</td><td>-</td></tr><tr><td>JSON_INVALID_RESPONSE_FORMAT</td><td>-</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-json-validation/blob/master/CHANGELOG.md" %}
