---
hidden: false
noIndex: false
description: A Virtual Cluster presents one or more Kafka backends to clients as one cluster. Learn the key concepts, Kafka Mesh, and the limitations that apply.
---
# Virtual Clusters overview

A Virtual Cluster presents one or more Kafka backends to clients as a single Kafka cluster. Client applications connect to one address and work with topics spread across the backends, without knowing which backend owns which topic.

{% hint style="info" %}
For a guided walkthrough, see [Establish a Virtual Cluster](establish-a-virtual-cluster.md).
{% endhint %}

## What it is

You compose a Virtual Cluster from backends. A backend is one connection of a deployed Cluster, so two connections of the same Cluster can be two backends of one Virtual Cluster. The Event Gateway merges the metadata of the backends, routes each request to the backend that owns the topic, and coordinates the consumer groups that span backends.

Clients don't reach a Virtual Cluster on its own. A Kafka Service exposes it, with the **Virtual Cluster** binding mode, and applies its plans and policies to every backend. See [Create a Kafka Service with a Virtual Cluster](../../apis/kafka-services/create-a-kafka-service-with-a-virtual-cluster.md).

A Virtual Cluster needs at least one backend. The console calls a Virtual Cluster with two or more backends a **Kafka Mesh**, and marks it with the **Kafka Mesh** badge. The Event Gateway, however, routes every Virtual Cluster the same way, whatever its number of backends, so the [limitations](#limitations) apply to a Virtual Cluster with a single backend too. To govern a single Kafka cluster without them, bind a Kafka Service directly to a Cluster instead, with the **Managed Cluster** binding mode.

## Why use a Virtual Cluster

| Problem | How a Virtual Cluster helps |
|:--------|:----------------------------|
| Clients need separate connections per Kafka cluster | One endpoint covers all backends |
| Consumer groups can't span multiple clusters natively | The Event Gateway coordinates consumer groups across backends |
| Topic ownership is spread across clusters | Clients query all backends through a single metadata view |
| Governance overhead multiplies with cluster count | One Kafka Service with one set of plans covers the entire Virtual Cluster |

## Key concepts

### Cluster

A reusable connection profile for a real Kafka cluster, registered on the **Clusters** page. Each Cluster stores the bootstrap server addresses and the security configuration of one or more named connections. Multiple Kafka Services and Virtual Clusters can reference the same Cluster. Changes to a Cluster reach the gateway when you deploy them with **Deploy changes**. See [Register your Kafka clusters](../clusters/register-your-kafka-clusters.md).

### Backend

One connection of a deployed Cluster, added to a Virtual Cluster. The order of the backends matters: when two backends hold a topic with the same name, the first one in configuration order wins.

### Virtual Cluster

A configuration object, listed on the **Virtual Clusters** page, that groups one or more backends into one logical cluster. The Event Gateway merges the topic metadata of all backends into a single view, and routes produce, consume, and admin requests to the backend that owns each topic.

### Lifecycle

| Status | Description |
|:------|:------------|
| **Undeployed** | The Virtual Cluster exists but isn't active on the Event Gateway. Kafka Services can't start on it. |
| **Deployed** | The Virtual Cluster is active and serving traffic. |
| **Pending changes** | The Virtual Cluster was edited after its last deployment. The gateway keeps running the previously deployed configuration until you select **Deploy changes**. |

Deploy or undeploy a Virtual Cluster from the actions above its pages, or from the row menu of the **Virtual Clusters** list. See [Manage a Virtual Cluster](manage-a-virtual-cluster.md).

## Limitations

The following limitations apply to every Virtual Cluster. For the full behavior, see [Virtual Cluster runtime behavior reference](kafka-virtual-cluster-runtime-behavior-reference.md).

* **ACL management**: ACL operations are refused with `SECURITY_DISABLED`. Manage ACLs directly on each backend cluster.
* **Transactions**: a transaction must keep all its topics on one backend. A transaction that spans backends is refused with `INVALID_TXN_STATE`.
* **Idempotent producers**: the gateway maps one virtual producer ID to a producer ID on each backend. In a deployment with several gateway instances, configure a distributed cache, or a producer can fail with `PRODUCER_FENCED` after a gateway restart or a reconnection to another instance.
* **Topic name collisions**: when two backends hold a topic with the same name, only the one on the first backend in configuration order appears in the metadata.
* **Consumer group assignors**: a consumer group that spans backends must use the `range` or `roundrobin` assignor, or the consumer group protocol of KIP-848. The sticky assignors, `cooperative-sticky` included, and custom assignors are refused with `INCONSISTENT_GROUP_PROTOCOL`.
* **Share groups**: KIP-932 share groups aren't available.
* **Broker IDs**: the gateway rewrites the broker IDs of the backends, which affects your DNS setup. See [Virtual Cluster broker addressing](https://documentation.gravitee.io/apim/4.13/kafka-gateway/virtual-cluster-broker-addressing).
* **Kafka Explorer**: a Virtual Cluster can't be the **Cluster** target of a Kafka Explorer connection.

## Next steps

* [Establish a Virtual Cluster](establish-a-virtual-cluster.md). Create a Virtual Cluster from the connections of your Clusters.
* [Create a Kafka Service with a Virtual Cluster](../../apis/kafka-services/create-a-kafka-service-with-a-virtual-cluster.md). Expose the Virtual Cluster to clients, with plans and policies.
