---
description: See the other agents an agent calls through an A2A Proxy subscription in Gamma. Find the gateway proxy that fronts each one.
---

# Read the agents an agent calls

The **Agents** page lists other agents a registered agent can call through an A2A Proxy that its gateway application subscribes to.

This page works the same way as [Read the models an agent uses](subscribe-an-agent-to-an-llm-proxy.md). A subscription is created on the proxy, in the Developer Portal, through automation, or a similar path. The page lists the result.

A source does not yet report which agents its agent calls, so there is no row from the provider. The page says **Depending on the provider, some of the agents this agent calls may not be listed here.**

## Open the Agents page

1. In the Gamma console, open **Agent Management**.
2. In the **Catalog** section of the sidebar, select **Agents**.
3. Click the agent's name.
4. In the **Access** section of the agent's sidebar, click **Agents**.

The heading is **Agents**. The description reads **Other agents this one can call through the agent proxies it subscribes to on the gateway.**

## Read the agents

**Search name, proxy** filters the rows. When nothing matches, the page reads **No matching related agents** and offers **Clear filters**. Every row goes through the gateway, so the page has no **Gateway status** filter and no count of how many go through the gateway.

The following table describes the columns:

<table>
    <thead>
        <tr>
            <th width="180">Column</th>
            <th>What it shows</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Name</strong></td>
            <td>The name of the agent the proxy fronts. A proxy created on an address, with no agent in the Catalog, shows the proxy's name.</td>
        </tr>
        <tr>
            <td><strong>Entity ID</strong></td>
            <td>The identifier of the proxy, which you can copy.</td>
        </tr>
        <tr>
            <td><strong>Type</strong></td>
            <td><strong>A2A agent</strong> when the proxy fronts an agent in the Catalog. <strong>A2A proxy</strong> when it fronts an address only.</td>
        </tr>
        <tr>
            <td><strong>Gateway proxy</strong></td>
            <td>The proxy's context path, or its name when it has no context path. It links to the proxy's <strong>Overview</strong> when you can read APIs.</td>
        </tr>
        <tr>
            <td><strong>Source</strong></td>
            <td><strong>Proxied on Gateway</strong>.</td>
        </tr>
    </tbody>
</table>

Several proxies in front of the same Catalog agent are one row. The first subscription stands for that agent.

## When the agent calls no other agent through the gateway

The page reads **No related agents**, followed by one of the following messages:

* For an agent synced from a provider, the message reads **No related agents were imported from &lt;source&gt;, and this agent is not subscribed to an A2A proxy. An agent calls other agents through Gravitee by subscribing to their A2A proxy.**
* For any other agent, the message reads **This agent is not subscribed to an A2A proxy, so it cannot call other agents through Gravitee. Consuming an agent requires subscribing to its A2A proxy.**

The steps are the same as on **Models**. The proxy step reads **Subscribe the agent to an A2A proxy** and **Pick the proxy in front of the agent you want to call.** **Open A2A Proxies**, or **Subscribe to an A2A proxy** once the agent has an application, opens the **A2A Proxies** page under **Secure**. The last step reads **The agent appears here.** The agent behind the proxy is listed on this tab, marked **Proxied on Gateway**.

A pending subscription reads **waiting for approval**, and a paused one reads **paused**. The agent appears once it is accepted or resumed. When the subscriptions cannot be read, the page reads **Could not load the gateway subscriptions of this agent** and offers **Retry**.

## Next steps

* [Read the models an agent uses](subscribe-an-agent-to-an-llm-proxy.md). Read how models work, and where a subscription is created.
* [Route an agent through an A2A Proxy](route-an-agent-through-an-a2a-proxy.md). See how an A2A Proxy is put in front of an agent.
* [Manage subscriptions](../publish/manage-subscriptions.md). Approve, pause, or close the subscription from the proxy's side.
