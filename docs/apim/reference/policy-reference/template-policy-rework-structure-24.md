---
description: This page provides the technical details of the JSON-to-XML policy
---

# Regex Threat Protection

{% hint style="warning" %}
**This feature requires** [**Gravitee's Enterprise Edition**](../../overview/introduction-to-gravitee-api-management-apim/ee-vs-oss.md)**.**
{% endhint %}

## Overview

Functional and implementation information for the JSON-to-XML policy is organized into the following sections:

* [Configuration](template-policy-rework-structure-24.md#configuration)
* [Errors](template-policy-rework-structure-24.md#errors)
* [Changelogs](template-policy-rework-structure-24.md#changelogs)



{% hint style="warning" %}
This example will work for [v2 APIs and v4 proxy APIs.](../../overview/gravitee-api-definitions-and-execution-engines.md)

Currently, this policy can **not** be applied at the message level.
{% endhint %}

You can use the `regex-threat-protection` to extract information from a request (headers, path, query parameters, body payload) and evaluate that content against pre-defined regular expressions. If any content matches the specified regular expression, the request is considered a threat and rejected with a 400 BAD REQUEST. The policy injects processing report messages into request metrics for analytics.

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

### Reference

<table><thead><tr><th>Property</th><th data-type="checkbox">Required</th><th>Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>regex</td><td>true</td><td>Regex used to detect malicious injections. You can enable this regular expression on headers, path and body or add multiple Regex threat protection policies with different regex, depending on your needs.</td><td>string</td><td></td></tr><tr><td>caseSensitive</td><td>false</td><td>Perform case-sensitive matching. <strong>WARNING</strong>: Use with caution. Enabling case sensitive matching may miss some risky patterns such as <code>DrOp TaBlE</code>.</td><td>boolean</td><td>false</td></tr><tr><td>checkHeaders</td><td>false</td><td>Evaluate regex on request headers</td><td>boolean</td><td>true</td></tr><tr><td>checkPath</td><td>false</td><td>Evaluate regex on request path and query parameters</td><td>boolean</td><td>true</td></tr><tr><td>checkBody</td><td>false</td><td>Evaluate regex on request body content</td><td>boolean</td><td>true</td></tr></tbody></table>

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into [phases](broken-reference) that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the Regex threat Protection policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="188.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>false</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>true</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>true</td></tr><tr><td>onResponseContent</td><td>true</td><td>onMessageResponse</td><td>true</td></tr></tbody></table>

## Compatibility

The [changelog for each version of APIM](../../releases-and-changelog/changelog/) provides a list of policies included in the default distribution.&#x20;

## Errors

#### HTTP status code

| Code  | Message                                                                                                                                      |
| ----- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `400` | <p>Applies to:</p><ul><li>Matching request headers</li><li>Matching request path or query parameters</li><li>Matching request body</li></ul> |

#### Default response override

You can use the response template feature to override the default response provided by the policy. These templates must be defined at the API level (see the API Console **Response Templates** option in the API **Proxy** menu).

#### Error keys

The error keys sent by this policy are as follows:

| Key                      | Parameters |
| ------------------------ | ---------- |
| HEADER\_THREAT\_DETECTED | -          |
| PATH\_THREAT\_DETECTED   | -          |
| BODY\_THREAT\_DETECTED   | -          |

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-regex-threat-protection/blob/master/CHANGELOG.md" %}
