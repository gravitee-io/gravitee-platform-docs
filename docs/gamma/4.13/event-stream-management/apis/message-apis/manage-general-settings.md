---
hidden: false
noIndex: false
description: Rename a Message API in Event Stream Management, set its description, labels, categories, and images, export, import, or duplicate it, detach it from Kubernetes, and delete it. Follow the steps on its Settings page.
---

# Manage general settings

The **Settings** page of a Message API holds its name, version, description, labels, categories, and images. It also exports and imports the Message API's definition, duplicates the Message API, detaches it from the Gravitee Kubernetes Operator, and deletes it.

## Open the settings

1. From the Gamma console, open **Event Stream Management**.
2. In the sidebar, click **Message APIs**.
3. Click the name of the Message API.
4. In the **General** group of the Message API sidebar, click **Settings**.

Without permission to change the Message APIs of the environment, the fields and images are read-only, and the **Import**, **Duplicate**, and **Promote** buttons are hidden. When the Gravitee Kubernetes Operator manages the Message API, the fields and images are read-only too, and **Import** and **Duplicate** are hidden, but **Promote** stays. See [Kubernetes-managed Message APIs](#kubernetes-managed-message-apis). **Export** needs permission to read the API definition. The **Message API events** card shows only the actions that your role allows.

## Edit the general information

1. Change the fields you need:

<table>
    <thead>
        <tr>
            <th width="160">Field</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Name</strong></td>
            <td>Required.</td>
        </tr>
        <tr>
            <td><strong>Version</strong></td>
            <td>Required. Up to 32 characters.</td>
        </tr>
        <tr>
            <td><strong>Description</strong></td>
            <td>Optional.</td>
        </tr>
        <tr>
            <td><strong>Labels</strong></td>
            <td>Optional. Type a label, then press Enter or type a comma.</td>
        </tr>
        <tr>
            <td><strong>Categories</strong></td>
            <td>Optional. Select categories of the environment.</td>
        </tr>
    </tbody>
</table>

2. At the top of the page, click **Save changes**. **Save changes** and **Discard** appear once you change a field. **Save changes** stays disabled while **Name** or **Version** is empty.

The console confirms with **Message API updated**.

To drop your changes instead, click **Discard**.

## Set the images

The **Images** section holds the **Picture** and the **Background** of the Message API. Each accepts a PNG, JPG, or SVG file of up to 500 KB.

* To set an image, click it and select a file.
* To clear an image, click **Remove**.

An image change applies at once, without **Save changes**.

The **Details** section below the images shows the owner, the creation and update dates, the visibility, the lifecycle, and the status of the Message API. When the environment uses the API review workflow, it also shows the review state.

## Export the definition

1. Click **Export**.
2. In the **Export Message API** panel, select a format:
    * **Gravitee API definition**. A JSON file. Under **Include additional data**, clear the data you want to leave out: **Groups**, **Members**, **Pages**, **Plans**, or **Metadata**.
    * **CRD API Definition**. A YAML file of the Message API as a Kubernetes custom resource, for the Gravitee Kubernetes Operator.
    * **Terraform HCL resource**. A link to the Gravitee Terraform provider tutorial. This format has no export.
3. Click **Export**.

The browser downloads the file, named after the Message API.

## Import a definition over the Message API

Importing updates the Message API from the content of a Gravitee API definition.

1. Click **Import**.
2. Choose the source of the definition:
    * **Local file**. Drop the JSON file on the drop zone, or click it to browse. The console accepts only a v4 definition of a Message API.
    * **Remote URL**. Enter the http or https address of the definition in **Definition URL**. The Management API fetches the definition itself, so the address must be reachable from the Management API and allowed by its import allow list.
3. Click **Import**.

The console confirms with **Message API definition imported**.

## Duplicate the Message API

Duplicating creates a new Message API with the same definition, plans, flows, properties, resources, members, and metadata.

1. Click **Duplicate**.
2. In the **Duplicate Message API** dialog, enter the **Name** and the **Version** of the copy. **Name** is pre-filled with the name of the original followed by `(copy)`, and **Version** with the version of the original.
3. When the Message API has an entrypoint that listens over HTTP, enter the **Context path** of the copy, for example `/orders-copy`. A context path is unique in the environment, so the copy can't reuse the path of the original, which the dialog shows under the field. The path follows the rules of the **Entrypoints** page, and the dialog checks that it's available. See [Configure entrypoints](configure-entrypoints.md#set-the-context-paths). A Message API whose only entrypoint is **Webhook** doesn't ask for a context path.
4. Click **Duplicate**. The button stays disabled while a field is empty or invalid.

The console confirms with **Message API duplicated** and opens the **Overview** of the copy. The copy is stopped and not yet deployed, and its plans keep the status they have on the original. Start it when it's ready. See [Start, stop, and deploy a Message API](start-stop-and-deploy-a-message-api.md).

**Promote** opens a dialog that explains that promotion to another environment goes through Gravitee Cloud. It doesn't promote the Message API.

## Delete the Message API

Deleting a Message API removes it, with its plans and subscriptions.

{% hint style="warning" %}
Deleting a Message API can't be undone.
{% endhint %}

1. Stop the Message API. The Management API refuses to delete a started API. See [Start, stop, and deploy a Message API](start-stop-and-deploy-a-message-api.md).
2. When the Message API is published, unpublish it. See [Publish and review a Message API](publish-and-review-a-message-api.md).
3. On the **Settings** page, scroll to the **Message API events** card.
4. Click **Delete this Message API**. The tile stays disabled while the Message API is started or published. It appears only when you have permission to delete the Message APIs of the environment.
5. In the **Delete Message API?** dialog, under **Type <name> to confirm**, type the name of the Message API. You can select and copy the name from the prompt.
6. Keep **Also close and delete its plans (required if the Message API has active plans)** checked. While a plan is published, the Management API refuses to delete the Message API unless its plans are closed.
7. Click **Delete Message API**.

The console confirms with **Message API deleted** and returns to the **Message APIs** list.

The **Delete** action of the Message API's row in the **Message APIs** list opens the same confirmation. Like the tile, it's disabled while the Message API is started or published, and reads **Stop and unpublish it first**.

## Kubernetes-managed Message APIs

A Message API that the Gravitee Kubernetes Operator manages is defined by its custom resource. The console makes most of it read-only, so that your changes don't drift from the resource:

* Read-only: the general settings, the entrypoints, endpoints, failover, flows, response templates, resources, properties, CORS, reporter settings, and sharding tags, the plans, the members, and the metadata.
* Hidden: **Start**, **Stop**, **Delete this Message API**, **Import**, **Duplicate**, and the **Publication** section.
* Still available: **Deploy**, rollback from the deployment history, **Promote**, **Export**, the subscriptions, the notifications, the alerts, the broadcasts, the API Score, and the webhook logs settings of the **Webhooks** page.

A subscription that the operator itself manages stays read-only. See [Manage subscriptions](manage-subscriptions.md).

### Detach a Message API from Kubernetes

Detaching a Message API from its automation source makes it editable again in the console. You need permission to change the Message API's definition.

{% hint style="warning" %}
When the Message API is attached to the Gravitee Kubernetes Operator again, the operator overwrites every change made while it was detached.
{% endhint %}

1. On the **Settings** page, scroll to the **Message API events** card.
2. Click **Detach the Message API**. The tile appears only on a Message API that the Gravitee Kubernetes Operator manages.
3. In the **Detach API** dialog, under **Type <name> to confirm**, type the name of the Message API.
4. Click **Yes, detach it**.

The console confirms with **The API has been detached from its automation source.**

## Verification

To verify that the settings are saved, follow these steps:

1. Reload the **Settings** page.
2. Check that the fields show the values you saved.
