---
hidden: false
noIndex: false
description: Review, create, approve, pause, transfer, and close the subscriptions of a Message API in Event Stream Management, and manage their API keys. Follow the steps to handle consumer access.
---

# Manage subscriptions

A subscription binds one application to one plan of a Message API. The **Subscriptions** page lists the subscriptions of a Message API, and each subscription opens on a detail page with its lifecycle actions and, for API key plans, its API keys.

## Open the subscriptions

1. From the Gamma console, open **Event Stream Management**.
2. In the sidebar, click **Message APIs**.
3. Click the name of the Message API.
4. In the **Consumers** group of the Message API sidebar, click **Subscriptions**.

Once the Message API has a subscription, the page shows three counters: **Total subscriptions**, **Active** for accepted and resumed subscriptions, and **Pending approval**. Click a counter to filter the list on it.

## Find a subscription

Narrow the list with the following filters:

* The search box finds a subscription by its API key.
* **Status** keeps the subscriptions with the selected statuses: **Pending**, **Accepted**, **Paused**, **Resumed**, **Rejected**, or **Closed**.
* **Plan** keeps the subscriptions to the selected plans.

To clear every filter, click **Reset**.

To download the subscriptions that match the filters, click **Export CSV**. The file holds up to 1,000 subscriptions.

## Create a subscription

1. Open the subscriptions of the Message API.
2. Click **Create subscription**.
3. In **Application**, type at least two characters of the application's name, then select the application.
4. In **Plan**, select a published plan. Keyless plans aren't offered, because consumers don't subscribe to them.
5. Optional: For an API key plan, when the environment allows custom API keys, enter a key in **Custom API key (optional)**. Left empty, the key is generated.
6. Click **Create subscription**.

A JWT or OAuth2 plan needs an application that has a client ID. The panel shows a reminder when you select one.

The **Create subscription** panel lists Push plans, but it can't create a subscription to one. It doesn't collect the webhook settings, and the Management API refuses a Push plan subscription without them.

The console accepts the new subscription at once, whatever the subscription validation of the plan. The validation applies to the subscriptions that consumers request from the Developer Portal.

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

A subscription whose consumer is in failure also offers **Resume from failure**, which clears the failure and resumes consumption.

A subscription managed by the Gravitee Kubernetes Operator shows **Managed by Kubernetes** and offers no actions. Change it in its custom resource instead.

Without permission to change the Message API's subscriptions, the detail page offers no actions.

## Manage the API keys of a subscription

A subscription to an API key plan lists its API keys once it's accepted, paused, or resumed.

* **Renew** issues a new key for the subscription. Optional: When the environment allows custom API keys, enter a custom API key.
* **Expire** stops a key on the date you choose.
* **Revoke** stops a key immediately.
* **Reactivate** restores a revoked or expired key while the subscription is accepted or paused.

An application that shares one API key across its subscriptions shows **Shared API key**. Renew or revoke that key from the application instead.

## Verification

To verify that an application can consume the Message API, follow these steps:

1. Open the subscriptions of the Message API.
2. Click the **Active** counter.
3. Check that the application is listed with the plan you expect.
