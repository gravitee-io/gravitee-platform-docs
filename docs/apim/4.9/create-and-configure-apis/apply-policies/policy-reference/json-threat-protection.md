---
description: An overview about json threat protection.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/bGmDEarvnV52XdcOiV8o/create-and-configure-apis/apply-policies/policy-reference/json-threat-protection
---

# JSON Threat Protection

## Overview

You can use the `json-threat-protection` policy to validate a JSON request body by specifying limits for various JSON structures (such as arrays, field names and string values). When an invalid request is detected (meaning the limit is reached), the request will be considered a threat and rejected with a `400 BAD REQUEST`.

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs and v4 HTTP proxy APIs. It cannot be applied to v4 message APIs or v4 TCP proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="HTTP proxy API example" %}
Sample policy configuration:

```json
{
  "name" : "JSON Threat Protection",
  "enabled" : true,
  "policy" : "json-threat-protection",
  "configuration" : {
    "maxDepth" : 90,
    "maxNameLength" : 90,
    "maxValueLength" : 400,
    "maxEntries" : 90,
    "maxArraySize" : 90
  }
}
```
{% endtab %}
{% endtabs %}

## Configuration

### Phases

The phases checked below are supported by the `json-threat-protection` policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>false</td><td>onRequest</td><td>false</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

The `json-threat-protection` policy can be configured with the following options:

<table><thead><tr><th width="185">Property</th><th width="106" data-type="checkbox">Required</th><th width="227">Description</th><th width="179">Type</th><th>Default</th></tr></thead><tbody><tr><td>maxEntries</td><td>false</td><td>Maximum number of entries allowed for a JSON object. Example: In <code>{ "a":{ "b":1, "c":2, "d":3 }}</code>, <code>a</code> has 3 entries</td><td>integer (-1 to specify no limit)</td><td>100</td></tr><tr><td>maxArraySize</td><td>false</td><td>Maximum number of elements allowed in an array</td><td>integer (-1 to specify no limit)</td><td>100</td></tr><tr><td>maxDepth</td><td>false</td><td>Maximum depth of JSON structure. Example: <code>{ "a":{ "b":{ "c":true }}}</code> has a depth of 3.</td><td>integer (-1 to specify no limit)</td><td>100</td></tr><tr><td>maxNameLength</td><td>false</td><td>Maximum string length allowed for a JSON property name</td><td>integer (-1 to specify no limit)</td><td>100</td></tr><tr><td>maxValueLength</td><td>false</td><td>Maximum string length allowed for a JSON property value</td><td>integer (-1 to specify no limit)</td><td>500</td></tr></tbody></table>

## Errors

<table data-full-width="false"><thead><tr><th width="196.5">HTTP status code</th><th width="387">Message</th></tr></thead><tbody><tr><td><code>400</code></td><td><ul><li>Invalid JSON structure</li><li>Maximum depth exceeded</li><li>Maximum JSON entries exceeded</li><li>Maximum JSON array size exceeded</li><li>Maximum JSON field name length exceeded</li><li>Maximum JSON field value length exceeded</li></ul></td></tr></tbody></table>

You can override the default response provided by the policy with the response templates feature. These templates must be defined at API level (see the API Console **Response Templates** option in the API **Proxy** menu).

The error keys sent by this policy are as follows:

<table><thead><tr><th width="339.5">Key</th><th>Parameters</th></tr></thead><tbody><tr><td>JSON_THREAT_DETECTED</td><td>-</td></tr><tr><td>JSON_THREAT_MAX_DEPTH</td><td>-</td></tr><tr><td>JSON_THREAT_MAX_ENTRIES</td><td>-</td></tr><tr><td>JSON_THREAT_MAX_NAME_LENGTH</td><td>-</td></tr><tr><td>JSON_THREAT_MAX_VALUE_LENGTH</td><td>-</td></tr><tr><td>JSON_MAX_ARRAY_SIZE</td><td>-</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-json-threat-protection/blob/master/CHANGELOG.md" fullWidth="true" %}
