---
description: This page provides the technical details of the JSON Threat Protection policy
---

# JSON Threat Protection

## Overview

{% hint style="warning" %}
This example will work for [v2 APIs and v4 proxy APIs.](../../overview/gravitee-api-definitions-and-execution-engines.md)

Currently, this policy can **not** be applied at the message level.
{% endhint %}

Functional and implementation information for the JSON Threat Protection policy is organized into the following sections:

* [Configuration](template-policy-rework-structure-14.md#configuration)
* [Errors](template-policy-rework-structure-14.md#errors)
* [Changelogs](template-policy-rework-structure-14.md#changelogs)

You can use the `json-threat-protection` policy to validate a JSON request body by specifying limits for various JSON structures (such as arrays, field names and string values). When an invalid request is detected (meaning the limit is reached), the request will be considered a threat and rejected with a `400 BAD REQUEST`.

## Configuration

### Reference

<table><thead><tr><th>Property</th><th data-type="checkbox">Required</th><th>Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>maxEntries</td><td>false</td><td>Maximum number of entries allowed for a JSON object. Example: In <code>{ "a":{ "b":1, "c":2, "d":3 }}</code>, <code>a</code> has 3 entries</td><td>integer (-1 to specify no limit)</td><td>100</td></tr><tr><td>maxArraySize</td><td>false</td><td>Maximum number of elements allowed in an array</td><td>integer (-1 to specify no limit)</td><td>100</td></tr><tr><td>maxDepth</td><td>false</td><td>Maximum depth of JSON structure. Example: <code>{ "a":{ "b":{ "c":true }}}</code> has a depth of 3.</td><td>integer (-1 to specify no limit)</td><td>100</td></tr><tr><td>maxNameLength</td><td>false</td><td>Maximum string length allowed for a JSON property name</td><td>integer (-1 to specify no limit)</td><td>100</td></tr><tr><td>maxValueLength</td><td>false</td><td>Maximum string length allowed for a JSON property value</td><td>integer (-1 to specify no limit)</td><td>500</td></tr></tbody></table>

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into [phases](broken-reference) that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the JSON Threat Protection policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>false</td><td>onRequest</td><td>false</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

## Errors

<table data-full-width="false"><thead><tr><th width="210">Phase</th><th width="171">HTTP status code</th><th width="387">Message</th></tr></thead><tbody><tr><td>onRequestContent</td><td><code>400</code></td><td><p></p><p>Received in the following cases:</p><ul><li>Invalid JSON structure</li><li>Maximum depth exceeded</li><li>Maximum JSON entries exceeded</li><li>Maximum JSON array size exceeded</li><li>Maximum JSON field name length exceeded</li><li>Maximum JSON field value length exceeded</li></ul></td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-json-threat-protection/blob/master/CHANGELOG.md" %}
