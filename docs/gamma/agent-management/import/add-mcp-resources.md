---
hidden: false
noIndex: true
---

# Add MCP resources

Resources in the Catalog are read-only data items that agents use as context. Cataloging resources makes them governable — you can reference them in authorization policies, include them in Composite MCP Servers, and track which agents access which resources.

## How MCP resources are discovered

MCP Resources are not created manually. Instead, they are automatically discovered and synced from connected MCP servers. 

When you register an MCP server (see [Register an MCP server](register-an-mcp-server.md)), Gamma inspects the server's exposed capabilities. If the server exposes resources (such as database schemas, application logs, or files), Gamma automatically catalogs them. 

No additional import steps are required. The resources appear in the Catalog as part of the MCP server registration flow.

To review cataloged resources:

1. From the Gamma console sidebar, select **Agent Management**.
2. Navigate to the **Catalog** → **Resources** list.
3. Select any resource to view its URI, MIME Type, and Entity ID.

## Add external knowledge

If you want to manually upload structured documentation, files, or reference material that is not exposed by an MCP server, you should create a **Knowledge Source** instead. See [Add a knowledge source](add-knowledge-source.md).

## Next steps

* **Compose into a Studio** — Include cataloged resources as context in a Composite MCP Server. See [Create an MCP Studio](../build/create-an-mcp-studio.md).

<!-- Source: gravitee-gamma-module-aim/src/main/ui/app/features/catalog/resources/McpResourcesPage.tsx -->
