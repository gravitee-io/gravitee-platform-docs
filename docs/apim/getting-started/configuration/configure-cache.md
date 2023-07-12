# Configure Cache

## Overview

Caches are used to store different types of data in Gravitee API Management (APIM).

Cache Managers are now available via plugins. Default distribution contains a Standalone Cache Manager which was and still is the default one.

Two plugins are available :

* Standalone Cache Manager which is the default plugin. The cache will not be distributed and will always remain local to the node (in-memory).
* Hazelcast Cache Manager which has to be added to the distribution and enable by setting `cache.type` to `hazelcast`. With this plugin the cache could be either local (in-memory) or distributed (Hazelcast IMap). Please see the below example of the Hazelcast implementation:

```
<cluster-name>gio-apim-distributed-cache</cluster-name>
<network>
    <port auto-increment="true" port-count="100">5701</port>
    <join>
        <auto-detection enabled="true"/>
        <multicast enabled="false"/>
        <tcp-ip enabled="true">
            <interface>127.0.0.1</interface>
        </tcp-ip>
    </join>
</network>
```

### Networking

There are multiple ways to configure Hazelcast networking depending on your installation (regular VMs, Kubernetes, AWS, etc.​). However, we do not currently recommend enabling the distribution mode with Hazelcast unless there is a strong and clear reason to do so. The distribution mode is not relevant for most use cases. The provided default configuration is designed to work in standalone mode.

If you need run Hazelcast in a cluster, the simplest way is to enable multicast:

```xml
<?xml version="1.0" encoding="UTF-8"?>

<hazelcast xmlns="http://www.hazelcast.com/schema/config"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://www.hazelcast.com/schema/config
           http://www.hazelcast.com/schema/config/hazelcast-config-4.1.xsd">

    <network>
        <join>
            <auto-detection enabled="false"/>
            <!-- Enable multicast to allow hazelcast discovers other nodes -->
            <multicast enabled="true" />
        </join>
    </network>
</hazelcast>
```

{% hint style="info" %}
You can find more information in the [Hazelcast documentation](https://docs.hazelcast.org/docs) which details how to configure Hazelcast as a cluster.
{% endhint %}

## Cache resource management

API publishers can create cache resources:

* to cache upstream of a response with the Cache policy.
* to cache access tokens with the OAuth2 policy.

The default distribution comes with the Cache resource plugin. This plugin stores content in memory and is locally managed on each Gateway node of the installation.

Configuration of cache resources cannot be managed using the `hazelcast.xml` file. The configuration is directly defined on the cache resource.&#x20;

### Persistent cache

APIM also supports the Gravitee Redis Cache resource plugin based on [Redis](https://redis.io/documentation). This plugin is not in the default distribution, but you can [download](https://download.gravitee.io/#graviteeio-apim/plugins/resources/gravitee-resource-cache-redis/) the plugin and follow these [instructions](../../overview/introduction-to-gravitee-api-management-apim/plugins.md#deployment) to deploy it.
