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



## OAuth2 - Gravitee Access Management



## OAuth2 - Generic Authorization Server



