---
hidden: false
noIndex: false
---
<--- to be published --->

# Create a Kafka service with a Virtual Cluster
<!-- GAP-STRUCTURAL: Missing procedural content source -->

A Kafka Service backed by a Virtual Cluster lets you govern access to a federated multi-cluster Kafka environment through a single endpoint. The Virtual Cluster fans out requests across its backend Registered Clusters, while the Kafka Service adds the governance layer — security plans, policies, and observability — on top of that unified endpoint.

Use this approach when you want clients to interact with topics spread across multiple Kafka backends without managing separate connections, or when you need centralized access control over a federated cluster topology.

{% hint style="info" %}
To create a Kafka Service directly on a single Registered Cluster instead, see [Create a Kafka service with a registered cluster](create-a-kafka-service-with-a-registered-cluster.md).
{% endhint %}

## How it works

When you create a Kafka Service backed by a Virtual Cluster, the Event Gateway intercepts client requests at the Kafka Service endpoint and routes them to the appropriate backend cluster within the Virtual Cluster. Clients see a single Kafka endpoint; the Event Gateway resolves which backend owns each topic and fans out operations accordingly.

A single Virtual Cluster can host multiple Kafka Services, each with its own security plan and access controls.

## Prerequisites

* Access to a running Gamma console instance
* At least two Registered Clusters (see [Register your Kafka clusters](../import/register-your-kafka-clusters.md))
* A Virtual Cluster federating those clusters (see [Establish a Virtual Cluster](establish-a-virtual-cluster.md))

## Create a Kafka service with a Virtual Cluster

1. From the Gamma console sidebar, select **Event Stream Management**.
2. Navigate to **Kafka Services**.
3. Select **Create Kafka Service**.

The console opens the Kafka Service creation wizard. Binding the service to a Virtual Cluster is done in the **Endpoint** step.

### 1. Identity

| Field            | Description                                                                          |
| ---------------- | ------------------------------------------------------------------------------------ |
| **Name**         | A human-readable name that identifies this Kafka Service in the console and Catalog. |
| **Version**      | The version of this service (e.g., 1.0).                                             |
| **Description**  | Optional. A description of the service's purpose.                                    |

### 2. Listener

Enter a **Host prefix** — a single DNS label (lowercase letters, digits, and hyphens; max 63 characters). The Event Gateway appends its configured domain, and clients connect on the gateway's SNI port.

### 3. Endpoint

Select the **Virtual Cluster** binding mode, then choose the Virtual Cluster this service routes through. Requests are fanned out across the Virtual Cluster's federated backends.

### 4. Review and create

1. Review the identity, listener, and endpoint binding.
2. Select **Create Kafka Service**.

The console creates the Kafka Service and registers it with the Event Gateway. The service is backed by the selected Virtual Cluster and its federated backends.

After creation, configure a security plan and, optionally, policies on the service's overview page to control how consumers and producers authenticate and to apply fine-grained governance.

## Expose as a Kafka API Tool

Once the Kafka Service is running, you can expose its topics as **Kafka API Tools** in the Catalog, bridging your event infrastructure to the AI agent layer. Kafka API Tools become available as building blocks in MCP Studio alongside other tools, resources, and prompts.

## Next steps

* **Create topics** — Set up Kafka topics across the Virtual Cluster's backends.
* **Monitor your service** — View the service in Explorer.
