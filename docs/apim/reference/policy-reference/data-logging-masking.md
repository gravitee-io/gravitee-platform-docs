---
description: This page provides the technical details of the Data Logging Masking policy
---

# Data Logging Masking

{% hint style="warning" %}
**This feature requires** [**Gravitee's Enterprise Edition**](../../overview/introduction-to-gravitee-api-management-apim/ee-vs-oss.md)**.**
{% endhint %}

## Overview

If you enable logging on APIs, you can use the `data-logging-masking` policy to configure rules to conceal sensitive data. You can use `json-path`, `xml-path` or a regular expression to identify the information to hide.

Functional and implementation information for the `data-logging-masking` policy is organized into the following sections:

* [Configuration](data-logging-masking.md#configuration)
* [Compatibility Matrix](data-logging-masking.md#compatibility-matrix)

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into [phases](broken-reference/) that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the `data-logging-masking` policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>false</td><td>onRequest</td><td>false</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>true</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

You can configure the `data-logging-masking` policy with the following options:

<table><thead><tr><th>Property</th><th data-type="checkbox">Required</th><th>Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>scope</td><td>true</td><td>Scope where the policy is executed</td><td>Policy scope</td><td>REQUEST_CONTENT</td></tr><tr><td>headerRules</td><td>false</td><td>List of mask rules to apply on client and proxy headers</td><td>List&#x3C;MaskHeaderRule></td><td></td></tr><tr><td>bodyRules</td><td>false</td><td>List of mask rules to apply on client and proxy body</td><td>List&#x3C;MaskBodyRule></td><td></td></tr></tbody></table>

#### Mask header rule

| Property | Required | Description              | Type   | Default |
| -------- | -------- | ------------------------ | ------ | ------- |
| path     |          | Header name to transform | String |         |
| replacer |          | Replacement character    | String | \*      |

#### Mask body rule

<table><thead><tr><th>Property</th><th width="104">Required</th><th>Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>path</td><td></td><td>Context-dependent. If "Content-type" is <code>application / json</code> you must use <code>json-path</code>, if it is "application / xml" you must use <code>xml-path</code>, otherwise not used.</td><td>String</td><td></td></tr><tr><td>type</td><td></td><td>Value selector type</td><td>MaskPattern</td><td></td></tr><tr><td>regex</td><td></td><td>Custom value selector (use regular expression)</td><td>String</td><td></td></tr><tr><td>replacer</td><td></td><td>Replacement character</td><td>String</td><td></td></tr></tbody></table>

### Compatibility matrix

The [changelog for each version of APIM](../../releases-and-changelogs/changelogs/) provides a list of policies included in the default distribution. The chart below summarizes this information in relation to the `data-logging-masking` policy.

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>>= 2.x</td><td>>=3.18</td></tr><tr><td>1.x - 2.x</td><td>&#x3C;= 3.17.x</td></tr></tbody></table>
