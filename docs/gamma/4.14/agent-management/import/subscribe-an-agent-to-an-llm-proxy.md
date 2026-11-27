---
description: The Models page of an agent lists the models it uses. Subscribing to an LLM Proxy is done under Secure, not on this page.
---

# Read the models an agent uses

The **Models** page lists every model a registered agent uses. A model is either reported by the agent's source or routed by an LLM Proxy that the agent's gateway application subscribes to. The page is read-only. You subscribe to the proxy under **Secure**.

## Open the Models page

1. In the Gamma console, open **Agent Management**.
2. In the **Catalog** section of the sidebar, select **Agents**.
3. Click the agent's name.
4. In the **Access** section of the agent's sidebar, click **Models**.

The page heading is **Models**. The description reads **Every model this agent uses — reported from a source or routed through the Gravitee API gateway.**

## Read the models

Above the table, a count reads **&lt;n&gt; of &lt;m&gt; models go through the gateway**. **Search model, proxy** filters the rows. **Gateway status** filters them further:

* **All gateway statuses**
* **Through the gateway**
* **Direct to the provider**

**Reset** clears a filter you set. When nothing matches, the page reads **No matching models** and offers **Clear filters**.

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
            <td><strong>Proxied on Gateway</strong> when the model goes through a subscription. Otherwise <strong>Declared on the agent</strong>, or <strong>&lt;source&gt; imported</strong> for an agent synced from a provider.</td>
        </tr>
    </tbody>
</table>

Models the source declares come first, in the source's order. A declared model that is linked to an LLM Proxy the agent subscribes to is one row, badged **Proxied on Gateway**, and that proxy does not list the same model again. The same name declared with no link, and also routed by a proxy, stays two rows.

Only an accepted subscription is a route. A subscription that is pending or paused is not shown in the table.

When the agent has models listed and no gateway application yet, the page reads **Gateway subscriptions need a gateway application, which the agent gets with its identity.** **Go to Identity** opens the agent's **Identity** page. That link appears for a user who can update the Catalog.

## When the agent has no models

The page reads **No models**.

* For an agent synced from a provider: **No models were imported from &lt;source&gt;, and this agent is not subscribed to an LLM proxy. An agent calls models through Gravitee by subscribing to an LLM proxy.**
* For any other agent: **This agent is not subscribed to an LLM proxy, so it cannot call models through Gravitee. An agent gets its models by subscribing to an LLM proxy.**

Three steps follow, under **How to connect**:

1. **Give the agent a gateway application.** Subscriptions belong to an application. Create it on the Identity tab. **Create application on Identity** opens that page, for a user who can update the Catalog.
2. **Subscribe the agent to an LLM proxy.** **Pick the proxy that routes the models you need. The subscription gives the agent its credential.**
3. **The proxy's models appear here.** Each model the proxy routes is listed on this tab, marked **Proxied on Gateway**.

Until the agent has an application, the second button reads **Open LLM Proxies** and opens **Secure** → **LLM Proxies**. Once it has an application, that button reads **Subscribe to an LLM proxy** and opens the same list. The subscription is made on the proxy, not on this page. A user who cannot take the next step reads **Ask an agent administrator to subscribe this agent.** and gets no buttons. The link to the proxy list appears only for a user who can read APIs.

When the agent already has a subscription that is not accepted, and the page has nothing to list, it names the proxy. A pending subscription reads **waiting for approval**, and the models appear once it is **accepted**. A paused subscription reads **paused**, and the models appear once it is **resumed**. The page does not offer another subscription while that one is waiting.

When the subscriptions cannot be read, the page reads **Could not load the gateway subscriptions of this agent** and offers **Retry**. The empty state then reads **What this agent reaches through the gateway could not be read.** and leaves the steps out.

## Next steps

* [Expose your agent with an LLM Proxy](../build/create-an-llm-proxy.md). Create the proxy the agent subscribes to.
* [Manage subscriptions](../publish/manage-subscriptions.md). Approve, pause, or close the subscription from the proxy's side.
* [Manage a registered agent](manage-a-registered-agent.md). Find your way around the rest of the agent's page.
