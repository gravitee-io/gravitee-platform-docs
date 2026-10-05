---
hidden: false
noIndex: false
description: Add metadata to a Kafka Service in Event Stream Management, and override the metadata it inherits from the environment. Follow the steps to manage its entries.
---

# Configure API metadata

Metadata entries are named values attached to a Kafka Service. A Kafka Service inherits the global metadata of its environment and can hold entries of its own. The **Metadata** page lists both.

## Open the metadata

1. From the Gamma console, open **Event Stream Management**.
2. In the **APIs** group of the sidebar, click **Kafka Services**.
3. Click the name of the Kafka Service.
4. In the **General** group of the Kafka Service sidebar, click **Metadata**.

The table shows the **Name**, **Format**, **Value**, and **Origin** of each entry. **Inherited** marks an entry that comes from the environment. **Local** marks an entry of the Kafka Service itself, including an inherited entry that the Kafka Service overrides.

Without permission to read the metadata of the Kafka Service, the **Metadata** item doesn't appear in the sidebar. **Add metadata**, the edit icon, and the delete icon each need the matching metadata permission.

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
            <td>Required. It must match the format, except for a String value. A <strong>Boolean</strong> value is a checkbox. The console doesn't check the format of a value that holds an expression such as <code>${...}</code>.</td>
        </tr>
    </tbody>
</table>

3. Click **Add metadata**.

The console saves the entry at once and confirms with **Metadata created**.

## Override or edit an entry

1. Click the edit icon of the entry.
2. Change the fields you need.
3. Click **Save changes**.

Editing an **Inherited** entry overrides the global value for this Kafka Service only, and the entry becomes **Local**. The console confirms with **Metadata updated**.

## Delete an entry

Only **Local** entries can be deleted.

1. Click the delete icon of the entry.
2. In the **Delete metadata** confirmation, click **Delete**.

The console confirms with **Metadata deleted**.

## Verification

To verify the metadata, follow these steps:

1. Reload the **Metadata** page.
2. Check that each entry shows the value and the origin you expect.
