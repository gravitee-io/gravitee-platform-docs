---
hidden: false
noIndex: false
description: The Secure group of the Agent Management sidebar holds the proxies that govern LLM, MCP, and agent-to-agent traffic. Start with the proxy you need.
---

# Secure

The **Secure** group of the Agent Management sidebar holds the **LLM Proxies**, **MCP Proxies**, and **A2A Proxies** pages.

* [**LLM Proxies**](llm-proxies/README.md). Create, design, and publish an LLM Proxy that routes model traffic through the AI Gateway.
* [**MCP Proxies**](mcp-proxies/README.md). Create and govern an MCP Proxy that fronts an upstream MCP server with authentication, policies, and observability.
* [**A2A Proxies**](a2a-proxies/README.md). Expose an upstream agent behind the AI Gateway with an A2A Proxy, then configure and secure it.
* [**Manage subscriptions**](../publish/manage-subscriptions.md). A subscription binds one application to one plan on a Gamma LLM or MCP Proxy.
* [**Publish a proxy to the Developer Portal**](../publish/publish-a-proxy-to-the-developer-portal.md). Make an LLM, MCP, or A2A Proxy discoverable to consumers in the Developer Portal.
* [**Agent kill switch**](agent-killswitch.md). Stop an agent in one move from its page in the Catalog, which stops the A2A Proxy in front of it, pauses its gateway subscriptions, and disables it on Azure AI Foundry, or stop a proxy on its own.
