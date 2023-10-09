---
description: This page provides the technical details of the XML Validation policy
---

# XML Validation

## Overview

You can use the `xml-validation` policy to validate XML using an XSD schema. This policy uses `javax.xml`. A 400 BAD REQUEST error is received with a custom error message body when validation fails. Injects processing report messages into request metrics for analytics.

Functional and implementation information for the `xml-validation` policy is organized into the following sections:

* [Configuration](xml-validation.md#configuration)
* [Compatibility Matrix](xml-validation.md#compatibility-matrix)
* [Errors](xml-validation.md#errors)

{% hint style="warning" %}
This policy can be applied to v2 APIs and v4 proxy APIs. It cannot be applied to v4 message APIs.
{% endhint %}

## Configuration

### Phases

The phases checked below are supported by the `xml-validation` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="202.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>false</td><td>onRequest</td><td>false</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

The `xml-validation` policy can be configured with the following options:

<table><thead><tr><th width="160">Property</th><th data-type="checkbox">Required</th><th width="248">Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>errorMessage</td><td>false</td><td>Custom error message in XML format. Spel is allowed.</td><td>string</td><td>validation/internal</td></tr><tr><td>xsdSchema</td><td>true</td><td>Xsd schema.</td><td>string</td><td></td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `xml-validation` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>1.x</td><td>All</td></tr></tbody></table>

## Errors

<table data-full-width="false"><thead><tr><th width="201.5">HTTP status code</th><th width="387">Message</th></tr></thead><tbody><tr><td><code>400</code></td><td><p>* Invalid payload</p><p>* Invalid XSD schema</p><p>* Invalid error message XML format</p></td></tr></tbody></table>
