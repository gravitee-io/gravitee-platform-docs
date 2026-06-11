# Embedding the MCP Installation Widget in Portal Pages

## Prerequisites

Before embedding the MCP installation widget in portal pages, ensure the following:

* Published API with at least one configured entrypoint
* For MCP Proxy APIs: V4 entrypoint with `mcp` or `mcp-proxy` type and `mcpPath` configuration
* Portal navigation item created for the API
* Portal page editing permissions

# ${api.name}

Welcome to the documentation for **${api.name}**.

<#if api.description?? && api.description?has_content>
${api.description}

</#if>
## Install this MCP server

<gmd-install-mcp name="${api.name}" transport="http" url="<#if api.entrypoints?? && (api.entrypoints?size > 0)>${api.entrypoints[0]}</#if><#if api.mcp?? && api.mcp.mcpPath??>${api.mcp.mcpPath}</#if>" />
```

## Authoring Custom Portal Pages

### Using the Install MCP Component

You can manually add the `<gmd-install-mcp>` component to any Gravitee Markdown portal page. The component supports three transport protocols: `http`, `sse`, and `stdio`. For remote transports (`http` and `sse`), provide the `url` attribute and optionally include `headers` as a JSON object. For local stdio transport, provide the `command` attribute and optionally include `args` (JSON array) and `env` (JSON object). Use the `clients` attribute to specify which AI client tabs to display (comma-separated: `cursor`, `vscode`, `claude-desktop`).

The HTML sanitizer preserves the `<gmd-install-mcp>` component and its allowlisted attributes in stored portal content. If required attributes are missing for the selected transport (for example: `url` for `http` or `command` for `stdio`), the component displays a placeholder instead of functional installer actions.

**Component Attributes:**

| Attribute | Description |
|:----------|:------------|
| `name` | MCP server name in generated configs |
| `transport` | `http`, `sse`, or `stdio` |
| `url` | Remote endpoint URL (`http` / `sse`) |
| `headers` | JSON object of HTTP headers |
| `command` | Stdio executable |
| `args` | JSON array of stdio arguments |
| `env` | JSON object of stdio environment variables |
| `clients` | Comma-separated client ids to show as tabs |

**Remote HTTP Example:**

```html
<gmd-install-mcp 
  name="Weather Service" 
  transport="http" 
  url="https://api.example.com/mcp" 
  headers='{"Authorization": "Bearer token"}' 
  clients="cursor,vscode,claude-desktop" />
```

**Local Stdio Example:**

```html
<gmd-install-mcp 
  name="Everything Server" 
  transport="stdio" 
  command="npx" 
  args='["-y", "@modelcontextprotocol/server-everything"]' />
```


