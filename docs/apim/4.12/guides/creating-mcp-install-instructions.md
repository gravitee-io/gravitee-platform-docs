
# Creating MCP Install Instructions

MCP install instructions enable API consumers to configure AI clients (Cursor, VS Code, Claude Desktop) to connect to your MCP Proxy API. The `<gmd-install-mcp>` component generates client-specific configuration snippets and deep links for one-click installation.

To add MCP client installation instructions to a portal documentation page, embed the `<gmd-install-mcp>` component in Gravitee Markdown content.
 The component requires a server name and either a remote URL (for HTTP/SSE transports) or a command (for stdio transports). If required inputs are missing, the component renders the placeholder message: "Provide a server name and URL, or use stdio inputs for a local MCP server."

**Remote HTTP transport:**

```html
<gmd-install-mcp 
  name="weather" 
  url="https://api.example.com/mcp" 
  clients="cursor,vscode,claude-desktop" />
```

**Local stdio transport:**

```html
<gmd-install-mcp 
  name="weather-local" 
  transport="stdio" 
  command="npx" 
  args='["-y","@acme/weather-mcp"]' 
  clients="cursor,vscode,claude-desktop" />
```

The component displays installer tabs for each client listed in the `clients` attribute.

## Component Attributes

| Attribute | Description | Example |
|:----------|:------------|:--------|
| `name` | MCP server name used in generated client configurations | `"weather"` |
| `transport` | MCP transport protocol: `http`, `sse`, or `stdio` (default: `http`) | `"http"` |
| `url` | Remote MCP endpoint URL for `http` and `sse` transports | `"https://api.example.com/mcp"` |
| `headers` | JSON object or string of headers for remote transports | `'{"Authorization":"Bearer token"}'` |
| `command` | Executable used to start a stdio MCP server | `"npx"` |
| `args` | JSON array or comma-separated string of stdio command arguments | `'["-y","@acme/weather-mcp"]'` |
| `env` | JSON object or string of environment variables for stdio transports | `'{"API_KEY":"secret"}'` |
| `clients` | Comma-separated list of installer IDs to display | `"cursor,vscode,claude-desktop"` |

## Installer Behavior

| Client | Installation Mode | Configuration File | Deep Link Support |
|:-------|:------------------|:-------------------|:------------------|
| Cursor | Deep link | `~/.cursor/mcp.json` | Yes (`cursor://anysphere.cursor-deeplink/mcp/install`) |
| VS Code | Deep link | `mcp.json` | Yes (`vscode:mcp/install`) |
| Claude Desktop | Snippet only | `claude_desktop_config.json` | No |

The copy button label changes from "Copy" to "Copied" for 2 seconds after clicking. If no installers match the requested `clients` input, the component renders: "No supported installers are available for the selected clients."

## Theming

Customize component appearance using the `@gmd.install-mcp-overrides()` SCSS mixin:

```scss
@use '@gravitee/gravitee-markdown' as gmd;

@include gmd.install-mcp-overrides((
  container-color: #1f2937,
  container-outline-color: #334155,
  headline-color: #f8fafc,
  subdued-text-color: #cbd5e1,
  tab-inactive-color: #0f172a,
  tab-inactive-text-color: #e2e8f0,
  code-background-color: #020617,
  code-text-color: #e2e8f0,
));
```

Available tokens: `container-color`, `container-outline-color`, `headline-color`, `subdued-text-color`, `tab-active-color`, `tab-active-text-color`, `tab-inactive-color`, `tab-inactive-text-color`, `code-background-color`, `code-text-color`.
