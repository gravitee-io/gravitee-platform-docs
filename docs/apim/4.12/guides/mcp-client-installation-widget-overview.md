# MCP Client Installation Widget Overview

## Overview

Portal Next automatically generates MCP-specific Overview pages for MCP Proxy APIs, enabling API consumers to install and configure MCP servers in AI clients with one click. The Overview page includes deep links for Cursor, VS Code, and Claude Desktop, plus copyable configuration snippets for HTTP, SSE, and stdio transports. API publishers can also manually author custom portal pages using the `<gmd-install-mcp>` Gravitee Markdown component and FreeMarker template variables.

## Prerequisites

* Published API with at least one configured entrypoint
* For MCP Proxy APIs: V4 entrypoint with `mcp` or `mcp-proxy` type and `mcpPath` configuration
* Portal navigation item created for the API

# ${api.name}

Welcome to the documentation for **${api.name}**.

<#if api.description?? && api.description?has_content>
${api.description}

</#if>

## Install this MCP server

<gmd-install-mcp name="${api.name}" transport="http" url="<#if api.entrypoints?? && (api.entrypoints?size > 0)>${api.entrypoints[0]}</#if><#if api.mcp?? && api.mcp.mcpPath??>${api.mcp.mcpPath}</#if>" />
