---
description: This page provides the technical details of the Rate Limit policy
---

# Rate Limit

## Overview

Functional and implementation information for the Rate Limit policy is organized into the following sections:

* [Examples](template-policy-rework-structure-24.md#examples)
* [Configuration](template-policy-rework-structure-24.md#configuration)
* [Errors](template-policy-rework-structure-24.md#errors)
* [Changelogs](template-policy-rework-structure-24.md#changelogs)

## Examples

There are three `rate-limit` policies:

* **Quota**: configures the number of requests allowed over a period of time (hours, days, weeks, months)
* **Rate-Limit**: configures the number of requests allowed over a limited period of time (seconds, minutes)
* **Spike-Arrest**: throttles the number of requests processed and sends them to the backend to avoid a spike

{% hint style="warning" %}
This example will work for [v2 APIs and v4 proxy APIs.](../../overview/gravitee-api-definitions-and-execution-engines.md)

Currently, this policy can **not** be applied at the message level.
{% endhint %}

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

### Quota

{% code title="Sample Configuration" %}
```json
"quota": {
    "limit": "1000",
    "periodTime": 1,
    "periodTimeUnit": "MONTHS"
  }
```
{% endcode %}

#### Reference

<table><thead><tr><th>Property</th><th data-type="checkbox">Required</th><th>Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>key</td><td>false</td><td>Key to identify a consumer to apply the quota against. Leave it empty to apply the default behavior (plan/subscription pair). Supports Expression Language.</td><td>String</td><td>null</td></tr><tr><td>limit</td><td>false</td><td>Static limit on the number of requests that can be sent (this limit is used if the value > 0).</td><td>integer</td><td>0</td></tr><tr><td>dynamicLimit</td><td>false</td><td>Dynamic limit on the number of requests that can be sent (this limit is used if static limit = 0). The dynamic value is based on Expression Language expressions.</td><td>string</td><td>null</td></tr><tr><td>periodTime</td><td>true</td><td>Time duration</td><td>Integer</td><td>1</td></tr><tr><td>periodTimeUnit</td><td>true</td><td>Time unit (<code>HOURS</code>, <code>DAYS</code>, <code>WEEKS</code>, <code>MONTHS</code>)</td><td>String</td><td>MONTHS</td></tr></tbody></table>

### Rate Limit

{% code title="Sample Configuration" %}
```json
"rate": {
    "limit": "10",
    "periodTime": 10,
    "periodTimeUnit": "MINUTES"
  }
```
{% endcode %}

#### Reference

<table><thead><tr><th>Property</th><th data-type="checkbox">Required</th><th>Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>key</td><td>false</td><td>Key to identify a consumer to apply rate-limiting against. Leave it empty to use the default behavior (plan/subscription pair). Supports Expression Language.</td><td>String</td><td>null</td></tr><tr><td>limit</td><td>false</td><td>Static limit on the number of requests that can be sent (this limit is used if the value > 0).</td><td>integer</td><td>0</td></tr><tr><td>dynamicLimit</td><td>false</td><td>Dynamic limit on the number of requests that can be sent (this limit is used if static limit = 0). The dynamic value is based on Expression Language expressions.</td><td>string</td><td>null</td></tr><tr><td>periodTime</td><td>true</td><td>Time duration</td><td>Integer</td><td>1</td></tr><tr><td>periodTimeUnit</td><td>true</td><td>Time unit ("SECONDS", "MINUTES" )</td><td>String</td><td><p></p><p></p><p>SECONDS</p></td></tr></tbody></table>

### Spike Arrest

{% code title="Sample Configuration" %}
```json
"spike": {
    "limit": "10",
    "periodTime": 10,
    "periodTimeUnit": "MINUTES"
  }
```
{% endcode %}

#### Reference

The Spike-Arrest policy configures the number of requests allow over a limited period of time (from seconds to minutes). This policy prevents request spikes by throttling incoming requests. For example, a SpikeArrest policy configured to 2000 requests/second will limit the execution of simultaneous requests to 200 requests per 100ms.

By default, the SpikeArrest policy is applied to a plan, not a consumer. To apply a spike arrest to a consumer, you need to use the `key` attribute, which supports Expression Language.

<table><thead><tr><th>Property</th><th data-type="checkbox">Required</th><th>Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>key</td><td>false</td><td>Key to identify a consumer to apply spike arresting against. Leave it empty to use the default behavior. Supports Expression Language (example: <code>{#request.headers['x-consumer-id']}</code>).</td><td>String</td><td>null</td></tr><tr><td>limit</td><td>false</td><td>Static limit on the number of requests that can be sent (this limit is used if the value > 0).</td><td>integer</td><td>0</td></tr><tr><td>dynamicLimit</td><td>false</td><td>Dynamic limit on the number of requests that can be sent (this limit is used if static limit = 0). The dynamic value is based on Expression Language expressions.</td><td>string</td><td>null</td></tr><tr><td>periodTime</td><td>true</td><td>Time duration</td><td>Integer</td><td>1</td></tr><tr><td>periodTimeUnit</td><td>true</td><td>Time unit (<code>SECONDS</code>, <code>MINUTES</code>)</td><td>String</td><td>SECONDS</td></tr></tbody></table>

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into [phases](broken-reference) that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the Rate Limit policies:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="188.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

## Errors

#### Default response override

You can use the response template feature to override the default response provided by the policies. These templates must be defined at the API level (see the API Console **Response Templates** option in the API **Proxy** menu).

#### Error keys

The error keys sent by these policies are as follows:

| Key                                | Parameters                                                                                            |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------- |
| RATE\_LIMIT\_TOO\_MANY\_REQUESTS   | limit - period\_time - period\_unit                                                                   |
| QUOTA\_TOO\_MANY\_REQUESTS         | limit - period\_time - period\_unit                                                                   |
| SPIKE\_ARREST\_TOO\_MANY\_REQUESTS | limit - period\_time - period\_unit - slice\_limit - slice\_period\_time - slice\_limit\_period\_unit |

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-ratelimit/blob/master/CHANGELOG.md" %}

\
