---
hidden: true
noIndex: true
description: The Tools page of an agent lists the tools its platform declares and the MCP Proxies that front them. Follow the steps to subscribe the agent's application to a proxy.
---

# Subscribe an agent to an MCP Proxy

An agent calls a tool on an MCP server, and the AI Gateway governs that call when the agent reaches the server through an MCP Proxy instead of directly. The agent's **Tools** page lists the tools the agent is configured with, the MCP Proxies that front the same servers, and, for each proxy, either the subscription the agent's gateway application already holds or the plans it could take. You subscribe and unsubscribe from the same page.

The agent's gateway application is the application that acts for the agent at the AI Gateway. Subscriptions belong to it, so the page can't subscribe until the agent has one. The page tells you so and points you to the agent's **Identity** page, where the application is created.

## Open the Tools page

1. From the Gamma console sidebar, select **Agent Management**.
2. In the **Catalog** section of the sidebar, select **Agents**.
3. Click the agent's name.
4. In the **Agent** section of the agent's sidebar, click **Tools**.

<!-- TODO: Screenshot of the Tools page of an agent, showing a declared MCP server card with a proxy block under it -->

<figure><img src="../.gitbook/assets/PLACEHOLDER-gamma-aim-agent-tools.png" alt=""><figcaption><p>The Tools page of an agent</p></figcaption></figure>

## Where the declared tools come from

The tools on the page are the ones the agent's platform declares for it. Gamma reads them when it synchronizes an agent from Azure AI Foundry, and it reads them again on every synchronization, so a tool removed on the platform disappears from the page after the next run. Gamma keeps up to 64 declared tools per agent. An agent registered by hand declares no tool, so its page holds only the cards its subscriptions bring.

For each declared tool, Gamma records its type, its name, the server address it points at, and the list of tools the agent may call on that server. Headers, credentials, and connection references from the platform are never read. The server address is stored without any user information, query string, or fragment.

## Read the page

The page shows one card per declared tool, in the order the platform lists them, followed by one card per MCP server that the agent reaches through a subscription but that no declared tool names. Each card carries the tool's name, a badge with its type as the platform spells it, and a **declared by the platform** badge when the platform declared it. A card built from a subscription reads **Reached through a line the agent holds, not declared by its platform.** instead.

A declared MCP server card shows the server address and how the platform restricts the agent on that server:

<table>
    <thead>
        <tr>
            <th width="260">Restriction the platform recorded</th>
            <th>What the card reads</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>No restriction</td>
            <td><strong>Every tool on this server</strong></td>
        </tr>
        <tr>
            <td>An empty list of allowed tools</td>
            <td><strong>No tool on this server</strong></td>
        </tr>
        <tr>
            <td>A list of allowed tools</td>
            <td><strong>Restricted to</strong> followed by the tool names</td>
        </tr>
    </tbody>
</table>

Under the card, the page lists every MCP Proxy that fronts the same server. A proxy fronts a server when its server URL and the declared address are the same after Gamma ignores the case of the scheme and host and any trailing slash. The path is compared as written. The cards for tools that no proxy can front read as follows:

* A tool that isn't an MCP tool: **Not an MCP tool, so no proxy can carry it. The agent calls it wherever its platform sends it.**
* An MCP tool with no server address: **The platform names no address for this server, so no proxy can be matched to it.**
* An MCP server that no proxy you can open fronts: **No MCP proxy you can open fronts this server.**

Each proxy block shows the proxy's name, which links to the proxy, an **MCP proxy** badge, and a **subscribed** badge when the application holds a subscription on it. The **Policies & guardrails** button opens the proxy's Policy Studio. What follows in the block depends on whether the application already holds a subscription on the proxy:

<table>
    <thead>
        <tr>
            <th width="260">State</th>
            <th>What the block shows</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>The application holds a subscription</td>
            <td>A <strong>Plan</strong> row with the plan's name and the subscription status, <strong>Pending</strong>, <strong>Accepted</strong>, or <strong>Paused</strong>. A <strong>Client ID</strong> row when the subscription carries one. A <strong>Call path</strong> row with the proxy's context path. A <strong>Credential</strong> row with a <strong>Read the key on the subscription</strong> link, which opens the subscription on the proxy's <strong>Consumers</strong> page. The page never shows the key itself. An <strong>Unsubscribe</strong> button.</td>
        </tr>
        <tr>
            <td>No subscription, and the proxy publishes plans</td>
            <td>One row per published plan, with the plan's name and its security badge: <strong>Keyless</strong>, <strong>API Key</strong>, or <strong>OAuth2</strong>. A keyless plan reads <strong>Keyless: no subscription needed</strong>. Every other plan carries a <strong>Subscribe</strong> button.</td>
        </tr>
        <tr>
            <td>No subscription, and the proxy publishes no plan</td>
            <td><strong>No published plan to subscribe to yet. Publish one on &lt;proxy&gt;, then come back.</strong> The proxy's name links to its <strong>Plans</strong> page.</td>
        </tr>
    </tbody>
</table>

An OAuth2 plan needs a client ID on the application. When the application has none, the plan's row reads **needs a client id, attach an OAuth identity on Identity** and its **Subscribe** button stays disabled. An API Key plan has no such requirement.

The page shows the tools and subscriptions to anyone who can read the Catalog. The **Subscribe**, **Unsubscribe**, and **Subscribe to an MCP proxy** controls appear only for users who can update the Catalog.

The link at the bottom of the page, **See what this agent was observed reaching**, opens the agent's **Lineage** page.

## Subscribe from a tool's card

To take a plan on a proxy that fronts one of the agent's declared servers, follow these steps:

1. On the **Tools** page, find the server and the proxy that fronts it.
2. In the plan's row, click **Subscribe**.

A **Subscribed** notification appears, and the block switches to the subscription's rows, with the plan and the subscription's status.

## Subscribe to any MCP Proxy

When no card lists the proxy you want, subscribe through the picker instead. The picker lists every MCP Proxy you can see, whether it fronts one of the agent's declared servers.

1. On the **Tools** page, click **Subscribe to an MCP proxy**. The button is disabled until the agent has a gateway application.
2. In the **Subscribe to an MCP proxy** dialog, select the proxy under **MCP proxy**. The list holds the first 100 proxies. When the environment has more, the dialog says so and asks you to subscribe from the proxy itself.
3. Select a plan under **Plan**. The list holds the proxy's published plans other than keyless plans. An OAuth2 plan reads **needs a client id, attach an OAuth identity on Identity** and can't be selected while the application has no client ID. When the proxy publishes no plan a subscription can take, the dialog reads **This proxy publishes no plan a subscription can take. Publish one on the proxy, then come back.**
4. Click **Subscribe**.

## Unsubscribe

Unsubscribing closes the subscription. It can't be reopened, so giving the agent the same proxy again means subscribing to a plan afresh.

1. On the **Tools** page, in the proxy's block, click **Unsubscribe**.
2. In the **Unsubscribe from &lt;proxy&gt;?** dialog, click **Unsubscribe**.

A **Subscription closed** notification appears.

## Next steps

* [Subscribe an agent to an LLM Proxy](subscribe-an-agent-to-an-llm-proxy.md). Give the agent's application access to the models an LLM Proxy routes.
* [Manage subscriptions](../publish/manage-subscriptions.md). Approve, reject, or close the subscription from the proxy's side, and read its credentials.
* [Manage a registered agent](manage-a-registered-agent.md). Find your way around the rest of the agent's page.
