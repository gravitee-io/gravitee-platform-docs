---
description: Consumers reach your agent by subscribing an application to a plan on its A2A Proxy. Follow the steps to create and publish a plan in the Gamma console, show your terms in the Developer Portal, and approve the requests.
---

# Let consumers subscribe to your agent

A consumer gets access to an agent by subscribing an application to a plan of the A2A Proxy that exposes it. The plan decides how the consumer authenticates. In the Gamma console, the A2A Proxy's **Plans** page is where you create and publish plans, and its **Consumers** page is where subscription requests are handled. In the Developer Portal, the agent's listing carries the **Subscribe** action, and the terms you write for the agent are shown to the consumer before the request is sent.

## Create and publish a plan

1. From the Gamma console sidebar, select **Agent Management**.
2. In the **Secure** section of the sidebar, select **A2A Proxies**.
3. Click the proxy's name.
4. Under **Consumer Access**, click **Plans**. The page lists the proxy's plans with their **Name**, **Security**, **Created** date, and **Status**.
5. Click **Create plan** and pick the security type: **Keyless**, **API key**, **JWT**, **OAuth 2.0**, or **mTLS**.
6. In the **General** step, enter the **Name**. It's shown to consumers subscribing to this proxy. A plan on an A2A Proxy takes a name and a security configuration and nothing else.
7. In the **Configure** step, set the security. A **Keyless** plan skips the step. An **OAuth 2.0** plan names the **OAuth 2.0 resource** declared on the proxy that validates the tokens, or an expression that resolves to one, and can **Extract payload** to forward the token payload to the upstream agent and **Check required scopes** against the **Required scopes** you list. The other security types use the same step an LLM Proxy plan does.
8. In the **Review** step, check the plan and create it. The plan is created in staging.
9. On the **Plans** page, open the plan's actions menu and click **Publish**. Consumers can subscribe to a published plan only.

To withdraw a plan, click **Close** in its actions menu. The **Close plan?** dialog warns that **Consumers lose access immediately**.

<!-- TODO: Screenshot of an A2A Proxy's Plans page with a published plan and the actions menu open -->

<figure><img src="../.gitbook/assets/PLACEHOLDER-gamma-aim-a2a-proxy-plans.png" alt=""><figcaption><p>The Plans page of an A2A Proxy</p></figcaption></figure>

## Show your terms to the consumer

The terms a consumer accepts before subscribing to an agent are written on the agent's navigation item in the New Developer Portal settings. The item must exist first. See [Publish your agent to the Developer Portal](publish-your-agent-to-the-developer-portal.md).

1. In the APIM Console, open **Settings**.
2. Under **Portal**, click **Settings**.
3. Scroll to the **New Developer Portal** section.
4. Click **Open Settings**. The New Developer Portal settings open in a new browser tab.
5. Click **Navigation**.
6. In the **Navigation items** panel, select the agent's item. The panel header reads **Linked Agent** followed by the name of the proxy.
7. Turn on **Show Terms and Conditions**. The toggle is offered to users who can update the environment's documentation.
8. Write the terms in the editor. Turn on **Preview** to read them as the consumer will.

## What the consumer does

In the Developer Portal catalog, the consumer switches from **APIs** to **Agents**, opens the agent's listing, and clicks **Subscribe**. The flow then runs through the following steps:

1. **Choose a plan**. The consumer picks one of the published plans.
2. **Choose an application**. The consumer picks the application that holds the credentials. The step is skipped when the application is already chosen for the agent, and for a **Keyless** plan.
3. **Configure Consumer**. When a subscription form is defined for the New Developer Portal, it's filled in here. When the agent has terms, a **Terms and Conditions** section shows them, and the request can't be sent until the consumer ticks the checkbox labelled `I accept the terms and conditions`.
4. **Review**. The consumer clicks **Subscribe**.

## Handle the requests

1. On the A2A Proxy, under **Consumer Access**, click **Consumers**.
2. Approve or reject each request that waits for a decision, and read the credential issued to an accepted one, the same way as for an LLM Proxy or MCP Proxy. See [Manage subscriptions](manage-subscriptions.md).

## Next steps

* [Expose your agent with the A2A Proxy](../build/expose-agent-with-a2a-proxy.md). Create the proxy the plans belong to.
* [Publish your agent to the Developer Portal](publish-your-agent-to-the-developer-portal.md). List the agent so consumers can find it.
* [Manage subscriptions](manage-subscriptions.md). The subscription lifecycle on the Consumers page.
