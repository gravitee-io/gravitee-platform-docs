---
description: This page provides the technical details of the Data Logging Masking policy
---

# Data Logging Masking

{% hint style="warning" %}
**This feature requires** [**Gravitee's Enterprise Edition**](../../overview/introduction-to-gravitee-api-management-apim/ee-vs-oss.md)**.**
{% endhint %}

## Overview

Functional and implementation information for the Data Logging Masking policy is organized into the following sections:

* [Configuration](template-policy-rework-structure-8.md#configuration)
* [Compatibility Matrix](template-policy-rework-structure-8.md#compatibility-matrix)
* [Errors](template-policy-rework-structure-8.md#errors)
* [Changelogs](template-policy-rework-structure-8.md#changelogs)

**If you enable logging on APIs**, you can use the `data-logging-masking` policy to configure rules to conceal sensitive data. You can use `json-path`, `xml-path` or a regular expression to identify the information to hide.

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

### Reference

<table><thead><tr><th>Property</th><th data-type="checkbox">Required</th><th>Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>scope</td><td>true</td><td>Scope where the policy is executed</td><td>Policy scope</td><td>REQUEST_CONTENT</td></tr><tr><td>headerRules</td><td>false</td><td>List of mask rules to apply on client and proxy headers</td><td>List&#x3C;MaskHeaderRule></td><td></td></tr><tr><td>bodyRules</td><td>false</td><td>List of mask rules to apply on client and proxy body</td><td>List&#x3C;MaskBodyRule></td><td></td></tr></tbody></table>

#### Mask header rule

| Property | Required | Description              | Type   | Default |
| -------- | -------- | ------------------------ | ------ | ------- |
| path     |          | Header name to transform | String |         |
| replacer |          | Replacement character    | String | \*      |

#### Mask body rule

| Property | Required | Description                                                                                                                                                      | Type        | Default |
| -------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- | ------- |
| path     |          | Context-dependent. If "Content-type" is `application / json` you must use `json-path`, if it is "application / xml" you must use `xml-path`, otherwise not used. | String      |         |
| type     |          | Value selector type                                                                                                                                              | MaskPattern |         |
| regex    |          | Custom value selector (use regular expression)                                                                                                                   | String      |         |
| replacer |          | Replacement character                                                                                                                                            | String      |         |

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into [phases](broken-reference) that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the Data Logging Masking policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>false</td><td>onRequest</td><td>false</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>true</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

## Compatibility matrix

The [changelog for each version of APIM](../../releases-and-changelog/changelog/) provides a list of policies included in the default distribution. The chart below summarizes this information in relation to the `Data-logging-masking` policy.

<table data-full-width="false"><thead><tr><th width="161.33333333333331">Plugin Version</th><th width="242">Supported APIM versions</th><th>Included in APIM default distribution</th></tr></thead><tbody><tr><td>>= 2.x</td><td>>=3.18</td><td>N/A</td></tr><tr><td>1.x - 2.x</td><td>&#x3C;= 3.17.x</td><td>N/A</td></tr></tbody></table>
