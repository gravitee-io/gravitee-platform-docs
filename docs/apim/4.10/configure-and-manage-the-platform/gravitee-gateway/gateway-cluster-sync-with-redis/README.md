# Gateway Cluster sync with Redis

## Overview

### What is Gateway Cluster sync with Redis?

This guide explains how to enable and configure the Gateway Cluster sync with Redis.

The Gateway Cluster sync uses Redis to synchronize the state of APIs, API Keys, Subscriptions, Dictionaries, and Organizations across your API Gateways. This process maintains the state in memory, which ensures that gateways remain resilient and high-performing, even if the main repository is down.

### What issue does it solve?

The Gateway Cluster sync improves both scalability and resilience.

**Scalability**: Without the Gateway Cluster sync, each API Gateway must directly call the repository for synchronization. This configuration is not scalable because the addition of more gateways increases the repository load and slows the bootstrap time for each gateway. By using a primary node to manage the state, which significantly reduces the load, The Gateway Cluster sync solves this issue.

\
**Resilience & High Availability**: By maintaining the state in Redis, new gateway instances can start and serve API traffic even if the central management repository (database) or control plane is down. This ensures that you do not have a risk API outages during database maintenance or network disruptions.

### How does it work?

The new repository scope, `Distributed Sync`,  is responsible for keeping the sync state for a cluster.

In the repository, the primary node stores information regarding the current synchronization state and what is currently deployed.

This allows another node to take over if the current primary node goes down without the need of doing a full sync again.

By enabling the Gateway Cluster sync on your gateways, the master node fetches the API definitions from the management repository (MongoDB, Bridge, JDBC), and then stores them in the Redis distributed sync repository, while the other gateways only read the API definitions from the Redis distributed sync repository.

<figure><img src="../../../.gitbook/assets/image (156).png" alt=""><figcaption></figcaption></figure>

### Distributed Synchronization State

The Synchronization State tracks the current sync process. It contains the following information:

* cluster id
* node version
* node id
* Last successful synchronization timeframe.

### Distributed Synchronization Event

The objects are used to know what needs to be deployed or undeployed across the cluster. They contain the following information:

* `id`: the identifier of the object
* `Type`:  `API`, `API_KEY`, `SUBSCRIPTION`, `DICTIONARY`,  `ORGANIZATION` , and `LICENSE`&#x20;
* `SyncAction`:  `DEPLOY` or  `UNDEPLOY`
* `Payload`: The object to deploy or undeploy
* `UpdatedAt`: Date of the update to allow incremental syncs

After any business object is deployed, and only if distributed sync is enabled, the primary node stores those objects in the new distributed sync repository.

## Prerequisites&#x20;

Before you enable the distributed sync with Redis, you must complete the following steps:

* Install Redis. For more information about Redis, see [redis.md](../../../prepare-a-production-environment/repositories/redis.md "mention").
* Obtain an Enterprise License. For more information about obtaining an enterprise license, see [enterprise-edition.md](../../../readme/enterprise-edition.md "mention").
* Deploy a fully Self-Hosted Installation or a Hybrid Installation of APIM. For more information about self-hosted installation, see [self-hosted-installation-guides](../../../self-hosted-installation-guides/ "mention") or [hybrid-installation-and-configuration-guides](../../../hybrid-installation-and-configuration-guides/ "mention").

## Enable Distributed sync

To configure Distributed sync with Redis, complete the following steps:

* [#docker-installations-only-configure-your-hazelcast-cluster](./#docker-installations-only-configure-your-hazelcast-cluster "mention")
* [#configure-your-redis-repository](./#configure-your-redis-repository "mention")
* [#configure-the-distributed-sync-on-the-apim-gateway](./#configure-the-distributed-sync-on-the-apim-gateway "mention")

### (Docker installations only) Configure your Hazelcast Cluster

1.  In your `gravitee.yml` file navigate to the `cluster` section, and then add the following configuration:&#x20;

    ```yaml
    cluster:
        type: hazelcast
    ```
2.  Add the following configuration to the`${gravitee.home}/config/hazelcast-cluster.xml` file:

    ```xml
    <hazelcast xmlns="http://www.hazelcast.com/schema/config"
               xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
               xsi:schemaLocation="http://www.hazelcast.com/schema/config
               http://www.hazelcast.com/schema/config/hazelcast-config-5.3.xsd">

        <cluster-name>gio-apim-cluster</cluster-name>
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

    * Replace `<gateway_client>` with the name of your first Gateway.
    * Replace `<gateway_client_2>` with the name of your second Gateway .
    * Replace `<gateway_server>` with your the name of your third Gateway.

### Configure your Redis Repository

To enable your distributed sync repository, you must enable the Search module on your Redis instance.&#x20;

*   Enable the Search module using the following command:<br>

    ```yaml
    docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
    ```

### Configure the distributed sync on the APIM Gateway

* Configure the distributed sync. Follow the instructions that are relevant for your installation type:

{% tabs %}
{% tab title="Docker" %}
1.  In your Docker Compose file, navigate to the `distributed-sync` section, and then add the following configuration:

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
2.  Navigate to the `services` section, and then add the following configuration:<br>

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
3.  Start the Gateway using the following command:

    ```bash
    docker compose up -d
    ```
{% endtab %}

{% tab title="Helm" %}
1.  In your `values.yaml` file, navigate to the `gateway` section, and then, after the `name:gateway` line, add the following configuration:<br>

    ```bash
    replicaCount: 2

      # Cluster configuration for distributed sync
      cluster:
        type: hazelcast
        hazelcast:
          configPath: /opt/graviteeio-gateway/config/hazelcast.xml

      # Distributed sync configuration
      distributedSync:
        enabled: true
        type: redis
        redis:
          host: host.docker.internal
          port: 6379

      # Services configuration for distributed sync
      services:
        sync:
          repository:
            enabled: true
          distributed:
            enabled: true
    ```
2.  In your `gateway-configmap.yaml` file, navigate to the `data.gravitee.yml` section, and then add the following configuration:<br>

    ```yaml
    {{- if .Values.gateway.cluster }}
        cluster:
          type: {{ .Values.gateway.cluster.type }}
          {{- if eq .Values.gateway.cluster.type "hazelcast" }}
          hazelcast:
            config-path: {{ .Values.gateway.cluster.hazelcast.configPath }}
          {{- end }}
        {{- end }}

        {{- if .Values.gateway.distributedSync }}
        distributed-sync:
          type: {{ .Values.gateway.distributedSync.type }}
          {{- if eq .Values.gateway.distributedSync.type "redis" }}
          redis:
            host: {{ .Values.gateway.distributedSync.redis.host }}
            port: {{ .Values.gateway.distributedSync.redis.port }}
          {{- end }}
        {{- end }}

        {{- if .Values.gateway.services }}
        services:
          {{- if .Values.gateway.services.sync }}
          sync:
            {{- if .Values.gateway.services.sync.repository }}
            repository:
              enabled: {{ .Values.gateway.services.sync.repository.enabled }}
            {{- end }}
            {{- if .Values.gateway.services.sync.distributed }}
            distributed:
              enabled: {{ .Values.gateway.services.sync.distributed.enabled }}
            {{- end }}
          {{- end }}
        {{- end }}
    ```
3.  Deploy your installation with your new configurations using the following command:<br>

    ```bash
    helm upgrade --install graviteeio-apim . \
      --namespace gravitee-apim \
      --create-namespace \
      --set gateway.replicaCount=2 \
      --set gateway.distributedSync.enabled=true \
      --set gateway.distributedSync.type=redis \
      --set gateway.distributedSync.redis.host=redis \
      --set gateway.distributedSync.redis.port=6379 \
      --set gateway.services.sync.repository.enabled=true \
      --set gateway.services.sync.distributed.enabled=true \
      --wait
    ```
{% endtab %}
{% endtabs %}

## Verification

*   Your Gateway's logs show the following output:<br>

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

    11:42:12.677 [main] [] INFO  i.g.node.container.AbstractNode - Gravitee.io - API Gateway id[da56a9b0-7e6a-4dec-96a9-b07e6a2decfd] version[4.3.6] pid[17705] build[${env.BUILD_NUMBER}#${env.GIT_COMMIT}] jvm[Eclipse Adoptium/OpenJDK 64-Bit Server VM/17.0.6+10] started in 8687 ms.
    ```
