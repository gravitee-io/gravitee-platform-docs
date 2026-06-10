# MCP Server Installation Widget Overview

## Overview

The MCP server installation widget (`<gmd-install-mcp>`) enables API publishers to embed one-click installer actions and copyable configuration snippets for MCP clients directly into portal pages. When added to Gravitee Markdown (GMD) content, the widget generates deep links for supported AI clients (Cursor, VS Code, Claude Desktop) and provides manual configuration snippets for both remote HTTP/SSE servers and local stdio-based servers. This widget is designed for portal page authors and API publishers who want to streamline MCP server onboarding for developers.

## Key Concepts

### MCP Transport Protocols

The widget supports three transport protocols for MCP server communication:

- **http**: Remote MCP server accessed via HTTP requests
- **sse**: Remote MCP server using Server-Sent Events
- **stdio**: Local MCP server launched as a subprocess with standard input/output communication

Each transport requires different configuration attributes. Remote transports (`http`, `sse`) require a `url` and optional `headers`, while `stdio` requires a `command` with optional `args` and `env`. The widget does not render a default `Authorization` header in snippets for remote servers—authors must explicitly provide headers via the `headers` attribute.

### Supported MCP Clients

| Client | Install Mode | Snippet File | Deep Link Support |
|:-------|:-------------|:-------------|:------------------|
| Cursor | Deep link + snippet | `~/.cursor/mcp.json` | Yes |
| VS Code | Deep link + snippet | `mcp.json` | Yes |
| Claude Desktop | Snippet only | `claude_desktop_config.json` | No |

Cursor and VS Code installers define fallback link methods, but the widget UI does not display web installer fallback buttons.

### API Template Variables

Portal page templates (FreeMarker + GMD) can access MCP-related API metadata through two template variables:

- **api.entrypoints**: List of gateway entrypoint URLs. The first element (`${api.entrypoints[0]}`) is commonly used as the base URL for MCP install endpoints.
- **api.mcp**: Map of MCP configuration extracted from the API's **first listener only**. Contains properties like `mcpPath` (the path segment appended to the entrypoint URL for the MCP endpoint).

The MCP configuration extraction logic inspects only the first listener in the API's listener list. If multiple listeners exist, only the first is evaluated. The extraction searches for entrypoints with type `"mcp"` or `"mcp-proxy"` (case-sensitive, exact match). If the entrypoint's `configuration` field contains invalid JSON, the `api.mcp` map will be empty—no error is thrown. The map is also empty if the API has no listeners, no entrypoints, or no matching MCP entrypoint.

### New API Types

The platform now recognizes three additional API types for specialized proxy scenarios:

| API Type | Description |
|:---------|:------------|
| `MCP_PROXY` | Model Context Protocol proxy APIs; triggers automatic MCP-oriented Overview page seeding |
| `LLM_PROXY` | Large Language Model proxy APIs |
| `A2A_PROXY` | Agent-to-Agent proxy APIs |

Only `MCP_PROXY` APIs receive specialized default portal content. Other types use the generic Overview template.

## Prerequisites

- Published API with at least one configured entrypoint
- For MCP-specific features: V4 API with an entrypoint of type `mcp` or `mcp-proxy` in the **first listener**
- Portal page editing permissions (for manual widget insertion)
- For automatic Overview seeding: API navigation item without existing child pages
