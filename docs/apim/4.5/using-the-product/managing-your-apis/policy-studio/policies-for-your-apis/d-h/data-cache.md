---
description: Configuration and usage guide for data cache.
---

# Data Cache

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
