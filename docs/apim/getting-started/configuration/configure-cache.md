# Configure Cache

## Overview

Caches are used to store different types of data in Gravitee API Management (APIM).

The caches use a [Hazelcast](https://docs.hazelcast.org/docs/rn/index.html#3-12-12) implementation. You can tune the configuration in the `hazelcast.xml` file.

## Default configuration

By default, the configuration contains three maps to cache API keys, subscriptions, and APIs. These caches can be shared between nodes if you configure Hazelcast to be able to contact the other nodes.

{% code title="hazelcast.xml" %}
```xml
<?xml version="1.0" encoding="UTF-8"?>

<hazelcast xmlns="http://www.hazelcast.com/schema/config"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://www.hazelcast.com/schema/config
           http://www.hazelcast.com/schema/config/hazelcast-config-4.1.xsd">

    <network>
        <join>
            <!-- Auto-detection and multicast are disabled by default to avoid latency when starting local / standalone  gateway -->
            <auto-detection enabled="false"/>
            <multicast enabled="false" />
        </join>
    </network>

    <map name="apikeys">
        <!-- Eviction is managed programmatically-->
        <eviction eviction-policy="NONE" size="0"></eviction>
    </map>

    <map name="subscriptions">
        <!-- Eviction is managed programmatically-->
        <eviction eviction-policy="NONE" size="0"></eviction>
    </map>

    <map name="apis">
        <!-- Eviction is managed programmatically-->
        <eviction eviction-policy="NONE" size="0"></eviction>
    </map>
</hazelcast>
```
{% endcode %}

{% hint style="warning" %}
Be careful when modifying the default configuration, it is designed with performance in mind.
{% endhint %}

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
