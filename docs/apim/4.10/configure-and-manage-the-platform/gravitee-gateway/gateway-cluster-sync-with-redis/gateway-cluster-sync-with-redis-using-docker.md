---
tags:
  - distributed-sync
---

# Gateway Cluster sync with Redis using Docker

## Overview

Gateway Cluster sync leverages Redis to synchronize the state of APIs, keys, and other configurations across your API Gateways in memory, significantly improving system scalability and resilience. Instead of every gateway directly calling the central management repository, a primary node fetches the state and stores it in a Redis-backed Distributed Sync repository, from which all secondary nodes read. This architecture minimizes the load on the main database and ensures high availability, allowing gateways to continue serving traffic—and new instances to bootstrap—even if the central control plane experiences downtime. By actively tracking synchronization states and deployment events, the cluster maintains consistent, incremental updates and supports seamless failovers if the primary node goes offline.

## Prerequisites

Before you enable the distributed sync with Redis, complete the following steps:

{% hint style="info" %}
A standard Redis deployment without the Search module appears to connect successfully. However, every distributed-sync write fails with `Unknown command 'FT.CREATE'`, and the API Gateway never reaches a "ready" state.
{% endhint %}

* Install Redis with the search module. Distributed sync requires the RedisSearch module. To ensure that you have the RedisSearch module, use one of the following Redis modules:
  * The `redis/redis-stack` Docker image, which bundles RediSearch.
  * Redis 8+, which includes the Search module natively.
  * Redis 7 or earlier with the RediSearch module loaded. You can load the module by adding `loadmodule /usr/local/lib/redis/modules/redisearch.so` to your Redis configuration. For more information about Redis and RedisSearch, see [redis.md](../../../prepare-a-production-environment/repositories/redis.md "mention") and the [RedisSearch documentation](https://redis.io/docs/latest/develop/interact/search-and-query/).
* Obtain an Enterprise License. You must mount the license into every API Gateway pod to start the `repository-redis` plugin and load `DISTRIBUTED_SYNC`. For more information about obtaining an enterprise license, see [enterprise-edition.md](../../../readme/enterprise-edition.md "mention").
* Deploy a fully Self-Hosted Installation or a Hybrid Installation of APIM. For more information about self-hosted installation, see [self-hosted-installation-guides](../../../self-hosted-installation-guides/ "mention") or [hybrid-installation-and-configuration-guides](../../../hybrid-installation-and-configuration-guides/ "mention").
* Deploy at least two API Gateway replicas. Distributed sync works only when `gateway.replicaCount` is greater than or equal to 2, and `gateway.autoscaling.enabled` is `false`, because the Helm chart only honors `replicaCount` when the HPA is disabled.

## Enable Distributed sync

To configure Distributed sync with Redis, complete the following steps:

1. [Configure your Hazelcast Cluster](gateway-cluster-sync-with-redis-using-docker.md#configure-your-hazelcast-cluster-for-docker-installations)
2. [Configure your Redis Repository](gateway-cluster-sync-with-redis-using-docker.md#configure-your-redis-repository-for-docker-installations)
3. [Configure the distributed sync on the APIM Gateway](gateway-cluster-sync-with-redis-using-docker.md#configure-the-distributed-sync-on-the-apim-gateway)

### Configure your Hazelcast Cluster

1.  In your `gravitee.yml` file, navigate to the `cluster` section, and then add the following configuration:

    <pre class="language-yaml" data-title="gravitee.yml"><code class="lang-yaml">cluster:
        type: hazelcast
    </code></pre>
2.  In the `${gravitee.home}/config/hazelcast-cluster.xml` file, add the following configuration:

    <pre class="language-xml" data-title="hazelcast-cluster.xml"><code class="lang-xml">&#x3C;hazelcast xmlns="[http://www.hazelcast.com/schema/config](http://www.hazelcast.com/schema/config)"
               xmlns:xsi="[http://www.w3.org/2001/XMLSchema-instance](http://www.w3.org/2001/XMLSchema-instance)"
               xsi:schemaLocation="[http://www.hazelcast.com/schema/config](http://www.hazelcast.com/schema/config)
               [http://www.hazelcast.com/schema/config/hazelcast-config-5.3.xsd](http://www.hazelcast.com/schema/config/hazelcast-config-5.3.xsd)">

        &#x3C;cluster-name>gio-apim-cluster&#x3C;/cluster-name>
        &#x3C;network>
            &#x3C;port auto-increment="true" port-count="100">5701&#x3C;/port>
            &#x3C;join>
                &#x3C;auto-detection enabled="true"/>
                &#x3C;multicast enabled="false"/>
                &#x3C;tcp-ip enabled="true">
                    &#x3C;member>&#x3C;gateway_client>&#x3C;/member>
                    &#x3C;member>&#x3C;gateway_client_2>&#x3C;/member>
                    &#x3C;member>&#x3C;gateway_server>&#x3C;/member>
                &#x3C;/tcp-ip>
            &#x3C;/join>
        &#x3C;/network>
    &#x3C;/hazelcast>
    </code></pre>

    Use the following values to replace the variables:

    * `<gateway_client>`. Replace this with the name of your first API Gateway.
    * `<gateway_client_2>`. Replace this with the name of your second API Gateway.
    * `<gateway_server>`. Replace this with the name of your third API Gateway.

### Configure your Redis Repository

To enable your distributed sync repository, enable the Search module on your Redis instance.

1.  Enable the Search module using the following command:

    ```bash
    docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
    ```

### Configure the distributed sync on the APIM Gateway

1.  In your Docker Compose file, navigate to the `distributed-sync` section, and then add the following configuration:

    <pre class="language-yaml" data-title="docker-compose.yml"><code class="lang-yaml">distributed-sync:
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
    </code></pre>
2.  In the `services` section, add the following configuration:

    <pre class="language-yaml" data-title="docker-compose.yml"><code class="lang-yaml">services:
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
    </code></pre>
3.  Start the API Gateway using the following command:

    ```bash
    docker compose up -d
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
