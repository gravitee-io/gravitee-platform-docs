---
description: This page provides the technical details of the XML to JSON policy
---

# XML to JSON

## Overview

Functional and implementation information for the JSON-to-XML policy is organized into the following sections:

* [Configuration](template-policy-rework-structure-40.md#configuration)
* [Compatibility Matrix](template-policy-rework-structure-40.md#compatibility-matrix)
* [Errors](template-policy-rework-structure-40.md#errors)
* [Changelogs](template-policy-rework-structure-40.md#changelogs)

You can use the `xml-json` policy to transform XML content to JSON content.

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

{% code title="Sample Configuration" %}
```json
"xml-json": {
    "scope": "RESPONSE"
}
```
{% endcode %}

### Reference

<table><thead><tr><th>Property</th><th data-type="checkbox">Required</th><th>Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>scope</td><td>true</td><td>The execution scope (<code>request</code> or <code>response</code>).</td><td>string</td><td><code>RESPONSE</code></td></tr></tbody></table>

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into phases that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the XML-to-JSON policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="188.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>true</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

## Compatibility

The [changelog for each version of APIM](../../releases-and-changelog/changelog/) provides a list of policies included in the default distribution.

## Errors

### HTTP status code

| Code  | Message                                        |
| ----- | ---------------------------------------------- |
| `500` | The transformation cannot be executed properly |

### Nested objects

To limit the processing time and memory consumption in case of nested object, a default max depth of nested object has been defined to 100. This default value can be overridden using the environment variable `gravitee_policy_xmljson_maxdepth`.

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-xml-json/blob/master/CHANGELOG.md" %}
