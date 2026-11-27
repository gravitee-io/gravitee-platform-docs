---
description: Manage a registered agent in the Agent Management Catalog. Read its Overview, change its owner, publish or retire it, and learn what each page offers.
---

# Manage a registered agent

When you register an agent, the Gamma console opens the agent's page in the Catalog. The page is the hub for the agent. Its **Overview** shows who owns it and what the Catalog records about it. The sidebar leads to the pages that give it an identity, endpoints, models, tools, and other agents. The actions on the **Overview** page change its state in the Catalog. Come back to it to publish the agent, to change its owner, to route its calls through the AI Gateway, or to remove it.

## Open an agent's page

Immediately after you register an agent, the console opens the new agent's page for you. To return to it later, follow these steps:

1. In the Gamma console, open **Agent Management**.
2. In the **Catalog** section of the sidebar, select **Agents**.
3. Click the agent's name. Optional: To find it in a long list, type part of its name, description, or skill in the search box.

The **Agents** page lists agents added directly or synced from connected providers. By default it shows the **Name**, **Catalog state**, **Entity ID**, **Source**, and **Sponsor** columns. Use **Toggle columns** to show the **Owner**, **Risk classification**, **Last updated**, **Description**, and **Version** columns, and use **Column order** to arrange them. You can switch between **Table view** and **Card view**.

The actions menu at the end of each row offers **View agent**, **Edit details**, **Publish** or **Unpublish**, **Retire agent**, and **Remove**. **Edit details** appears only for an agent registered by hand that isn't retired.

## Read the Overview

The **Overview** is the first page of the agent. Its header carries the following fields:

<table>
    <thead>
        <tr>
            <th width="220">Field</th>
            <th>What it shows</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Name</strong></td>
            <td>The agent's name. The sidebar header also shows the version as a badge and the Entity ID.</td>
        </tr>
        <tr>
            <td><strong>State</strong></td>
            <td>The agent's catalog state. See <a href="#change-the-catalog-state">Change the catalog state</a>.</td>
        </tr>
        <tr>
            <td><strong>Owner</strong></td>
            <td>The user who owns the agent.</td>
        </tr>
        <tr>
            <td><strong>Sponsor</strong></td>
            <td>The user accountable for the agent.</td>
        </tr>
        <tr>
            <td><strong>Agent identity</strong></td>
            <td>The OAuth client ID of the agent's identity.</td>
        </tr>
    </tbody>
</table>

Under the header, a setup guide lists the steps that connect the agent to the gateway. The steps are to give it an identity, connect models through an LLM Proxy, connect tools through an MCP Proxy, and expose the agent through an A2A Proxy. Each step opens the page that completes it, and **Show steps** and **Hide steps** open and close the guide.

A summary of the agent's connections follows. A **Provider** tile reads **Synced from the provider** for an imported agent. A tile for each of **Models**, **Tools**, and **Related agents** shows how many connections go through the gateway. A tile with no connections reads **No models yet.**, **No tools yet.**, or **No related agents yet.** An exposure tile reads **Exposed** when an A2A Proxy fronts the agent and runs. It reads **Proxy stopped** when the proxy doesn't run, and **No A2A proxy in front of it** when none exists.

The **Overview** then lists the details the Catalog records:

<table>
    <thead>
        <tr>
            <th width="220">Detail</th>
            <th>What it holds</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Entity ID</strong></td>
            <td>The stable identifier other Gamma modules use.</td>
        </tr>
        <tr>
            <td><strong>ID</strong></td>
            <td>The identifier of the agent in the Catalog.</td>
        </tr>
        <tr>
            <td><strong>Description</strong></td>
            <td>The agent's description.</td>
        </tr>
        <tr>
            <td><strong>Version</strong></td>
            <td>The agent's version.</td>
        </tr>
        <tr>
            <td><strong>Source</strong></td>
            <td>Where the agent came from.</td>
        </tr>
        <tr>
            <td><strong>Provider state</strong></td>
            <td>The provider's own state for the agent. It appears only for an agent synced from a provider.</td>
        </tr>
        <tr>
            <td><strong>Risk classification</strong></td>
            <td>The agent's risk rating.</td>
        </tr>
        <tr>
            <td><strong>Created</strong></td>
            <td>When the agent was added to the Catalog.</td>
        </tr>
        <tr>
            <td><strong>Last updated</strong></td>
            <td>When the agent's record last changed.</td>
        </tr>
    </tbody>
</table>

When the agent has an A2A card, a summary of it follows, with its **Version**, **Description**, and **Skills**, or **None declared**. **View on Endpoints** opens the **Endpoints** page.

## Find your way around the sidebar

The agent's sidebar has two groups. Each entry is a page of its own.

<table>
    <thead>
        <tr>
            <th width="140">Group</th>
            <th width="160">Entry</th>
            <th>What the page does</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Agent</strong></td>
            <td><strong>Overview</strong></td>
            <td>This page.</td>
        </tr>
        <tr>
            <td><strong>Agent</strong></td>
            <td><strong>Identity</strong></td>
            <td>Manages the agent's identity, which it uses to prove who it is, for delegated access, for authorization policies, and for observability. The page shows its <strong>OAuth client ID</strong>, <strong>Agent Identity Provider</strong>, and <strong>Gateway application</strong>.</td>
        </tr>
        <tr>
            <td><strong>Agent</strong></td>
            <td><strong>Endpoints</strong></td>
            <td>Lists each endpoint of the agent by <strong>Type</strong>, <strong>Endpoint</strong>, and <strong>Gateway proxy</strong>. For an agent registered by hand, it also holds the A2A Agent Card. See <a href="route-an-agent-through-an-a2a-proxy.md">Route an agent through an A2A Proxy</a>.</td>
        </tr>
        <tr>
            <td><strong>Access</strong></td>
            <td><strong>Models</strong></td>
            <td>Every model the agent uses, reported by its source or routed through the gateway, and the LLM Proxies that route them. See <a href="subscribe-an-agent-to-an-llm-proxy.md">Subscribe an agent to an LLM Proxy</a>.</td>
        </tr>
        <tr>
            <td><strong>Access</strong></td>
            <td><strong>Tools</strong></td>
            <td>What the agent calls, and whether those calls go through the gateway. See <a href="subscribe-an-agent-to-an-mcp-proxy.md">Subscribe an agent to an MCP Proxy</a>.</td>
        </tr>
        <tr>
            <td><strong>Access</strong></td>
            <td><strong>Agents</strong></td>
            <td>The other agents this one can call through the A2A Proxies it subscribes to on the gateway.</td>
        </tr>
    </tbody>
</table>

An agent reaches models, tools, and other agents only through a proxy it subscribes to. An agent whose source declares none of them still lists the **Models** and **Tools** pages, and the page explains which proxy to subscribe to.

## Edit the name and description

Only the name and the description are editable, and only for an agent registered by hand that isn't retired. The endpoint URL and the version are shown and can't be changed. To point the Catalog at a different endpoint, register the agent again.

1. On the **Overview** page of the agent, click **Edit**.
2. On the **Edit agent** page, change the **Name** or the **Description**.
3. Click **Save changes**.

An **Agent updated** notification appears. An imported agent isn't edited here, because its provider declares its details, and the next import would undo the change.

## Change the owner and the sponsor

The **Overview** header names the agent's owner and its sponsor. Open the more-actions menu of the agent to assign or transfer the ownership to a user of the organization, or to add, change, or remove the sponsor. A sponsor is the user accountable for the agent. A retired agent takes no new owner or sponsor.

## Change the catalog state

An agent is in one of four catalog states: **Registered**, **Published**, **Deprecated**, or **Retired**. A **Deprecated** agent is one whose source no longer reports it, so it can't be published.

<table>
    <thead>
        <tr>
            <th width="180">Action</th>
            <th width="220">Starts from</th>
            <th>What it does</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Publish</strong></td>
            <td><strong>Registered</strong></td>
            <td>Moves the agent to <strong>Published</strong>.</td>
        </tr>
        <tr>
            <td><strong>Unpublish</strong></td>
            <td><strong>Published</strong></td>
            <td>Moves the agent back to <strong>Registered</strong>.</td>
        </tr>
        <tr>
            <td><strong>Retire agent</strong></td>
            <td><strong>Registered</strong>, <strong>Published</strong>, or <strong>Deprecated</strong></td>
            <td>Moves the agent to <strong>Retired</strong>.</td>
        </tr>
    </tbody>
</table>

To retire an agent, click **Retire agent** on its **Overview** page. In the **Retire &lt;agent&gt;?** dialog, read the warning, and then click **Retire agent**. A retired agent is no longer published, and its details, owner, and sponsor can no longer change. Its catalog record and history are kept. A retired agent is final and read-only, so you can only remove it.

## Remove an agent

1. On the **Overview** page of the agent, click **Remove**.
2. In the **Remove this agent?** dialog, click **Remove agent**.

The dialog warns that removal can't be undone and that experiences that reference the agent can no longer use it. A **Remove failed** alert appears when the agent can't be removed.

## Next steps

* [Register an agent](import-an-agent.md). Add another agent to the Catalog from the agent card it publishes.
* [Route an agent through an A2A Proxy](route-an-agent-through-an-a2a-proxy.md). Put the agent behind the AI Gateway from its **Endpoints** page.
* [Subscribe an agent to an LLM Proxy](subscribe-an-agent-to-an-llm-proxy.md). Give the agent access to models through its **Models** page.
* [Subscribe an agent to an MCP Proxy](subscribe-an-agent-to-an-mcp-proxy.md). Give the agent access to tools through its **Tools** page.
