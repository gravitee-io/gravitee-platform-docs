# Cache

## Overview

You can use the `cache` policy to cache upstream responses (content, status and headers) to eliminate the need for subsequent calls to the back end.

This policy is based on a _cache resource_, which aligns the underlying cache system with the API lifecycle (stop/start).

Consumers can bypass the cache by adding a `cache=BY_PASS` query parameter or by providing a _`X-Gravitee-Cache=BY_PASS`_ HTTP header.

{% hint style="info" %}
**Make sure to define your Cache resource**

If no cache resource is defined for the policy, or it is not well configured, the API will not be deployed. The resource name is specified in the policy configuration `cacheName`.
{% endhint %}

## Examples

{% hint style="warning" %}
This policy can only be applied to v2 APIs. It cannot be applied to v4 message APIs or v4 proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="HTTP proxy API example" %}
The key used to store elements in cache can use the Gravitee Expression Language to provide a dynamic value.

Key based on the `productId` query parameter:

```json
"key": "{#request.params['productId']}"
```

Key based on the `api-key` of the consumer:

```json
"key": "{#request.headers['X-Gravitee-Api-Key']}"
```

Key based on an API’s property and a query parameter:

```json
"key": "{#properties['siteID']}-{#request.params['productId']}"
```
{% endtab %}
{% endtabs %}

## Configuration

Sample policy configuration:

{% code title="Sample Configuration" %}
```json
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
{% endcode %}

#### Gateway configuration (gravitee.yml)

```yaml
  policy:
    cache:
      serialization: text # default value or "binary" (not compatible with Redis)
```

The `policy.cache.serialization` allows configuration of the serialization format of the cache.

The default value is `text`, but you can also use `binary` to use a binary serialization format. The `binary` serialization format is not compatible with the Redis cache resource.

### Phases

The phases checked below are supported by the `cache` policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>false</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

You can configure the `cache` policy with the following options:

<table><thead><tr><th width="267">Property</th><th data-type="checkbox">Required</th><th width="273">Description</th><th width="140">Type</th><th>Default</th></tr></thead><tbody><tr><td>cacheName</td><td>true</td><td>The cache resource used to store the element</td><td>string</td><td></td></tr><tr><td>key</td><td>false</td><td>The key used to store the element (supports EL)</td><td>string</td><td></td></tr><tr><td>timeToLiveSeconds</td><td>true</td><td>Time to live of the element put in cache (default is 10 minutes)</td><td>integer</td><td>600</td></tr><tr><td>methods</td><td>true</td><td>Select which method you want to cache</td><td>array of strings</td><td>[GET, OPTIONS, HEAD]</td></tr><tr><td>responseCondition</td><td>false</td><td>Add an extra condition (with Expression Language) based on the response to activate cache. For example use <code>{#upstreamResponse.status == 200}</code> to only cache 200 responses status. By default, all 2xx are cached.</td><td>string</td><td></td></tr><tr><td>useResponseCacheHeaders</td><td>false</td><td>Time to live based on 'Cache-Control' and / or 'Expires' headers from backend response</td><td>boolean</td><td>false</td></tr><tr><td>scope</td><td>true</td><td>Cached response can be set for a single consumer (application) or for all applications.<br><strong>WARNING:</strong> Please be aware that by using an "API" scope, data will be shared between all consumers!</td><td>API / APPLICATION</td><td>APPLICATION</td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `cache` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>1.x</td><td>3.x</td></tr><tr><td>2.x</td><td>4.0+</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-cache/blob/master/CHANGELOG.md" %}
