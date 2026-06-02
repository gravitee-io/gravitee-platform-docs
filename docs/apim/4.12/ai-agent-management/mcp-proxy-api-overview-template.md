# MCP Proxy API Overview Template

## MCP Proxy Template

The MCP Proxy template is designed for APIs exposing Model Context Protocol servers. It includes a `<gmd-install-mcp>` component that generates one-click installation configurations for AI clients (Cursor, VS Code, Claude Desktop). The template displays the MCP server path alongside standard API metadata and emphasizes secure gateway routing. The "What you can do" section highlights tools, resources, and subscription requirements specific to MCP workflows.

The template constructs the gateway endpoint URL using `${api.entrypoints[0]}` and `${api.mcp.mcpPath}` FreeMarker variables. The `<gmd-install-mcp>` component is a new feature introduced with this template. FreeMarker variable usage for dynamic content population and inline CSS styling with primary color theming follow the same patterns as the standard template.
