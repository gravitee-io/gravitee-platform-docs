---
description: Manage a registered agent in the Gamma Catalog, from its Overview to its owner and state. Follow the steps to edit, publish, retire, or remove it.
---

# Manage a registered agent

When you register an agent, the Gamma console opens the agent's page in the Catalog. The page is the hub for the agent. Its **Overview** shows who owns it, what still needs setting up, and what the Catalog records about it. The sidebar leads to the pages that give it an identity, endpoints, models, tools, and other agents. The actions on the **Overview** page change its state in the Catalog. Return to it to publish the agent, change its owner, route its calls through the AI Gateway, or remove it.

## Open an agent's page

Immediately after you register an agent, the console opens the new agent's page for you. To return to it later, follow these steps:

1. In the Gamma console, open **Agent Management**.
2. In the **Catalog** section of the sidebar, select **Agents**.
3. Click the agent's name. Optional: To find it in a long list, type part of its name, description, or skill in the search box.

The **Agents** page lists agents added directly or synced from connected providers. By default it shows the **Name**, **Catalog state**, **Entity ID**, **Source**, and **Sponsor** columns. Use **Toggle columns** to show the **Owner**, **Risk classification**, **Last updated**, **Description**, and **Version** columns, and use **Column order** to arrange them. You can switch between **Table view** and **Card view**.

The actions menu at the end of each row offers **View agent**, **Edit details**, **Publish** or **Unpublish**, **Retire agent**, and **Remove**. **Edit details** appears only for an agent registered by hand that isn't retired.

## Read the Overview

The **Overview** is the first page of the agent, under **Agent**. Its header carries the following fields:

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
            <td>The OAuth client ID of the agent's identity, which you can copy. It reads <strong>Not set</strong> when the agent has no client ID.</td>
        </tr>
    </tbody>
</table>

### Set up this agent

**Set up this agent** sits under the header while setup is unfinished. Open, it reads **Follow these steps in order. An agent reaches models, tools and other agents only through a proxy it subscribes to.** Closed, it reads **Next:** and the title of the next step. The card shows **N of M done**, **Hide steps**, and **Show steps**. It goes away once every step that applies is done.

The card lists the following steps:

<table>
    <thead>
        <tr>
            <th width="280">Step</th>
            <th>Done when</th>
            <th>Button</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Give the agent an identity</strong></td>
            <td>The agent has a gateway application.</td>
            <td><strong>Set up identity</strong>, which opens <strong>Identity</strong>.</td>
        </tr>
        <tr>
            <td><strong>Connect models through an LLM proxy</strong></td>
            <td>At least one model goes through the gateway.</td>
            <td><strong>Open LLM Proxies</strong>, or <strong>Open Models</strong> when you cannot read APIs.</td>
        </tr>
        <tr>
            <td><strong>Connect tools through an MCP proxy</strong></td>
            <td>At least one tool goes through the gateway.</td>
            <td><strong>Open MCP Proxies</strong>, or <strong>Open Tools</strong>.</td>
        </tr>
        <tr>
            <td><strong>Expose the agent through an A2A proxy</strong></td>
            <td>An A2A Proxy fronts the agent.</td>
            <td><strong>Open Agent Endpoints</strong>.</td>
        </tr>
    </tbody>
</table>

The expose step is included only when you can read APIs and the agent can be exposed. A custom agent does not get it.

### At a glance

**At a glance** has the following five tiles:

<table>
    <thead>
        <tr>
            <th width="240">Tile</th>
            <th>What it shows</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Provider</strong></td>
            <td>The provider name and <strong>Synced from the provider</strong>, or <strong>No provider</strong> with <strong>Custom</strong> or <strong>Agent Card</strong>.</td>
        </tr>
        <tr>
            <td><strong>Models</strong>, <strong>Tools</strong>, <strong>Related agents</strong></td>
            <td>The count. <strong>N of M through the gateway</strong> when there are any, otherwise <strong>None connected</strong>. The name opens that page.</td>
        </tr>
        <tr>
            <td><strong>Exposed</strong></td>
            <td><strong>Exposed</strong> when the A2A Proxy is running, <strong>Proxy stopped</strong> when it is stopped, <strong>Not exposed</strong> with <strong>No A2A proxy in front of it</strong>, or <strong>Unknown</strong> with <strong>Its A2A proxy could not be read</strong>. Opens <strong>Endpoints</strong>.</td>
        </tr>
    </tbody>
</table>

If you cannot read APIs, the **Exposed** tile does not appear. When the subscriptions cannot be read, the page shows **Could not load the gateway subscriptions of this agent** and **Retry**, and the three count tiles stay off.

### Connections

**Connections** follows when there is at least one model, tool, or related agent. Its description is **What this agent reaches, and the gateway proxy each call goes through. Without a proxy, calls are not governed by Gravitee.** Each column lists five rows, then **+N more**, with **View all**. A row reads **Direct, not through the gateway**, or **LLM proxy**, **MCP proxy**, or **A2A proxy** plus its name. An empty column reads **No models yet.**, **No tools yet.**, or **No related agents yet.**

### Details

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
            <td><strong>Running</strong>, <strong>Stopped</strong>, or <strong>Unknown</strong>. It appears only for an agent synced from a provider.</td>
        </tr>
        <tr>
            <td><strong>Risk classification</strong></td>
            <td><strong>Negligible</strong>, <strong>Limited</strong>, <strong>Moderate</strong>, <strong>High</strong>, or <strong>Unclassified</strong>.</td>
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

When the agent has an A2A card, a summary of it follows, with its **Name**, **Version**, **Description**, and **Skills**, or **None declared**. Eight skills are listed, then **+N more**. **View on Endpoints** opens the **Endpoints** page.

## Find your way around the sidebar

The agent's sidebar has two groups. Each entry is a page of its own. The following table lists each entry and what its page does:

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
            <td>Lists each endpoint of the agent by <strong>Type</strong>, <strong>Endpoint</strong>, and <strong>Gateway proxy</strong>. For an agent registered by hand, it also holds the A2A Agent Card. The A2A Proxy is created on the <strong>A2A Proxies</strong> page under <strong>Secure</strong>. See <a href="route-an-agent-through-an-a2a-proxy.md">Read an agent's endpoints</a>.</td>
        </tr>
        <tr>
            <td><strong>Access</strong></td>
            <td><strong>Models</strong></td>
            <td>Lists the models the source reported and the models a subscription grants. The subscription is created on the proxy, in the Developer Portal, through automation, or a similar path. See <a href="subscribe-an-agent-to-an-llm-proxy.md">Read the models an agent uses</a>.</td>
        </tr>
        <tr>
            <td><strong>Access</strong></td>
            <td><strong>Tools</strong></td>
            <td>Lists the tools the source reported and the tools a subscription grants. The subscription is created on the proxy, in the Developer Portal, through automation, or a similar path. See <a href="subscribe-an-agent-to-an-mcp-proxy.md">Read the tools an agent calls</a>.</td>
        </tr>
        <tr>
            <td><strong>Access</strong></td>
            <td><strong>Agents</strong></td>
            <td>Lists the other agents an A2A Proxy subscription grants. A source does not yet report which agents an agent calls.</td>
        </tr>
    </tbody>
</table>

An agent reaches models, tools, and other agents only through a proxy it subscribes to. An agent whose source declares none of them still lists the **Models**, **Tools**, and **Agents** pages.

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

The following table lists the actions that change the state:

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
* [Read an agent's endpoints](route-an-agent-through-an-a2a-proxy.md). The A2A Proxy is created on the **A2A Proxies** page under **Secure**.
* [Read the models an agent uses](subscribe-an-agent-to-an-llm-proxy.md). The **Models** page lists models. The subscription is created on the proxy, in the Developer Portal, through automation, or a similar path.
* [Read the tools an agent calls](subscribe-an-agent-to-an-mcp-proxy.md). The **Tools** page lists tools the same way.