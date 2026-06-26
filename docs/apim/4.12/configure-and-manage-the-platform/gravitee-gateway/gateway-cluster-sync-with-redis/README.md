# Gateway Cluster sync with Redis

## Gateway Cluster sync with Redis

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td>Gateway Cluster sync with Redis using Docker</td><td><a href="gateway-cluster-sync-with-redis-using-docker.md">gateway-cluster-sync-with-redis-using-docker.md</a></td></tr><tr><td>Gateway Cluster sync with Redis using Kubernetes (Helm)</td><td><a href="gateway-cluster-sync-with-redis-using-kubernetes-helm.md">gateway-cluster-sync-with-redis-using-kubernetes-helm.md</a></td></tr></tbody></table>

### Overview

#### What is Gateway Cluster sync with Redis?

This guide explains how to enable and configure the Gateway Cluster sync with Redis.

The Gateway Cluster sync uses Redis to synchronize the state of APIs, API Keys, Subscriptions, Dictionaries, and Organizations across your API Gateways. This process maintains the state in memory, which ensures that API Gateways remain resilient and high-performing, even if the main repository is down.

#### What issue does it solve?

The Gateway Cluster sync improves both scalability and resilience.

**Scalability**: Without the Gateway Cluster sync, each API Gateway must directly call the repository for synchronization. This configuration is not scalable because adding more API Gateways increases the repository load and slows the bootstrap time for each API Gateway. The Gateway Cluster sync solves this issue by using a primary node to manage the state, which significantly reduces the load.

**Resilience & High Availability**: By maintaining the state in Redis, new API Gateway instances can start and serve API traffic even if the central management repository or control plane is down. This ensures that you do not risk API outages during database maintenance or network disruptions.

#### How does it work?

The new repository scope, `Distributed Sync`, is responsible for keeping the sync state for a cluster.

In the repository, the primary node stores information regarding the current synchronization state and what is currently deployed.

This allows another node to take over if the current primary node goes down without doing a full sync again.

When you enable the Gateway Cluster sync on your API Gateways, the primary node fetches the API definitions from the management repository, and then stores them in the Redis distributed sync repository. The other API Gateways read the API definitions from the Redis distributed sync repository.

#### Distributed Synchronization State

The Synchronization State tracks the current sync process. It contains the following information:

* Cluster ID.
* Node version.
* Node ID.
* Last successful synchronization timeframe.

#### Distributed Synchronization Event

The objects are used to know what needs to be deployed or undeployed across the cluster. They contain the following information:

* `id`. This is the identifier of the object.
* `Type`. This includes `API`, `API_KEY`, `SUBSCRIPTION`, `DICTIONARY`, `ORGANIZATION`, and `LICENSE`.
* `SyncAction`. This is `DEPLOY` or `UNDEPLOY`.
* `Payload`. This is the object to deploy or undeploy.
* `UpdatedAt`. This is the date of the update to allow incremental syncs.

After any business object is deployed, and only if distributed sync is enabled, the primary node stores those objects in the new distributed sync repository.

#### Cluster-scoped Redis (multi sharding-tag deployments)

From APIM 4.12, distributed sync events and sync state in Redis are **scoped by cluster ID**. The cluster ID is the Hazelcast `cluster-name` configured on each gateway deployment.

Use this model when several gateway deployments share one Redis instance—for example, separate Helm releases for `external`, `internal`, and `aog` sharding tags:

* Deploy **one gateway Helm release per sharding-tag cluster**.
* Give each release a **unique Hazelcast `cluster-name`** (runtime cluster ID). With the APIM Helm chart, the default is `<release-name>-<sharding_tags>`; override with `gateway.cluster.hazelcast.clusterName` if needed.
* All releases may use the **same Redis** host; keys are isolated by cluster ID.

Redis key layout:

| Key pattern | Purpose |
|:------------|:--------|
| `distributed_sync_state:<clusterId>` | Last successful sync timeframe for that cluster |
| `distributed_event:<clusterId>:<type>:<id>` | Deploy/undeploy events for that cluster |

If `sharding_tags` or `cluster-name` change, a **new** cluster ID is used. Delete stale `distributed_event:*` and `distributed_sync_state:*` keys for the old cluster ID in Redis.

{% hint style="warning" %}
**Deployment constraints:** The primary gateway must populate Redis before secondaries rely on it. On **fresh install**, start with one gateway replica, wait for sync, then scale up one replica at a time. On **upgrade**, use `maxUnavailable: 0` and `maxSurge: 1`. If autoscaling is enabled, throttle scale-up so new pods join one at a time. See the [Helm guide](gateway-cluster-sync-with-redis-using-kubernetes-helm.md#deployment-constraints) for details.
{% endhint %}

#### Upgrade from pre-cluster-scoped Redis keys

Upgrading to a version with cluster-scoped keys changes the Redis key format. New gateway pods do not read legacy global keys (`distributed_event:API:...`). During rolling upgrade, the primary repopulates Redis from the management repository into the new cluster-scoped format. **Cluster name and sharding tags do not need to change** for a routine version upgrade—only the Redis encoding changes once.

Future version upgrades (for example, 4.12 to 4.13) reuse the same cluster ID and Redis namespace; sync is incremental, not a full reload from the database.

***

## Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://documentation.gravitee.io/apim/4.10/configure-and-manage-the-platform/gravitee-gateway/gateway-cluster-sync-with-redis.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language. The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
