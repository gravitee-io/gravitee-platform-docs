---
hidden: false
noIndex: false
description: Add resources, such as caches and OAuth2 providers, to a Message API in Event Stream Management so that its policies can use them. Follow the steps to add and manage them.
---

# Configure resources

Resources are plugin instances, such as caches or OAuth2 providers, that the policies of a Message API use at runtime. Defining a resource once lets several policies share its configuration.

## Add a resource

1. From the Gamma console, open **Event Stream Management**.
2. In the sidebar, click **Message APIs**.
3. Click the name of the Message API.
4. In the **Design** group of the Message API sidebar, click **Resources**.
5. Click **Add resource**.
6. In the **Select Type** step, select the type of resource. Search the types by name or description.
7. Click **Next**.
8. In the **Configure** step, complete the following fields:
    * **Name**. Required. The name that policies use to reference the resource. Each resource of the Message API needs its own name.
    * The configuration of the resource type.
9. Click **Next**.
10. In the **Review** step, check the resource, then click **Add resource**.

The console adds the resource, enabled, and confirms with **Message API updated**. The resource reaches the gateway at the next deployment, and until then the Message API shows **Out of sync**. See [Start, stop, and deploy a Message API](start-stop-and-deploy-a-message-api.md).

Without permission to change the Message API's definition, the page is read-only.

## Manage the resources

The **Resources** page counts the total, enabled, and disabled resources, and lists them with their name, type, and status. Open the actions menu of a resource's row to:

* **Edit** the resource. The type can't change.
* **Enable** or **Disable** the resource. The change is saved at once.
* **Delete** the resource. Policies that reference it can stop working.

## Verification

To verify the resources, follow these steps:

1. Reload the **Resources** page.
2. Check that each resource shows the type and the status you expect.
