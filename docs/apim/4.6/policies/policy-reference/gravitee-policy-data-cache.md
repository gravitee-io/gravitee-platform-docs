= Gravitee Data Cache Policy

== Phases

[cols="4*", options="header"]
|===
^|onRequest
^|onResponse
^|onMessageRequest
^|onMessageResponse

^.^| X
^.^| X
^.^|
^.^|
|===

== Description

Policy to get/set arbitrary key-value pairs in the cache resource.

== Compatibility with APIM

|===
| Plugin version | APIM version
| 1.x            | 4.5 to latest

|===


== Configuration

You can configure the policy with the following options:

[cols="5*", options=header]
|===
^| Property
^| Required
^| Description
^| Type
^| Default

.^|resource
^.^|X
.^|The name of the cache resource to use.
^.^|string
.^|_

.^|cacheKey
^.^|X
.^|The cache key to look up. When the operation is GET, this key is used as the context attribute to refer to the cache value (Supports EL)
^.^|string
.^|_

.^|value
^.^|X
.^|The value to store in the cache for the specified key. Used only for SET operation (Supports EL)
^.^|string
.^|_

.^|defaultOperation
^.^|X
.^|The default operation to use if the `gravitee.attributes.policy.cache.operation` attribute is not set.
^.^|string
.^|_

.^|timeToLive
^.^|
.^|The time to live in seconds. This value can be overridden by the `gravitee.attributes.policy.cache.ttl` attribute. Used only for SET operation.
^.^|integer
.^|3600

.^|cacheMissAttributeKey
^.^|
.^|The attribute key to set when a cache miss occurs.
^.^|string
.^|gravitee.policy.data-cache.cache-miss

|===

Example configuration:

[source, json]
----
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
----

=== Value

The usage of the value depends on the operation:

- `SET`: The value to store in the cache.
- `GET`: The attribute key to set with the value from the cache.
- `EVICT`: The attribute key to set with the value from the cache before evict.

In all cases, the value supports EL and is optional. In case of value not provided, the policy will use the attribute with the key `gravitee.policy.data-cache.value`.

== Errors

With the provided default implementation, policy will fail if header `X-Template-Policy` value is equal to configured `errorKey` value.

|===
|Phase | Code | Error template key | Description

.^| REQUEST/RESPONSE
.^| ```500 - INTERNAL SERVER ERROR```
.^| `NO_CACHE`
.^| The cache is not found in the cache resource.

.^| REQUEST/RESPONSE
.^| ```500 - INTERNAL SERVER ERROR```
.^| `NO_CACHE_RESOURCE`
.^| The cache resource is not found.

|===
