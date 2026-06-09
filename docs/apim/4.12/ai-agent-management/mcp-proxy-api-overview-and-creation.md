# MCP Proxy API Overview and Creation

## Overview

MCP Proxy API support enables platform administrators to expose Model Context Protocol (MCP) servers through the API gateway and provide one-click installation instructions for popular MCP clients. This feature introduces a new API type (`MCP_PROXY`) and an embeddable installation component that generates client-specific configuration snippets and deep links for Cursor, VS Code, and Claude Desktop.

## Key Concepts

### MCP Proxy API Type

MCP Proxy APIs route requests to MCP servers using HTTP, SSE, or stdio transports. The API model includes an `entrypoints` list containing API entry URLs and an `mcp` configuration map that stores MCP-specific settings such as `mcpPath`. When creating documentation for MCP Proxy APIs, the platform automatically seeds an overview page template that includes installation instructions.

### Install MCP Component

The `gmd-install-mcp` component renders one-click installer actions and copyable configuration snippets for MCP clients. It supports three transport protocols: HTTP, SSE, and stdio. For HTTP and SSE transports, the component generates deep links and JSON snippets containing the remote endpoint URL and optional headers. For stdio transports, it generates snippets with the executable command, arguments, and environment variables. The component filters displayed installers based on a comma-separated list of client IDs.

| Client | Configuration File | Deep Link Support |
|:-------|:-------------------|:------------------|
| Cursor | `~/.cursor/mcp.json` | Yes |
| VS Code | `mcp.json` | Yes |
| Claude Desktop | `claude_desktop_config.json` | No |

### API Template Variables

MCP Proxy APIs expose two additional template variables for use in documentation pages: `api.entrypoints` (a list of API entry URLs) and `api.mcp` (a map containing MCP configuration extracted from the first listener's first entrypoint). If the MCP entrypoint configuration is not valid JSON, the `mcp` variable defaults to an empty map.

## Prerequisites

Before creating an MCP Proxy API, ensure the following requirements are met:

* API gateway version supporting the `MCP_PROXY` API type
* MCP server accessible via HTTP, SSE, or stdio transport

## Creating an MCP Proxy API

1. Create an MCP Proxy API by selecting `MCP_PROXY` as the API type during API creation.
2. Configure the API's entrypoints to route to your MCP server endpoint.
3. If your MCP server uses a custom path (for example: `/mcp`), store it in the `mcp` configuration map under the `mcpPath` key.
4. The platform automatically generates an overview page template that includes installation instructions using the `gmd-install-mcp` component.
5. Customize the installation component by editing the overview page markdown and adjusting the component's attributes to match your MCP server's transport protocol and connection details.
