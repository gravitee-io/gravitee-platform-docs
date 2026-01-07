---
description: An overview about circuit breaker.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/bGmDEarvnV52XdcOiV8o/create-and-configure-apis/apply-policies/policy-reference/circuit-breaker
---

# Circuit Breaker

## Overview

This policy allows switching to another backend or making the call fail with a `503 Service Unavailable` in case of errors or latency. It guarantees high availability by making your system resilient if your target is detected as failing.

It is possible to configure errors and latency threshold rates to open the circuit breaker.

Implementation is based on Resilience4j. Refer to [their documentation](https://resilience4j.readme.io/docs/circuitbreaker) for more information.

## Examples

{% hint style="warning" %}
This policy can only be applied to v2 APIs and v4 proxy APIs. It cannot be applied to v4 message APIs or v4 TCP proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="HTTP proxy API example" %}
Sample policy configuration:

```json
{
  "name": "Circuit breaker",
  "description": "",
  "enabled": true,
  "policy": "policy-circuit-breaker",
  "configuration": {
    "failureRateThreshold": 1,
    "slowCallRateThreshold": 10,
    "slowCallDurationThreshold": 500,
    "windowSize": 2,
    "waitDurationInOpenState": 50000,
    "redirectToURL": ""
  }
}
```
{% endtab %}
{% endtabs %}

## Configuration

### Options

You can configure the `circuit-breaker` policy with the following options:

<table><thead><tr><th width="267">Property</th><th data-type="checkbox">Required</th><th width="238">Description</th><th width="159">Type</th><th>Default</th></tr></thead><tbody><tr><td>failureRateThreshold</td><td>true</td><td>Failure rate threshold before the circuit breaker switches to open state. A failure represents a response’s status code >= 500. The threshold is expressed as a percentage.</td><td>integer (min. 0, max.100)</td><td>50</td></tr><tr><td>slowCallRateThreshold</td><td>true</td><td>Slow call rate threshold before the circuit breaker switches to open state. A slow call is represented by a response time greater than the configured <code>slowCallDurationThreshold</code>. The threshold is expressed as a percentage.</td><td>integer (min. 0, max.100)</td><td>50</td></tr><tr><td>slowCallDurationThreshold</td><td>true</td><td>The duration threshold above which a call is considered as slow, increasing <code>slowCallRateThreshold</code>. The duration is expressed in milliseconds.</td><td>integer (min. 1)</td><td>1000</td></tr><tr><td>windowSize</td><td>true</td><td>The size of the sliding window which is used to record the outcome of calls when the circuit is closed.</td><td>integer (min. 0)</td><td>100</td></tr><tr><td>waitDurationInOpenState</td><td>false</td><td>The duration in millisecond before switching from open circuit to half-open.</td><td>integer (min. 1)</td><td>1000</td></tr><tr><td>redirectToURL</td><td>false</td><td>Redirect the call to the given URL instead of returning '503 Service Unavailable' status (supports EL)</td><td>string</td><td></td></tr><tr><td>scope</td><td>true</td><td>Cached response can be set for a single consumer (application) or for all applications.&#x3C;br>&#x3C;strong>WARNING:&#x3C;/strong> Please be aware that by using an \"API\" scope, data will be shared between all consumers !</td><td>API / APPLICATION</td><td>APPLICATION</td></tr></tbody></table>

### Phases

The phases checked below are supported by the `circuit-breaker` policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `circuit-breaker` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>Up to 1.x</td><td>All</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-circuit-breaker/blob/master/CHANGELOG.md" %}
