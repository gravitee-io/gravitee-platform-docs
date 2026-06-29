---
hidden: false
noIndex: false
---
# Register your Kafka clusters


Registering a Kafka cluster with Gamma makes it available to Event Stream Management. Once registered, the cluster can be governed through the Event Gateway, used as the foundation for Kafka services and virtual clusters, and monitored from the Gamma console.

## Why register a cluster

Gamma does not host Kafka clusters — it governs them. Registration connects Gamma to your existing Kafka infrastructure so that:

* **Kafka Services** can be created on top of the cluster, adding security plans, policies, and access controls
* **Virtual Clusters** can be provisioned for multi-tenant isolation
* **Explorer** can connect to browse topics, inspect messages, and manage operations
* **Kafka APIs** from the cluster can be exposed as **Kafka API Tools** in the Catalog, bridging event streams to the AI agent layer

## Prerequisites

* Access to a running Gamma console instance
* A Kafka cluster accessible from the Gamma platform
* Kafka cluster connection details: bootstrap server addresses, authentication credentials (if applicable), and TLS certificates (if applicable)

## Register a cluster

1. From the Gamma console sidebar, select **Event Stream Management**.
2. Navigate to **Clusters**.
3. Select **Create cluster**.
4. In the **Identity** step, provide a recognizable name and optional description for the cluster.
5. In the **Configuration** step, enter the cluster connection details. The exact fields available are driven by the connection schema, but generally include:

| Field                 | Description                                                        |
| --------------------- | ------------------------------------------------------------------ |
| **Bootstrap servers** | One or more Kafka broker addresses in `host:port` format.          |
| **Authentication**    | The authentication method for connecting to the cluster.           |
| **TLS**               | TLS/SSL configuration for encrypted connections.                   |

6. Proceed to the **Review** step to confirm the configuration.
7. Select **Create cluster**.

The Registered Cluster appears in the cluster list and becomes available for Kafka Service creation and Virtual Cluster composition.

## Manage registered clusters

After registration, you can view and update cluster details from the Clusters page. Select a registered cluster to open its overview and navigate its detail views to:

* View connection status and health
* Update connection credentials or bootstrap servers
* Undeploy the cluster to suspend its connection
* Delete the cluster registration

{% hint style="warning" %}
Removing a cluster registration does not affect the cluster itself — it only removes Gamma's connection to it. Any Kafka Services or Virtual Clusters built on top of the cluster will lose their underlying connection.
{% endhint %}

<!-- Source: ClustersPage.tsx and CreateClusterWizard.tsx — gravitee-gamma-module-esm -->

## Next steps

* **Create a Kafka Service** — Build a governed Kafka Service on top of your Registered Cluster. See [Create a Kafka service with a registered cluster](../build/create-a-kafka-service-with-a-registered-cluster.md).
* **Browse topics in Explorer** — Connect to the cluster and inspect its topics and messages. See [Manage connections](../explorer/manage-connections.md).
