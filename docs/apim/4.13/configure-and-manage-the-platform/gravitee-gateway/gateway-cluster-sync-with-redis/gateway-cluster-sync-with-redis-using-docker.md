# Gateway Cluster sync with Redis using Docker

## Overview

Gateway Cluster sync leverages Redis to synchronize the state of APIs, keys, and other configurations across your API Gateways in memory, significantly improving system scalability and resilience. Instead of every gateway directly calling the central management repository, a primary node fetches the state and stores it in a Redis-backed Distributed Sync repository, from which all secondary nodes read. This architecture minimizes the load on the main database and ensures high availability, allowing gateways to continue serving traffic, and new instances to bootstrap, even if the central control plane experiences downtime. By actively tracking synchronization states and deployment events, the cluster maintains consistent, incremental updates and supports seamless failover if the primary node goes offline.

## Prerequisites

Before you enable the distributed sync with Redis, complete the following steps:

{% hint style="info" %}
A standard Redis deployment without the Search module appears to connect successfully. However, every distributed-sync write fails with `Unknown command 'FT.CREATE'`, and the API Gateway never reaches a "ready" state.
{% endhint %}

* Install Redis with the search module. Distributed sync requires the RedisSearch module. To ensure that you have the RedisSearch module, use one of the following Redis modules:
  * The `redis/redis-stack` Docker image, which bundles RediSearch.
  * Redis 8+, which includes the Search module natively.
  * Redis 7 or earlier with the RediSearch module loaded. You can load the module by adding `loadmodule /usr/local/lib/redis/modules/redisearch.so` to your Redis configuration. For more information about Redis and RedisSearch, see [Redis](/apim/4.10/prepare-a-production-environment/repositories/redis.md) and the [RedisSearch documentation](https://redis.io/docs/latest/develop/interact/search-and-query/).
* Obtain an Enterprise License. You must mount the license into every API Gateway pod to start the `repository-redis` plugin and load `DISTRIBUTED_SYNC`. For more information about obtaining an enterprise license, see [Enterprise Edition](../../../introduction/enterprise-edition.md).
* Deploy a fully Self-Hosted Installation or a Hybrid Installation of APIM. For more information about self-hosted installation, see [Self-Hosted Installation Guides](/apim/4.10/self-hosted-installation-guides.md) or [Hybrid Installation & Configuration Guides](/apim/4.10/hybrid-installation-and-configuration-guides.md).
* Deploy at least two API Gateway replicas. Distributed sync works only when `gateway.replicaCount` is greater than or equal to 2, and `gateway.autoscaling.enabled` is `false`, because the Helm chart only honors `replicaCount` when the HPA is disabled.

## Cluster-scoped Redis and Hazelcast cluster naming

From APIM 4.12, distributed sync keys in Redis are scoped by **cluster ID** (the Hazelcast `cluster-name`). When several gateway groups share one Redis instance (for example, `external` and `internal` gateway hosts), each group must use a **different** `<cluster-name>` in `hazelcast-cluster.xml`.

| Gateway group | Example `cluster-name` | Redis key prefix |
|:--------------|:-----------------------|:-----------------|
| External gateways | `gio-apim-external` | `distributed_event:gio-apim-external:...` |
| Internal gateways | `gio-apim-internal` | `distributed_event:gio-apim-internal:...` |

If you change `cluster-name` or sharding tags, delete stale `distributed_event:*` and `distributed_sync_state:*` keys for the old cluster ID in Redis.

{% hint style="warning" %}
**Deployment constraints:** Start with one gateway instance per group, wait for the primary to sync, then add peers one at a time. During upgrades, replace gateways sequentially so the primary populates Redis before secondaries join.
{% endhint %}

## Enable Distributed sync

To configure Distributed sync with Redis, complete the following steps:

1. [Configure your Hazelcast Cluster](#configure-your-hazelcast-cluster-for-docker-installations)
2. [Configure your Redis Repository](#configure-your-redis-repository-for-docker-installations)
3. [Configure the distributed sync on the APIM Gateway](#configure-the-distributed-sync-on-the-apim-gateway)

### Configure your Hazelcast Cluster

1. In your `gravitee.yml` file, navigate to the `cluster` section, and then add the following configuration:

   {% code title="gravitee.yml" %}
   ```yaml
   cluster:
          type: hazelcast
   ```
   {% endcode %}
2. In the `${gravitee.home}/config/hazelcast-cluster.xml` file, add the following configuration:

   {% code title="hazelcast-cluster.xml" %}
   ```xml
   <hazelcast xmlns="http://www.hazelcast.com/schema/config"
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 xsi:schemaLocation="http://www.hazelcast.com/schema/config
                 http://www.hazelcast.com/schema/config/hazelcast-config-5.3.xsd">
   
          <cluster-name>gio-apim-external</cluster-name>
          <network>
              <port auto-increment="true" port-count="100">5701</port>
              <join>
                  <auto-detection enabled="true"/>
                  <multicast enabled="false"/>
                  <tcp-ip enabled="true">
                      <member><gateway_client></member>
                      <member><gateway_client_2></member>
                      <member><gateway_server></member>
                  </tcp-ip>
              </join>
          </network>
      </hazelcast>
   ```
   {% endcode %}

   Use the following values to replace the variables:

   * `<gateway_client>`. Replace this with the name of your first API Gateway.
   * `<gateway_client_2>`. Replace this with the name of your second API Gateway.
   * `<gateway_server>`. Replace this with the name of your third API Gateway.

   {% hint style="info" %}
   All gateways in the **same** sharding-tag group must share the **same** `cluster-name`. Gateways in a **different** group (for example, internal vs external) that share Redis must use a **different** `cluster-name`.
   {% endhint %}

### Configure your Redis Repository

To enable your distributed sync repository, enable the Search module on your Redis instance.

1. Enable the Search module using the following command:

   ```bash
   docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
   ```

### Configure the distributed sync on the APIM Gateway

1. In your Docker Compose file, navigate to the `distributed-sync` section, and then add the following configuration:

   {% code title="docker-compose.yml" %}
   ```yaml
   distributed-sync:
       type: redis
       redis:
         # Redis Standalone settings
         host: localhost
         port: 6379
         password:
         # Redis Sentinel settings
         sentinel:
           master: redis-master
           nodes:
             - host: sentinel1
               port: 26379
             - host: sentinel2
               port: 26379
         # SSL settings
         ssl: false
         trustAll: true # default value is true to keep backward compatibility but you should set it to false and configure a truststore for security concerns
         tlsProtocols: # List of TLS protocols to allow comma separated i.e: TLSv1.2, TLSv1.3
         tlsCiphers: # List of TLS ciphers to allow comma separated i.e: TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384, TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384, TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384, TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384
         alpn: false
         openssl: false # Used to rely on OpenSSL Engine instead of default JDK SSL Engine
         # Keystore for redis mTLS (client certificate)
         keystore:
           type: pem # Supports jks, pem, pkcs12
           path: ${gravitee.home}/security/redis-keystore.jks # A path is required if certificate's type is jks or pkcs12
           password: secret
           keyPassword:
           alias:
           certificates: # Certificates are required if keystore's type is pem
             - cert: ${gravitee.home}/security/redis-mycompany.org.pem
           key: ${gravitee.home}/security/redis-mycompany.org.key
             - cert: ${gravitee.home}/security/redis-mycompany.com.pem
           key: ${gravitee.home}/security/redis-mycompany.com.key
         truststore:
           type: pem # Supports jks, pem, pkcs12
           path: ${gravitee.home}/security/redis-truststore.jks
           password: secret
           alias:
   ```
   {% endcode %}
2. In the `services` section, add the following configuration:

   {% code title="docker-compose.yml" %}
   ```yaml
   services:
        # Synchronization daemon used to keep the gateway state in sync with the configuration from the management repository
        # Be aware that, by disabling it, the gateway will not be sync with the configuration done through management API
        # and management UI
        sync:
          # Synchronization is done each 5 seconds
          delay: 5000
          unit: MILLISECONDS
          repository:
            enabled : true
          distributed:
            enabled : true # By enabling this mode, data synchronization process is distributed over clustered API gateways. You must configure distributed-sync repository.
          bulk_items: 100 # Defines the number of items to retrieve during synchronization (events, plans, API Keys, ...).
   ```
   {% endcode %}
3. Start the API Gateway using the following command:

   ```bash
   docker compose up -d
   ```

4. (Optional) Verify cluster-scoped keys in Redis:

   ```bash
   redis-cli KEYS 'distributed_sync_state:*'
   redis-cli KEYS 'distributed_event:*' | head
   # Expect prefixes matching your cluster-name, e.g. distributed_event:gio-apim-external:...
   ```

## Verification

Review your API Gateway logs for the following output:

```yaml
11:42:04.001 [main] [] INFO  i.g.n.c.plugin.ClusterPluginHandler - Install plugin: cluster-hazelcast [io.gravitee.node.plugin.cluster.hazelcast.HazelcastClusterManager]
11:42:04.270 [main] [] WARN  c.h.i.impl.HazelcastInstanceFactory - Hazelcast is starting in a Java modular environment (Java 9 and newer) but without proper access to required Java packages. Use additional Java arguments to provide Hazelcast access to Java internal API. The internal API access is used to get the best performance results. Arguments to be used:
 --add-modules java.se --add-exports java.base/jdk.internal.ref=ALL-UNNAMED --add-opens java.base/java.lang=ALL-UNNAMED --add-opens java.base/sun.nio.ch=ALL-UNNAMED --add-opens java.management/sun.management=ALL-UNNAMED --add-opens jdk.management/com.sun.management.internal=ALL-UNNAMED
11:42:04.699 [main] [] WARN  com.hazelcast.cp.CPSubsystem - [127.0.0.1]:5701 [gio-apim-gateway] [5.3.6] CP Subsystem is not enabled. CP data structures will operate in UNSAFE mode! Please note that UNSAFE mode will not provide strong consistency guarantees.
11:42:10.128 [main] [] INFO  i.g.n.c.plugin.ClusterPluginHandler - Cluster manager plugin 'cluster-hazelcast' installed.
11:42:10.128 [main] [] INFO  i.g.n.c.plugin.ClusterPluginHandler - Plugin 'cluster-hazelcast' installed.

...

11:42:11.746 [main] [] INFO  i.g.p.r.i.RepositoryPluginHandler - Install plugin: repository-redis [io.gravitee.repository.redis.RedisRepositoryProvider]
11:42:11.746 [main] [] INFO  i.g.p.r.i.RepositoryPluginHandler - Register a new repository: repository-redis [io.gravitee.repository.redis.RedisRepositoryProvider]
11:42:11.747 [main] [] INFO  i.g.p.r.i.RepositoryPluginHandler - Repository [DISTRIBUTED_SYNC] loaded by redis
11:42:11.788 [main] [] INFO  i.g.p.r.i.RepositoryPluginHandler - Plugin 'repository-redis' installed.

...

11:42:12.677 [main] [] INFO  i.g.node.container.AbstractNode - Gravitee - API Gateway id[da56a9b0-7e6a-4dec-96a9-b07e6a2decfd] version[4.3.6] pid[17705] build[${env.BUILD_NUMBER}#${env.GIT_COMMIT}] jvm[Eclipse Adoptium/OpenJDK 64-Bit Server VM/17.0.6+10] started in 8687 ms.
```


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://documentation.gravitee.io/apim/4.10/configure-and-manage-the-platform/gravitee-gateway/gateway-cluster-sync-with-redis/gateway-cluster-sync-with-redis-using-docker.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.