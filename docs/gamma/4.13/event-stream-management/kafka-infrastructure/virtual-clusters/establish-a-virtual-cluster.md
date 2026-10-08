---
hidden: false
noIndex: false
description: Present one or more Kafka backends to clients as one cluster by establishing a Virtual Cluster. Follow the steps to choose a topology, compose the backends, and deploy it.
---

# Establish a Virtual Cluster

A Virtual Cluster presents one or more Kafka backends to clients as a single cluster. Instead of managing separate connections for each team or workload, clients connect to one endpoint and work with topics spread across the backends.

Once deployed, a Virtual Cluster can back a Kafka Service. See [Create a Kafka Service with a Virtual Cluster](../../apis/kafka-services/create-a-kafka-service-with-a-virtual-cluster.md).

{% hint style="info" %}
For a simplified walkthrough, see [Create your first Virtual Cluster](../../get-started/create-your-first-virtual-cluster.md).
{% endhint %}

## Why Virtual Clusters

Managing connections to multiple Kafka clusters adds coordination overhead. Clients must know which cluster owns which topics, and consumer groups that span clusters require custom coordination logic. Virtual Clusters remove that complexity:

* **Unified endpoint**: clients connect once, and the Event Gateway routes each request to the right backend.
* **Consumer groups across backends**: consumers can subscribe to topics on several backends in a single group, without client-side coordination. Such a group must use the `range` or `roundrobin` assignor, or the KIP-848 consumer group protocol. See [Consumer groups](kafka-virtual-cluster-runtime-behavior-reference.md#consumer-groups).
* **Simplified architecture**: topic ownership is defined by the Virtual Cluster, not in client configuration.
* **Centralized governance**: the plans and policies of the Kafka Service cover all backends of the Virtual Cluster.

## Prerequisites

* Access to a running Gamma console instance.
* An environment role that grants the `CLUSTER` **Create** permission, and the `CLUSTER` **Update** permission to deploy the Virtual Cluster.
* At least one deployed Cluster with at least one connection. Each connection can be one backend, so the connections of a single Cluster are enough. See [Register your Kafka clusters](../clusters/register-your-kafka-clusters.md).

## Create a Virtual Cluster

1. From the Gamma console sidebar, select **Event Stream Management**.
2. In the **Kafka Infrastructure** group, select **Virtual Clusters**.
3. Select **Create Virtual Cluster**.

### Choose a topology template

Before the wizard opens, choose a topology template, or start from scratch. The choice only adds a hint above the wizard. Every option runs the same three-step wizard below.

* **Start from scratch**: the full wizard, to name the Virtual Cluster, compose its backends, and review.
* **Single Cluster Proxy**: front one physical Kafka cluster with Gravitee policies. The hint asks for one backend.
* **Kafka Mesh**: federate two or more Kafka clusters into one unified namespace behind a single endpoint. The hint asks for two or more backends.

To read how a Virtual Cluster sits between the Kafka clients and your Clusters, select the ⓘ button next to **Topology templates**. The **What is a Virtual Cluster?** diagram is hidden until you open it.

### Step 1: Identity

Provide details for the Virtual Cluster:

| Field           | Description                                                      |
| --------------- | ---------------------------------------------------------------- |
| **Name**        | Required. A human-readable name for this Virtual Cluster, up to 255 characters. |
| **Description** | Optional. A description of the Virtual Cluster's purpose.        |

Select **Next: Composition**.

### Step 2: Composition

Compose the Virtual Cluster from the connections of your deployed Clusters. You need at least one backend.

1. Select a **Cluster**. Only the deployed Clusters are listed.
2. Select a **Connection** of that Cluster.
3. Select **Add backend**.
4. Repeat for each backend. A connection already added can't be added again.

The order in which you add the backends is the configuration order. When two backends hold a topic with the same name, the first one wins. With two or more backends, the step shows the **Kafka Mesh** badge.

When no Cluster is deployed, the step shows **No deployed Clusters**. Deploy a Cluster first, then come back to the wizard.

Select **Next: Review**.

<figure><img src="../../.gitbook/assets/gamma-esm-virtual-cluster-composition.png" alt="The Composition step of the Virtual Cluster wizard started from the Kafka Mesh template, with two backends added and the Kafka Mesh badge"><figcaption><p>Two backends composed into one Virtual Cluster</p></figcaption></figure>

### Step 3: Review

1. Review the Virtual Cluster details and the composed backends.
2. Select **Create Virtual Cluster**.

The console confirms with **Cluster created** and opens the **Overview** page of the Virtual Cluster. A new Virtual Cluster is **Undeployed**.

## Deploy the Virtual Cluster

A Kafka Service can bind only to a deployed Virtual Cluster.

1. On any page of the Virtual Cluster, select **Deploy** above the page. Alternatively, open the row menu (**⋯**) of the Virtual Cluster in the **Virtual Clusters** list, and select **Deploy**.

The console confirms with **Cluster deployed**, and the status changes to **Deployed**.

## Verification

To verify that the Virtual Cluster is ready, follow these steps:

1. In the **Kafka Infrastructure** group, select **Virtual Clusters**.
2. Check that the row of your Virtual Cluster shows the **Deployed** status, and the number of backends in the **Connections/Backends** column.

## Next steps

* **Create a Kafka Service**: add plans and policies on top of the Virtual Cluster. See [Create a Kafka Service with a Virtual Cluster](../../apis/kafka-services/create-a-kafka-service-with-a-virtual-cluster.md).
* **Manage the Virtual Cluster**: change its backends, deploy your changes, and see which Kafka Services use it. See [Manage a Virtual Cluster](manage-a-virtual-cluster.md).
* **Check the DNS setup**: the gateway rewrites the broker IDs of the backends. See [Virtual Cluster broker addressing](https://documentation.gravitee.io/apim/4.13/kafka-gateway/virtual-cluster-broker-addressing).
