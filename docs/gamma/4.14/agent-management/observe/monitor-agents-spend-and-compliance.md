---
description: Quick Start is the page Agent Management opens on. It links to the Connect, Catalog, and Secure pages the user can open.
---

# Open Quick Start

**Quick Start** is the page Agent Management opens on. The heading reads **AI Agent Management**. The line under it reads **Discover models and MCP servers, secure them behind the AI Gateway, then build agents from your catalog.**

The page is a set of links into **Connect**, **Import**, and **Secure**. Cost is read on [Dashboards](dashboards/README.md). An agent and a proxy each have their own **Overview**.

## Open Quick Start

1. In the Gamma console, open **Agent Management**. The module opens on **Quick Start**.
2. To return to it, find the **General** group in the sidebar and select **Quick Start**.

## What the page links to

The page has three sections: **Connect**, **Import**, and **Secure**. Each card uses the same name as the sidebar entry it opens. A card is left out when that user cannot open the page. A section with no cards is left out.

### Connect

| Card | Where it goes |
| --- | --- |
| **Agent Discovery** | Connect your agent platforms and keep discovered agents in sync with the catalog. |
| **Providers** | Connect to an AI service with a stored credential and import the models it exposes. |

### Import

The cards open pages in the **Catalog** group of the sidebar.

| Card | Where it goes |
| --- | --- |
| **AI Models** | Register and curate the AI models reused across the platform. |
| **MCP Servers** | Centralize MCP servers, whether added manually or imported from registries. |
| **Prompts** | Browse reusable prompt templates exposed by your servers. |
| **MCP Resources** | Expose read-only resources from servers and curated bundles. |
| **Tools** | Browse MCP tools and custom tools generated from existing APIs. |
| **Knowledge & Data** | Register knowledge bases and retrieval sources for grounded answers. |
| **Skills** | Compose reusable skills from prompts, tools, and knowledge. |
| **Agents** | Catalog A2A-compatible agents for discovery and reuse. |

### Secure

| Card | Where it goes |
| --- | --- |
| **Guardrails** | Reusable guardrail policy sequences that monitor, block and redact AI traffic on your proxies. |
| **LLM Proxies** | Route and govern LLM traffic through the AI Gateway with policies and observability. |
| **MCP Proxies** | Expose MCP servers through the AI Gateway with authentication and policy enforcement. |
| **A2A Proxies** | Secure agent-to-agent traffic behind the AI Gateway with policies and observability. |

## Next steps

* [Create your first LLM Proxy](../get-started/create-your-llm-proxy.md). Configure an LLM Proxy and send a test prompt.
* [Create your first MCP server](../get-started/create-your-first-mcp-server.md). Put an MCP Proxy in front of an upstream MCP server.
* [Dashboards](dashboards/README.md). Read AI traffic, cost, and tool usage.
