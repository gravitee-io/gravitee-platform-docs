---
hidden: false
noIndex: false
description: Register an existing Kafka cluster with Gamma so Kafka Services and Virtual Clusters can be built on it. Follow the steps to register and deploy one.
---

# Register your Kafka clusters

When you register a Kafka cluster with Gamma, it becomes available to Event Stream Management. Once registered and deployed, the cluster can be governed through the Event Gateway, used as the foundation for Kafka Services and Virtual Clusters, and monitored from the Gamma console.

## Why register a cluster

Gamma does not host Kafka clusters—it governs them. Registration connects Gamma to your existing Kafka infrastructure to enable the following:

* **Kafka Services** can be created on top of the cluster, adding security plans, policies, and access controls
* **Virtual Clusters** can be provisioned for multi-tenant isolation

## Prerequisites

* Access to a running Gamma console instance
* A Kafka cluster accessible from the Gamma platform
* Kafka cluster connection details, including bootstrap server addresses and, where applicable, authentication credentials and TLS certificates

## Register a cluster

1. From the Gamma console sidebar, select **Event Stream Management**.
2. Navigate to **Clusters**.
3. Select **Create cluster**.
4. In the **Identity** step, provide a recognizable name and optional description for the cluster.
5. In the **Configuration** step, select **Add** to add an entry to the **Kafka Cluster Connections** list. Add one entry for each connection you want the cluster to expose, and complete the following fields for each entry:

| Field                 | Description                                                                                                                |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| **Connection name**   | Required. A name that identifies this connection.                                                                            |
| **Cross ID**          | Optional. A portable identifier for cross-environment references. Gamma generates one from the connection name if you leave this empty. |
| **Bootstrap servers** | Required. The Kafka bootstrap server address, in `host:port` format.                                                         |
| **Security protocol** | Required. One of `PLAINTEXT`, `SASL_PLAINTEXT`, `SASL_SSL`, or `SSL`. Defaults to `PLAINTEXT`.                                |

6. Proceed to the **Review** step to confirm the configuration.
7. Select **Create cluster**.
8. On the cluster overview, select **Deploy**.

A new cluster is created with a lifecycle state of **Undeployed** and appears in the cluster list. When you deploy it, its lifecycle state changes to **Deployed**, and it becomes available for Kafka Service creation and Virtual Cluster composition.

## Manage registered clusters

After registration, you can view and update cluster details from the Clusters page. Select a registered cluster to open its overview and navigate its detail views to perform the following tasks:

* View the cluster's lifecycle state, type, and connection count
* Update connection details, including bootstrap servers and security settings, from the **Configuration** view
* Undeploy the cluster to suspend its connection
* Delete the cluster registration

{% hint style="warning" %}
Removing a cluster registration does not affect the cluster itself—it only removes Gamma's connection to it. Any Kafka Services or Virtual Clusters built on top of the cluster will lose their underlying connection.
{% endhint %}

## Next steps

* **Create a Kafka Service**. Build a governed Kafka Service on top of your registered cluster. See [Create a Kafka service with a registered cluster](../build/create-a-kafka-service-with-a-registered-cluster.md).
