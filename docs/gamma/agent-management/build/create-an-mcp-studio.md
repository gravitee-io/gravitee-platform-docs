---
hidden: false
noIndex: false
---

# Create an MCP Studio
<!-- GAP-STRUCTURAL: Missing procedural content source -->

MCP Studio is a **mode** of the MCP Proxy — not a separate product. It's the authoring environment where you compose tools, resources, prompts, and skills from multiple sources into a **Composite MCP Server**: a new, governed MCP server that didn't exist as a single unit upstream.

## Why Composite MCP Servers matter

Enterprises don't have one MCP server. They have HubSpot's, GitHub's, Jira's, Slack's, the internal data lake's, the legacy mainframe wrapper. They don't want their Customer Success agent talking to all of them. They want a `cs-toolkit` Composite MCP Server with exactly the eleven tools, four resources, and two prompts that agent needs — with PII redaction on contact emails, rate limiting on writes, and fine-grained authorization evaluated on every call.

Naming the artifact (Composite MCP Server), registering it in the Catalog with `type=Composite`, and giving it a discoverable transport endpoint means it can be versioned, observed, governed, and referenced — just like any other Catalog entity.

## The tool palette

Studio provides a palette of building blocks drawn from the Catalog:

| Building block           | Source                                                                                              |
| ------------------------ | --------------------------------------------------------------------------------------------------- |
| **MCP tools**            | From any connected upstream MCP server                                                              |
| **API tools**            | From REST APIs in API Management (see [Create API tools](../import/create-api-tools.md))               |
| **Kafka API tools**      | From Kafka APIs in Event Stream Management (see [Create Event tools](../import/create-event-tools.md))        |
| **Skill resources**      | Skill folders exposed via FastMCP (see [Upload skills](../import/upload-skills.md))                    |
| **Repository resources** | Markdown, JSON, and structured docs from Git (see [Add MCP resources](../import/add-mcp-resources.md)) |
| **Prompt templates**     | Parameterized prompts registered in the Catalog (see [Import prompts](../import/import-prompts.md))    |

{% hint style="info" %}
Studio doesn't directly ingest APIs or Kafka topics. Instead, REST APIs are first exposed as **API Tools** in the Catalog, and Kafka APIs are first exposed as **Kafka API Tools**. Once cataloged, those tools become available in Studio alongside MCP-native building blocks. The bridge to existing enterprise infrastructure happens at the **Catalog layer** — Studio is the composition step on top.
{% endhint %}

## Create a Composite MCP Server

1. From the Gamma console sidebar, select **Agent Management**.
2. Navigate to **Build**.
3. Select **Create MCP Proxy**, then choose the **Studio mode** to launch the MCP Studio wizard.
4. **Define**: Provide a Name, Description, and a Context path for the Composite MCP Server.
5. **Secure**: Configure security for clients connecting to the server (Gravitee AM, External Authorization, or API Key). You can also enable Fine-Grained Authorization (FGA) here.
6. **Compose**: Select the tools, resources, and prompts from the Catalog palette to include in the server. You can assign aliases to tools to avoid naming collisions.
7. **Connect**: Configure upstream authentication for any required source servers that the selected tools depend on.
8. **Review**: Review the assembled Composite MCP Server configuration and select **Create**.

The Composite MCP Server is registered in the Catalog with `type=Composite` and assigned a transport endpoint that agents can connect to.

## After creation

The Composite MCP Server:

* Appears in the Catalog alongside Native MCP servers
* Has its own transport endpoint for agent connections
* Can have authorization policies applied at the tool level (see [Add policies to your MCP server](configure-your-mcp/add-policies-to-mcp-server.md))
* Emits observability data for every tool invocation through the AI Gateway

## Next steps

* [Add policies to your MCP server](configure-your-mcp/add-policies-to-mcp-server.md) — Apply fine-grained authorization to the Composite MCP Server's tools.
* [Register an MCP server](../import/register-an-mcp-server.md) — Import upstream MCP servers whose tools you can compose in Studio.
