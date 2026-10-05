---
hidden: false
noIndex: false
description: Find Virtual Clusters, change their backends, deploy or undeploy them, and see which Kafka Services use each one. Follow the steps to manage a Virtual Cluster.
---

# Manage a Virtual Cluster

The **Virtual Clusters** page lists the Virtual Clusters of the environment, separately from the **Clusters** page. A Virtual Cluster opens on the same detail pages as a Cluster: **Overview**, **Settings**, **Configuration**, and **User Permissions** in the **General** group, and **Used by Kafka Services** in the **Usage** group.

This page covers what differs for a Virtual Cluster. For the settings, the lifecycle actions, and the deletion, see [Manage clusters](../clusters/manage-a-cluster.md). For the members, see [Manage cluster permissions](../clusters/manage-cluster-permissions.md).

## Find a Virtual Cluster

1. From the Gamma console sidebar, select **Event Stream Management**.
2. In the **Kafka Infrastructure** group, select **Virtual Clusters**.

The page works like the **Clusters** page: a stat strip with the **Total**, **Deployed**, **Pending**, and **Undeployed** counts, **Search Virtual Clusters…**, the **Lifecycle** filter, and a row menu (**⋯**) on each row. The **Connections/Backends** column shows the number of backends, and a Virtual Cluster with two or more backends shows the **Kafka Mesh** badge next to its name.

In the row menu, **Deploy** is disabled with **Add a backend first** while the Virtual Cluster has no backend.

The ⓘ button next to the **Virtual Clusters** title opens the Virtual Cluster explainer.

## Read the overview

The **Overview** page of a Virtual Cluster shows its **Type**, **Virtual Cluster**, with the **Kafka Mesh** badge when it has two or more backends, its **Lifecycle** status, and its number of **Backends**. Below them, the **Summary** card lists the **Name**, the **Description**, the **Cross ID**, the **Version**, and the **Deployed at** date.

## Change the backends

With the `CLUSTER` **Update** permission of your environment role, you edit the backends of a Virtual Cluster in place, with the same composer as in the creation wizard.

1. Open the Virtual Cluster.
2. In the **General** group of the sidebar, select **Configuration**.
3. To add a backend, select a **Cluster** and one of its **Connection**s, then select **Add backend**. Only the deployed Clusters are listed.
4. To remove a backend, select the delete icon of its row.
5. At the bottom of the page, select **Save changes**, or **Discard** to restore the saved backends.
6. Select **Deploy changes** above the page.

The console confirms the save with **Cluster updated**. A deployed Virtual Cluster moves to **Pending changes**, and the gateway keeps running the previously deployed backends until you deploy the changes.

New backends go to the end of the list. The order of the backends is the configuration order, which decides which backend wins when two of them hold a topic with the same name. See [Topic routing](kafka-virtual-cluster-runtime-behavior-reference.md#topic-routing).

Without the `CLUSTER` **Update** permission, the page lists the backends read-only, with their **Cluster cross ID** and **Connection cross ID**.

{% hint style="warning" %}
Removing a backend from a deployed Virtual Cluster affects the clients that use topics on that backend once you deploy the change. Check the **Used by Kafka Services** page first, and confirm the impact before you change a Virtual Cluster in production.
{% endhint %}

### Remove every backend

When you save a **Deployed** Virtual Cluster, or one with **Pending changes**, with no backend left, the console asks you to confirm in the **Remove all backends?** dialog. The dialog says that the Virtual Cluster will be undeployed, and lists any started Kafka Service bound to it.

1. Select **Remove backends & undeploy**.

The Management API saves the empty configuration, but doesn't undeploy the Virtual Cluster: it moves to **Pending changes**, the gateway keeps serving the previously deployed backends, and **Deploy changes** stays disabled until you add a backend. To stop the traffic, stop the Kafka Services bound to the Virtual Cluster, then select **Undeploy**.

## Read the Kafka Mesh constraints

Below the backends, the **Configuration** page shows a **Kafka Mesh** card with the runtime constraints of the gateway. Its badge reads **Enabled** when the Virtual Cluster has two or more backends, and **Single backend** otherwise.

The card is informational: the constraints can't be configured. The gateway applies them to every Virtual Cluster, including one with a single backend. Two statements of the card differ from what the gateway does:

* The card says that topic names are unique across the Kafka Mesh. The gateway doesn't enforce it: when two backends hold a topic with the same name, the first backend in configuration order wins.
* The card says that idempotent producers are pinned to a single backend. The gateway lets an idempotent producer write to topics on several backends. Only transactions are pinned to one backend.

For the actual behavior, see [Virtual Cluster runtime behavior reference](kafka-virtual-cluster-runtime-behavior-reference.md).

## Deploy and undeploy

The lifecycle actions of a Virtual Cluster are the same as for a Cluster. See [Cluster lifecycle](../clusters/manage-a-cluster.md#cluster-lifecycle). The following rules are specific to a Virtual Cluster:

* **Deploy** requires at least one backend. The button is disabled, and its tooltip reads **A Virtual Cluster needs at least one backend before it can be deployed.**
* **Undeploy** is refused while a started Kafka Service is bound to the Virtual Cluster. The **Undeploy Cluster?** dialog names these Kafka Services, each with a link. Stop them first.
* A Kafka Service bound to the Virtual Cluster can start only while the Virtual Cluster is **Deployed** or has **Pending changes**.

## See which Kafka Services use a Virtual Cluster

1. Open the Virtual Cluster.
2. In the **Usage** group of the sidebar, select **Used by Kafka Services**.

The page lists the Kafka Services bound to the Virtual Cluster, with their **Name**, **Version**, **State**, and **Binding**. Select a name to open the Kafka Service.

## Verification

To verify that the gateway runs your latest backends, follow these steps:

1. In the **Kafka Infrastructure** group, select **Virtual Clusters**.
2. Check that the row of your Virtual Cluster shows the **Deployed** status, not **Pending changes**, and the number of backends that you expect.

## Next steps

* [Virtual Cluster runtime behavior reference](kafka-virtual-cluster-runtime-behavior-reference.md). How the gateway routes requests across the backends.
* [Virtual Cluster broker addressing](https://documentation.gravitee.io/apim/4.13/kafka-gateway/virtual-cluster-broker-addressing). How the gateway rewrites the broker IDs of the backends.
