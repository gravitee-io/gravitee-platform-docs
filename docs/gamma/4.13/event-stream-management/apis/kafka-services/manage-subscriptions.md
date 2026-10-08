---
hidden: false
noIndex: false
description: Review, create, approve, pause, transfer, and close the subscriptions of a Kafka Service in Event Stream Management, and manage their API keys and metadata. Follow the steps to handle consumer access.
---

# Manage subscriptions

A subscription binds one application to one plan of a Kafka Service. The **Subscriptions** page lists the subscriptions of a Kafka Service. Each subscription opens on a detail page with its lifecycle actions, its metadata, and, for API key plans, its API keys.

Keyless plans take no subscriptions. When a Kafka Service only has Keyless plans, its Kafka clients connect without a subscription.

## Open the subscriptions

1. From the Gamma console, open **Event Stream Management**.
2. In the **APIs** group of the sidebar, click **Kafka Services**.
3. Click the name of the Kafka Service.
4. In the **Consumers** group of the Kafka Service sidebar, click **Subscriptions**.

While the Kafka Service has no subscription, the page explains what subscriptions are for and offers **Create subscription**.

Once the Kafka Service has a subscription, the page shows three counters: **Total subscriptions**, **Active** for accepted and resumed subscriptions, and **Pending approval**. Click a counter to filter the list on it. The list shows the **Application**, **Plan**, **Security**, **Status**, **Created**, and **Ending** of each subscription.

## Find a subscription

Narrow the list with the following filters:

* The search box finds a subscription by its API key.
* **Status** keeps the subscriptions with the selected statuses: **Pending**, **Accepted**, **Paused**, **Resumed**, **Rejected**, or **Closed**.
* **Plan** keeps the subscriptions to the selected plans.

To clear every filter, click **Reset**. When no subscription matches, the list names the active filters and offers **Clear filters**.

To download the subscriptions that match the filters, click **Export CSV**. The file holds up to 1,000 subscriptions. When more subscriptions match, a warning says how many were left out.

## Create a subscription

1. Open the subscriptions of the Kafka Service.
2. Click **Create subscription**.
3. In **Application**, type at least two characters of the application's name, then select the application.
4. In **Plan**, select a published plan. Keyless plans aren't offered.
5. Optional: For an API key plan, enter a key in **Custom API key (optional)**. Left empty, the key is generated.
6. Click **Create subscription**.

A JWT or OAuth2 plan needs an application that has a client ID. The panel shows **Client ID required** when you select such a plan.

If you close the panel after you selected an application or a plan, the console asks you to confirm that you discard your changes.

## Handle a subscription

Click the application of a subscription to open its detail page. The actions depend on the status of the subscription:

<table>
    <thead>
        <tr>
            <th width="190">Status</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Pending</td>
            <td><strong>Approve</strong>, with optional start and end dates, a custom API key for an API key plan, and a reason. <strong>Reject</strong>, with a required reason.</td>
        </tr>
        <tr>
            <td>Accepted or resumed</td>
            <td><strong>Transfer</strong> to another published plan with the same security type. <strong>Change end date</strong>. <strong>Pause</strong>. <strong>Close</strong>.</td>
        </tr>
        <tr>
            <td>Paused</td>
            <td><strong>Resume</strong>. <strong>Close</strong>.</td>
        </tr>
        <tr>
            <td>Rejected or closed</td>
            <td>None.</td>
        </tr>
    </tbody>
</table>

A subscription managed by the Gravitee Kubernetes Operator shows **Managed by Kubernetes** and offers no actions. Change it in its custom resource instead.

Without permission to change the Kafka Service's subscriptions, the detail page offers no actions.

## Manage the credentials of a subscription

The detail page shows the credentials that match the plan's security type:

* For a JWT or OAuth2 plan, the **Credentials** card says that the plan authenticates with the client credentials configured on the application, not with keys issued on the subscription.
* For an API key plan, the **API keys** card lists the keys of an accepted, paused, or resumed subscription, with their **Key**, **State**, **Created**, and **Revoked / expires** dates. Each key has a copy button.

On the **API keys** card:

* **Renew** issues a new key for the subscription. Optional: enter a key in **Custom API key (optional)**.
* **Expire** stops a key on the date you choose.
* **Revoke** stops a key immediately.
* **Reactivate** restores a revoked or expired key.

An application that shares one API key across its subscriptions shows the **Shared API key** card instead. Renew or revoke that key from the application.

## View and edit subscription metadata

The **Metadata** card lists the key-value pairs that a subscription carries, usually filled in by the consumer through the Developer Portal subscription form. A policy reads an entry at runtime with the expression `{#subscription.metadata['key']}`. The copy button of each entry copies that expression.

You can add, edit, and remove entries when you have permission to change the Kafka Service's subscriptions, the subscription is pending, accepted, resumed, or paused, and it isn't managed by Kubernetes.

1. Open the detail page of the subscription.
2. On the **Metadata** card, click **Add**, or click the edit icon of an entry.
3. Enter the **Key** and the **Value**. The key uses letters, digits, dashes, or underscores only, up to 100 characters, and must be unique on the subscription. The value is required. To edit a JSON or multi-line value, switch the field to **Code editor**.
4. Click **Save**.

To remove an entry, click its delete icon, then click **Delete metadata** in the **Delete metadata `<key>`?** dialog.

Consider the following before you edit metadata:

* The server removes anything between angle brackets from a value. The dialog warns you when a value contains some.
* When a subscription form governs the Kafka Service, the card shows **This API has a subscription form**, with the name of the form. Values edited on this card aren't validated against that form, but follow it anyway: a value that the form refuses gets the consumer rejected at their next subscription update.
* Past 25 entries, the card shows a warning badge, because a consumer who submits the portal subscription form again would be refused. The card itself doesn't enforce the limit.

## Verification

To verify that an application can consume the Kafka Service, follow these steps:

1. Open the subscriptions of the Kafka Service.
2. Click the **Active** counter.
3. Check that the application is listed with the plan you expect.

## Next steps

* [Manage plans](manage-plans.md)
* [Broadcast messages to consumers](broadcast-messages-to-consumers.md)
