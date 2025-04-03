---
description: This page provides the technical details of the XML to JSON policy
hidden: true
---

# XML to JSON

## Overview

You can use the `xml-json` policy to transform XML content into JSON content.

Functional and implementation information for the `xml-json` policy is organized into the following sections:

* [Examples](xml-to-json.md#examples)
* [Configuration](xml-to-json.md#configuration)
* [Compatibility Matrix](xml-to-json.md#compatibility-matrix)
* [Errors](xml-to-json.md#errors)
* [Changelogs](xml-to-json.md#changelogs)

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs, v4 HTTP proxy APIs, and v4 message APIs. It cannot be applied to v4 TCP proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="HTTP proxy API example" %}
Example request configuration:

```json
{
    "name": "Xml to Json",
    "description": "",
    "enabled": true,
    "policy": "xml-json",
    "configuration": {}
 }
```
{% endtab %}

{% tab title="Message API example" %}
Example subscribe configuration:

```json
{
    "name": "Xml to Json",
    "description": "",
    "enabled": true,
    "policy": "xml-json",
    "configuration": {}
}
```
{% endtab %}
{% endtabs %}

## Configuration

### Phases

The phases checked below are supported by the `xml-json` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="197.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>false</td><td>onRequest</td><td>false</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>true</td></tr><tr><td>onResponseContent</td><td>true</td><td>onMessageResponse</td><td>true</td></tr></tbody></table>

### Reference

The `xml-json` policy can be configured with the following options:

<table><thead><tr><th width="128">Property</th><th data-type="checkbox">Required</th><th width="253">Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>scope</td><td>true</td><td>The execution scope (<code>request</code> or <code>response</code>).</td><td>string</td><td><code>RESPONSE</code></td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `xml-json` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>1.x</td><td>3.x</td></tr><tr><td>2.x</td><td>4.0+</td></tr></tbody></table>

## Errors

<table><thead><tr><th width="185.5">HTTP status code</th><th>Message</th></tr></thead><tbody><tr><td><code>500</code></td><td>The transformation cannot be executed properly</td></tr></tbody></table>

### Nested objects

To limit the processing time and memory consumption in case of nested object, a default max depth of nested object has been defined to 100. This default value can be overridden using the environment variable `gravitee_policy_xmljson_maxdepth`.

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-xml-json/blob/master/CHANGELOG.md" %}
