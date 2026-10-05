---
hidden: false
noIndex: false
description: Add resources, such as caches and OAuth2 providers, to a Kafka Service in Event Stream Management so that its policies can use them. Follow the steps to add and manage them.
---

# Configure resources

Resources are plugin instances, such as caches or OAuth2 providers, that the policies of a Kafka Service use at runtime. Defining a resource once lets several policies share its configuration.

## Add a resource

1. From the Gamma console, open **Event Stream Management**.
2. In the **APIs** group of the sidebar, click **Kafka Services**.
3. Click the name of the Kafka Service.
4. In the **Design** group of the Kafka Service sidebar, click **Resources**.
5. Click **Add resource**.
6. In the **Select Type** step, select the type of resource. Search the types by name, or filter them by category.
7. Click **Next**.
8. In the **Configure** step, complete the following fields:
    * **Name**. Required. The name that policies use to reference the resource. Each resource of the Kafka Service needs its own name: a name in use shows **A resource with this name already exists.**
    * The configuration of the resource type. A type with nothing to configure shows **This resource type has no configurable settings.**
9. Click **Next**.
10. In the **Review & Create** step, check the resource, then click **Add resource**.

The console adds the resource, enabled, and confirms with **Kafka Service updated**. The resource reaches the gateway at the next deployment, and until then the Kafka Service shows **Out of sync**. To deploy, click **Deploy** in the page header.

Without permission to change the Kafka Service's definition, the page is read-only.

## Manage the resources

The **Resources** page counts the **Total resources**, the **Enabled** ones, and the **Disabled** ones, and lists them with their **Name**, **Type**, and **Status**. Open the actions menu of a resource's row to:

* **Edit** the resource. The type can't change, and the wizard ends with **Save changes**.
* **Enable** or **Disable** the resource. The change is saved at once.
* **Delete** the resource. In the **Remove this resource?** dialog, click **Remove resource**. Policies that reference it can stop working.

## Verification

To verify the resources, follow these steps:

1. Reload the **Resources** page.
2. Check that each resource shows the type and the status you expect.
