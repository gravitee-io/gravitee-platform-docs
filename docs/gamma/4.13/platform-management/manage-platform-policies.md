---
hidden: false
noIndex: false
description: Platform flows apply policies to the request and response phases of every API in the organization. Create, order, tag, and deploy them from the Gamma console.
---

# Manage platform policies

A platform flow is a policy flow that belongs to the organization rather than to a single API. The gateway runs the request policies of a platform flow before each API's own flows, and its response policies after them. One platform flow applies a cross-cutting policy, such as a rate limit or a header transformation, to every API in the organization at once. Restrict a flow to a group of gateways by giving it sharding tags.

Platform flows belong to the organization, and the Policy Studio of the **Organization** section in the Gamma console creates, edits, orders, and deletes them. Saving deploys the flows to the gateways of the organization. The APIM Console edits the same flows, so a flow saved in either console appears in both.

## Open the organization's Policy Studio

The page sits in the **Design** group of the **Organization** section, with the other settings that apply across environments.

To open it, complete the following steps:

1. From the Gamma console sidebar, select **Platform Management**.
2. Open the **Organization** section.
3. Under **Design**, select **Policy Studio**.

The page is listed only for a role that reads the organization's policies. If your role reads them but doesn't update them, the studio opens read-only. You can inspect the flows and their policy steps. The controls that add, edit, reorder, or delete a flow or a step are hidden, and so is the **Save** button.

A banner at the top of the page states the scope of what you're editing. It reads: "Platform flows run on the request and response phases of every API in this organization, before and after each API's own flows. Native Kafka APIs have no such phases and are left untouched."

<!-- TODO: Screenshot of the organization's Policy Studio, showing the scope banner, the Platform flows sidebar with two flows, and the Request Phase and Response Phase canvas -->
<figure><img src="../.gitbook/assets/PLACEHOLDER-gamma-platform-policy-studio.png" alt=""><figcaption><p>The Policy Studio of the <strong>Organization</strong> section, with the platform flows in the sidebar and the two phases on the canvas</p></figcaption></figure>

## Understand where platform flows run

Platform flows run on API proxies, on APIs with a v2 definition, and on the LLM, MCP, and A2A Proxies of Agent Management. They don't run on native Kafka APIs, which have no request and response phases.

For each request, the gateway runs the **Request Phase** policies of the matching platform flows before the API's security checks and flows. It runs their **Response Phase** policies after the API's flows, even when the API's own processing ended in an error or a timeout.

A flow with no sharding tags is loaded by every gateway of the organization. When a flow carries tags, a gateway configured with sharding tags loads it only when one of the flow's tags is among the gateway's tags. The gateway also skips the flow when one of its tags is a tag the gateway excludes. A gateway with no sharding tags in its configuration file loads every platform flow, whether the flow carries tags or not.

## Read the studio

The sidebar lists the platform flows under **Platform flows**, in the order the gateway runs them. Each row shows the following details:

* The flow's path, with `/**` appended when the operator is **Starts With**.
* Badges for its HTTP methods, or an `ALL` badge.
* A `Conditioned` badge when the flow carries a condition.
* A tag badge with the number of sharding tags when the flow is restricted to some gateways. Hover over the badge to read the tag names.

The `Search flows...` field filters the list on the flow name, the path, and the methods.

Selecting a flow opens it on the canvas. The **Request Phase** runs from the client to the gateway, and the **Response Phase** runs from the gateway back to the client. The bar above the canvas names the selected flow, lists its tags, and holds the **Save** button.

When the organization has no platform flow yet, the studio opens on an explanatory screen with an **Add platform flow** link.

## Create a platform flow

To create a platform flow, complete the following steps:

1. Select **Add platform flow** in the sidebar, or on the explanatory screen when the organization has no flow yet.
2. In the **Create a new platform flow** panel, enter the flow details described in the following table:

    | Field | Description |
    | ----- | ----------- |
    | **Flow name** | The name shown in the sidebar. When you leave it empty, the studio names the flow after its path and methods, for example `/orders [GET, POST]`. |
    | **Operator** | **Equals** matches the request path exactly. **Starts With** matches every request path that begins with the path. |
    | **Path** | The request path the flow applies to. A leading `/` is added on save, and an empty path becomes `/`. |
    | **HTTP methods** | The methods the flow applies to. Leave the field empty to match all methods. |
    | **Condition** | An Expression Language condition the request must satisfy for the flow to run, for example `{#request.headers['x-custom'] == 'value'}`. |
    | **Tags** | The sharding tags of the gateways that load the flow. Leave the field empty to apply the flow on every gateway. The field appears only when the organization has sharding tags. |

3. Select **Create**.

The new flow is enabled and has no policy step yet.

## Add policies to a platform flow

The canvas holds the policy steps of the selected flow, in the order they run, on the **Request Phase** and on the **Response Phase**.

To add a step, complete the following steps:

1. Select the flow in the sidebar.
2. On the phase, select **Add policy**, or the **+** button at the end of the step row when the phase already holds a step.
3. Search the list and select a policy to add it, or select **Browse full catalog** to open the **Add Policy** catalog. In the catalog, filter by category, select a policy to read its documentation, and select **Add to flow**.
4. Complete the policy's configuration form in the panel that opens.

The catalog lists the policies that run on the phase you're adding to for any API type, together with the policies that don't declare which phases they support. Policies that only run on native Kafka phases aren't listed.

Work on an existing step from the canvas:

* Select the step to reopen its configuration panel.
* Drag the step to change where it runs in the order.
* Open the step's actions menu and clear **Enabled** to keep the step without running it, select **Duplicate** to copy it, or select **Remove** to take it out.

## Edit, reorder, disable, or delete a platform flow

Open the actions menu of a flow from its row in the sidebar, or from the bar above the canvas for the selected flow. The menu offers the following actions:

* `Edit flow...` opens the **Edit flow** panel, with the same fields as at creation. Select **Save** to apply the changes.
* **Duplicate flow**, in the sidebar menu only, adds a copy of the flow named after the original with ` - Copy` appended.
* **Enabled**, when cleared, keeps the flow in the list without running it. The gateway skips a disabled flow.
* **Delete flow** asks for confirmation, then removes the flow from the list.

Drag a flow in the sidebar to change its position. The gateway runs the matching flows in the order of the list.

None of these changes reaches the gateways until you save.

## Set the flow execution mode

The execution mode decides what the gateway does when several platform flows match one request. To set it, select the **Flow execution settings** button at the top of the sidebar, then choose a **Mode**:

* **Default**. The gateway runs every enabled flow whose path, methods, and condition match the request.
* **Best match**. Among the flows that match, the gateway runs only the one whose path is closest to the request path. Path segments are compared from left to right, and a segment that equals the request segment outranks a path parameter, which outranks a segment that differs.

Unlike the Policy Studio of an API proxy, the organization's studio has no **Match required** setting. The mode is saved together with the flows.

## Save and deploy platform flows

Saving writes the flows and the execution mode to the organization and deploys them to its gateways. The other settings of the organization are left as they are.

To save, complete the following steps:

1. Select **Save** on the bar above the canvas. The button stays disabled until you change something. It also stays disabled while a step's configuration is incomplete, and its tooltip then counts the steps to fix.
2. In the **Deploy the policies?** dialog, select **Save and deploy**. The dialog reads: "Platform policies are automatically deployed on gateways. Every HTTP API in this organization runs the updated flows as soon as they are saved." Select **Cancel** instead to keep your changes in the studio without saving them.

The console confirms with `Platform policies successfully updated!`. When the save fails, it reports `An error occurred while updating the platform policies.`, your changes stay in the studio, and the **Save** button carries the error in its tooltip.

## Next steps

* [Manage entrypoints and sharding tags](manage-entrypoints-and-sharding-tags.md). Create the sharding tags that restrict a platform flow to a group of gateways.
* [Control how policy flows are matched to requests](../api-management/build/configure-your-api-proxy/configure-flow-execution.md). Set the execution mode of the flows of a single API proxy.
