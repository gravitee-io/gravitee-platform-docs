---
hidden: false
noIndex: false
description: Add a flow and Kafka policies to a Kafka Service in the Event Stream Management Policy Studio, for client connections, Kafka interactions, and the messages clients produce and consume. Follow the steps to design them.
---

# Design flows in the Policy Studio

The Policy Studio of a Kafka Service holds its flows. A flow applies Kafka policies, such as ACLs, topic mapping, quotas, or message filtering, to the traffic of the Kafka Service in four phases, spread over two tabs:

* The **Global** tab holds the **Connect Phase**, for policies applied when the client connects to the gateway, before authentication, and the **Interact Phase**, for policies applied on all interactions between the client and the gateway.
* The **Event Messages** tab holds the **Publish Phase**, for policies applied when clients publish messages to the broker, and the **Subscribe Phase**, for policies applied when clients consume messages from the broker.

Unlike a Message API flow, a Kafka Service flow has no channel, operation, or condition: it applies to all the traffic of its scope.

## Open the Policy Studio

1. From the Gamma console, open **Event Stream Management**.
2. In the **APIs** group of the sidebar, click **Kafka Services**.
3. Click the name of the Kafka Service.
4. In the **Design** group of the Kafka Service sidebar, click **Policy Studio**.

## Choose where a flow applies

The flows list on the left has two sections:

* **Plan Flows**. The flows attached to a plan, listed under the name of their plan. A plan flow applies to the traffic of that plan only. A plan appears here once it holds a flow.
* **Common Flows**. The flow that applies to all traffic, whatever the plan.

A Kafka Service holds at most one common flow, and at most one flow per plan. The flow panel recalls it with **Only one flow is allowed for a native API.**, and the Management API refuses to save a second flow with **Native APIs cannot have more than one flow**.

A plan flow needs a plan to attach to, so **Plan Flows** accepts a flow only for a plan that is published or deprecated. See [Manage plans](manage-plans.md).

## Add a flow

1. Click the add icon next to **Plan Flows** or **Common Flows**. While no plan holds a flow, **Add plan flow** under **Plan Flows** opens the same panel.
2. In the **Create a new plan flow** or **Create a new common flow** panel, complete the fields:
    * **Flow name**. The name of the flow.
    * **Associated plan**. Plan flows only. The plan whose traffic the flow applies to.
3. Click **Create**.

To change a flow later, select it and open its actions menu. The same menu turns the flow off and deletes it.

## Add policies to the phases

1. Select the flow in the flows list.
2. Click the **Global** tab or the **Event Messages** tab.
3. On the phase that needs the policy, click **Add policy**. When the phase already holds a policy, click its add icon instead.
4. Search the catalog, then select the policy.
5. Complete the policy's configuration.

The catalog lists the policies installed on your platform that support the phase for Kafka APIs. It also lists, under **Shared Policy Group**, the shared policy groups of the environment that were built for Kafka APIs and for that phase.

## Save the flows

1. Click **Save**.

Saving writes the flows to the Kafka Service but doesn't deploy them. The Kafka Service then shows **Out of sync**, and the gateway applies the new flows at the next deployment. To deploy, click **Deploy** in the page header. Before 4.13, saving in the Policy Studio of a Kafka Service also deployed it.

If the save fails, the **Save** button turns red, and its tooltip starts with **Save failed:** followed by the reason.

## Verification

To verify that the flows are in place, follow these steps:

1. Reload the **Policy Studio** page, and check that your flows and their policies are listed.
2. Deploy the Kafka Service, and check that the header of the Kafka Service sidebar shows **Deployed**.
