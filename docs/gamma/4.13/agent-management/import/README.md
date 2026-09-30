---
hidden: false
noIndex: false
description: The Catalog group of the Agent Management sidebar holds the models, servers, tools, prompts, resources, skills, agents, and identities your agents use.
---

# Catalog

The **Catalog** group of the Agent Management sidebar holds the **Credentials**, **Providers**, **AI Models**, **MCP Servers**, **Prompts**, **MCP Resources**, **Tools**, **Knowledge & Data**, **Skills**, **Agents**, and **Agent Identity** pages.

* [**Integrations**](integrations/README.md). Integrations bring models and agents from outside Gamma into the Catalog.
* [**Add an AI model**](add-an-ai-model.md). Add an AI model to the Catalog so authorization policies, observability, and cost attribution can reference it.
* [**Add an MCP Registry**](add-an-mcp-registry.md). Importing MCP servers in bulk from an external registry is planned for a future release.
* [**Register an MCP server**](register-an-mcp-server.md). Register an MCP server to add it to the Catalog with its tools, resources, and prompts.
* [**Import prompts**](import-prompts.md). Prompts are reusable, parameterized templates discovered from registered MCP servers and cataloged for governance.
* [**Add MCP resources**](add-mcp-resources.md). MCP resources are read-only data items agents use as context, discovered from registered MCP servers.
* [**Create API tools**](create-api-tools.md). Expose REST APIs governed in API Management as agent-accessible tools in the Catalog.
* [**Add a knowledge source**](add-knowledge-source.md). Add a knowledge source so agents can read documentation and reference material as context.
* [**Upload skills**](upload-skills.md). Upload a skill package so agents can consume it as an MCP resource and you can govern it.
* [**Create an agent identity**](../build/create-an-agent-identity.md). Register an agent as an OAuth client in Gravitee Access Management with a persona that fits how it runs.

<figure><img src="../.gitbook/assets/gamma-aim-dashboard.png" alt="Agent Management Import catalog showing eight entity type cards"><figcaption><p>The Import section of the Agent Management dashboard. Each card links to a Catalog entity type. The full set of import operations — including integrations, API tools, and Event tools — is listed below.</p></figcaption></figure>
