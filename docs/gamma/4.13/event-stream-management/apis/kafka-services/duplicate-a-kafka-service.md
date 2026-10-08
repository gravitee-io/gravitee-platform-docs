---
hidden: false
noIndex: false
description: Copy an existing Kafka Service in Event Stream Management with a new name, version, and listener host prefix instead of rebuilding it. Follow the steps to duplicate one.
---

# Duplicate a Kafka Service

When you operate several Kafka Services with a consistent configuration, duplicating an existing one is faster than running the wizard again. The **Duplicate** action creates a new Kafka Service from the configuration of the source, under a new name, version, and listener host prefix.

## What the copy includes

The Management API copies the source on the server, from an export of its definition. The copy includes the following items of the source:

* The definition: the description, the listener, the endpoint groups and their endpoints, the flows, the resources, the properties, and the reporter settings. The copy reaches the same cluster, Virtual Cluster, or brokers as the source.
* The plans, the documentation pages, the members, the metadata, and the groups.

Only the name, the version, and the listener host prefix change, to the values that you enter. The copy doesn't keep the primary owner of the source.

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
            <td>Required. Empty when the dialog opens. The same format rules as at creation apply: lowercase letters, digits, hyphens, and underscores, with dots to separate labels, a first label of at most 49 characters, and at most 241 characters in all. Enter a prefix that no other API in the environment uses. The help text under the field shows the listener host of the source, which the copy can't reuse.</td>
        </tr>
    </tbody>
</table>

7. Click **Duplicate**.

The console confirms with **Kafka Service duplicated** and opens the **Overview** page of the new Kafka Service.

While you type, the dialog checks the format of the host prefix, then whether another API uses it: it shows **Checking availability…**, then **This host is already in use.** when the prefix is taken. **Duplicate** stays disabled until the host prefix is valid and free. When the Management API refuses the copy, the dialog shows the reason.

The **Duplicate** button doesn't appear on a Kafka Service managed by the Gravitee Kubernetes Operator. See [Detach a Kubernetes-managed Kafka Service](manage-general-settings.md#detach-a-kubernetes-managed-kafka-service).

## Verification

To verify the copy, follow these steps:

1. Open the **Kafka Services** list, and check that the new Kafka Service is listed with its own listener host.
2. Open the new Kafka Service, and check its **Entrypoint**, **Endpoints**, and **Plans** pages.

## Next steps

After duplicating the Kafka Service, prepare the copy to serve traffic:

* Check the plans of the copy. See [Manage plans](manage-plans.md).
* Review the endpoint binding on the **Endpoints** page if the copy targets other Kafka infrastructure. See [Configure endpoints](configure-endpoints.md).
* Start the Kafka Service from its **Settings** page when it's ready to accept connections. See [Manage general settings](manage-general-settings.md).
