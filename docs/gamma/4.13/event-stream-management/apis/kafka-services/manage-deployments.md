---
hidden: false
noIndex: false
description: Choose the gateways that load a Kafka Service with sharding tags, and compare its deployments in Event Stream Management. Follow the steps to control where the Kafka Service runs and review what changed.
---

# Manage deployments

The **Operations** group of the Kafka Service sidebar holds two deployment pages. **Sharding Tags** decides which Event Gateway instances load the Kafka Service. **Deployment History** lists every deployment of the Kafka Service and compares their definitions.

To push saved changes to the Event Gateway, see [Start, stop, and deploy a Kafka Service](start-stop-and-deploy-a-kafka-service.md).

## Choose the gateways that load the Kafka Service

Sharding tags decide which gateway instances load the Kafka Service. Only the gateway instances that advertise a matching sharding tag load its definition.

1. From the Gamma console, open **Event Stream Management**.
2. In the **APIs** group of the sidebar, click **Kafka Services**.
3. Click the name of the Kafka Service.
4. In the **Operations** group of the Kafka Service sidebar, click **Sharding Tags**.
5. On the **Tags** card, select one or more tags.
6. Click **Save changes**.

The console confirms with **Kafka Service updated**. If the Kafka Service then shows **Out of sync**, deploy it so that the gateways apply the new tags.

The tags come from your organization. When none exist, the page shows **No sharding tags configured**. See [Manage entrypoints and sharding tags](../../../platform-management/manage-entrypoints-and-sharding-tags.md).

Without permission to change the Kafka Service, the tags are read-only.

## Review the deployment history

1. In the **Operations** group of the Kafka Service sidebar, click **Deployment History**.

The page lists every deployment of the Kafka Service, newest first, with its **Version**, **Date**, **User**, and **Label**. On the first page, the newest deployment carries a **live** badge. A Kafka Service that was never deployed shows **No deployments yet**.

Without permission to read the events of the Kafka Service, the page shows **You cannot view deployment history**.

### Compare two deployments

1. Select the checkboxes of two deployments.

The comparison opens at once, in a dialog titled **Comparing v`<version>` → v`<version>`**. Choose **Side-by-side** or **Line-by-line**. In both views, the two sides are labelled **Before** and **After**, each with the version, the date, and the user of its deployment. Check the versions next to **Before** and **After** to know which deployment is on each side.

When the two definitions are identical, the dialog reads **No differences found between these two versions.**

To clear the selection, click **Clear**.

### Compare a deployment with the live one

On the first page of the history, every deployment except the live one has a **Compare with live** icon. Click it to open the comparison between that deployment and the live deployment. As for any comparison, check the versions next to **Before** and **After** to know which side is the live deployment.

### Read a deployed definition

Click the **View definition** icon of a deployment. The dialog shows the API definition of that version.

The page has no rollback. To restore an earlier configuration, change the Kafka Service back, then deploy it.

## Verification

To verify the deployment configuration, follow these steps:

1. Open **Deployment History** for the Kafka Service.
2. Check that the newest deployment carries the **live** badge and the version you expect.
3. Click its **View definition** icon, and check that its `tags` list contains the sharding tags you selected.
