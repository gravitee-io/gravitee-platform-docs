---
hidden: false
noIndex: false
description: Start, stop, and deploy a Kafka Service in Event Stream Management from its header, its Settings page, or the Kafka Services list. Follow the steps to run it on the Event Gateway.
---

# Start, stop, and deploy a Kafka Service

A Kafka Service serves Kafka clients when it's started and deployed on the Event Gateway. Starting and stopping decide whether the Event Gateway serves the Kafka Service. Deploying pushes your saved changes to the Event Gateway.

The header of the Kafka Service sidebar shows two badges: **Started** or **Stopped** for the runtime state, and **Deployed** or **Out of sync** for the deployment state.

## Prerequisites

* Permission to change the Kafka Services of the environment. Without it, the start, stop, and deploy actions don't appear. A Kafka Service managed by the Gravitee Kubernetes Operator offers **Deploy** but not **Start** or **Stop** on its pages. See [Detach a Kubernetes-managed Kafka Service](manage-general-settings.md#detach-a-kubernetes-managed-kafka-service).
* For a Kafka Service bound to a Virtual Cluster, the Virtual Cluster deployed. See [Start a Kafka Service bound to a Virtual Cluster](#start-a-kafka-service-bound-to-a-virtual-cluster).

## Start or stop a Kafka Service

The actions above every page of a Kafka Service include **Start** while it's stopped, and **Stop** while it's started.

1. Open the Kafka Service.
2. Click **Start**, or click **Stop**.
3. If you clicked **Stop**, click **Stop Kafka Service** in the **Stop `<name>`?** dialog. The Kafka Service stops serving traffic on the Event Gateway until you start it again.

The console confirms with **Kafka Service started** or **Kafka Service stopped**.

You can also start and stop a Kafka Service from the following places:

* The **Kafka Service events** card of the **Settings** page, with the **Start Kafka Service** and **Stop Kafka Service** tiles. In the **General** group of the Kafka Service sidebar, click **Settings**.
* The actions menu of its row in the **Kafka Services** list, with **Start** and **Stop**. When the bound Virtual Cluster isn't deployed, **Start** is disabled and reads **Deploy its Virtual Cluster first**.

When the environment uses the API review workflow, a Kafka Service in the review workflow can't start or stop until a reviewer accepts it. Until then, the page header and the **Kafka Service events** card don't offer **Start** or **Stop**. The actions menu of its row in the **Kafka Services** list still offers them.

## Deploy your changes

A change to what the Event Gateway runs is saved first, and reaches the Event Gateway at the next deployment. Until then, the header of the Kafka Service sidebar shows **Out of sync**.

To deploy the pending changes from the Kafka Service pages, follow these steps:

1. Open the Deploy dialog with one of the following actions:
    * In the page header, click **Deploy**.
    * On the **Settings** page, click the **Deploy changes** tile of the **Kafka Service events** card. The tile appears only while the Kafka Service is out of sync.
2. Optional: In the **Deploy your API** dialog, enter a **Deployment label** of up to 32 characters. The label identifies the deployment in the **Label** column of **Deployment History**.
3. Click **Deploy**.

The console confirms with **Deployment triggered**, and the badge changes to **Deployed**.

You can also deploy from the **Kafka Services** list: open the actions menu of the row, then select **Deploy**. This action deploys at once, without the **Deploy your API** dialog, so the deployment has no label.

Saving in the Policy Studio doesn't deploy the flows. Deploy them with one of the actions above.

## Start a Kafka Service bound to a Virtual Cluster

A Kafka Service whose endpoint is a Virtual Cluster can't start until that Virtual Cluster is deployed. While it isn't, the Kafka Service shows the **Virtual Cluster not deployed** banner, which links to the Virtual Cluster. The **Start** button of the page header, the **Start Kafka Service** tile of the **Settings** page, and the **Start** action of its row in the **Kafka Services** list are disabled.

1. Open the Virtual Cluster from the banner.
2. Deploy the Virtual Cluster.
3. Return to the Kafka Service, then click **Start**.

See [Establish a Virtual Cluster](../../kafka-infrastructure/virtual-clusters/establish-a-virtual-cluster.md).

## Delete a Kafka Service

The **Kafka Service events** card also holds the **Delete this Kafka Service** tile, for users with permission to delete Kafka Services. The tile is disabled while the Kafka Service is started or published: stop it, and unpublish it if it's published. See [Unpublish the Kafka Service](manage-general-settings.md#unpublish-the-kafka-service). Deleting a Kafka Service permanently removes it, with its plans, its subscriptions, and its analytics data.

## Verification

To verify that the Kafka Service is started and deployed, follow these steps:

1. Open the Kafka Service.
2. Check that the header of the Kafka Service sidebar shows **Started** and **Deployed**.

## Next steps

* [Manage deployments](manage-deployments.md)
* [Configure alerts](configure-alerts.md)
