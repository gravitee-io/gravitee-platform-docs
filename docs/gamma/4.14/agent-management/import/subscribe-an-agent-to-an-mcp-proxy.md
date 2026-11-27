---
description: See the tools an agent calls in Gamma, reported by its provider or granted by an MCP Proxy subscription. Find which calls go through the gateway.
---

# Read the tools an agent calls

The **Tools** page lists the tools a registered agent calls. A tool is either reported by the agent's source or reached through an MCP Proxy that the agent's gateway application subscribes to.

This page works the same way as [Read the models an agent uses](subscribe-an-agent-to-an-llm-proxy.md). A subscription is created on the proxy, in the Developer Portal, through automation, or a similar path. The page lists the result.

## Open the Tools page

1. In the Gamma console, open **Agent Management**.
2. In the **Catalog** section of the sidebar, select **Agents**.
3. Click the agent's name.
4. In the **Access** section of the agent's sidebar, click **Tools**.

The heading is **Tools**. The description reads **What this agent calls, and whether those calls go through the gateway.**

## Read the tools

Before the table, a count reads **&lt;n&gt; of &lt;m&gt; tools go through the gateway**. **Search name, description, URL, type, proxy** filters the rows. **Gateway status** filters them further: **All gateway statuses**, **Through the gateway**, and **Direct to upstream**. **Reset** clears a filter. When nothing matches, the page reads **No matching tools** and offers **Clear filters**.

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
            <td>The tool's name, with its description and address underneath when the source reported them. A tool reached only through a subscription shows the MCP Proxy's name.</td>
        </tr>
        <tr>
            <td><strong>Entity ID</strong></td>
            <td>The identifier of the proxy, which you can copy. A tool that does not go through the gateway reads <strong>Not governed yet</strong>.</td>
        </tr>
        <tr>
            <td><strong>Type</strong></td>
            <td><strong>MCP server</strong> when the source type is MCP, and when the row is a subscribed proxy with no linked tool. Any other type is the value the source reported. An empty type shows a dash.</td>
        </tr>
        <tr>
            <td><strong>Gateway proxy</strong></td>
            <td>The proxy's context path, or its name when it has no context path. It links to the proxy's <strong>Overview</strong> when you can read APIs. A tool that does not go through the gateway shows a dash.</td>
        </tr>
        <tr>
            <td><strong>Source</strong></td>
            <td><strong>Proxied on Gateway</strong> for a subscription. Otherwise <strong>Declared on the agent</strong>, or <strong>&lt;source&gt; imported</strong> for an agent synced from a provider.</td>
        </tr>
    </tbody>
</table>

Tools the source declares come first. A declared tool that is linked to an MCP Proxy the agent subscribes to is one row, badged **Proxied on Gateway**. A subscribed proxy that no declared tool is linked to is its own row, named for the proxy, with type **MCP server**.

## When the agent has no tools

The page reads **No tools**, followed by one of the following messages:

* For an agent synced from a provider, the message reads **No tools were imported from &lt;source&gt;, and this agent is not subscribed to an MCP proxy. An agent calls tools through Gravitee by subscribing to an MCP proxy.**
* For any other agent, the message reads **This agent is not subscribed to an MCP proxy, so it cannot call tools through Gravitee. An agent gets its tools by subscribing to an MCP proxy.**

The steps are the same as on **Models**. The proxy step reads **Subscribe the agent to an MCP proxy** and **Pick the proxy in front of the MCP server whose tools you need.** **Open MCP Proxies**, or **Subscribe to an MCP proxy** once the agent has an application, opens the **MCP Proxies** page under **Secure**. The last step reads **The proxy's tools appear here.** Each tool behind the proxy is listed on this tab, marked **Proxied on Gateway**.

A pending subscription reads **waiting for approval**, and a paused one reads **paused**. The tools appear once it is accepted or resumed. When the subscriptions cannot be read, the page reads **Could not load the gateway subscriptions of this agent** and offers **Retry**.

## Next steps

* [Read the models an agent uses](subscribe-an-agent-to-an-llm-proxy.md). Read how models work, and where a subscription is created.
* [Create an MCP proxy](../build/create-an-mcp-proxy.md). Create the proxy the agent subscribes to.
* [Manage subscriptions](../publish/manage-subscriptions.md). Approve, pause, or close the subscription from the proxy's side.
