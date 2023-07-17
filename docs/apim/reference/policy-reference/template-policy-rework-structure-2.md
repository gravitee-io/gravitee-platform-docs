---
description: This page provides the technical details of the Cache policy
---

# Cache

{% hint style="warning" %}
**This feature requires** [**Gravitee's Enterprise Edition**](../../overview/introduction-to-gravitee-api-management-apim/ee-vs-oss.md)**.**
{% endhint %}

## Overview

Functional and implementation information for the JSON-to-XML policy is organized into the following sections:

* [Examples](template-policy-rework-structure-2.md#examples)
* [Configuration](template-policy-rework-structure-2.md#configuration)
* [Compatibility Matrix](template-policy-rework-structure-2.md#compatibility-matrix)
* [Errors](template-policy-rework-structure-2.md#errors)
* [Changelogs](template-policy-rework-structure-2.md#changelogs)

## Examples

You can use the `cache` policy to cache upstream responses (content, status and headers) to eliminate the need for subsequent calls to the back end.

This policy is based on a _cache resource_, which aligns the underlying cache system with the API lifecycle (stop / start).

Consumers can bypass the cache by adding a `cache=BY_PASS_` query parameter or by providing a _`X-Gravitee-Cache=BY_PASS`_ HTTP header.

{% hint style="info" %}
**Make sure you define your Cache resource**

If no cache resource is defined for the policy, or it is not well configured, the API will not be deployed. The resource name is specified in the policy configuration `cacheName`.
{% endhint %}

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

Here is an example configuration:

```
"cache": {
    "cacheName": "policy-cache",
    "key": "{#request.params['productId']}",
    "timeToLiveSeconds": 600,
    "useResponseCacheHeaders": false,
    "scope": "APPLICATION",
    "methods": ["POST"],
    "responseCondition": "{#upstreamResponse.status == 201}"
}
```

#### Gateway configuration (gravitee.yml)

{% hint style="info" %}
**Compatibility**

The `binary` serialization format is not compatible with the Redis cache resource.
{% endhint %}

```
  policy:
    cache:
      serialization: text # default value or "binary" (not compatible with Redis)
```

The `policy.cache.serialization` allow to configure the serialization format of the cache.

The default value is `text` but you can also use `binary` to use a binary serialization format (not compatible with Redis).

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into [phases](./#phases) that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the Assign Metrics policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

## Compatibility matrix

The [changelog for each version of APIM](../../releases-and-changelog/changelog/) provides a list of policies included in the default distribution. The chart below summarizes this information in relation to the `cache` policy.

<table data-full-width="false"><thead><tr><th width="161.33333333333331">Plugin Version</th><th width="242">Supported APIM versions</th><th data-type="checkbox">Included in APIM default distribution</th></tr></thead><tbody><tr><td>&#x3C;=1.x</td><td>All</td><td>true</td></tr></tbody></table>

## Changelog

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-cache/blob/master/CHANGELOG.md" %}
