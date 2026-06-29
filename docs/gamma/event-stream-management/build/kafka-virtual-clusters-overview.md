---
hidden: false
noIndex: true
---
<-- to be published -->
# Virtual Clusters overview

A Virtual Cluster federates multiple independent Kafka backends into a single unified cluster endpoint. Client applications connect to one address and interact with topics spread across any number of underlying Registered Clusters — without needing to know which backend owns which topic.

{% hint style="info" %}
For a guided walkthrough, see [Establish a Virtual Cluster](establish-a-virtual-cluster.md).
{% endhint %}

## What it is

A Virtual Cluster (Mesh mode) presents N backend Kafka clusters as one. You define which Registered Clusters make up the Virtual Cluster, and the Event Gateway handles routing, metadata merging, and consumer group coordination transparently.

A Virtual Cluster requires at least one backend; adding two or more federates them into a Kafka Mesh. To govern a single Kafka cluster without federation, you can instead use a Kafka Service backed directly by a Registered Cluster.

## Why use a Virtual Cluster

| Problem | How a Virtual Cluster helps |
|:--------|:----------------------------|
| Clients need separate connections per Kafka cluster | One endpoint covers all backends |
| Consumer groups can't span multiple clusters natively | The Event Gateway coordinates cross-cluster consumer groups |
| Topic ownership is spread across clusters | Clients query all backends through a single metadata view |
| Governance overhead multiplies with cluster count | One Kafka Service with one security plan covers the entire Virtual Cluster |

## Key concepts

### Registered Cluster

A reusable connection profile for a real Kafka backend. Each Registered Cluster stores the bootstrap server addresses and security configuration (PLAINTEXT, SSL, SASL\_PLAINTEXT, or SASL\_SSL) for one or more named connections. Multiple Kafka Services and Virtual Clusters can reference the same Registered Cluster — updates to the cluster propagate automatically.

### Virtual Cluster (Mesh mode)

A configuration object that groups two or more Registered Clusters into one logical cluster. The Event Gateway merges topic metadata from all backends into a single view and routes produce, consume, and admin requests to the backend that owns each topic.

### Cluster lifecycle states

| State | Description |
|:------|:------------|
| `UNDEPLOYED` | The Virtual Cluster exists but is not active on the Event Gateway |
| `DEPLOYED` | The Virtual Cluster is active and serving traffic |
| `PENDING` | The configuration has changed but not yet been redeployed |

Deploy or undeploy a Virtual Cluster using the row actions on the **Virtual Clusters** list in the Gamma console.

## Limitations

* **ACL management** — ACL operations are not supported on a Virtual Cluster. Manage ACLs directly on each backend Registered Cluster.
* **Kafka transactions** — Transactional producers are not supported on Virtual Clusters.
* **Topic name collisions** — If two backends have a topic with the same name, the Event Gateway routes requests to the first backend in configuration order. Keep topic namespaces distinct across backends to avoid ambiguity.
* **Cooperative-sticky assignor** — Not supported for cross-cluster consumer groups.

## Next steps

* [Establish a Virtual Cluster](establish-a-virtual-cluster.md) — Create and configure a Virtual Cluster in the Gamma console.
* [Create a Kafka service with a Virtual Cluster](create-a-kafka-service-with-a-virtual-cluster.md) — Add a governance layer on top of your Virtual Cluster.
