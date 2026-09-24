---
hidden: false
noIndex: false
description: Rename a Message API in Event Stream Management, set its description, labels, categories, and images, export or import its definition, and delete it. Follow the steps on its Settings page.
---

# Manage general settings

The **Settings** page of a Message API holds its name, version, description, labels, categories, and images. It also exports and imports the Message API's definition, and deletes the Message API.

## Open the settings

1. From the Gamma console, open **Event Stream Management**.
2. In the sidebar, click **Message APIs**.
3. Click the name of the Message API.
4. In the **General** group of the Message API sidebar, click **Settings**.

Without permission to change the Message APIs of the environment, the fields are read-only.

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

2. Click **Save changes**.

The console confirms with **Message API updated**.

To drop your changes instead, click **Discard**.

## Set the images

The **Images** section holds the **Picture** and the **Background** of the Message API. Each accepts a PNG or JPG file of up to 500 KB.

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

**Promote** opens a dialog that explains that promotion to another environment goes through Gravitee Cloud. It doesn't promote the Message API.

## Delete the Message API

Deleting a Message API removes it, with its plans and subscriptions. It can't be undone.

1. Stop the Message API. The Management API refuses to delete a started API. See [Start, stop, and deploy a Message API](start-stop-and-deploy-a-message-api.md).
2. When the Message API is published, unpublish it. See [Publish and review a Message API](publish-and-review-a-message-api.md).
3. On the **Settings** page, scroll to the **Service events** section.
4. Click **Delete this service**. The tile stays disabled while the Message API is started or published.
5. In **Type <name> to confirm**, type the name of the Message API.
6. Keep **Also close and delete its plans (required if the Message API has active plans)** checked. While a plan is published, the Management API refuses to delete the Message API unless its plans are closed.
7. Click **Delete Message API**.

The console confirms with **Message API deleted** and returns to the **Message APIs** list.

The **Delete** action of the Message API's row in the **Message APIs** list opens the same confirmation.

## Verification

To verify that the settings are saved, follow these steps:

1. Reload the **Settings** page.
2. Check that the fields show the values you saved.
