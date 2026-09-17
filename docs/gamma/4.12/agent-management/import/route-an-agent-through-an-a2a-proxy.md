---
hidden: true
noIndex: true
description: Put an A2A Proxy in front of a registered agent from its Proxies page, or link an existing proxy to it. Learn what the link enforces and how to detach it.
---

# Route an agent through an A2A Proxy

Registering an agent in the Catalog records what the agent declares. It doesn't put anything between the agent and its callers. To govern the calls that reach the agent, you route them through an A2A Proxy, and Gamma records which agent the proxy fronts. The agent's **Proxies** page shows that proxy, creates one for the agent, or links a proxy that already exists.

The link is one to one. An agent is fronted by at most one A2A Proxy, and a proxy fronts at most one agent. A linked proxy forwards to the address the agent publishes on its own agent card, and Gamma refuses a link, or a later change, that would point the pair at two different addresses.

## Before you start

* The agent must publish an A2A address: the URL on its agent card, or an A2A endpoint it declares. When it doesn't, the **Proxies** page reads **This agent has no A2A address, so it cannot have a proxy.** and offers no action.
* The **Create a proxy** button appears only for users who can create APIs in the environment, and **Link an existing proxy** only for users who can update them. Anyone who can read the Catalog sees the page and the linked proxy.

## Open the Proxies page

1. From the Gamma console sidebar, select **Agent Management**.
2. In the **Catalog** section of the sidebar, select **Agents**.
3. Click the agent's name.
4. In the **Agent** section of the agent's sidebar, click **Proxies**.

The page holds one card, **Exposed through**, described as the A2A proxy callers use to reach the agent. Before any proxy is linked, it reads **No A2A proxy. Callers reach &lt;agent&gt; directly, so no plans or policies apply.** and offers two buttons: **Create a proxy** and **Link an existing proxy**.

<figure><img src="../.gitbook/assets/gamma-aim-agent-proxies.png" alt="The Proxies page of an agent, with the Exposed through card showing the linked A2A Proxy, its plan count and running badge, and the Open proxy, Policies &amp; guardrails, and Detach buttons"><figcaption><p>The Proxies page of an agent with a linked A2A Proxy</p></figcaption></figure>

## Route the agent through a new proxy

To create an A2A Proxy for the agent without leaving its page, follow these steps:

1. On the **Proxies** page, click **Create a proxy**.
2. In the **Create an A2A proxy** card that opens on the page, complete the **Define** step. The name is filled in from the agent's name. Accept or change the **Context path**, the address callers use on the gateway.
3. In the **Secure** step, choose how callers authenticate.
4. In the **Connect** step, the **Target URL** is the address from the agent's card and is read-only, with the hint **Taken from the agent's card.**
5. Complete the **Review** step, and then click **Create A2A proxy**.

The card states that callers reach the agent through the proxy, at the address the agent publishes, and that the proxy is linked to the agent as soon as it is created. The steps are the ones of the A2A Proxy wizard under **Secure**, with the agent fixed.

When the agent's address ends in `.json` or contains `/.well-known/`, the **Connect** step warns that the address looks like the agent card itself rather than the endpoint the agent answers on. Fix the address on the agent before creating the proxy.

## Link an existing proxy

To link an A2A Proxy that already exists, follow these steps:

1. On the **Proxies** page, click **Link an existing proxy**.
2. In the **Link an existing proxy** dialog, under **Proxy to link**, select the proxy. The list holds the first 50 A2A Proxies of the environment. A proxy that fronts another agent reads **already attached**, one that forwards somewhere else reads **forwards elsewhere**, and a stopped one reads **stopped** and can still be selected. Only a proxy that forwards to the address the agent publishes can be linked.
3. Click **Link proxy**.

The dialog pre-selects a proxy when it finds one among those it can link. It looks first for a proxy whose entity ID contains the agent's slug, and otherwise for a proxy whose name is the only one to contain a word of the agent's name longer than three characters.

A proxy's target URL and the agent's address count as the same when they match after trailing slashes are dropped and the scheme and host are compared without regard to case. The path is compared as written.

## What the page shows once the proxy is linked

The **Exposed through** card shows the proxy's name, a badge with the number of plans on the proxy, and a status badge that reads **running** or **stopped**. Below them, the card shows the proxy's entity ID and its context path. Three buttons follow: **Open proxy**, which opens the proxy's **Overview**, **Policies & guardrails**, which opens the proxy's Policy Studio, and **Detach**.

The link is visible from the proxy's side too:

* The **General** card on the proxy's **Overview** page gains an **Agent** row that names the agent's slug.
* On the proxy's **Endpoint** page, the **Target URL** field is read-only while the link stands, with the hint **Taken from the linked agent's card. Detach the agent to change it.** A change submitted another way is refused with a message that names the agent and its published address.

Plans, policies, and guardrails stay on the proxy. Stopping the agent isn't on this page either. The **Stop** button in the bar at the top of the agent's page cuts every subscription its application holds, this proxy included. See [Manage a registered agent](manage-a-registered-agent.md).

## Detach the proxy

Detaching removes the link and nothing else. The proxy keeps running with its target URL, plans, and policies, and callers keep reaching the agent through it.

1. On the **Proxies** page, click **Detach**.

The card returns to its unlinked state, and the proxy's **Target URL** becomes editable again.

Removing the agent from the Catalog detaches the proxy in the same way before the record is deleted. When a proxy's stored slug no longer matches any agent, the proxy's **General** card shows the slug with the note **no longer in the catalog** and a **Detach** button to clear it.

## Create the proxy from the wizard

The A2A Proxy wizard under **Secure** can link the proxy as it creates it, in the same way as the card on the agent's page.

1. From the Gamma console sidebar, select **Agent Management**.
2. Under **Secure**, select **A2A Proxies**.
3. Click **Create A2A proxy**.
4. Complete the **Define** and **Secure** steps.
5. In the **Connect** step, under **Upstream agent**, select the agent under **Registered agent**. The list offers the agents that publish an A2A address and that no proxy fronts yet. When none qualifies, the field is disabled and explains why. Selecting `None, I will enter the address myself` creates an unlinked proxy.
6. Complete the rest of the step and the **Review** step, and then click **Create A2A proxy**.

Picking an agent fills the **Target URL** with the address from the agent's card and makes the field read-only, with the hint **Taken from the agent's card. Clear the agent above to type another.** When the name and description of the proxy are still empty, the wizard fills them from the agent too.

## Next steps

* [Expose your agent with the A2A Proxy](../build/expose-agent-with-a2a-proxy.md). What the proxy does, and how to give a client access to it.
* [Publish your agent to the Developer Portal](../publish/publish-your-agent-to-the-developer-portal.md). List the agent in the Developer Portal once a proxy fronts it.
* [Manage a registered agent](manage-a-registered-agent.md). Find your way around the rest of the agent's page.
