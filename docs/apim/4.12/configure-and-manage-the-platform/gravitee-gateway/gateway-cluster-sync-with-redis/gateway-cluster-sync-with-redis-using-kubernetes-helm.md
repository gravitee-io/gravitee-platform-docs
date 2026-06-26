# Gateway Cluster sync with Redis using Kubernetes (Helm)

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
  * Redis 7 or earlier with the RediSearch module loaded. You can load the module by adding `loadmodule /usr/local/lib/redis/modules/redisearch.so` to your Redis configuration. For more information about Redis and RedisSearch, see [Redis](../../../prepare-a-production-environment/repositories/redis.md) and the [RedisSearch documentation](https://redis.io/docs/latest/develop/interact/search-and-query/).
* Obtain an Enterprise License. You must mount the license into every API Gateway pod to start the `repository-redis` plugin and load `DISTRIBUTED_SYNC`. For more information about obtaining an enterprise license, see [Enterprise Edition](../../../introduction/enterprise-edition.md).
* Deploy a fully Self-Hosted Installation or a Hybrid Installation of APIM. For more information about self-hosted installation, see [Self-Hosted Installation Guides](../../../self-hosted-installation-guides/README.md) or [Hybrid Installation & Configuration Guides](../../../hybrid-installation-and-configuration-guides/README.md).
* Deploy at least two API Gateway replicas. Distributed sync works only when `gateway.replicaCount` is greater than or equal to 2, and `gateway.autoscaling.enabled` is `false`, because the Helm chart only honors `replicaCount` when the HPA is disabled.

## Cluster-scoped Redis and Hazelcast cluster naming

When multiple gateway Helm releases share one Redis instance (for example, one release per sharding tag: `external`, `internal`, `aog`), each release must form its **own Hazelcast cluster** with a **unique `cluster-name`**. That name becomes the runtime **cluster ID** and scopes all distributed sync keys in Redis.

| Setting | Description |
|:--------|:------------|
| `gateway.sharding_tags` | Comma-separated sharding tags for this release (for example, `external`). Deploy one Helm release per tag set. |
| `gateway.cluster.type` | Set to `hazelcast` when distributed sync is enabled. The chart renders `hazelcast.xml` and validates this pairing. |
| `gateway.cluster.hazelcast.clusterName` | Optional override. Default: `<helm-release-name>-<sharding_tags>` (slugged, max 63 characters). Must differ across releases that share Redis. |

{% hint style="info" %}
From APIM 4.12, the Helm chart can render `config/hazelcast.xml` automatically when `gateway.cluster.type` is `hazelcast`. You do not need a separate `extraObjects` ConfigMap unless you override `gateway.cluster.hazelcast.configPath` with a custom file.
{% endhint %}

### Deployment constraints

Secondary gateways read distributed state from Redis. Initial sync on a secondary is one-shot; the primary must publish state and events before secondaries can serve APIs.

| Scenario | Requirement |
|:---------|:--------------|
| **Fresh install** | Set `gateway.replicaCount: 1` (or `gateway.autoscaling.minReplicas: 1`). Wait until the primary has synchronized. Scale up **one replica at a time**. |
| **Upgrade** | Set `gateway.deployment.strategy.rollingUpdate.maxUnavailable: 0` and `maxSurge: 1` so pods join the Hazelcast cluster one at a time. |
| **Autoscaling** | Do not set a high `minReplicas` on first install. Configure HPA `behavior.scaleUp` to add at most one pod per interval when distributed sync is enabled. |

Example rolling strategy:

<pre class="language-yaml" data-title="values.yaml"><code class="lang-yaml">gateway:
  deployment:
    strategy:
      type: RollingUpdate
      rollingUpdate:
        maxUnavailable: 0
        maxSurge: 1
</code></pre>

### Upgrade from legacy Redis keys

Cluster-scoped keys are introduced in APIM 4.12. After upgrade:

* New pods use keys such as `distributed_event:&lt;clusterId&gt;:...` and RediSearch index `distributed-event-search-idx-v2`.
* Legacy keys without a cluster ID prefix are not read.
* The primary repopulates Redis from the management repository during rollout; a second manual restart is not required if MongoDB is reachable.
* Optionally delete stale `distributed_event:*` and `distributed_sync_state:*` entries and drop the old search index after all gateways are healthy.

If `gateway.sharding_tags` or `gateway.cluster.hazelcast.clusterName` change, treat it as a new cluster: delete Redis keys for the old cluster ID.

## Configure the distributed sync on the APIM Gateway

1. In your `values.yaml` file, navigate to the `gateway.additionalPlugins` section, and then add the `gravitee-node-cluster-plugin-hazelcast` plugin. You must download the Hazelcast plugin at pod startup, and it must match the `gravitee-node` version of your APIM release. For example, for 4.10.x, the `gravitee-node` version is 7.26.x, and the URL of the Hazelcast plugin is `https://repo1.maven.org/maven2/io/gravitee/node/gravitee-node-cluster-plugin-hazelcast/7.26.3/gravitee-node-cluster-plugin-hazelcast-7.26.3.zip`. To confirm the bundled `gravitee-node`, check the `gravitee-api-management` `pom.xml` on the matching branch by using `grep gravitee-node.version`.

   <pre class="language-yaml" data-title="values.yaml"><code class="lang-yaml">gateway:
     additionalPlugins:
       - [https://repo1.maven.org/maven2/io/gravitee/node/gravitee-node-cluster-plugin-hazelcast/7.26.3/gravitee-node-cluster-plugin-hazelcast-7.26.3.zip](https://repo1.maven.org/maven2/io/gravitee/node/gravitee-node-cluster-plugin-hazelcast/7.26.3/gravitee-node-cluster-plugin-hazelcast-7.26.3.zip)
   </code></pre>

   <div data-gb-custom-block data-tag="hint" data-style="info" class="hint hint-info"><p>The Helm chart automatically downloads plugins listed in <code>additionalPlugins</code> using an init container at pod startup. Ensure that the pod has outbound access to <code>repo1.maven.org</code>, or mirror the file internally and adjust the URL.</p></div>
1a. (Optional) Configure Redis Cluster nodes for rate limiting and Redis resource pool settings for cache and AI vector store resources. These settings apply gateway-wide and are sourced from `gravitee.yml` in production deployments.

   | Property | Description | Default |
   |:---------|:------------|:--------|
   | `gateway.ratelimit.redis.cluster.nodes` | Redis Cluster nodes for rate limiting (array of `{host, port}`) | `[]` |
   | `gateway.cacheRedis.maxPoolSize` | Redis cache resource max connections per endpoint (gateway-wide) | `6` |
   | `gateway.cacheRedis.maxPoolWaiting` | Redis cache resource max queued requests waiting for a connection | `1024` |
   | `gateway.cacheRedis.poolCleanerInterval` | Redis cache resource idle-connection cleaner interval (ms) | `30000` |
   | `gateway.cacheRedis.poolRecycleTimeout` | Redis cache resource idle connection recycle timeout (ms) | `180000` |
   | `gateway.cacheRedis.maxWaitingHandlers` | Redis cache resource max queued commands on a connection | `1024` |
   | `gateway.cacheRedis.connectTimeout` | Redis cache resource TCP connect timeout (ms) | `2000` |
   | `gateway.aiVectorStoreRedis.maxPoolSize` | AI vector store Redis resource max connections per endpoint (APIM 4.12+) | `6` |
   | `gateway.aiVectorStoreRedis.maxPoolWaiting` | AI vector store Redis resource max queued requests waiting for a connection | `1024` |
   | `gateway.aiVectorStoreRedis.poolCleanerInterval` | AI vector store Redis resource idle-connection cleaner interval (ms) | `30000` |
   | `gateway.aiVectorStoreRedis.poolRecycleTimeout` | AI vector store Redis resource idle connection recycle timeout (ms) | `180000` |
   | `gateway.aiVectorStoreRedis.maxWaitingHandlers` | AI vector store Redis resource max queued commands on a connection | `1024` |
   | `gateway.aiVectorStoreRedis.connectTimeout` | AI vector store Redis resource TCP connect timeout (ms) | `2000` |

   **Example**:
   <pre class="language-yaml" data-title="values.yaml"><code class="lang-yaml">gateway:
     ratelimit:
       redis:
         cluster:
           nodes:
             - host: redis-node-1.example.com
               port: 6379
             - host: redis-node-2.example.com
               port: 6379
     cacheRedis:
       maxPoolSize: 10
       maxPoolWaiting: 2048
       poolCleanerInterval: 30000
       poolRecycleTimeout: 180000
       maxWaitingHandlers: 1024
       connectTimeout: 2000
     aiVectorStoreRedis:
       maxPoolSize: 10
       maxPoolWaiting: 2048
   </code></pre>
2. Create the Hazelcast configuration `ConfigMap` using the top-level `extraObjects` value. **Skip this step** if you rely on the chart-rendered `hazelcast.xml` (`gateway.cluster.type: hazelcast` without a custom `configPath`). Hazelcast requires an XML configuration for pods to discover each other. For Kubernetes, use Hazelcast Kubernetes discovery. For more information about Hazelcast Kubernetes discovery, see the [Kubernetes auto discovery documentation](https://docs.hazelcast.com/hazelcast/5.4/kubernetes/kubernetes-auto-discovery).

   <div data-gb-custom-block data-tag="hint" data-style="warning" class="hint hint-warning"><p><code>&#x3C;service-port>5701&#x3C;/service-port></code> is mandatory. Without the service port, the pod-label discovery of Hazelcast silently fails. Peer pods are discovered, but the cluster never forms because port <code>5701</code> is not declared as a <code>containerPort</code> on the Gateway deployment. The <code>&#x3C;service-port></code> element tells Hazelcast which port to use against the discovered pods directly. This bypasses the missing <code>containerPort</code> or Service entry.</p></div>

   <pre class="language-yaml" data-title="values.yaml"><code class="lang-yaml">extraObjects:
     - apiVersion: v1
       kind: ConfigMap
       metadata:
         name: hazelcast-config
       data:
         hazelcast.xml: |
           &#x3C;?xml version="1.0" encoding="UTF-8"?>
           &#x3C;hazelcast xmlns="[http://www.hazelcast.com/schema/config](http://www.hazelcast.com/schema/config)"
                      xmlns:xsi="[http://www.w3.org/2001/XMLSchema-instance](http://www.w3.org/2001/XMLSchema-instance)"
                      xsi:schemaLocation="[http://www.hazelcast.com/schema/config](http://www.hazelcast.com/schema/config)
                      [http://www.hazelcast.com/schema/config/hazelcast-config-5.3.xsd](http://www.hazelcast.com/schema/config/hazelcast-config-5.3.xsd)">

               &#x3C;cluster-name>gio-apim-cluster&#x3C;/cluster-name>

               &#x3C;properties>
                   &#x3C;property name="hazelcast.logging.type">slf4j&#x3C;/property>
                   &#x3C;property name="hazelcast.max.wait.seconds.before.join">20&#x3C;/property>
                   &#x3C;property name="hazelcast.member.list.publish.interval.seconds">10&#x3C;/property>
                   &#x3C;property name="hazelcast.socket.client.bind.any">false&#x3C;/property>
                   &#x3C;property name="hazelcast.max.no.heartbeat.seconds">20&#x3C;/property>
               &#x3C;/properties>

               &#x3C;network>
                   &#x3C;port auto-increment="false">5701&#x3C;/port>
                   &#x3C;join>
                       &#x3C;multicast enabled="false"/>
                       &#x3C;tcp-ip enabled="false"/>
                       &#x3C;kubernetes enabled="true">
                           &#x3C;namespace>YOUR_NAMESPACE&#x3C;/namespace>
                           &#x3C;pod-label-name>app.kubernetes.io/component&#x3C;/pod-label-name>
                           &#x3C;pod-label-value>gateway&#x3C;/pod-label-value>
                           &#x3C;service-port>5701&#x3C;/service-port>
                       &#x3C;/kubernetes>
                   &#x3C;/join>
               &#x3C;/network>
           &#x3C;/hazelcast>
   </code></pre>

   To complete the configuration, replace `YOUR_NAMESPACE` with the Kubernetes namespace where your gateways are deployed.
3. Mount the ConfigMap into the API Gateway with `extraVolumes` and `extraVolumeMounts`.

   <pre class="language-yaml" data-title="values.yaml"><code class="lang-yaml">gateway:
     extraVolumes: |
       - name: hazelcast-config
         configMap:
           name: hazelcast-config
     extraVolumeMounts: |
       - name: hazelcast-config
         mountPath: /opt/graviteeio-gateway/config/hazelcast.xml
         subPath: hazelcast.xml
   </code></pre>
4. Grant the API Gateway `ServiceAccount` the RBAC permissions it needs to list pods. The Kubernetes discovery plugin for Hazelcast calls the Kubernetes API to list pods. The API Gateway `ServiceAccount` therefore needs `pods`, `endpoints`, `nodes`, and `services` read permissions. The default role of the chart only includes `configmaps` and `secrets`. Append the Hazelcast rules with `apim.roleRules`:

   <pre class="language-yaml" data-title="values.yaml"><code class="lang-yaml">apim:
     roleRules:
       # Default chart rules — keep these.
       - apiGroups: [""]
         resources: [configmaps, secrets]
         verbs: [get, list, watch]
       # Required for Hazelcast Kubernetes auto-discovery.
       - apiGroups: [""]
         resources: [pods, endpoints, nodes, services]
         verbs: [get, list]
   </code></pre>

   <div data-gb-custom-block data-tag="hint" data-style="warning" class="hint hint-warning"><p>Without these RBAC rules, the Hazelcast plugin starts but fails to discover peers. You see <code>Forbidden: cannot list resource "pods"</code> in the gateway logs, and the second API Gateway never joins the cluster.</p></div>
5. Enable clustering and distributed sync by setting the following configuration in your `values.yaml` file:

   <div data-gb-custom-block data-tag="hint" data-style="warning" class="hint hint-warning"><p>Do not enable <code>services.sync.kubernetes.enabled</code> unless you are running the Gravitee Kubernetes Operator (GKO). That property turns on a parallel sync source that reads API definitions from Kubernetes <code>ConfigMap</code>s, not a "use Kubernetes in distributed-sync mode" switch.</p></div>

   <pre class="language-yaml" data-title="values.yaml"><code class="lang-yaml">gateway:
     replicaCount: 2
     sharding_tags: external   # one tag set per Helm release; cluster-name defaults to &lt;release&gt;-external
     autoscaling:
       enabled: false

     cluster:
       type: hazelcast
       # hazelcast.xml is rendered by the chart; optional override:
       # hazelcast:
       #   clusterName: my-release-external

     distributedSync:
       enabled: true
       type: redis
       redis:
         host: redis
         port: 6379
         # password:                  # if Redis requires auth
         # ssl: false
         # trustAll: true
         # tlsProtocols: TLSv1.2
         # sentinel:                  # uncomment for Sentinel
         #   master: redis-master
         #   nodes:
         #     - host: sentinel1
         #       port: 26379

     services:
       sync:
         repository:
           enabled: true
         distributed:
           enabled: true
         # Do NOT enable services.sync.kubernetes.enabled unless you are running
         # the Gravitee Kubernetes Operator (GKO / dbLess mode). It is unrelated to
         # distributed sync and is a frequent source of failing startup probes
         # on secondary nodes — see the Troubleshooting section.
   </code></pre>
6. Mount your Enterprise license, and then create the secret using the following configurations:

   <pre class="language-yaml" data-title="values.yaml"><code class="lang-yaml">license:
     name: licensekey-apim   # K8s secret name holding key 'licensekey'
   </code></pre>

   ```bash
   kubectl -n gravitee-apim create secret generic licensekey-apim \
     --from-file=licensekey=/path/to/license.key
   ```

   Review the following full `values.yaml` example:

   <pre class="language-yaml" data-title="values.yaml"><code class="lang-yaml">extraObjects:
     - apiVersion: v1
       kind: ConfigMap
       metadata:
         name: hazelcast-config
       data:
         hazelcast.xml: |
           &#x3C;?xml version="1.0" encoding="UTF-8"?>
           &#x3C;hazelcast xmlns="[http://www.hazelcast.com/schema/config](http://www.hazelcast.com/schema/config)"
                      xmlns:xsi="[http://www.w3.org/2001/XMLSchema-instance](http://www.w3.org/2001/XMLSchema-instance)"
                      xsi:schemaLocation="[http://www.hazelcast.com/schema/config](http://www.hazelcast.com/schema/config)
                      [http://www.hazelcast.com/schema/config/hazelcast-config-5.3.xsd](http://www.hazelcast.com/schema/config/hazelcast-config-5.3.xsd)">
               &#x3C;cluster-name>gio-apim-cluster&#x3C;/cluster-name>
               &#x3C;properties>
                   &#x3C;property name="hazelcast.logging.type">slf4j&#x3C;/property>
                   &#x3C;property name="hazelcast.max.wait.seconds.before.join">20&#x3C;/property>
                   &#x3C;property name="hazelcast.member.list.publish.interval.seconds">10&#x3C;/property>
                   &#x3C;property name="hazelcast.socket.client.bind.any">false&#x3C;/property>
                   &#x3C;property name="hazelcast.max.no.heartbeat.seconds">20&#x3C;/property>
               &#x3C;/properties>
               &#x3C;network>
                   &#x3C;port auto-increment="false">5701&#x3C;/port>
                   &#x3C;join>
                       &#x3C;multicast enabled="false"/>
                       &#x3C;tcp-ip enabled="false"/>
                       &#x3C;kubernetes enabled="true">
                           &#x3C;namespace>gravitee-apim&#x3C;/namespace>
                           &#x3C;pod-label-name>app.kubernetes.io/component&#x3C;/pod-label-name>
                           &#x3C;pod-label-value>gateway&#x3C;/pod-label-value>
                           &#x3C;service-port>5701&#x3C;/service-port>
                       &#x3C;/kubernetes>
                   &#x3C;/join>
               &#x3C;/network>
           &#x3C;/hazelcast>

   apim:
     roleRules:
       - apiGroups: [""]
         resources: [configmaps, secrets]
         verbs: [get, list, watch]
       - apiGroups: [""]
         resources: [pods, endpoints, nodes, services]
         verbs: [get, list]

   license:
     name: licensekey-apim

   gateway:
     enabled: true
     replicaCount: 2
     autoscaling:
       enabled: false

     additionalPlugins:
       - [https://repo1.maven.org/maven2/io/gravitee/node/gravitee-node-cluster-plugin-hazelcast/7.26.3/gravitee-node-cluster-plugin-hazelcast-7.26.3.zip](https://repo1.maven.org/maven2/io/gravitee/node/gravitee-node-cluster-plugin-hazelcast/7.26.3/gravitee-node-cluster-plugin-hazelcast-7.26.3.zip)

     cluster:
       type: hazelcast
       hazelcast:
         configPath: /opt/graviteeio-gateway/config/hazelcast.xml

     distributedSync:
       enabled: true
       type: redis
       redis:
         host: redis-stack
         port: 6379

     services:
       sync:
         repository:
           enabled: true
         distributed:
           enabled: true

     extraVolumes: |
       - name: hazelcast-config
         configMap:
           name: hazelcast-config
     extraVolumeMounts: |
       - name: hazelcast-config
         mountPath: /opt/graviteeio-gateway/config/hazelcast.xml
         subPath: hazelcast.xml
   </code></pre>

## Verification&#x20;

After the `helm upgrade --install ... --wait` command completes, complete the following steps to verify the Gateway cluster sync with Redis:

1. Ensure that both API Gateway pods are `Running` and `Ready` using `kubectl -n gravitee-apim get pods -l app.kubernetes.io/component=gateway`. With distributed sync enabled, the default Helm `startupProbe` queries `/_node/health?probes=http-server,sync-process`.
2. Ensure that the Hazelcast cluster has two members. Exec into either pod, and then grep the log with the following command:

   ```bash
   kubectl -n gravitee-apim logs <pod> -c gravitee-apim-gateway | grep "MembershipEvent"
   ```

   You see `members=[Member [10.x.x.x]:5701 …, Member [10.y.y.y]:5701 …]`.
3. Ensure that the Redis repository is loaded with the `DISTRIBUTED_SYNC` scope. Here is an example output:

   ```
   INFO  i.g.p.r.i.RepositoryPluginHandler - Repository [DISTRIBUTED_SYNC] loaded by redis
   ```
4. Ensure that the Distributed sync writes to Redis for the primary node only using the following commands:

   ```bash
   kubectl -n gravitee-apim exec deploy/redis-stack -- redis-cli FT._LIST
   # Expect: distributed-event-search-idx-v2 (cluster-scoped index)

   kubectl -n gravitee-apim exec deploy/redis-stack -- redis-cli KEYS 'distributed_sync_state:*'
   kubectl -n gravitee-apim exec deploy/redis-stack -- redis-cli KEYS 'distributed_event:*' | head
   # Expect cluster-scoped prefixes, e.g. distributed_event:my-gw-external:...
   ```

   With multiple sharding-tag releases on shared Redis, you should see **one `distributed_sync_state:<clusterId>` per release**, each with a distinct cluster ID.
5. Ensure that All probes return `200` with the following command:

   ```bash
   kubectl -n gravitee-apim exec <pod> -c gravitee-apim-gateway -- \
     curl -s "http://admin:<password>@127.0.0.1:18082/_node/health?probes=http-server,sync-process"
   # Expect: {"sync-process":{"healthy":true},"http-server":{"healthy":true}}
   ```


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://documentation.gravitee.io/apim/4.10/configure-and-manage-the-platform/gravitee-gateway/gateway-cluster-sync-with-redis/gateway-cluster-sync-with-redis-using-kubernetes-helm.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
