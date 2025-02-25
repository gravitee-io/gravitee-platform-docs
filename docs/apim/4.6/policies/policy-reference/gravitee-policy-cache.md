= Cache policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-cache/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-cache/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-cache/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-cache.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-cache"]
endif::[]

== Phase

|===
|onRequest |onResponse

| X
|

|===

== Description

You can use the `cache` policy to cache upstream responses (content, status and headers) to eliminate the need for subsequent calls to the back end.

This policy is based on a _cache resource_, which aligns the underlying cache system with the API lifecycle (stop / start).

Consumers can bypass the cache by adding a `cache=BY_PASS` query parameter or by providing a `X-Gravitee-Cache=BY_PASS` HTTP header.

NOTE: If no cache resource is defined for the policy, or it is not well configured, the API will not be deployed. The resource name is specified in the
policy configuration `cacheName`, as described below.

== Compatibility with APIM

|===
| Plugin version | APIM version

| 1.x            | 3.x
| 2.x            | 4.0 to latest
|===

== Configuration

You can configure the policy with the following options:

|===
|Property |Required |Description |Type |Default

|cacheName|X|The cache resource used to store the element|string|
|key||The key used to store the element (support EL)|string|
|timeToLiveSeconds|X|Time to live of the element put in cache (Default to 10 minutes)|integer|600
|methods|X|Select which method you want to cache|array of strings|[GET, OPTIONS, HEAD]
|responseCondition||Add an extra condition (with Expression Language) based on the response to activate cache. For example use `{#upstreamResponse.status == 200}` to only cache 200 responses status. By default, all 2xx are cached.|string|
|useResponseCacheHeaders||Time to live based on 'Cache-Control' and / or 'Expires' headers from backend response|boolean|false
|scope|X|Cached response can be set for a single consumer (application) or for all applications.<br><strong>WARNING:</strong> Please be aware that by using an \"API\" scope, data will be shared between all consumers !|API / APPLICATION|APPLICATION

|===

== Examples

The key used to store elements in cache can use the Gravitee Expression Language to provide a dynamic value.

TIP: To learn more about the Gravitee Expression Language, see the *API Publisher Guide*.

=== Key based on the `productId` query parameter

[source, json]
----
"key": "{#request.params['productId']}"
----

=== Key based on the `api-key` of the consumer

[source, json]
----
"key": "{#request.headers['X-Gravitee-Api-Key']}"
----

=== Key based on an API's property and a query parameter

[source, json]
----
"key": "{#properties['siteID']}-{#request.params['productId']}"
----

=== Configuration example

[source, json]
----
"cache": {
    "cacheName": "policy-cache",
    "key": "{#request.params['productId']}",
    "timeToLiveSeconds": 600,
    "useResponseCacheHeaders": false,
    "scope": "APPLICATION",
    "methods": ["POST"],
    "responseCondition": "{#upstreamResponse.status == 201}"
}
----


=== Gateway configuration (gravitee.yml)

WARNING: The `binary` serialization format is not compatible with the Redis cache resource.

[source, yaml]
----
  policy:
    cache:
      serialization: text # default value or "binary" (not compatible with Redis)
----

The `policy.cache.serialization` allow to configure the serialization format of the cache.

The default value is `text` but you can also use `binary` to use a binary serialization format (not compatible with Redis).
