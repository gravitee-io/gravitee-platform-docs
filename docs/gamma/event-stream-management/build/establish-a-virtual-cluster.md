---
hidden: false
noIndex: false
---
<-- to be published-->
# Establish a Virtual Cluster
<!-- Source: CreateVirtualClusterPage.tsx — gravitee-gamma-module-esm -->

A Virtual Cluster federates multiple independent Kafka backends into a single unified endpoint. Instead of managing separate cluster connections for each team or workload, a Virtual Cluster lets clients connect to one endpoint and transparently interact with topics spread across multiple underlying Registered Clusters.

Once established, a Virtual Cluster can back a Kafka Service — see [Create a Kafka service with a virtual cluster](create-a-kafka-service-with-a-virtual-cluster.md).

{% hint style="info" %}
For a simplified walkthrough, see [Create your first virtual cluster](../get-started/create-your-first-virtual-cluster.md).
{% endhint %}

## Why Virtual Clusters

Managing connections to multiple Kafka clusters adds coordination overhead — clients must know which cluster owns which topics, and cross-cluster consumer groups require custom coordination logic. Virtual Clusters remove that complexity:

* **Unified endpoint** — Clients connect once; the Event Gateway routes requests to the correct backend automatically
* **Cross-cluster consumer groups** — Consumers can subscribe to topics across backends in a single group without client-side coordination
* **Simplified architecture** — Topic ownership is defined at the Virtual Cluster level, not in client configuration
* **Centralized governance** — Security plans and policies applied to the Kafka Service cover all backends in the Virtual Cluster

## Prerequisites

* Access to a running Gamma console instance
* At least two Registered Clusters (see [Register your Kafka clusters](../import/register-your-kafka-clusters.md))

## Create a Virtual Cluster

1. From the Gamma console sidebar, select **Event Stream Management**.
2. Navigate to **Virtual Clusters**.
3. Select **Create virtual cluster**.

### Choose a topology template

Before the wizard opens, choose a topology template, or start from scratch. The choice only tailors the on-screen guidance — every option runs the same three-step wizard below.

* **Single Cluster Proxy**: Front one physical Kafka cluster with Gravitee policies.
* **Mesh Federation**: Federate two or more Kafka clusters into one unified namespace behind a single endpoint.
* **Start from scratch**: Full wizard to name the virtual cluster, compose its backends, and review.

### Step 1: Identity

Provide details for the Virtual Cluster:

| Field           | Description                                                      |
| --------------- | ---------------------------------------------------------------- |
| **Name**        | Required. A human-readable name for this Virtual Cluster.        |
| **Description** | Optional. A description of the Virtual Cluster's purpose.        |

Select **Next** to proceed.

### Step 2: Composition

Compose the Virtual Cluster by adding backends from already-deployed clusters. You must select at least one backend.

1. Select a **Cluster**.
2. Select a **Connection** associated with that cluster.
3. Select **Add backend**.

If you add two or more backends, they form a **Kafka Mesh**.

Select **Next** to proceed.

### Step 3: Review

1. Review the Virtual Cluster details and composed backends.
2. Select **Create virtual cluster**.

After creation, you are navigated to the Virtual Cluster's overview page.

## Manage Virtual Clusters

Virtual Clusters appear alongside standard managed clusters in the **Clusters** view. Once created, you can navigate to the Virtual Cluster's **Configuration** tab to view its composed backends in the Backends Table. Virtual Clusters act as routing abstractions and do not manage the lifecycle of the underlying topics.

{% hint style="warning" %}
Removing a backend from a deployed Virtual Cluster affects any clients consuming topics on that backend. Confirm the impact before making changes in production.
{% endhint %}

## Next steps

* **Create topics** — Set up Kafka topics inside your Virtual Cluster.
* **Create a Kafka Service** — Add governance, security plans, and policies on top of the Virtual Cluster. See [Create a Kafka service with a virtual cluster](create-a-kafka-service-with-a-virtual-cluster.md).
