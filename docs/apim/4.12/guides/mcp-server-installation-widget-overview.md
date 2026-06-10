
# MCP Server Installation Widget Overview

## Overview

MCP Proxy APIs in the Gravitee Portal automatically receive a specialized overview page that includes installation instructions for AI clients. This page template embeds an interactive MCP server installation widget, allowing developers to quickly configure Claude Desktop, Cursor, VS Code, and other MCP-compatible clients with one-click deep links and copyable configuration snippets.

## Key Concepts

### MCP Server Installation Widget

The `<gmd-install-mcp>` component renders interactive installation instructions for MCP (Model Context Protocol) servers. It generates client-specific configuration snippets and deep links for supported AI development tools.


### FreeMarker Template Variables

Portal page templates use FreeMarker expressions to inject API metadata. The `api.entrypoints` list provides gateway URLs, while `api.mcp` exposes MCP-specific configuration like `mcpPath`. These variables enable dynamic construction of installation endpoints in overview pages.

| Variable | Description | Example Usage |
|:---------|:------------|:--------------|
| `api.name` | API display name | `${api.name}` |
| `api.description` | API description text | `${api.description}` |
| `api.entrypoints` | List of gateway entrypoint URLs | `${api.entrypoints[0]}` |
| `api.mcp.mcpPath` | MCP endpoint path from entrypoint configuration | `${api.mcp.mcpPath}` |
| `api.id` | API identifier | `${api.id}` |
| `api.version` | API version | `${api.version}` |
| `api.type` | API type (e.g., `MCP_PROXY`) | `${api.type}` |
| `api.visibility` | API visibility setting | `${api.visibility}` |


## Creating MCP Proxy API Overview Pages

When you create default portal pages for an API navigation item using `POST /portal-navigation-items/_default-pages`, the system automatically seeds an unpublished "Overview" child page. For MCP Proxy APIs (`ApiType.MCP_PROXY`), this page uses the `api-overview-mcp-proxy-page-content.md` template, which includes the API name, description (if present), and an embedded `<gmd-install-mcp>` widget. The widget's `url` attribute is constructed by concatenating the first entrypoint URL (`api.entrypoints[0]`) with the MCP path (`api.mcp.mcpPath`) when available. The `name` attribute is set to the API name, and `transport` is fixed to `"http"`. All other API types receive the generic `api-overview-page-content.md` template. If the API navigation item already has a child page, seeding is skipped entirely.

**MCP Proxy Overview Template Structure:**

| Element | Source | Purpose |
|:--------|:-------|:--------|
| Page title | `${api.name}` | Display API name as H1 heading |
| Description block | `${api.description}` | Conditionally rendered if description exists |
| Installation widget | `<gmd-install-mcp>` | Interactive MCP client configuration |
| Widget `name` | `${api.name}` | Server name in generated configs |
| Widget `transport` | `"http"` | Fixed HTTP transport type |
| Widget `url` | `${api.entrypoints[0]}${api.mcp.mcpPath}` | Constructed installation endpoint |

