---
hidden: false
noIndex: false
description: Create, publish, deprecate, and close the plans of a Kafka Service in Event Stream Management, and replace a live plan with a plan of another security type. Follow the steps to decide how Kafka clients connect.
---

# Manage plans

A plan decides how Kafka clients access a Kafka Service: with no credentials, with an API key, a JWT, an OAuth2 token, or a client certificate. The **Plans** page lists the plans of a Kafka Service by status and holds their lifecycle actions.

## Open the plans

1. From the Gamma console, open **Event Stream Management**.
2. In the **APIs** group of the sidebar, click **Kafka Services**.
3. Click the name of the Kafka Service.
4. In the **Consumers** group of the Kafka Service sidebar, click **Plans**.

The status cards, **Staging**, **Published**, **Deprecated**, and **Closed**, show how many plans have each status. Click a card to list its plans. The page opens on **Staging**. The table shows the **Name**, **Security type**, **Status**, and **Validation** of each plan.

Without permission to change the Kafka Service's plans, the page is read-only.

A Kafka Service created with the wizard already has plans. Its **Security** step adds a Keyless plan by default and publishes it at creation. Every other plan chosen in that step is created in **Staging**, so you finish its configuration and publish it here. See [Create a Kafka Service with a registered cluster](create-a-kafka-service-with-a-registered-cluster.md).

## Plan types

The security type of a plan is set when you create it, and it can't change later.

<table>
    <thead>
        <tr>
            <th width="160">Type</th>
            <th>How Kafka clients access the Kafka Service</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Keyless</strong></td>
            <td>Without credentials. Consumers don't subscribe to a Keyless plan.</td>
        </tr>
        <tr>
            <td><strong>API key</strong></td>
            <td>With the API key issued for their subscription.</td>
        </tr>
        <tr>
            <td><strong>OAuth2</strong></td>
            <td>With an OAuth2 token. The subscribing application needs a client ID.</td>
        </tr>
        <tr>
            <td><strong>JWT</strong></td>
            <td>With a JSON Web Token. The subscribing application needs a client ID.</td>
        </tr>
        <tr>
            <td><strong>mTLS</strong></td>
            <td>With a client certificate presented on the TLS connection.</td>
        </tr>
    </tbody>
</table>

## Which plans can be live together

On a Kafka Service, a plan is live while it's published or deprecated. The security types fall into three groups, and only one group can be live at a time:

* **Keyless**. At most one Keyless plan, and no other plan.
* **mTLS**. One or more mTLS plans.
* **Authentication**. One or more API key, JWT, and OAuth2 plans, in any mix.

A deprecated plan still counts as live. These rules apply when you publish a plan. Creating a plan of any type in **Staging** is always accepted, so you can prepare the plan that replaces a live one before you publish it.

## Create a plan

1. Open the plans of the Kafka Service.
2. Create the plan:
    * When the Kafka Service has no plan, the page shows **No plans yet**. Click **Create plan**. The form opens for a Keyless plan.
    * Otherwise, click **Create plan**, then select **Keyless**, **API key**, **OAuth2**, **JWT**, or **mTLS**.
3. Complete the plan form:

<table>
    <thead>
        <tr>
            <th width="220">Field</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Name</strong></td>
            <td>Required. The name shown in the plans list.</td>
        </tr>
        <tr>
            <td><strong>Security type</strong></td>
            <td>Read-only. The type you chose.</td>
        </tr>
        <tr>
            <td><strong>API key settings</strong>, <strong>JWT settings</strong>, or <strong>OAuth2 settings</strong></td>
            <td>API key, JWT, and OAuth2 plans only. The security configuration of the plan, built from the security policy.</td>
        </tr>
        <tr>
            <td><strong>Subscription validation</strong></td>
            <td><code>AUTO</code> accepts new subscriptions immediately. With <code>MANUAL</code>, the subscriptions that consumers request from the Developer Portal wait for someone to approve them. New plans use <code>MANUAL</code>.</td>
        </tr>
        <tr>
            <td><strong>Description</strong></td>
            <td>Optional. What the plan offers.</td>
        </tr>
    </tbody>
</table>

4. Click **Create plan**.

The console confirms with **Plan created**, and the plan appears under **Staging**.

## Publish, deprecate, or close a plan

Open the actions menu of the plan's row, then select the action. Each action asks for confirmation.

<table>
    <thead>
        <tr>
            <th width="140">Action</th>
            <th width="180">Offered for</th>
            <th>Effect</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Publish</strong></td>
            <td>Staging plans</td>
            <td>Makes the plan available for subscriptions. Kafka clients use a published Keyless plan without a subscription.</td>
        </tr>
        <tr>
            <td><strong>Deprecate</strong></td>
            <td>Published plans</td>
            <td>Existing subscriptions continue, and no new subscriptions are accepted.</td>
        </tr>
        <tr>
            <td><strong>Close</strong></td>
            <td>Staging, published, and deprecated plans</td>
            <td>Closes every active subscription of the plan. A closed plan can't be published again.</td>
        </tr>
    </tbody>
</table>

The console confirms with **Plan published**, **Plan deprecated**, or **Plan closed**.

The **Plans** page has no delete action. To retire a plan, deprecate it so that it takes no new subscriptions, then close it.

## Replace a live plan with another security type

When you publish a plan that can't be live together with the live plans, the console offers to close the live plans that block it. For example, publishing an API key plan while a Keyless plan is live closes the Keyless plan. Publishing a Keyless plan closes every live plan.

1. Create the new plan, and complete its security configuration.
2. In the actions menu of the new plan's row, select **Publish**.
3. Read the **Close current plan and publish?** dialog, titled **Close current plans and publish?** when it closes several plans. It explains the conflict and lists each plan that it closes, with its security type and status.
4. Click **Close & publish**.

The console closes the listed plans, then publishes the new one, and confirms with, for example, **Plan published, 1 plan closed**.

{% hint style="warning" %}
Closing a plan also closes its active subscriptions. Kafka clients that use the closed plans lose access immediately, and the closure can't be undone. Before you publish the new plan, make sure that its consumers have subscriptions and credentials ready.
{% endhint %}

If the closures succeed but the publication fails, the dialog stays open as **Publish plan?**, and **Publish** retries the publication alone.

## Edit or reorder plans

* To edit a plan, click its name, or select **Edit** in its actions menu. The name, the security configuration, the subscription validation, and the description can change. Click **Save changes**. The console confirms with **Plan updated**.
* To reorder the plans, click the up or down arrow of a row. The arrows move the plan within the plans of the selected status.

## Verification

To verify that a plan is ready for Kafka clients, follow these steps:

1. Open the plans of the Kafka Service.
2. Click the **Published** card.
3. Check that the plan is listed with the security type and the validation mode you expect, and that no plan of a conflicting type is listed under **Published** or **Deprecated**.

## Next steps

* [Manage subscriptions](manage-subscriptions.md)
* [Start, stop, and deploy a Kafka Service](start-stop-and-deploy-a-kafka-service.md)
