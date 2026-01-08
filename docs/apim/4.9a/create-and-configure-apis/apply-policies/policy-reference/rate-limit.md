---
description: An overview about rate limit.
---

# Rate Limit

## Overview

There are three `rate-limit` policies:

* **Quota**: Configures the number of requests allowed over a period of time (hours, days, weeks, months)
* **Rate Limit**: Configures the number of requests allowed over a limited period of time (seconds, minutes)
* **Spike Arrest**: Throttles the number of requests processed and sends them to the backend to avoid a spike

For any [`rate-limit` policy](rate-limit.md) and irrespective of plan, the user can select the option to ignore the IP address and subscription of the caller and only use a custom key for the quota. Users can then share an API's rate limit calculations across machines to enforce the limit regardless of caller IP or subscriber ID. Using a custom key, the quota will increment after each call to the API across multiple hosts.

To dynamically set the custom key, it can be defined using Gravitee Expression Language.

{% hint style="warning" %}
An arbitrary custom key can be incorrectly defined via Gravitee Expression Language and potentially bypass the constraints of this mechanism to impact the quota of a different user. Users must assess this risk when using custom keys.
{% endhint %}

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs, v4 HTTP proxy APIs, and v4 message APIs. It cannot be applied to v4 TCP proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="V2 API definition" %}
This snippet of a V2 API definition includes a flow that chains all three rate limit policies.

```json
{
  "name" : "Rate limited v2 API",
  "flows" : [ 
    {
      "name" : "common-flow",
      "enabled" : true,
      "path-operator" : {
        "path" : "/",
        "operator" : "STARTS_WITH"
      },
      "pre" : [ 
        {
          "name" : "Rate Limit",
          "description" : "ACME has rate limits on all APIs.",
          "enabled" : true,
          "policy" : "rate-limit",
          "configuration" : {
            "rate" : {
              "periodTime" : 1,
              "limit" : 10,
              "periodTimeUnit" : "SECONDS"
            }
          }
        }, {
          "name" : "Quota",
          "description" : "ACME uses quotas on all APIs.",
          "enabled" : true,
          "policy" : "quota",
          "configuration" : {
            "quota" : {
              "periodTime" : 1,
              "limit" : 10,
              "periodTimeUnit" : "MONTHS"
            }
          }
        }, {
          "name" : "Spike Arrest",
          "description" : "ACME uses spike arrest on all APIs.",
          "enabled" : true,
          "policy" : "spike-arrest",
          "configuration" : {
            "spike" : {
              "periodTime" : 1,
              "limit" : 10,
              "periodTimeUnit" : "SECONDS"
            }
          }
        } 
      ]
    } 
  ],
  ...
}
```
{% endtab %}

{% tab title="V4 API definition" %}
This snippet of a V4 API definition includes a flow that chains all three rate limit policies.

```json
{
  "api": {
    "name": "Rate limited v4 API",
    "flows": [
      {
        "name": "common-flow",
        "enabled": true,
        "selectors": [
          {
            "type": "HTTP",
            "path": "/",
            "pathOperator": "EQUALS"
          }
        ],
        "request": [
          {
            "name" : "Rate Limit",
            "description" : "ACME has rate limits on all APIs.",
            "enabled" : true,
            "policy" : "rate-limit",
            "configuration" : {
              "rate" : {
                "periodTime" : 1,
                "limit" : 10,
                "periodTimeUnit" : "SECONDS"
              }
            }
          }, {
            "name" : "Quota",
            "description" : "ACME uses quotas on all APIs.",
            "enabled" : true,
            "policy" : "quota",
            "configuration" : {
              "quota" : {
                "periodTime" : 1,
                "limit" : 10,
                "periodTimeUnit" : "MONTHS"
              }
            }
          }, {
            "name" : "Spike Arrest",
            "description" : "ACME uses spike arrest on all APIs.",
            "enabled" : true,
            "policy" : "spike-arrest",
            "configuration" : {
              "spike" : {
                "periodTime" : 1,
                "limit" : 10,
                "periodTimeUnit" : "SECONDS"
              }
            }
          } 
        ]
      }
    ],
  ...
  }
  ...
}
```
{% endtab %}

{% tab title="V2 API CRD" %}
This snippet of a V2 API yaml manifest for the Gravitee Kubernetes Operator includes a flow that chains all three rate limit policies.

```yaml
apiVersion: "gravitee.io/v1alpha1"
kind: "ApiDefinition"
metadata:
  name: "rate-limited-v2-gko-api"
spec:
  name: "Rate limited V2 GKO API"
  flows:
  - name: "common-flow"
    path-operator:
      path: "/"
      operator: "STARTS_WITH"
    enabled: true
    pre:
    - name: "Rate Limit"
      description: "ACME has rate limits on all APIs."
      enabled: true
      policy: "rate-limit"
      configuration:
        rate:
          periodTime: 1
          limit: 10
          periodTimeUnit: "SECONDS"
    - name: "Quota"
      description: "ACME uses quotas on all APIs."
      enabled: true
      policy: "quota"
      configuration:
        quota:
          periodTime: 1
          limit: 10
          periodTimeUnit: "MONTHS"
    - name: "Spike Arrest"
      description: "ACME uses spike arrest on all APIs."
      enabled: true
      policy: "spike-arrest"
      configuration:
        spike:
          periodTime: 1
          limit: 10
          periodTimeUnit: "SECONDS"
    ...
```
{% endtab %}

{% tab title="V4 API CRD" %}
This snippet of a V4 API yaml manifest for the Gravitee Kubernetes Operator includes a flow that chains all three rate limit policies.

```yaml
apiVersion: "gravitee.io/v1alpha1"
kind: "ApiV4Definition"
metadata:
  name: "rate-limited-v4-gko-api"
spec:
  name: "Rate limited V4 GKO API"
  flows:
    - name: "common-flow"
      enabled: true
      selectors:
      - type: "HTTP"
        path: "/"
        pathOperator: "EQUALS"
      request:
      - name: "Rate Limit"
        description: "ACME has rate limits on all APIs."
        enabled: true
        policy: "rate-limit"
        configuration:
          rate:
            periodTime: 1
            limit: 10
            periodTimeUnit: "SECONDS"
      - name: "Quota"
        description: "ACME uses quotas on all APIs."
        enabled: true
        policy: "quota"
        configuration:
          quota:
            periodTime: 1
            limit: 10
            periodTimeUnit: "MONTHS"
      - name: "Spike Arrest"
        description: "ACME uses spike arrest on all APIs."
        enabled: true
        policy: "spike-arrest"
        configuration:
          spike:
            periodTime: 1
            limit: 10
            periodTimeUnit: "SECONDS"
    ...
```
{% endtab %}
{% endtabs %}

## Configuration

### Phases

The phases checked below are supported by the `rate-limit` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="202.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>true</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

You can configure the `rate-limit` policies with the following options:

#### Quota

The Quota policy configures the number of requests allowed over a large period of time (from hours to months). This policy does not prevent request spikes.

#### Rate Limit

The Rate Limit policy configures the number of requests allowed over a limited period of time (from seconds to minutes). This policy does not prevent request spikes.

#### Spike Arrest

The Spike Arrest policy configures the number of requests allow over a limited period of time (from seconds to minutes). This policy prevents request spikes by throttling incoming requests. For example, a Spike Arrest policy configured to 2000 requests/second will limit the execution of simultaneous requests to 200 requests per 100ms.

By default, the Spike Arrest policy is applied to a plan, not a consumer. To apply a spike arrest to a consumer, you need to use the `key` attribute, which supports Expression Language.

## Compatibility matrix

The following is the compatibility matrix for APIM and the`rate-limit` policies:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>1.x</td><td>Up to 3.19</td></tr><tr><td>2.x</td><td>3.20+</td></tr></tbody></table>

## Errors

You can use the response template feature to override the default response provided by the policies. These templates must be defined at the API level (see the API Console **Response Templates** option in the API **Proxy** menu).

The error keys sent by these policies are as follows:

<table><thead><tr><th width="357.5">Key</th><th>Parameters</th></tr></thead><tbody><tr><td>RATE_LIMIT_TOO_MANY_REQUESTS</td><td>limit - period_time - period_unit</td></tr><tr><td>QUOTA_TOO_MANY_REQUESTS</td><td>limit - period_time - period_unit</td></tr><tr><td>SPIKE_ARREST_TOO_MANY_REQUESTS</td><td>limit - period_time - period_unit - slice_limit - slice_period_time - slice_limit_period_unit</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-ratelimit/blob/master/CHANGELOG.md" %}
