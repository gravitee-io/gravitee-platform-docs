# Data Cache

## Overview

The Data Cache policy allows you to get, set, and expire arbitrary key-value pairs in a cache resource. You can use this policy to do things like:

* Obtain an authentication token and store it in the cache before passing it to the HTTP callout policy, so that you don't have to obtain the token on every call.
* Maintain state in the gateway to track the number of tokens passed to an upstream LLM proxied by the API.
* Restrict the number of ongoing connections to an endpoint in order to protect a legacy backend from overload.

## Basic Usage

* First, you create a [cache resource](https://github.com/gravitee-io/gravitee-platform-docs/blob/6f69d3d43334c5f35db35e34f1d23832790b9725/docs/apim/4.6/policies/resources.md) for the policy to use.
* You specify the cache key to use for getting, setting, or expiring. The key name is dynamic and can be set using expression language.
* When using the `SET` operation, you specify the `value` to set in the cache. The value is also dynamic and supports expression language.

## Manipulating Return Values

Suppose the cache key is named `my-key`. Then, when running the `GET` operation, the value will be accessible in the execution context via the `my-key` context attribute.

For example, in the assign attributes policy, you can modify the value by using `{#context.attributes['my-key']}`. Note that you may need to cast the result to a different data type, as many caches store data in plain text. For example, to increment a value by 1 when it is obtained from Redis, use the expression:

```
{new Integer(#context.attributes['my-key']) + 1}
```

## Handling Cache Misses <a href="#user-content-phases" id="user-content-phases"></a>

When performing a `GET` operation, the policy will set a context attribute to `true` or `false` depending on whether the key was found in the cache or not. The name of the attribute is defined by the `Cache Miss Attribute Key` field and defaults to `gravitee.policy.data-cache.cache-miss`. You can use this attribute as a condition in other policies. For example:

* In the HTTP Callout policy, you can set the `Trigger condition` field to `{#gravitee.policy.data-cache.cache-miss}`, so as to only trigger the callout when a key is not found in the cache.
* If you want to increment a counter or start at 1 if the value is not found in the cache, you can use the assign attributes policy and set the attribute as:

```
{#context.attributes['gravitee.policy.data-cache.cache-miss'] ? 1 : new Integer(#context.attributes['my-key']) + 1}
```

## Dynamic Cache Key Names

The name of the cache key is dynamic. For example, if you want to have a key in the cache for every application connecting to the API, then you can set the cache key to `{#context.attributes['application']}`. Later, if you perform a `GET` operation, you can manipulate the return value using `{#context.attributes[#context.attributes['application']}`.

## Example - Caching OAuth Token <a href="#user-content-phases" id="user-content-phases"></a>

Suppose you want to proxy an endpoint that requires an OAuth token, with a different token per client and custom transformation required on the token. So for each client connection to the API, you'll need to get an access token and pass as it in the Authorization header to the upstream endpoint.

You _could_ call the token generation endpoint every time, but if you've already obtained a token for the caller, and the token is still valid, it will be better from a performance point of view to use the same token from the previous request.

{% hint style="info" %}
The OAuth2 resource already has a built-in caching mechanism, but this example will be relevant if there is custom logic required to modify the access token.
{% endhint %}

* To start with, add a [cache resource](../resources.md#cache) to the API (Redis or the built-in gateway cache). Then, add a new flow to the API in the policy studio.
* Add a Data Cache policy on the request phase to look up the token in the cache, if it exists.
* If the token does not exist in the cache, make an [HTTP callout](http-callout.md) to the token endpoint.
* Put the new token in the cache (editing it as necessary).
* Add a transform headers policy to set the Authorization header explicitly.

The full example is shown below:

{% tabs %}
{% tab title="Policy Studio" %}
The sequence of policies is as follows:

<figure><img src="../../../../4.6/.gitbook/assets/image (145) (1).png" alt=""><figcaption></figcaption></figure>

The configuration for the first data cache policy is:

<figure><img src="../../../../4.6/.gitbook/assets/image (146) (1).png" alt=""><figcaption></figcaption></figure>

Then the HTTP Callout policy has a trigger condition representing the attribute. The return value is put in a context variable called `access-token`:

<figure><img src="../../../../4.6/.gitbook/assets/image (147) (1).png" alt=""><figcaption></figcaption></figure>

Lastly, if the first policy resulted in a cache miss, put the token from the HTTP callout policy in the cache:

<figure><img src="../../../../4.6/.gitbook/assets/image (148) (1).png" alt=""><figcaption></figcaption></figure>
{% endtab %}

{% tab title="API Definition" %}
The v4 API definition for the request phase containing the whole flow is as follows, assuming the resource is called `test-cache`:

```json
"request": [
  {
    "name": "Data Cache Policy",
    "description": "Check if the token is in the cache",
    "enabled": true,
    "policy": "data-cache",
    "configuration": {
      "cacheKey": "test-token",
      "resource": "test-cache",
      "cacheMissAttributeKey": "gravitee.policy.data-cache.cache-miss",
      "defaultOperation": "GET"
    }
  },
  {
    "name": "HTTP Callout",
    "description": "Get the token if there is a cache miss",
    "enabled": true,
    "policy": "policy-http-callout",
    "configuration": {
      "headers": [
        {
          "name": "Authorization",
          "value": "Basic {#properties['auth']}"
        }
      ],
      "variables": [
        {
          "name": "access-token",
          "value": "{#jsonPath(#calloutResponse.content, '$.access_token')}"
        }
      ],
      "method": "POST",
      "fireAndForget": false,
      "scope": "REQUEST",
      "errorStatusCode": "500",
      "errorCondition": "{#calloutResponse.status >= 400 and #calloutResponse.status <= 599}",
      "url": "{#properties['token-url']}",
      "exitOnError": false
    },
    "condition": "{#context.attributes['gravitee.policy.data-cache.cache-miss']}"
  },
  {
    "name": "Data Cache Policy",
    "description": "Put the token in the cache if there was a cache miss",
    "enabled": true,
    "policy": "data-cache",
    "configuration": {
      "cacheKey": "test-token",
      "resource": "test-cache",
      "cacheMissAttributeKey": "gravitee.policy.data-cache.cache-miss",
      "defaultOperation": "SET",
      "value": "{#context.attributes['access-token']}"
    },
    "condition": "{#context.attributes['gravitee.policy.data-cache.cache-miss']}"
  },
  {
    "name": "Transform Headers",
    "description": "Set custom authorization header",
    "enabled": true,
    "policy": "transform-headers",
    "configuration": {
      "whitelistHeaders": [],
      "addHeaders": [
        {
          "name": "Authorization",
          "value": "Bearer {#context.attributes['access-token']}"
        }
      ],
      "scope": "REQUEST",
      "removeHeaders": []
    }
  }
]
```
{% endtab %}

{% tab title="GKO" %}
The CRD for the request phase containing the whole flow is as follows, assuming the resource is called `test-cache`:

```yaml
request:
- name: "Data Cache Policy"
  description: "Check if the token is in the cache"
  enabled: true
  policy: "data-cache"
  configuration:
    cacheKey: "test-token"
    resource: "test-cache"
    cacheMissAttributeKey: "gravitee.policy.data-cache.cache-miss"
    defaultOperation: "GET"
- name: "HTTP Callout"
  description: "Get the token if there is a cache miss"
  enabled: true
  policy: "policy-http-callout"
  configuration:
    headers:
    - name: "Authorization"
      value: "Basic {#properties['auth']}"
    variables:
    - name: "access-token"
      value: "{#jsonPath(#calloutResponse.content, '$.access_token')}"
    method: "POST"
    fireAndForget: false
    scope: "REQUEST"
    errorStatusCode: "500"
    errorCondition: "{#calloutResponse.status >= 400 and #calloutResponse.status\
      \ <= 599}"
    url: "{#properties['token-url']}"
    exitOnError: false
  condition: "{#context.attributes['gravitee.policy.data-cache.cache-miss']}"
- name: "Data Cache Policy"
  description: "Put the token in the cache if there was a cache miss"
  enabled: true
  policy: "data-cache"
  configuration:
    cacheKey: "test-token"
    resource: "test-cache"
    cacheMissAttributeKey: "gravitee.policy.data-cache.cache-miss"
    defaultOperation: "SET"
    value: "{#context.attributes['access-token']}"
  condition: "{#context.attributes['gravitee.policy.data-cache.cache-miss']}"
- name: "Transform Headers"
  description: "Set custom authorization header"
  enabled: true
  policy: "transform-headers"
  configuration:
    whitelistHeaders: []
    addHeaders:
    - name: "Authorization"
      value: "Bearer {#context.attributes['access-token']}"
    scope: "REQUEST"
    removeHeaders: []
```
{% endtab %}
{% endtabs %}

## Technical Reference <a href="#user-content-phases" id="user-content-phases"></a>

### Phases <a href="#user-content-phases" id="user-content-phases"></a>

| onRequest | onResponse | onMessageRequest | onMessageResponse |
| --------- | ---------- | ---------------- | ----------------- |
| X         | X          |                  |                   |

### Description <a href="#user-content-description" id="user-content-description"></a>

Policy to get/set arbitrary key-value pairs in the cache resource.

### Compatibility with APIM <a href="#user-content-compatibility-with-apim" id="user-content-compatibility-with-apim"></a>

| Plugin version | APIM version  |
| -------------- | ------------- |
| 1.x            | 4.5 to latest |

### Configuration <a href="#user-content-configuration" id="user-content-configuration"></a>

You can configure the policy with the following options:

| Property              | Required | Description                                                                                                                                     | Type    | Default                               |
| --------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ------- | ------------------------------------- |
| resource              | X        | The name of the cache resource to use.                                                                                                          | string  | \_                                    |
| cacheKey              | X        | The cache key to look up. When the operation is GET, this key is used as the context attribute to refer to the cache value (Supports EL)        | string  | \_                                    |
| value                 | X        | The value to store in the cache for the specified key. Used only for SET operation (Supports EL)                                                | string  | \_                                    |
| defaultOperation      | X        | The default operation to use if the `gravitee.attributes.policy.cache.operation` attribute is not set.                                          | string  | \_                                    |
| timeToLive            |          | The time to live in seconds. This value can be overridden by the `gravitee.attributes.policy.cache.ttl` attribute. Used only for SET operation. | integer | 3600                                  |
| cacheMissAttributeKey |          | The attribute key to set when a cache miss occurs.                                                                                              | string  | gravitee.policy.data-cache.cache-miss |

Example configuration:

```
{
    "configuration": {
        "resource": "my-cache-resource",
        "cacheKey": "my-cache-key",
        "value": "my-cache-value",
        "defaultOperation": "SET",
        "timeToLive": 3600,
        "cacheMissAttributeKey": "gravitee.policy.data-cache.cache-miss"
    }
}
```

#### Value <a href="#user-content-value" id="user-content-value"></a>

The usage of the value depends on the operation:

* `SET`: The value to store in the cache.
* `GET`: The attribute key to set with the value from the cache.
* `EVICT`: The attribute key to set with the value from the cache before evict.

In all cases, the value supports EL and is optional. In case of value not provided, the policy will use the attribute with the key `gravitee.policy.data-cache.value`.

### Errors <a href="#user-content-errors" id="user-content-errors"></a>

With the provided default implementation, policy will fail if header `X-Template-Policy` value is equal to configured `errorKey` value.

| Phase            | Code                          | Error template key  | Description                                   |
| ---------------- | ----------------------------- | ------------------- | --------------------------------------------- |
| REQUEST/RESPONSE | `500 - INTERNAL SERVER ERROR` | `NO_CACHE`          | The cache is not found in the cache resource. |
| REQUEST/RESPONSE | `500 - INTERNAL SERVER ERROR` | `NO_CACHE_RESOURCE` | The cache resource is not found.              |
