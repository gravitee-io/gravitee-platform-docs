---
description: This page provides the technical details of the Latency policy
---

# Latency

## Overview

Functional and implementation information for the Latency policy is organized into the following sections:

* [Configuration](latency.md#configuration)
* [Compatibility Matrix](latency.md#compatibility-matrix)
* [Errors](latency.md#errors)
* [Changelogs](latency.md#changelogs)

You can use the latency policy to add latency to either the request or the response. So for example, if you configure the policy on the request with a latency of 100ms, the gateway waits 100ms before routing the request to the backend service.

This policy is particularly useful in two scenarios:

* Testing: adding latency allows you to test client applications when APIs are slow to respond.
* Monetization: a longer latency can be added to free plans to encourage clients to move to a better (or paid) plan.

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into phases that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the JSON-to-XML policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="188.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>true</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>true</td></tr></tbody></table>

## Compatibility matrix

The [changelog for each version of APIM](../../releases-and-changelogs/changelogs/) provides a list of policies included in the default distribution. The chart below summarizes this information in relation to the `latency` policy.

| Plugin version | APIM version  |
| -------------- | ------------- |
| Up to 1.3.x    | Up to 3.9.x   |
| 1.4.x          | Up to 3.20    |
| 2.x            | 4.x to latest |

## Errors

<table data-full-width="false"><thead><tr><th>HTTP status code</th><th>Message</th></tr></thead><tbody><tr><td><code>500</code></td><td>Server error</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-latency/blob/master/CHANGELOG.md" %}
