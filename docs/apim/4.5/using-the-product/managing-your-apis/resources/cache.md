---
description: Configuration and usage guide for cache.
---

# Cache

{% tabs %}
{% tab title="Cache" %}
<figure><img src="../../../../../../.gitbook/assets/resource_cache (1).png" alt=""><figcaption><p>Create a Cache resource</p></figcaption></figure>

<table><thead><tr><th width="161">Config param</th><th width="417">Description</th><th>Default</th></tr></thead><tbody><tr><td>Cache name</td><td>Name of the cache</td><td>my-cache</td></tr><tr><td>Time to idle</td><td>Maximum number of seconds an element can exist in the cache without being accessed. When this threshold is reached, the element expires and will no longer be returned from the cache. The default value is 0, i.e., no timeToIdle (TTI) eviction takes place (infinite lifetime).</td><td>0</td></tr><tr><td>Time to live</td><td>Maximum number of seconds an element can exist in the cache, regardless of usage. When this threshold is reached, the element expires and will no longer be returned from the cache. The default value is 0, i.e., no timeToLive (TTL) eviction takes place (infinite lifetime).</td><td>0</td></tr><tr><td>Max entries on heap</td><td>Maximum number of objects to be held in local heap memory (0 = no limit)</td><td>1000</td></tr></tbody></table>
{% endtab %}

{% tab title="Cache Redis" %}
<figure><img src="../../../../../../.gitbook/assets/resource_cache redis (1).png" alt=""><figcaption><p>Create a Cache Redis resource</p></figcaption></figure>

The Cache Redis resource can operate standalone or with the Redis Sentinel monitoring solution. The majority of Cache Redis configuration options are common to both modes of operation, but several are exclusive to either standalone or Sentinel as indicated with a **bold asterisk (\*)**.

<table><thead><tr><th width="167">Config param</th><th width="304">Description</th><th>Default</th></tr></thead><tbody><tr><td>Cache name</td><td>Name of the cache</td><td>my-redis-cache</td></tr><tr><td>Release cache</td><td><p>Enabled: The resource will release the cache when the API is stopped</p><p>Disabled: The cache must be managed manually on the Redis server</p></td><td>false</td></tr><tr><td>Max total</td><td>Maximum number of connections supported by the pool</td><td>8</td></tr><tr><td>Password</td><td>The password for the instance</td><td>-</td></tr><tr><td>Time to live</td><td>Maximum number of seconds an element can exist in the cache, regardless of usage. When this threshold is reached, the element expires and will no longer be returned from the cache. The default value is 0, i.e., no timeToLive (TTL) eviction takes place (infinite lifetime).</td><td>0</td></tr><tr><td>Timeout</td><td>Specifies the connection timeout and the read/write timeout</td><td>2000</td></tr><tr><td>Use SSL</td><td>Toggle to use SSL connections</td><td>true</td></tr><tr><td>Use standalone mode</td><td>Toggle to use standalone mode</td><td>true</td></tr><tr><td>Host</td><td>The host of the instance<br><strong>*Standalone config only</strong></td><td>localhost</td></tr><tr><td>Port</td><td>The port of the instance<br><strong>*Standalone config only</strong></td><td>6379</td></tr><tr><td>Use sentinel mode</td><td>Toggle to use sentinel mode. Sentinel provides high availability for Redis (effectively, the Redis deployment persists without human intervention, barring certain kinds of failures)</td><td>false</td></tr><tr><td>Master</td><td>Sentinel master ID<br><strong>*Sentinel config only</strong></td><td>sentinel-master</td></tr><tr><td>Sentinel password</td><td>Sentinel password<br><strong>*Sentinel config only</strong></td><td>-</td></tr><tr><td>Sentinel nodes</td><td>Array of sentinel nodes<br><strong>*Sentinel config only</strong></td><td>-</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

## Examples

{% tabs %}
{% tab title="Cache" %}
```json
{
    "name": "cache",
    "type": "cache",
    "enabled": true,
    "configuration": {
        "name": "my-cache",
        "timeToIdleSeconds":0,
        "timeToLiveSeconds":0,
        "maxEntriesLocalHeap":1000
    }
}
```
{% endtab %}

{% tab title="Cache Redis" %}
```json
{
    "name": "my-redis-cache",
    "type": "cache-redis",
    "enabled": true,
    "configuration": {
        "name": "my-redis-cache",
        "releaseCache": false,
        "maxTotal": 8,
        "password": "secret",
        "timeToLiveSeconds": 600,
        "timeout": 2000,
        "useSsl": true,
        "sentinelMode" : false,
        "standalone": {
            "host": "localhost",
            "port": 6379
        }
    }
}
Sentinel configuration example:
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
{% endtab %}
{% endtabs %}
