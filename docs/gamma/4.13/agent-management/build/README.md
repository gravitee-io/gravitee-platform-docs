---
hidden: false
noIndex: false
description: Create and secure the AI Gateway components that govern LLM, MCP, and A2A traffic. Start with the proxy type you need.
---

# Secure

Create and configure the AI Gateway components that govern LLM, MCP, and A2A traffic, and manage the settings that every proxy type shares.

* [**MCP Proxies**](mcp-proxies/README.md). Govern an upstream MCP server with authentication, authorization, and observability, or compose a Composite MCP Server in MCP Studio.
* [**LLM Proxies**](llm-proxies/README.md). Route model traffic through the AI Gateway with authentication, cost attribution, guardrails, and observability.
* [**A2A Proxies**](a2a-proxies/README.md). Make an agent's skills discoverable and callable across trust boundaries with per-skill authorization.
* [**Manage subscriptions**](../publish/manage-subscriptions.md). Subscribe an application to a plan, approve the request, and find the credential the AI Gateway checks.
* [**Broadcast messages to proxy consumers**](broadcast-messages-to-proxy-consumers.md). Send a one-way announcement to the consumers of an LLM Proxy, MCP Proxy, or A2A Proxy.
* [**Configure properties for your proxies**](configure-properties-for-your-proxies.md). Define the key/value properties that policies read at runtime, import them in bulk, or sync them from an HTTP endpoint.
* [**Configure resources for your proxies**](configure-resources-for-your-proxies.md). Create and manage the resources that the policies of a proxy reference at runtime.
