---
hidden: false
noIndex: false
description: Register an existing Kafka cluster with Gamma so Kafka Services and Virtual Clusters can be built on it. Follow the steps to register and deploy one.
---

# Register your Kafka clusters

When you register a Kafka cluster with Gamma, it becomes a **Cluster** of Event Stream Management. Once it's deployed, Kafka Services can bind to one of its connections, and Virtual Clusters can use its connections as backends.

## Why register a cluster

Gamma doesn't host Kafka clusters. It governs them. A Cluster stores the connection details of an existing Kafka cluster once, so that the following objects can reuse them:

* **Kafka Services**, which add plans, policies, and access control on top of one of the Cluster's connections. In the Kafka Service wizard, this binding mode is called **Managed Cluster**.
* **Virtual Clusters**, which present one or more connections of your Clusters to clients as a single Kafka cluster.
* **Kafka Explorer connections**, which read the brokers, topics, consumer groups, and messages of a Cluster. Kafka Explorer doesn't need the Cluster to be deployed.

## Prerequisites

* Access to a running Gamma console instance.
* An environment role that grants the `CLUSTER` **Create** permission. The **Create Cluster** button appears only when you have it. The built-in **API_PUBLISHER** role only reads Clusters.
* A Kafka cluster that the Event Gateway can reach. To read it with Kafka Explorer, the Management API must reach it too.
* The connection details of the Kafka cluster: the bootstrap server addresses and, where applicable, the authentication credentials and the TLS stores.

## Register a cluster

1. From the Gamma console sidebar, select **Event Stream Management**.
2. In the **Kafka Infrastructure** group, select **Clusters**.
3. Select **Create Cluster**.
4. In the **Identity** step, enter a **Name** and an optional **Description**. The name is required and accepts up to 255 characters.
5. Select **Next: Configuration**.
6. In the **Configuration** step, select **Add** to add an entry to the **Kafka Cluster Connections** list. Add one entry for each connection that you want the Cluster to expose, and complete the fields of each entry. See [Connection fields](#connection-fields).
7. Select **Next: Review**.
8. In the **Review** step, check the summary. Secrets are masked.
9. Select **Create Cluster**.

The console confirms with **Cluster created** and opens the **Overview** page of the Cluster. A new Cluster is **Undeployed**: it appears in the **Clusters** list, but the gateway doesn't know it yet, and Kafka Services and Virtual Clusters can't use it.

If the creation fails, the wizard shows **Create failed** with the reason, and keeps what you entered.

### Connection fields

A Cluster needs at least one connection. Each connection carries the following fields:

| Field                 | Description                                                                                                                |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| **Connection name**   | Required. A name that identifies this connection. Two connections of the same Cluster can't share a name.                  |
| **Cross ID**          | Optional. A portable identifier for cross-environment references. Gamma generates one from the connection name if you leave this empty. Two connections of the same Cluster can't share a cross ID. |
| **Bootstrap servers** | Required. The Kafka bootstrap server address, in `host:port` format.                                                       |
| **Security protocol** | Required. One of `PLAINTEXT`, `SASL_PLAINTEXT`, `SASL_SSL`, or `SSL`. Defaults to `PLAINTEXT`.                              |

The `SASL_PLAINTEXT` and `SASL_SSL` protocols add a **SASL Configuration** section, where **Select SASL mechanism** offers `NONE`, `AWS_MSK_IAM`, `GSSAPI`, `OAUTHBEARER`, `OAUTHBEARER_TOKEN`, `PLAIN`, `SCRAM-SHA-256`, `SCRAM-SHA-512`, and `DELEGATE_TO_BROKER`. The `SASL_SSL` and `SSL` protocols add the SSL options, with the truststore and the key store.

Gamma derives the Cluster's own cross ID from its name. A second Cluster whose name yields the same cross ID in the environment is refused.

## Deploy the cluster

1. On any page of the Cluster, select **Deploy** above the page.

    Alternatively, in the **Clusters** list, open the row menu (**⋯**) of the Cluster and select **Deploy**.

The console confirms with **Cluster deployed**, and the Cluster's status changes to **Deployed**. The gateway now knows the Cluster, and its connections are offered to Kafka Services and Virtual Clusters.

The **Deploy** action requires the `CLUSTER` **Update** permission of your environment role.

## Verification

To verify that the Cluster is ready to use, follow these steps:

1. In the **Kafka Infrastructure** group, select **Clusters**.
2. Check that the row of your Cluster shows the **Deployed** status, and the number of connections that you added in the **Connections/Backends** column.

## Next steps

* **Manage the Cluster**. Edit its settings and connections, deploy your changes, and see which Kafka Services use it. See [Manage clusters](manage-a-cluster.md).
* **Decide who can manage it**. See [Manage cluster permissions](manage-cluster-permissions.md).
* **Create a Kafka Service**. Build a governed Kafka Service on one of the Cluster's connections. See [Create a Kafka Service with a registered cluster](../../apis/kafka-services/create-a-kafka-service-with-a-registered-cluster.md).
* **Compose a Virtual Cluster**. Present one or more connections to clients as a single Kafka cluster. See [Establish a Virtual Cluster](../virtual-clusters/establish-a-virtual-cluster.md).
