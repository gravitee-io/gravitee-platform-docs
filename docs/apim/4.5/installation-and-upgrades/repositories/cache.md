# Configuring caching

## Overview

Caching is used in API management to store responses from upstream systems in order to improve response time performance to clients and reduce network overhead of talking to the upstream system unnecessarily. Within Gravitee, caching can be defined in a few different ways:

* **Standalone Cache Manager:** The default method for caching data locally in memory. The cache will not be distributed and will always remain local to the node running the gateway.
* **Hazelcast Cache Manager:** This method of caching relies on Hazelcast to provide the cache. This plugin be added to the distribution and enabled by setting `cache.type` to `hazelcast`. The cache can be either local (in-memory) or distributed (Hazelcast IMap).&#x20;

## Hazelcast Configuration

{% hint style="warning" %}
The example below must be modified according to your installation context.
{% endhint %}

The following is an example of the Hazelcast implementation:

```xml
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

## Networking

Depending on your installation (VMs, Kubernetes, AWS, etc.​), there are multiple ways to configure Hazelcast networking. The default configuration is designed to work in standalone mode. Distribution mode is not relevant to most use cases and not recommended.

If you need to run Hazelcast in a cluster, the simplest way is to enable multicast:

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
More information can be found in the [Hazelcast documentation](https://docs.hazelcast.org/docs), including how to configure Hazelcast as a cluster.
{% endhint %}

## Cache resource management

API publishers can [create Cache resources](../../using-the-product/managing-your-apis/resources/README.md#how-to-create-a-resource) to:

* Cache upstream of a response with the [Cache policy](../../using-the-product/managing-your-apis/policy-studio/policies-for-your-apis/a-c/cache.md)
* Cache access tokens with the [OAuth2 policy](../../using-the-product/managing-your-apis/policy-studio/policies-for-your-apis/l-p/oauth2/README.md)

The default distribution includes the [Cache resource](../../using-the-product/managing-your-apis/resources/cache.md#cache) plugin, which stores content in-memory and is locally managed on each Gateway node of the installation.

Configuration of Cache resources cannot be managed using the `hazelcast.xml` file. The configuration is directly defined on the Cache resource.

## Persistent cache

APIM also supports the Gravitee [Redis Cache resource](../../using-the-product/managing-your-apis/resources/cache.md#cache-redis) plugin, based on [Redis](https://redis.io/documentation). This plugin is not in the default distribution, but can be [downloaded](https://download.gravitee.io/#graviteeio-apim/plugins/resources/gravitee-resource-cache-redis/) and deployed with these [instructions](../../overview/plugins-and-api-definitions/plugins/deploying-plugins.md#deployment).
