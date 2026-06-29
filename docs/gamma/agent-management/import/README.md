---
hidden: false
noIndex: true
---

# Import

Populate the Catalog with the assets your agents need — models, MCP servers, tools, prompts, resources, skills, and agents. The Catalog is the authoritative registry of everything an agent can use, and fine-grained authorization policies are authored against cataloged entities. A rich Catalog enables precise governance.

<figure><img src="https://3745118555-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fa6QVD3iIxTvnV5eQ8OH1%2Fuploads%2Fgit-blob-373a44719c46f317ac2b1e6ca9bb141e1585011d%2Fgamma-aim-dashboard.png?alt=media" alt="Agent Management Import catalog showing eight entity type cards"><figcaption><p>The Import section of the Agent Management dashboard. Each card links to a Catalog entity type. The full set of import operations — including integrations, API tools, and Event tools — is listed below.</p></figcaption></figure>

* [**Connect integrations**](connect-integrations.md) — Link Gamma to upstream providers (Vertex AI, Bedrock, Azure AI Foundry) to sync AI models and agents into the Catalog.
* [**Add an AI model**](add-an-ai-model.md) — Register AI models from connected integrations or add them manually.
* [**Add an MCP Registry**](add-an-mcp-registry.md) _(coming soon)_ — Connecting to external MCP registries (GitHub, Smithery) to import servers in bulk is planned for a future release.
* [**Register an MCP server**](register-an-mcp-server.md) — Add an MCP server through a guided setup or a direct URL, including upstream authentication configuration.
* [**Import prompts**](import-prompts.md) — Upload reusable, parameterized prompt templates to the Catalog.
* [**Add MCP resources**](add-mcp-resources.md) — Catalog server resources from connected MCP servers and repository resources from Git.
* [**Create API tools**](create-api-tools.md) — Expose REST APIs from API Management as agent-accessible tools in the Catalog.
* [**Create Event tools**](create-event-tools.md) — Expose Kafka APIs from Event Stream Management as agent-accessible tools in the Catalog.
* [**Add a knowledge source**](add-knowledge-source.md) — Add external knowledge (documentation, knowledge bases) to the Catalog for agent consumption.
* [**Upload skills**](upload-skills.md) — Catalog skill folders that agents can consume as MCP resources.
* [**Import an agent from an integration**](import-an-agent.md) — Import A2A agents and hyperscaler-federated agents from connected integrations.
