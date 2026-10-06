---
hidden: false
noIndex: false
description: The Catalog group of the Agent Management sidebar holds the models, servers, tools, prompts, resources, skills, agents, and identities your agents use.
---

# Catalog

The **Catalog** group of the Agent Management sidebar holds the **AI Models**, **MCP Servers**, **Prompts**, **MCP Resources**, **Tools**, **Knowledge & Data**, **Skills**, **Agents**, and **Agent Identity** pages.

* [**Add an AI model**](add-an-ai-model.md). Add an AI model to the Catalog so an LLM Proxy can route to it.
* [**Add an MCP Registry**](add-an-mcp-registry.md). Importing MCP servers in bulk from an external registry is planned for a future release.
* [**Register an MCP server**](register-an-mcp-server.md). Register an MCP server to add it to the Catalog with its tools, resources, and prompts.
* [**Import prompts**](import-prompts.md). Prompts are reusable, parameterized templates discovered from registered MCP servers and cataloged for governance.
* [**Add MCP resources**](add-mcp-resources.md). MCP resources are read-only data items agents use as context, discovered from registered MCP servers.
* [**Create API tools**](create-api-tools.md). Expose REST APIs governed in API Management as agent-accessible tools in the Catalog.
* [**Add a knowledge source**](add-knowledge-source.md). Add a knowledge source so agents can read documentation and reference material as context.
* [**Upload skills**](upload-skills.md). Upload a skill package so agents can consume it as an MCP resource and you can govern it.
* [**Integrations**](integrations/README.md). Integrations bring models and agents from outside Gamma into the Catalog.
* [**Create an agent identity**](../build/create-an-agent-identity.md). Register an agent as an OAuth client in Gravitee Access Management with a persona that fits how it runs.
* [**Re-sync catalog assets**](re-sync-catalog-assets.md). Refresh imported AI models and MCP servers against the source they came from, and read what changed.

<figure><img src="../.gitbook/assets/gamma-aim-dashboard.png" alt="Agent Management Import catalog showing eight entity type cards"><figcaption><p>The Import section of the Agent Management dashboard. Each card links to a Catalog entity type. The full set of import operations is listed under Import operations.</p></figcaption></figure>

## Catalog entity types

| Entity type | Sources |
| --- | --- |
| **AI Models** | Synced from a connected provider integration, synced from Azure AI Foundry, or registered manually. |
| **MCP Servers** | Registered from a Streamable HTTP endpoint, or authored in MCP Studio. Type: **Native** (upstream) or **Composite**. |
| **Prompts** | Reusable, parameterized templates with declared arguments. |
| **MCP Resources** | Server resources discovered from registered MCP servers, and repository resources from Git. |
| **Tools** | **MCP Tools** from connected MCP servers, **API Tools** built from REST APIs in API Management, and **Kafka API Tools** from Event Stream Management. |
| **Knowledge & Data** | Document sources registered for agent consumption, inline or fetched from a remote URL. |
| **Skills** | Uploaded as `.zip` skill packages, exposed to agents as MCP resources using the FastMCP Skills-as-Resources pattern. |
| **Agents** | Registered from the A2A agent card an agent publishes, or discovered as shadow AI agents from the domains Edge Management detects. |

## Import operations

* [**Connect integrations**](connect-integrations.md). Connect Gamma to a model provider or to Azure AI Foundry so their models import into the Catalog.
* [**Add an AI model**](add-an-ai-model.md). Import models from a connected integration, and see the metadata each model records.
* [**Add an MCP Registry**](add-an-mcp-registry.md) _(coming soon)_. Connecting to external MCP registries (GitHub, Smithery) to import servers in bulk is planned for a future release.
* [**Register an MCP server**](register-an-mcp-server.md). Add an MCP server through a guided setup or a direct URL, including upstream authentication configuration.
* [**Import prompts**](import-prompts.md). Upload reusable, parameterized prompt templates to the Catalog.
* [**Add MCP resources**](add-mcp-resources.md). Catalog server resources from connected MCP servers and repository resources from Git.
* [**Create API tools**](create-api-tools.md). Expose REST APIs from API Management as agent-accessible tools in the Catalog.
* [**Add a knowledge source**](add-knowledge-source.md). Add external knowledge (documentation, knowledge bases) to the Catalog for agent consumption.
* [**Upload skills**](upload-skills.md). Catalog skill folders that agents can consume as MCP resources.
* [**Register an agent**](import-an-agent.md). Add an external agent to the Catalog from the A2A agent card it publishes.
* [**Discover shadow AI agents from Edge Management**](discover-shadow-ai-agents-from-edge-management.md). Turn the AI provider domains Edge Management detects into shadow AI agents in the Catalog, and read which processes and devices reached each one.
* [**Re-sync catalog assets**](re-sync-catalog-assets.md). Refresh imported AI models and MCP servers against the source they came from, and read what changed.
