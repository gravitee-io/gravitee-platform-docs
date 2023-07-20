---
description: This page provides the technical details of the Circuit Breaker policy
---

# Circuit Breaker

## Overview

Functional and implementation information for the Circuit Breaker policy is organized into the following sections:

* [Configuration](template-policy-rework-structure-7.md#configuration)
* [Compatibility Matrix](template-policy-rework-structure-7.md#compatibility-matrix)
* [Changelogs](template-policy-rework-structure-7.md#changelogs)

This policy allows to switch to another backend or making the call fails with a `503 Service Unavailable` in case of errors or latency. It is possible to configure errors and latency threshold rate to open the circuit breaker.

Implementation is based on Resilience4j, you can find more information on [their documentation](https://resilience4j.readme.io/docs/circuitbreaker).

It guaranties high availability making your system resilient if your target is detected as failing.

## Configuration reference

<table><thead><tr><th>Property</th><th data-type="checkbox">Required</th><th>Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>failureRateThreshold</td><td>true</td><td>Failure rate threshold before the circuit breaker switches to open state. A failure represents a response’s status code >= 500. The threshold is expressed as a percentage.</td><td>integer (min. 0, max.100)</td><td>50</td></tr><tr><td>slowCallRateThreshold</td><td>true</td><td>Slow call rate threshold before the circuit breaker switches to open state. A slow call is represented by a response time greater than the configured <code>slowCallDurationThreshold</code>. The threshold is expressed as a percentage.</td><td>integer (min. 0, max.100)</td><td>50</td></tr><tr><td>slowCallDurationThreshold</td><td>true</td><td>The duration threshold above which a call is considered as slow, increasing <code>slowCallRateThreshold</code>. The duration is expressed in milliseconds.</td><td>integer (min. 1)</td><td>1000</td></tr><tr><td>windowSize</td><td>true</td><td>The size of the sliding window which is used to record the outcome of calls when the circuit is closed.</td><td>integer (min. 0)</td><td>100</td></tr><tr><td>waitDurationInOpenState</td><td>false</td><td>The duration in millisecond before switching from open circuit to half-open.</td><td>integer (min. 1)</td><td>1000</td></tr><tr><td>redirectToURL</td><td>false</td><td>Redirect the call to the given URL instead of returning '503 Service Unavailable' status (supports EL)</td><td>string</td><td></td></tr><tr><td>scope</td><td>true</td><td>Cached response can be set for a single consumer (application) or for all applications.&#x3C;br>&#x3C;strong>WARNING:&#x3C;/strong> Please be aware that by using an \"API\" scope, data will be shared between all consumers !</td><td>API / APPLICATION</td><td>APPLICATION</td></tr></tbody></table>

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into [phases](broken-reference) that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the Circuit Breaker policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

## Compatibility matrix

The [changelog for each version of APIM](../../releases-and-changelog/changelog/) provides a list of policies included in the default distribution. The chart below summarizes this information in relation to the `json-xml` policy.

<table data-full-width="false"><thead><tr><th width="161.33333333333331">Plugin Version</th><th width="242">Supported APIM versions</th><th data-type="checkbox">Included in APIM default distribution</th></tr></thead><tbody><tr><td>&#x3C;= 1.x</td><td>All</td><td>false</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-circuit-breaker/blob/master/CHANGELOG.md" %}
