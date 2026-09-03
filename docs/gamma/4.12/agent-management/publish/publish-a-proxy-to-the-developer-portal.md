---
hidden: false
noIndex: false
description: Make an LLM, MCP, or A2A Proxy discoverable to consumers in the Developer Portal. Follow the steps to set its categories and publish the underlying API.
---

# Publish a proxy to the Developer Portal

Deploying a proxy makes it reachable at its context path on the AI Gateway. Publishing it is a separate step that makes it discoverable in the Developer Portal, where consumers browse what's available. Every proxy you create in Agent Management is backed by an API in API Management, and it's that API the portal lists.

## What Gamma sets for you

A new proxy arrives with two portal-relevant values already set, and they don't carry the same weight.

**Visibility is set to public.** Every LLM Proxy, MCP Proxy, MCP Studio, and A2A Proxy is created with private visibility, then switched to public once its plans are in place. The proxy's **Settings** page shows the result, but visibility is read-only there. Change it from the APIM Console.

**The API lifecycle state stays at `CREATED`.** That's the state a new API is created in, and Agent Management leaves it there. The proxy's **Settings** page shows it under **Lifecycle**. That matters, because the Classic Developer Portal serves only APIs whose lifecycle state is `PUBLISHED`.

So a freshly created proxy is public but unpublished. It's reachable on the gateway once deployed, and absent from the Classic Developer Portal until you publish it.

## Set the portal categories

Categories are the environment's portal categories, the ones configured in the APIM Console. They're the one portal field you set from Agent Management.

1. From the Gamma console sidebar, select **Agent Management**.
2. In the **Secure** section of the sidebar, select **LLM Proxies**, **MCP Proxies**, or **A2A Proxies**.
3. Select the proxy.
4. In the **General** section of the proxy sidebar, select **General**. For an MCP Proxy, select **Settings** instead.
5. In **Categories**, select the categories to apply. The field lists the categories configured for the environment, and it reports `No matching categories` when a search matches none.
6. Click **Save changes**.

The same page carries the proxy's **Name**, **Version**, **Description**, and **Labels**, and a **Discard** button appears next to **Save changes** while you have unsaved edits.

## Publish to the Classic Developer Portal

The Classic Developer Portal serves an API only when its lifecycle state is `PUBLISHED`. Because Agent Management leaves proxies at `CREATED`, you publish the API from the APIM Console.

1. Open the APIM Console.
2. Open the API that backs your proxy. It carries the same name as the proxy.
3. In the **Configuration** section of the API sidebar, select **General**.
4. Scroll to the **Danger Zone**.
5. Click **Publish the API**.

Once the API is published and its visibility is public, the Classic Developer Portal serves it to anyone, signed in or not. A published API whose visibility is private is served only to signed-in users who can consume it.

{% hint style="info" %}
The **Danger Zone** actions affect the Classic Developer Portal only. The card says so directly: "These actions only affect Classic Developer Portal visibility and publication. Manage Next Gen Portal API visibility in Next Gen Portal settings."
{% endhint %}

## Show a proxy in the New Developer Portal

The New Developer Portal doesn't read the API lifecycle state at all, so publishing the API in the **Danger Zone** doesn't put a proxy there. It resolves what to show from the portal's own navigation instead. An API appears when a published navigation item points at it and that item's portal visibility is public. A navigation item that isn't public is served only to signed-in users who are members of the API or hold a subscription to it.

Add the proxy's API to the portal navigation from the APIM Console. The API Management documentation covers that flow under **Manage Portal Navigation and APIs**.

## What isn't available in this release

Three limits are worth stating plainly, because each one shapes how far this flow goes.

* **There are no marketplace listings.** A published proxy appears in the Developer Portal catalog like any other API. There's no separate listing object with its own title, summary, logo, or consumer-group visibility.
* **A catalogued agent has no publish action of its own.** Agents registered in the Catalog aren't APIs, so the portal has nothing to list for them. An agent reaches consumers through an A2A Proxy that fronts it. See [Expose your agent with the A2A Proxy](../build/expose-agent-with-a2a-proxy.md).
* **An A2A Proxy's plans are fixed at creation.** The plans you define in the creation wizard are created and published with the proxy, and the A2A Proxy sidebar carries no **Consumer Access** section, so there's no plan or subscription management afterward. LLM Proxies and MCP Proxies both carry that section.

## Verification

To verify a proxy is published as expected, follow these steps:

1. In the **General** section of the proxy sidebar, select **General**, or **Settings** for an MCP Proxy.
2. Confirm **Visibility** reads `Public` and **Lifecycle** reads `PUBLISHED`.
3. Open the Classic Developer Portal.
4. Confirm the proxy appears in the catalog, under each category you applied.

## Next steps

* [Publish your LLM Proxy](publish-your-llm-proxy.md). Deploy an LLM Proxy so consumers can reach it on the AI Gateway.
* [Manage subscriptions](manage-subscriptions.md). Review and act on the subscriptions consumers request.
