---
hidden: false
noIndex: false
description: Register your first Kafka cluster in the Gamma console and add its first connection. Follow the quickstart to create and deploy the cluster.
---
# Register your first cluster

This quickstart walks you through registering your first Kafka cluster in the Gamma console, adding its first connection, and deploying it. Kafka Services can bind to a deployed cluster, and Virtual Clusters are composed from the connections of deployed clusters.

Gamma does not host Kafka clusters. It governs them. A registered cluster is a reusable **Multi-connection** profile: it holds one or more named **connections**, each pointing at a Kafka backend with its own bootstrap servers and security settings.

{% hint style="info" %}
For a complete reference on registering and managing clusters, see [Register your Kafka clusters](../kafka-infrastructure/clusters/register-your-kafka-clusters.md).
{% endhint %}

## Prerequisites

* Access to a running Gamma console instance, with an environment role that can create and update clusters
* A running Kafka cluster reachable from the Gamma platform
* The cluster's connection details: bootstrap server addresses and, if applicable, SASL credentials and TLS certificates

## Step 1: Open the cluster wizard

1. From the Gamma console sidebar, select **Event Stream Management**.
2. In the **Kafka Infrastructure** group of the sidebar, select **Clusters**.
3. Select **Create Cluster**.

You can also select **Create Cluster** on the **Clusters** card of the [Overview page](../general/use-the-overview-page.md).

The console opens the cluster creation wizard, with the steps **Identity**, **Configuration**, and **Review**.

## Step 2: Identity

| Field           | Value                | Notes                                                        |
| --------------- | -------------------- | ------------------------------------------------------------ |
| **Name**        | `My First Cluster`   | Required. A recognizable name (max 255 characters).          |
| **Description** | Leave blank          | Optional. Explain what this cluster is used for.             |

Select **Next: Configuration**.

## Step 3: Configuration: add your first connection

The Configuration step is a form that the Management API serves. A cluster needs at least one connection.

1. In the **Kafka Cluster Connections** list, add an entry.
2. Complete the following fields:

| Field                 | Description                                                                                                                              |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **Connection name**   | Required. A name that identifies this connection.                                                                                        |
| **Cross ID**          | Optional. A portable identifier for cross-environment references. Gamma generates one from the connection name if you leave this empty. |
| **Bootstrap servers** | Required. The Kafka bootstrap server address, in `host:port` format.                                                                     |
| **Security protocol** | Required. One of `PLAINTEXT`, `SASL_PLAINTEXT`, `SASL_SSL`, or `SSL`. Defaults to `PLAINTEXT`.                                           |

When you pick `SASL_PLAINTEXT` or `SASL_SSL`, the form adds a **SASL Configuration** section. When you pick `SSL` or `SASL_SSL`, it adds the SSL settings.

A Multi-connection cluster can hold several connections. You can add more later from **Configuration** in the cluster's sidebar.

3. Select **Next: Review**.

## Step 4: Review and create

1. Review the identity and configuration. Secret values are masked.
2. Select **Create Cluster**.

The console creates the cluster and opens its overview page. A newly created cluster is **Undeployed**.

## Step 5: Deploy your cluster

A cluster must be deployed before Kafka Services can bind to it or Virtual Clusters can use its connections.

1. At the top of the cluster's page, select **Deploy**.

When the cluster's status reads **Deployed**, it is available to Kafka Services and Virtual Clusters.

You can also deploy from the **Clusters** list: open the row menu (**⋯**) of the cluster, and then select **Deploy**.

{% hint style="info" %}
When you edit a deployed cluster, its status becomes **Pending changes**, and the gateway keeps the last deployed configuration. To apply your edits, select **Deploy changes**.
{% endhint %}

## Next steps

* **Create a Kafka Service**. Put a governed endpoint in front of your cluster. See [Create your first Kafka Service](create-your-first-kafka-service.md).
* **Create a Virtual Cluster**. Put this cluster's connections, alone or with the connections of other clusters, behind a single endpoint. See [Create your first Virtual Cluster](create-your-first-virtual-cluster.md).
