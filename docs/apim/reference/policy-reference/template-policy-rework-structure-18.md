---
description: This page provides the technical details of the JSON Validation policy
---

# JSON Validation

## Overview



{% hint style="warning" %}
This example will work for [v2 APIs and v4 proxy APIs.](../../overview/gravitee-api-definitions-and-execution-engines.md)

Currently, this policy can **not** be applied at the message level.
{% endhint %}

Functional and implementation information for the JSON Validation policy is organized into the following sections:

* [Configuration](template-policy-rework-structure-18.md#configuration)
* [Errors](template-policy-rework-structure-18.md#errors)
* [Changelogs](template-policy-rework-structure-18.md#changelogs)

You can use the `json-validation` policy to validate JSON payloads. This policy uses [JSON Schema Validator](https://github.com/java-json-tools/json-schema-validator). It returns 400 BAD REQUEST when request validation fails and 500 INTERNAL ERROR when response validation fails, with a custom error message body. It can inject processing report messages into request metrics for analytics.

## Configuration

### Reference

<table><thead><tr><th>Property</th><th data-type="checkbox">Required</th><th>Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>scope</td><td>true</td><td>Policy scope from where the policy is executed</td><td>Policy scope</td><td>REQUEST_CONTENT</td></tr><tr><td>errorMessage</td><td>true</td><td>Custom error message in JSON format. Spel is allowed.</td><td>string</td><td>{"error":"Bad request"}</td></tr><tr><td>schema</td><td>true</td><td>Json schema.</td><td>string</td><td></td></tr><tr><td>deepCheck</td><td>false</td><td>Validate descendant even if JSON parent container is invalid</td><td>boolean</td><td>false</td></tr><tr><td>validateUnchecked</td><td>false</td><td>Unchecked validation means that conditions which would normally cause the processing to stop with an exception are instead inserted into the resulting report. Warning: this means that anomalous events like an unresolvable JSON Reference, or an invalid schema, are masked!.</td><td>boolean</td><td>false</td></tr><tr><td>straightRespondMode</td><td>false</td><td>Only for RESPONSE scope. Straight respond mode means that responses failed to validate still will be sent to user without replacement. Validation failures messages are still being written to the metrics for further inspection.</td><td>boolean</td><td>false</td></tr></tbody></table>

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into [phases](broken-reference) that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the JSON Validation policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>false</td><td>onRequest</td><td>false</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>true</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

## Errors

<table data-full-width="false"><thead><tr><th width="210">Phase</th><th width="171">HTTP status code</th><th width="387">Error template key</th></tr></thead><tbody><tr><td>onRequestContent</td><td><code>400</code></td><td><p>Sent in the following cases:</p><p>* Invalid payload</p><p>* Invalid JSON schema</p><p>* Invalid error message JSON format</p></td></tr><tr><td>onResponseContent</td><td><code>500</code></td><td><p>Sent in the following cases:</p><p>* Invalid payload</p><p>* Invalid JSON schema</p><p>* Invalid error message JSON format</p></td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-json-validation/blob/master/CHANGELOG.md" %}
