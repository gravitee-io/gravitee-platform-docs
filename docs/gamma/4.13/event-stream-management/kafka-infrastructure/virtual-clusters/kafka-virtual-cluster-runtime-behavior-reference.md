---
hidden: false
noIndex: false
description: What a Virtual Cluster does on the Event Gateway, from lifecycle rules to topic routing, consumer groups, producers, and refused operations. Browse the full reference.
---
# Virtual Cluster runtime behavior

This page describes what happens when a Virtual Cluster is active on the Event Gateway: how the console and the Management API guard its lifecycle, how the gateway routes client requests across the backends, and which Kafka features it refuses.

The Event Gateway applies the same routing to every Virtual Cluster, whatever its number of backends. The console calls a Virtual Cluster with two or more backends a **Kafka Mesh**, but a Virtual Cluster with one backend follows the rules on this page too.

## Lifecycle

A Virtual Cluster moves through three states:

| Status | Description |
|:------|:------------|
| **Undeployed** | The Virtual Cluster configuration exists but the gateway doesn't run it. A new Virtual Cluster starts in this state. |
| **Deployed** | The gateway routes requests to the backends and merges their responses. |
| **Pending changes** | The configuration was saved after the last deployment. The gateway keeps running the previously deployed configuration until you select **Deploy changes**. |

The lifecycle actions are above every page of the Virtual Cluster, and in the row menu of the **Virtual Clusters** list: **Deploy** from **Undeployed**, **Deploy changes** and **Undeploy** from **Pending changes**, and **Undeploy** from **Deployed**. **Undeploy** asks for confirmation in the **Undeploy Cluster?** dialog. See [Manage a Virtual Cluster](manage-a-virtual-cluster.md).

The Management API enforces the following rules between a Virtual Cluster and the Kafka Services bound to it:

* **A Virtual Cluster needs a backend to deploy.** Deploying a Virtual Cluster with no backend is refused. The console disables **Deploy** and explains **A Virtual Cluster needs at least one backend before it can be deployed.**
* **A Kafka Service starts only on a live Virtual Cluster.** A Kafka Service bound to a Virtual Cluster can be started or deployed only while the Virtual Cluster is **Deployed** or has **Pending changes**.
* **A Virtual Cluster with a started Kafka Service can't be undeployed.** Stop every Kafka Service bound to it first. The **Undeploy Cluster?** dialog lists the started Kafka Services that block the undeployment.
* **Removing every backend doesn't undeploy the Virtual Cluster.** Saving a deployed Virtual Cluster with no backend moves it to **Pending changes**. The gateway keeps serving the previously deployed backends, and the Virtual Cluster can't be deployed again until it has a backend.
* **Changes to a backend Cluster reach the Virtual Cluster when you deploy them.** When you deploy changes to a Cluster used as a backend, the gateway rebuilds the Virtual Clusters that use it.

## Broker addressing

The gateway merges the brokers of all backends into one cluster identity, and rewrites their broker IDs so that they stay unique. The IDs that clients see aren't the IDs configured on your brokers, which affects the DNS entries that you need. See [Virtual Cluster broker addressing](https://documentation.gravitee.io/apim/4.13/kafka-gateway/virtual-cluster-broker-addressing).

## Topic routing

When a client requests metadata or sends produce and consume requests, the Event Gateway does the following:

1. Fetches the metadata of every backend in the Virtual Cluster.
2. Merges the topic lists into a single view, and removes the internal topics, whose names start with `__`.
3. Routes each request to the backend that owns the topic.

When two backends hold a topic with the same name, only the topic of the first backend in configuration order appears in the merged metadata. The other backend's topic is hidden from clients that look it up by name. A request that names the topic by its topic ID still reaches the right backend. Keep topic names distinct across backends to avoid ambiguity.

## Consumer groups

A consumer group whose topics live on several backends is served through one shadow group per backend, named `<group>__shadow-c<N>`, where `<N>` is the position of the backend in the configuration, starting at `0`. Clients see a single consumer group. On the backends, the shadow groups appear under their own names. A static member becomes `<instance>__shadow-c<N>` on each backend.

The gateway computes the partition assignment of these groups itself, which limits the assignors:

| Group protocol | Supported across backends |
|:------|:------------|
| Classic, `range` or `roundrobin` assignor | Yes. |
| Classic, `sticky`, `cooperative-sticky`, or a custom assignor | No. The join is refused with `INCONSISTENT_GROUP_PROTOCOL`. |
| Consumer group protocol of KIP-848 (`group.protocol=consumer`) | Yes. |

A group ID that matches the shadow group pattern, such as `orders__shadow-c0`, is reserved and refused with `INVALID_GROUP_ID`.

## Producers

* **Idempotent producers.** When a producer initializes, the gateway allocates a producer ID on every backend and gives the client one virtual producer ID. On each produce request, it replaces the virtual ID with the backend's own. An idempotent producer can therefore write to topics on several backends.
* **Transactional producers.** A transaction is pinned to one backend, chosen from the first topic that the transaction adds. A transaction that names topics on more than one backend is refused with `INVALID_TXN_STATE`, and the client aborts it before any data is written. For an exactly-once read-process-write pipeline, the coordinator of the input consumer group and the output topics must be on the same backend.

The gateway keeps the mapping between virtual and real producer IDs in its cache. When the gateway loses a mapping, for example after a restart with a local cache, or when the producer reconnects to another gateway instance, the next produce request fails with `PRODUCER_FENCED`. This error is fatal for a Kafka producer, so the application must create a new producer. In a deployment with several gateway instances, configure a distributed cache, Hazelcast or Redis, for the gateway.

## Refused operations

| Operation | Behavior |
|:------|:------------|
| ACL operations (create, describe, delete) | Refused with `SECURITY_DISABLED`. Manage ACLs directly on each backend cluster. |
| KIP-932 share groups | Not available. The gateway removes `SHARE_GROUP_HEARTBEAT` from its supported API versions. |
| `DescribeTopicPartitions` (KIP-966) | Not advertised. Clients that support it describe topics with `Metadata` requests instead, which the gateway merges across backends. |

## Next steps

* [Create a Kafka Service with a Virtual Cluster](../../apis/kafka-services/create-a-kafka-service-with-a-virtual-cluster.md). Expose a deployed Virtual Cluster to clients, with plans and policies.
* [Manage a Virtual Cluster](manage-a-virtual-cluster.md). Change the backends of a Virtual Cluster and deploy your changes.
