---
hidden: false
noIndex: true
---
# Create your first Virtual Cluster


This quickstart walks you through creating a Virtual Cluster that federates two Registered Clusters into a single unified endpoint. Clients connecting to the Virtual Cluster can access topics from both backends without needing separate connections.

{% hint style="info" %}
For a complete reference on all Virtual Cluster options, see [Establish a Virtual Cluster](../build/establish-a-virtual-cluster.md).
{% endhint %}

## Prerequisites

* Access to a running Gamma console instance
* At least two Registered Clusters (see [Register your Kafka clusters](../import/register-your-kafka-clusters.md))

## Step 1: Open the Virtual Cluster wizard

1. From the Gamma console sidebar, select **Event Stream Management**.
2. Navigate to **Virtual Clusters**.
3. Select **Create virtual cluster**.

## Step 2: Choose a topology

Select **Mesh Federation**.

This topology federates two or more Kafka clusters into one unified namespace behind a single endpoint.

## Step 3: Enter cluster details

| Field       | Value                          | Notes                                                   |
| ----------- | ------------------------------ | ------------------------------------------------------- |
| **Name**    | `My First Virtual Cluster`     | Required. Identifies the Virtual Cluster in the console. |

Select **Next** to proceed.

## Step 4: Compose backends

1. Under the **Cluster** dropdown, select your first deployed cluster.
2. Under the **Connection** dropdown, select a connection.
3. Select **Add backend**.
4. Repeat this process for a second deployed cluster to form a Kafka Mesh.

Once you have added at least two backends, select **Next**.

## Step 5: Review and create

1. Review the Virtual Cluster details and composed backends.
2. Select **Create virtual cluster**.

After creation, you are navigated to the Virtual Cluster's overview page, where it can be managed and monitored.

## Next steps

* **Add a Kafka Service** — Apply security plans and policies on top of the Virtual Cluster. See [Establish a Virtual Cluster](../build/establish-a-virtual-cluster.md).

<!-- Source: CreateVirtualClusterPage.tsx — gravitee-gamma-module-esm -->
