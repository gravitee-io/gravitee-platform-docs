---
description: Models, Tools, and Agents list what a provider reported and what a subscription grants the agent. You subscribe on the proxy, in the Developer Portal, through automation, or a similar path.
---

# Read the models an agent uses

**Models**, **Tools**, and **Agents** sit under **Access** on a registered agent. Each page lists two kinds of entry:

* Models, tools, and agents reported by the provider source.
* Models, tools, and agents the agent reaches through a subscription on its gateway application.

| Page | From the provider source | From a subscription |
| --- | --- | --- |
| **Models** | Models the source reported | Models an LLM Proxy routes for a subscription on this agent |
| **Tools** | Tools the source reported | Tools an MCP Proxy exposes for a subscription on this agent |
| **Agents** | Other agents the source reported | Other agents an A2A Proxy fronts for a subscription on this agent |

A subscription is created on the proxy, in the Developer Portal, through automation, or a similar path. These pages list the result. An accepted subscription appears as rows marked **Proxied on Gateway**. A pending subscription reads **waiting for approval**, and a paused one reads **paused**. Their models, tools, or agents appear once the subscription is accepted or resumed.

[Read the tools an agent calls](subscribe-an-agent-to-an-mcp-proxy.md) and [Read the agents an agent calls](read-the-agents-an-agent-calls.md) use the same layout for tools and other agents. The Agents page lists subscription rows. A source does not yet report which agents its agent calls.

## Open the Models page

1. In the Gamma console, open **Agent Management**.
2. In the **Catalog** section of the sidebar, select **Agents**.
3. Click the agent's name.
4. In the **Access** section of the agent's sidebar, click **Models**.

The heading is **Models**. The description reads **Every model this agent uses — reported from a source or routed through the Gravitee API gateway.**

## Read the models

Above the table, a count reads **&lt;n&gt; of &lt;m&gt; models go through the gateway**. **Search model, proxy** filters the rows. **Gateway status** filters them further: **All gateway statuses**, **Through the gateway**, and **Direct to the provider**. **Reset** clears a filter. When nothing matches, the page reads **No matching models** and offers **Clear filters**.

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
            <td>For a model the source declares, <strong>Provider inference</strong> when the agent is synced from a provider, and <strong>Declared model</strong> otherwise. For a model reached through a subscription, the name of the LLM Proxy.</td>
        </tr>
        <tr>
            <td><strong>Entity ID</strong></td>
            <td>The identifier of the proxy, which you can copy. A model that does not go through the gateway reads <strong>Not governed yet</strong>.</td>
        </tr>
        <tr>
            <td><strong>Model</strong></td>
            <td>The model name. A subscribed proxy that routes no model leaves this cell empty, so the subscription stays visible. That row is not counted as a model.</td>
        </tr>
        <tr>
            <td><strong>Gateway proxy</strong></td>
            <td>The proxy's context path, or its name when it has no context path. It links to the proxy's <strong>Overview</strong> for a user who can read APIs. A model that does not go through the gateway shows a dash.</td>
        </tr>
        <tr>
            <td><strong>Source</strong></td>
            <td><strong>Proxied on Gateway</strong> for a subscription. Otherwise <strong>Declared on the agent</strong>, or <strong>&lt;source&gt; imported</strong> for an agent synced from a provider.</td>
        </tr>
    </tbody>
</table>

Models the source declares come first. A declared model that is linked to an LLM Proxy the agent subscribes to is one row, badged **Proxied on Gateway**. The same name with no link, and also routed by a proxy, stays two rows.

When the agent has models listed and no gateway application yet, the page reads **Gateway subscriptions need a gateway application, which the agent gets with its identity.** **Go to Identity** opens the **Identity** page, for a user who can update the Catalog.

## When the agent has no models

The page reads **No models**.

* For an agent synced from a provider: **No models were imported from &lt;source&gt;, and this agent is not subscribed to an LLM proxy. An agent calls models through Gravitee by subscribing to an LLM proxy.**
* For any other agent: **This agent is not subscribed to an LLM proxy, so it cannot call models through Gravitee. An agent gets its models by subscribing to an LLM proxy.**

Three steps follow, under **How to connect**:

1. **Give the agent a gateway application.** Subscriptions belong to an application. Create it on the Identity tab. **Create application on Identity** opens that page, for a user who can update the Catalog.
2. **Subscribe the agent to an LLM proxy.** **Pick the proxy that routes the models you need. The subscription gives the agent its credential.**
3. **The proxy's models appear here.** Each model the proxy routes is listed on this tab, marked **Proxied on Gateway**.

The second step is one way in. **Open LLM Proxies**, or **Subscribe to an LLM proxy** once the agent has an application, opens **Secure** → **LLM Proxies**. The same subscription can be created on that proxy, in the Developer Portal, through automation, or a similar path. A user who cannot take the next step reads **Ask an agent administrator to subscribe this agent.**

When the subscriptions cannot be read, the page reads **Could not load the gateway subscriptions of this agent** and offers **Retry**. The empty state then reads **What this agent reaches through the gateway could not be read.**

## Next steps

* [Read the tools an agent calls](subscribe-an-agent-to-an-mcp-proxy.md). The same page for tools, through an MCP Proxy.
* [Read the agents an agent calls](read-the-agents-an-agent-calls.md). The same page for other agents, through an A2A Proxy.
* [Expose your agent with an LLM Proxy](../build/create-an-llm-proxy.md). Create the proxy the agent subscribes to.
* [Publish a proxy to the Developer Portal](../publish/publish-a-proxy-to-the-developer-portal.md). Offer the proxy where a consumer can subscribe.
* [Manage subscriptions](../publish/manage-subscriptions.md). Approve, pause, or close the subscription from the proxy's side.
