---
hidden: false
noIndex: false
description: Track the setup of a Kafka Service in Event Stream Management from the checklist on its Overview page, and find the bootstrap server that clients use. Follow the checklist to finish the setup.
---

# Follow the setup checklist

A Kafka Service opens on its **Overview** page. The page holds the state of the Kafka Service, a setup checklist, and the connection details that Kafka clients and operators need. A banner warns when the Kafka Service reports no connection metrics.

## Open the overview

1. From the Gamma console, open **Event Stream Management**.
2. In the **APIs** group of the sidebar, click **Kafka Services**.
3. Click the name of the Kafka Service.

The **Overview** page opens. To come back to it from another page of the Kafka Service, click **Overview** in the **General** group of the Kafka Service sidebar.

## Read the status cards

Three cards at the top of the page show:

* **State**. **Started** or **Stopped**, the runtime state of the Kafka Service on the gateway.
* **Deployment**. **Deployed** when the gateway runs the latest configuration, or **Out of sync** when changes wait for the next deployment.
* **Backend binding**. How the Kafka Service reaches Kafka: **Standalone**, **Cluster**, or **Virtual Cluster**.

## Work through the checklist

The **Checklist** card lists five items, with a counter and a completion ring. Each item links to the page that completes it, and its info icon explains it:

<table>
    <thead>
        <tr>
            <th width="230">Item</th>
            <th width="170">Link</th>
            <th>Marks itself done when</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Set the Kafka listener host</strong></td>
            <td><strong>Configure listener</strong></td>
            <td>The listener of the Kafka Service has a host prefix. See <a href="configure-the-entrypoint.md">Configure the entrypoint</a>.</td>
        </tr>
        <tr>
            <td><strong>Configure a backend endpoint</strong></td>
            <td><strong>Configure backend</strong></td>
            <td>The first endpoint of the Kafka Service has bootstrap servers, a cluster, or a Virtual Cluster. See <a href="configure-endpoints.md">Configure endpoints</a>.</td>
        </tr>
        <tr>
            <td><strong>Publish a plan</strong></td>
            <td><strong>Manage plans</strong></td>
            <td>At least one plan is published. See <a href="manage-plans.md">Manage plans</a>.</td>
        </tr>
        <tr>
            <td><strong>Apply policies</strong></td>
            <td><strong>Open Policy Studio</strong></td>
            <td>The common flow of the Kafka Service, or the flow of one of its plans, holds at least one policy. See <a href="design-flows-in-the-policy-studio.md">Design flows in the Policy Studio</a>.</td>
        </tr>
        <tr>
            <td><strong>Grant team access</strong></td>
            <td><strong>Manage access</strong></td>
            <td>The Kafka Service has more than one direct member. Access given through groups doesn't count. See <a href="manage-user-permissions.md">Manage user permissions</a>.</td>
        </tr>
    </tbody>
</table>

A Kafka Service created with the wizard usually starts with three items done: the wizard sets the listener and the endpoint, and publishes the default Keyless plan.

Depending on your role, policies that sit only on plan flows may not mark **Apply policies** done. Mark it done by hand in that case.

To mark an item done or not done by hand, click its checkbox. An item that you clear by hand stays cleared even when its condition is met. These manual marks are stored in your browser only, so other users and other browsers don't see them.

To fold the checklist, click the arrow next to its counter.

## Read the connection details

Two cards under the checklist give the addresses of the Kafka Service:

* **Bootstrap server**. The address that the gateway resolved for the listener, which Kafka clients use as their bootstrap server. Until the gateway can resolve it, the card reads **Available once the Kafka Service is deployed**.
* **Backend**. The bootstrap servers of a Standalone binding, or the identifier of the cluster or the Virtual Cluster that the Kafka Service binds to.

Each value has a copy button.

## Fix the metrics banner

When the Kafka Service doesn't report connection metrics, the **Connection metrics are disabled** banner at the top of the page says that **Logs** in Observability stays empty for this Kafka Service. It appears unless both **Aggregated metrics** and **Connection events** are selected on the **Reporter Settings** page of the Kafka Service.

To clear the banner, click the **Reporter Settings** link of the banner, select **Aggregated metrics** and **Connection events**, then save. See [Configure reporter settings](../../observability/configure-reporter-settings.md).

## Verification

To verify that the Kafka Service is set up, follow these steps:

1. Open the **Overview** page of the Kafka Service.
2. Check that the counter of the **Checklist** card reads 5/5. Items that you marked done by hand count toward it too.
3. Check that the **Bootstrap server** card shows an address.
