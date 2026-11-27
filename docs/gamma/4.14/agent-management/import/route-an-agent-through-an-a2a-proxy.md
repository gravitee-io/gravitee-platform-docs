---
description: View an agent's endpoints in Gamma, including its A2A Agent Card and the A2A Proxy that fronts it. Follow the steps to add or replace a card.
---

# Read an agent's endpoints

The **Endpoints** page of a registered agent lists how callers reach it. Each row is an endpoint the agent declares. When an A2A Proxy fronts the agent, that proxy shows on the A2A endpoint it was created for. You create the proxy under **Secure**. This page does not create, link, or detach one.

## Open the Endpoints page

1. In the Gamma console, open **Agent Management**.
2. In the **Catalog** section of the sidebar, select **Agents**.
3. Click the agent's name.
4. In the **Agent** section of the agent's sidebar, click **Endpoints**.

## Read the endpoints

The page heading is **Endpoints**. For an agent synced from a provider, the description reads **Reported by the agent's source and updated on each sync.** Those endpoints are read-only, and a re-import updates them. For an agent registered by hand, the description reads **Register agent interfaces and manage inbound gateway proxies for exposed endpoints.**

The endpoints table has the following columns:

<table>
    <thead>
        <tr>
            <th width="180">Column</th>
            <th>What it shows</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Type</strong></td>
            <td><strong>A2A</strong>, <strong>Responses</strong>, or <strong>Custom</strong>.</td>
        </tr>
        <tr>
            <td><strong>Name</strong></td>
            <td>The endpoint's name. The column appears only when at least one endpoint has a name.</td>
        </tr>
        <tr>
            <td><strong>Endpoint</strong></td>
            <td>The endpoint URL. You can copy it.</td>
        </tr>
        <tr>
            <td><strong>Gateway proxy</strong></td>
            <td>The A2A Proxy that fronts this endpoint, or a dash when none does.</td>
        </tr>
    </tbody>
</table>

The **Gateway proxy** cell names the proxy and links to it, shows its context path, and badges it **Running** or **Stopped**. The proxy is shown on the A2A endpoint it fronts. When the proxy's target was changed after it was created, the cell stays on the agent's A2A endpoint.

When the agent has no endpoint, the page reads **No endpoints** and adds the following:

* For an agent synced from a provider, it adds **The agent's source reports no endpoint for it.**
* For a custom agent that can be given a card, it adds **Import an A2A Agent Card to register how this agent is exposed.**
* Otherwise it adds **No endpoint is recorded for this agent.**

## Add an A2A Agent Card

A custom agent registered by hand, and with no card yet, can be given one. **Add interface** appears only when you can update the Catalog. An agent synced from a provider does not show it, and neither does an agent whose source owns the card. The API refuses the change for those agents.

1. On the **Endpoints** page, click **Add interface**.
2. In the **Import A2A Agent Card** sheet, enter the **Endpoint URL**, and then click **Fetch card**. The card is read from `/.well-known/agent-card.json`. The endpoints the card declares become the agent's A2A endpoints. The sheet reads **Fetch the card from an endpoint or paste its JSON, then review before import.**
3. Instead, under **Or paste the Agent Card JSON**, paste the card, and then click **Review card**.
4. Review the card, and then click **Import**.

An invalid card shows an error and nothing is saved. An **A2A Agent Card imported** notification appears when the card is saved. When the card states a different description or version, importing replaces those too. A blank description or version on the card leaves what the agent already has.

**View card** opens the **Agent card** sheet. Its description reads **Capabilities, security, and skills declared for this endpoint.**

To replace a card the agent already has, open the actions menu and click **Replace card**. The sheet is titled **Replace A2A Agent Card**, and it reads **Fetch the card again or paste its new JSON, then review before it replaces the current one.** When you save, **A2A Agent Card replaced** appears. An agent whose source owns the card can be viewed and not replaced.

A custom agent can also have its card removed, but only when you can delete the Catalog. In the actions menu, click **Remove card**. The **Remove the A2A Agent Card?** dialog warns that this removes the card and the agent's A2A endpoint. The dialog also warns that the name and description the card gave the agent stay. When you confirm, **A2A Agent Card removed** appears.

## See the A2A Proxy that fronts the agent

The **Gateway proxy** column is read-only. To put a proxy in front of the agent, create it under **Secure**:

1. In the Gamma console, open **Agent Management**.
2. Under **Secure**, select **A2A Proxies**.
3. Click **Create A2A proxy** and complete the **Define** and **Secure** steps. See [Expose your agent with the A2A Proxy](../build/expose-agent-with-a2a-proxy.md).
4. In the **Connect** step, under **Upstream agent**, select the agent under **Registered agent**. **None, I will enter the address myself** creates a proxy that is not linked to a catalog agent.

The list offers agents of the current environment that publish an A2A address and that no proxy fronts yet. A custom agent is not listed, even after it has a card. A retired agent is not listed. The field explains: **Picking one takes the address from its card and links the proxy to it. Only agents that publish an A2A address and are not already fronted are listed.**

When the agent declares one A2A endpoint, the **Target URL** is filled from the card and is read-only, with the hint **Taken from the agent's card. Clear the agent above to type another.** When it declares several, you pick the one the proxy fronts. The hint reads **The agent declares several A2A endpoints. The proxy fronts the one you choose.**

The link survives a re-import of the agent. A deleted proxy no longer shows on the agent. When you remove the agent from the Catalog, its proxies keep running. A proxy that already fronts a custom agent is left as it is.

## Next steps

* [Expose your agent with the A2A Proxy](../build/expose-agent-with-a2a-proxy.md). Create the proxy and give a client access to it.
* [Manage a registered agent](manage-a-registered-agent.md). Find your way around the rest of the agent's page.
