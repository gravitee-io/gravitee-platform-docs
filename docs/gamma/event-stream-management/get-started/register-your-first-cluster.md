---
hidden: false
noIndex: true
---
<-- to be published -->
# Register your first cluster
<!-- Source: gravitee-gamma-module-esm/src/main/ui/features/clusters/components/create/CreateClusterWizard.tsx -->

This quickstart walks you through registering your first Kafka cluster in the Gamma console and adding its first connection. Registering a cluster is the foundational first step — Kafka Services and Virtual Clusters are built on top of registered clusters.

Gamma does not host Kafka clusters; it governs them. A registered cluster is a reusable **Multi-connection** profile: it holds one or more named **connections**, each pointing at a Kafka backend with its own bootstrap servers and security settings.

{% hint style="info" %}
For a complete reference on registering and managing clusters, see [Register your Kafka clusters](../import/register-your-kafka-clusters.md).
{% endhint %}

## Prerequisites

* Access to a running Gamma console instance
* A running Kafka cluster reachable from the Gamma platform
* The cluster's connection details: bootstrap server addresses, and — if applicable — authentication credentials and TLS certificates

## Step 1: Open the cluster wizard

1. From the Gamma console sidebar, select **Event Stream Management**.
2. Navigate to **Clusters**.
3. Select **Create cluster**.

The console opens the cluster creation wizard.

## Step 2: Identity

| Field           | Value                | Notes                                                        |
| --------------- | -------------------- | ------------------------------------------------------------ |
| **Name**        | `My First Cluster`   | Required. A recognizable name (max 255 characters).          |
| **Description** | Leave blank          | Optional. Explain what this cluster is used for.             |

Select **Next** to proceed.

## Step 3: Configuration — add your first connection

The Configuration step is driven by the connection schema, so the exact fields depend on your platform. To add the cluster's first connection, you generally provide:

| Field                 | Description                                                          |
| --------------------- | ------------------------------------------------------------------- |
| **Connection name**   | A recognizable name for this connection.                            |
| **Bootstrap servers** | One or more Kafka broker addresses in `host:port` format.           |
| **Authentication**    | The authentication method for connecting to the cluster (if any).   |
| **TLS**               | TLS/SSL configuration for encrypted connections (if any).           |

A Multi-connection cluster can hold several connections; you can add more later from the cluster's **Configuration** tab. Select **Next** to proceed.

## Step 4: Review and create

1. Review the identity and configuration. Secret values are masked.
2. Select **Create cluster**.

The console creates the cluster and redirects you to its overview page. A newly created cluster starts in the **Undeployed** state.

## Step 5: Deploy your cluster

A cluster must be deployed before Kafka Services or Virtual Clusters can use it.

1. Go to the **Clusters** list.
2. On your cluster's row, select **Deploy**.

When the cluster reaches the **Deployed** state, it is available as a backend.

## Next steps

* **Create a Kafka Service** — Put a governed endpoint in front of your cluster. See [Create your first Kafka service](create-your-first-kafka-service.md).
* **Create a Virtual Cluster** — Federate this cluster's connections with others behind a single endpoint. See [Create your first virtual cluster](create-your-first-virtual-cluster.md).
