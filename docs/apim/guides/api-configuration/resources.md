# Resources

## Overview

APIM comes with some default common _resources_, for standard APIM usage. The default resources are described in this section.

You can configure resources for your APIs during the API design phase. From APIM 3.5, the recommended way of doing this is with [Design Studio](https://docs.gravitee.io/apim/3.x/apim\_publisherguide\_design\_studio\_overview.html).

## Cache

### Description

The cache resource is used to maintain a cache and link it to the API lifecycle. It means that the cache is initialized when the API is starting and released when API is stopped.

This cache is responsible to store HTTP response from the backend to avoid subsequent calls.

Current implementation of the cache resource is based on [Hazelcast](https://hazelcast.com/).

### Configuration

You can configure the resource with the following options :

| Property            | Required | Description                                                                                                                                                                                                                                                                | Type    | Default  |
| ------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- | -------- |
| name                | X        | The name of the cache.                                                                                                                                                                                                                                                     | string  | my-cache |
| timeToIdleSeconds   | X        | The maximum number of seconds an element can exist in the cache without being accessed. The element expires at this limit and will no longer be returned from the cache. The default value is 0, which means no timeToIdle (TTI) eviction takes place (infinite lifetime). | integer | 0        |
| timeToLiveSeconds   | X        | The maximum number of seconds an element can exist in the cache regardless of use. The element expires at this limit and will no longer be returned from the cache. The default value is 0, which means no timeToLive (TTL) eviction takes place (infinite lifetime).      | integer | 0        |
| maxEntriesLocalHeap | X        | The maximum objects to be held in local heap memory (0 = no limit).                                                                                                                                                                                                        | integer | 1000     |

Configuration example

```
{
    "name" : "cache",
    "type" : "cache",
    "enabled" : true,
    "configuration" : {
        "name": "my-cache",
        "timeToIdleSeconds":0,
        "timeToLiveSeconds":0,
        "maxEntriesLocalHeap":1000
    }
}
```

\


## Cache Redis

|   | This plugin is not in distribution by default, but you can [download the plugin](https://download.gravitee.io/#graviteeio-apim/plugins/resources/gravitee-resource-cache-redis/) and follow the [instructions](https://docs.gravitee.io/apim/3.x/apim\_installation\_guide\_docker\_customize.html#install\_an\_additional\_plugin) to install it. For more information on configuring cache in APIM, see [Configure cache](https://docs.gravitee.io/apim/3.x/apim\_installguide\_cache.html). For information on configuring the Rate Limit repository plugin for Redis, see the [Redis](https://docs.gravitee.io/apim/3.x/apim\_installguide\_repositories\_redis.html) page. |
| - | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

## Redis Cache Resource <a href="#redis_cache_resource" id="redis_cache_resource"></a>

### Description

The Redis cache resource is used to maintain a cache and link it to the API lifecycle. It means that the cache is initialized when the API is starting and released when API is stopped.

This cache is responsible to store HTTP response from the backend to avoid subsequent calls.

Current implementation of the cache resource is based on [Redis](https://redis.io/).

### Configuration

You can configure the resource with the following options :

| Property          | Required | Description                                                                                                                                                                                                                                                           | Type    | Default        |
| ----------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- | -------------- |
| name              | X        | The name of the cache.                                                                                                                                                                                                                                                | string  | my-redis-cache |
| releaseCache      | X        | Release the cache when API is stopped? If enabled, the resource will release the cache. If not, you will have to manage it by yourself on your Redis server.                                                                                                          | boolean | false          |
| maxTotal          | X        | The maximum number of connections that are supported by the pool.                                                                                                                                                                                                     | integer | 8              |
| password          |          | The password of the instance.                                                                                                                                                                                                                                         | string  |                |
| timeToLiveSeconds | X        | The maximum number of seconds an element can exist in the cache regardless of use. The element expires at this limit and will no longer be returned from the cache. The default value is 0, which means no timeToLive (TTL) eviction takes place (infinite lifetime). | integer | 0              |
| timeout           | X        | The timeout parameter specifies the connection timeout and the read/write timeout.                                                                                                                                                                                    | integer | 2000           |
| timeout           | X        | The timeout parameter specifies the connection timeout and the read/write timeout.                                                                                                                                                                                    | integer | 2000           |
| useSsl            | X        | Use SSL connections.                                                                                                                                                                                                                                                  | boolean | true           |
| sentinelMode      | X        | Sentinel provides high availability for Redis. In practical terms this means that using Sentinel you can create a Redis deployment that resists without human intervention certain kinds of failures.                                                                 | boolean | false          |

#### Standalone configuration

| Property | Required | Description               | Type    | Default   |
| -------- | -------- | ------------------------- | ------- | --------- |
| host     | X        | The host of the instance  | string  | localhost |
| port     | X        | The port of the instance. | integer | 6379      |

Configuration example

```
{
    "name" : "my-redis-cache",
    "type" : "cache-redis",
    "enabled" : true,
    "configuration" : {
        "name" : "my-redis-cache",
        "releaseCache": false,
        "maxTotal" : 8,
        "password" : "secret",
        "timeToLiveSeconds" : 600,
        "timeout" : 2000,
        "useSsl" : true,
        "sentinelMode" : false,
        "standalone": {
            "host" : "localhost",
            "port" : 6379
        }
    }
}
```

#### Sentinel configuration

| Property | Required | Description             | Type   | Default         |
| -------- | -------- | ----------------------- | ------ | --------------- |
| masterId | X        | The sentinel master id  | string | sentinel-master |
| password | -        | The sentinel password.  | string |                 |
| nodes    | X        | List of sentinel nodes. | Array  |                 |

Configuration example

```
{
    "name" : "my-redis-cache",
    "type" : "cache-redis",
    "enabled" : true,
    "configuration" : {
        "name" : "my-redis-cache",
        "releaseCache": false,
        "maxTotal" : 8,
        "password" : "secret",
        "timeToLiveSeconds" : 600,
        "timeout" : 2000,
        "useSsl" : true,
        "sentinelMode" : true,
        "sentinel" : {
            "masterId" : "sentinel-master",
            "password" : "secret",
            "nodes": [
              {
                "host" : "localhost",
                "port" : 26379
              },
              {
                "host" : "localhost",
                "port" : 26380
              },
              {
                "host" : "localhost",
                "port" : 26381
              }
            ]
        }
    }
}
```

\


## OAuth2 - Gravitee Access Management

### Description

Gravitee.io Access Management resource is defined to introspect an access\_token generated by a Gravitee.io Access Management instance.

### Compatibility with APIM

| Plugin version   | APIM version     |
| ---------------- | ---------------- |
| 2.x and upper    | 3.18.x to latest |
| 1.14.x and upper | 3.10.x to 3.17.x |
| Up to 1.13.x     | Up to 3.9.x      |

### Configuration

You can configure the resource with the following options :

| Property       | Required | Description                                                                                 | Type    | Default |
| -------------- | -------- | ------------------------------------------------------------------------------------------- | ------- | ------- |
| serverURL      | X        | The URL of the Gravitee.io Access Management server.                                        | string  | -       |
| securityDomain | X        | The security domain (realm) from where the token has been generated and must be introspect. | string  | -       |
| clientId       | X        | The client identifier.                                                                      | string  | -       |
| clientSecret   | X        | The client secret.                                                                          | string  | -       |
| userClaim      | -        | User claim field used to store end user on log analytics.                                   | string  | sub     |
| useSystemProxy | -        | Use system proxy.                                                                           | boolean | false   |

Configuration example

```
{
    "configuration": {
        "clientId": "my-client",
        "clientSecret": "f2ddb55e-30b5-4a45-9db5-5e30b52a4574",
        "securityDomain": "my-security",
        "serverURL": "https://graviteeio_access_management",
        "userClaim": "sub"
    }
}
```

\


## OAuth2 - Generic Authorization Server

### Description

Generic OAuth2 Authorization Server resource is defined to introspect an access\_token generated by a generic OAuth2 authorization server.

This resource should be able to handle common authorization server from the market by providing a complete configuration about the way to apply token introspection.

### Compatibility with APIM

| Plugin version   | APIM version     |
| ---------------- | ---------------- |
| 2.x and upper    | 3.18.x to latest |
| 1.16.x and upper | 3.10.x to 3.17.x |
| Up to 1.15.x     | Up to 3.9.x      |

### Configuration

You can configure the resource with the following options :

| Property                        | Required | Description                                                                                                                                                                               | Type        | Default       |
| ------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- | ------------- |
| introspectionEndpoint           | X        | The URL which is used by the resource to introspect an incoming access token.                                                                                                             | string      | -             |
| useSystemProxy                  | X        | TUse system proxy.                                                                                                                                                                        | boolean     | false         |
| introspectionEndpointMethod     | X        | HTTP method used to introspect the access token.                                                                                                                                          | HTTP Method | GET           |
| clientId                        | X        | The client identifier.                                                                                                                                                                    | string      | -             |
| clientSecret                    | X        | The client secret.                                                                                                                                                                        | string      | -             |
| useClientAuthorizationHeader    | -        | To prevent token scanning attacks, the endpoint MUST also require some form of authorization to access this endpoint. In this case we are using an HTTP header for client authentication. | boolean     | true          |
| clientAuthorizationHeaderName   | -        | Authorization header.                                                                                                                                                                     | string      | Authorization |
| clientAuthorizationHeaderScheme | -        | Authorization scheme.                                                                                                                                                                     | string      | Basic         |
| tokenIsSuppliedByQueryParam     | -        | Access token is passed to the introspection endpoint using a query parameter.                                                                                                             | boolean     | true          |
| tokenQueryParamName             | -        | Query parameter used to supply access token.                                                                                                                                              | string      | token         |
| tokenIsSuppliedByHttpHeader     | -        | Access token is passed to the introspection endpoint using an HTTP header.                                                                                                                | boolean     | false         |
| tokenHeaderName                 | -        | HTTP header used to supply access token.                                                                                                                                                  | string      | -             |

Configuration example

```
{
    "configuration": {
        "introspectionEndpoint": "https://my_authorization_server/oauth/check_token",
        "introspectionEndpointMethod": "POST",
        "clientAuthorizationHeaderName": "Authorization",
        "clientAuthorizationHeaderScheme": "Basic",
        "clientId": "my-client",
        "clientSecret": "f2ddb55e-30b5-4a45-9db5-5e30b52a4574",
        "tokenIsSuppliedByHttpHeader": false,
        "tokenIsSuppliedByQueryParam": true,
        "tokenQueryParamName": "token",
        "useClientAuthorizationHeader": true
    }
}
```

\


