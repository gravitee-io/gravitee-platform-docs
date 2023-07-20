---
description: This page provides the technical details of the XML Validation policy
---

# XML Validation

## Overview

Functional and implementation information for the JSON-to-XML policy is organized into the following sections:

* [Configuration](template-policy-rework-structure-38.md#configuration)
* [Compatibility](template-policy-rework-structure-38.md#compatibility-matrix)
* [Errors](template-policy-rework-structure-38.md#errors)

{% hint style="warning" %}
This example will work for [v2 APIs and v4 proxy APIs.](../../overview/gravitee-api-definitions-and-execution-engines.md)

Currently, this policy can **not** be applied at the message level.
{% endhint %}

You can use the `xml-validation` policy to validate XML using an XSD schema. This policy uses `javax.xml`. A 400 BAD REQUEST error is received with a custom error message body with a custom error message body when validation fails. Injects processing report messages into request metrics for analytics.

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

### Reference

<table><thead><tr><th>Property</th><th data-type="checkbox">Required</th><th>Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>errorMessage</td><td>false</td><td>Custom error message in XML format. Spel is allowed.</td><td>string</td><td>validation/internal</td></tr><tr><td>xsdSchema</td><td>true</td><td>Xsd schema.</td><td>string</td><td></td></tr></tbody></table>

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into [phases](broken-reference) that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the XML Validation policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="188.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>false</td><td>onRequest</td><td>false</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

## Compatibility matrix

The [changelog for each version of APIM](../../releases-and-changelog/changelog/) provides a list of policies included in the default distribution.&#x20;

## Errors

<table data-full-width="false"><thead><tr><th width="171">HTTP status code</th><th width="387">Message</th></tr></thead><tbody><tr><td><code>400</code></td><td><p>Applies to:</p><p>* Invalid payload</p><p>* Invalid XSD schema</p><p>* Invalid error message XML format</p></td></tr></tbody></table>
