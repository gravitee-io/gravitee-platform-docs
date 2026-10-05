---
hidden: false
noIndex: false
description: Copy an existing Kafka Service in Event Stream Management with a new name, version, and listener host prefix instead of rebuilding it. Follow the steps to duplicate one.
---

# Duplicate a Kafka Service

When you operate several Kafka Services with a consistent configuration, duplicating an existing one is faster than running the wizard again. The **Duplicate** action creates a new Kafka Service from the configuration of the source, under a new name, version, and listener host prefix.

## What the copy includes

The duplicated Kafka Service reuses the following configuration of the source:

* The description, the visibility, the tags, and the groups.
* The listener, with the host prefix replaced by the value that you enter.
* The endpoint groups and their endpoints, so the copy reaches the same cluster, Virtual Cluster, or brokers.

The copy doesn't include the labels, categories, plans, flows, resources, properties, metadata, members, or reporter settings of the source. The new Kafka Service is created stopped.

{% hint style="info" %}
The copy has no plan, so clients can't connect to it until you create and publish one. See [Manage plans](manage-plans.md).
{% endhint %}

## Duplicate the Kafka Service

1. From the Gamma console, open **Event Stream Management**.
2. In the **APIs** group of the sidebar, click **Kafka Services**.
3. Click the name of the Kafka Service that you want to copy.
4. In the **General** group of the Kafka Service sidebar, click **Settings**.
5. Click **Duplicate**. The button appears only when you have permission to change the Kafka Service.
6. In the **Duplicate Kafka Service** dialog, complete the following fields:

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
            <td>Required. Pre-filled with the name of the source followed by <code>(copy)</code>.</td>
        </tr>
        <tr>
            <td><strong>Version</strong></td>
            <td>Required. Pre-filled with the version of the source.</td>
        </tr>
        <tr>
            <td><strong>Host prefix</strong></td>
            <td>Required. Empty when the dialog opens. The same format rules as at creation apply: lowercase letters, digits, hyphens, and underscores, with dots to separate labels, a first label of at most 49 characters, and at most 241 characters in all. Enter a prefix that no other API in the environment uses. The host prefix of the source, shown under the field, is already in use.</td>
        </tr>
    </tbody>
</table>

7. Click **Duplicate**.

The console confirms with **Kafka Service duplicated** and opens the **Overview** page of the new Kafka Service.

The dialog checks the format of the host prefix while you type, but not whether another API uses it. When the host prefix is in use, the Management API refuses the copy, and the dialog shows the reason. Enter another prefix, then click **Duplicate** again.

## Verification

To verify the copy, follow these steps:

1. Open the **Kafka Services** list, and check that the new Kafka Service is listed with its own listener host.
2. Open the new Kafka Service, and check its **Entrypoint** and **Endpoints** pages.

## Next steps

After duplicating the Kafka Service, prepare the copy to serve traffic:

* Create and publish a plan. See [Manage plans](manage-plans.md).
* Review the endpoint binding on the **Endpoints** page if the copy targets other Kafka infrastructure. See [Configure endpoints](configure-endpoints.md).
* Start the Kafka Service from its **Settings** page when it's ready to accept connections. See [Manage general settings](manage-general-settings.md).
