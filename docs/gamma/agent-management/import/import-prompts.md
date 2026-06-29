---
hidden: false
noIndex: false
---

# Import prompts

Prompts in the Catalog are reusable, parameterized templates with declared arguments. Promoting prompts to a catalog primitive — rather than embedding them in tool definitions or agent configurations — makes prompt governance possible. You can version prompts, reference them in authorization policies, and compose them into MCP Studios.

## How prompts are discovered

Prompt templates are not created manually in Gamma. Instead, they are automatically discovered and ingested from connected MCP servers. 

When you register an MCP server (see [Register an MCP server](register-an-mcp-server.md)), Gamma automatically discovers any Prompt templates it exposes according to the Model Context Protocol.

Each cataloged prompt records:

| Field                  | Description                                                                                                  |
| ---------------------- | ------------------------------------------------------------------------------------------------------------ |
| **Name**               | A descriptive name for the prompt template.                                                                  |
| **Description**        | What the prompt is used for.                                                                                 |
| **Entity ID**          | A unique identifier within the Catalog.                                                                      |

## Review imported prompts

No additional import steps are required. The prompts appear in the Catalog as part of the MCP server registration flow.

To review cataloged prompts:

1. From the Gamma console sidebar, select **Agent Management**.
2. Navigate to the **Catalog** → **Prompts** list.
3. Select any prompt to view its Entity ID, source details, and description.

## Next steps

* **Compose into a Studio** — Include cataloged prompts in a Composite MCP Server. See [Create an MCP Studio](../build/create-an-mcp-studio.md).

<!-- Source: gravitee-gamma-module-aim/src/main/ui/app/features/catalog/prompts/McpPromptsPage.tsx -->
