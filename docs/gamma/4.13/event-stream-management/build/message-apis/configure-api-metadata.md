---
hidden: false
noIndex: false
description: Add metadata to a Message API in Event Stream Management, and override the metadata it inherits from the environment. Follow the steps to manage its entries.
---

# Configure API metadata

Metadata entries are named values attached to a Message API. A Message API inherits the global metadata of its environment and can hold entries of its own. The **Metadata** page lists both.

## Open the metadata

1. From the Gamma console, open **Event Stream Management**.
2. In the sidebar, click **Message APIs**.
3. Click the name of the Message API.
4. In the **General** group of the Message API sidebar, click **Metadata**.

The table shows the **Name**, **Format**, **Value**, and **Origin** of each entry. **Inherited** marks an entry that comes from the environment. **Local** marks an entry of the Message API itself, including an inherited entry that the Message API overrides.

Without permission to read the metadata of the Message API, the **Metadata** item doesn't appear in the sidebar.

## Add a metadata entry

1. Click **Add metadata**.
2. Complete the following fields:

<table>
    <thead>
        <tr>
            <th width="140">Field</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Name</strong></td>
            <td>Required. The name of the entry.</td>
        </tr>
        <tr>
            <td><strong>Format</strong></td>
            <td>Required. <strong>String</strong>, <strong>Numeric</strong>, <strong>Boolean</strong>, <strong>Date</strong>, <strong>Email</strong>, or <strong>URL</strong>. The default is <strong>String</strong>.</td>
        </tr>
        <tr>
            <td><strong>Value</strong></td>
            <td>Required. It must match the format, except for a String value. The console doesn't check the format of a value that holds an expression such as <code>${...}</code>. The Management API resolves a value that starts with an expression, then checks the result.</td>
        </tr>
    </tbody>
</table>

3. Click **Add metadata**.

The console saves the entry at once and confirms with **Metadata created**.

## Override or edit an entry

1. Click the edit icon of the entry.
2. Change the fields you need.
3. Click **Save changes**.

Editing an **Inherited** entry overrides the global value for this Message API only, and the entry becomes **Local**. The console confirms with **Metadata updated**.

## Delete an entry

Only **Local** entries can be deleted.

1. Click the delete icon of the entry.
2. Click **Delete**.

The console confirms with **Metadata deleted**.

## Verification

To verify the metadata, follow these steps:

1. Reload the **Metadata** page.
2. Check that each entry shows the value and the origin you expect.
