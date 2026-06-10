# Adding MCP Install Widgets to Portal Pages

## Creating Portal Pages with MCP Install Widgets

Portal page authors can manually insert the `<gmd-install-mcp>` widget into Gravitee Markdown content to provide MCP client installation actions. The widget accepts the following attributes:

| Attribute | Description | Example |
|:----------|:------------|:--------|
| `name` | MCP server name used in generated client configurations | `my-mcp-server` |
| `transport` | Transport protocol: `http`, `sse`, or `stdio` | `http` |
| `url` | Remote MCP endpoint URL (required for `http` and `sse`) | `https://api.example.com/mcp` |
| `headers` | JSON object or string of HTTP headers for remote transports | `{"Authorization": "Bearer token"}` |
| `command` | Executable used to start a stdio MCP server | `node` |
| `args` | JSON array or comma-separated string of stdio command arguments | `["server.js", "--port", "3000"]` |
| `env` | JSON object or string of environment variables for stdio transports | `{"NODE_ENV": "production"}` |
| `clients` | Comma-separated list of installer IDs to display (`cursor`, `vscode`, `claude-desktop`) | `cursor,vscode` |

### Remote HTTP Server Example

```html
<gmd-install-mcp
  name="my-api-mcp"
  transport="http"
  url="https://api.example.com/mcp"
  headers='{"Authorization": "Bearer abc123"}'
  clients="cursor,vscode,claude-desktop">
</gmd-install-mcp>
```

### Local Stdio Server Example

```html
<gmd-install-mcp
  name="local-mcp"
  transport="stdio"
  command="node"
  args='["server.js"]'
  env='{"PORT": "8080"}'
  clients="cursor,claude-desktop">
</gmd-install-mcp>
```

### Widget Behavior

When required inputs (`name` and either `url` or `command`) are missing, the widget renders a placeholder message: "Provide a server name and URL, or use stdio inputs for a local MCP server."

The widget displays client tabs filtered by the `clients` attribute. The first available installer is selected by default. For clients supporting deep links (Cursor, VS Code), an "Install in [Client]" button generates a one-click install action. All clients provide a copyable JSON configuration snippet with file path instructions. The copy button label changes from "Copy" to "Copied" for 2 seconds after copying.

Portal-stored GMD pages retain the `<gmd-install-mcp>` tag and its attributes through the HTML sanitizer, which explicitly allows this custom element and its configuration attributes (`name`, `transport`, `url`, `headers`, `command`, `args`, `env`, `clients`).

### Theming

Use the `@gmd.install-mcp-overrides()` mixin to customize component tokens.

## Using FreeMarker Template Variables

Portal navigation page templates can construct MCP install URLs dynamically using FreeMarker expressions combined with the `<gmd-install-mcp>` widget. The `api.entrypoints` list provides gateway URLs, and the `api.mcp` map provides MCP-specific configuration extracted from the API's first listener.

### Typical Install URL Pattern

```html
<gmd-install-mcp
  name="${api.name}"
  transport="http"
  url="${api.entrypoints[0]}${api.mcp.mcpPath}"
  clients="cursor,vscode,claude-desktop">
</gmd-install-mcp>
```

In this example:
- `${api.entrypoints[0]}` resolves to the first entrypoint URL (e.g., `https://gateway.example.com/api`)
- `${api.mcp.mcpPath}` resolves to the MCP path segment (e.g., `/mcp`)
- The combined URL becomes `https://gateway.example.com/api/mcp`

Templates should include null/size checks for `api.entrypoints` to handle APIs without configured entrypoints. The `api.mcp` map is empty if:
- The API has no listeners
- The API has no entrypoints
- The first listener has no entrypoint with type `"mcp"` or `"mcp-proxy"` (case-sensitive, exact match)
- The MCP entrypoint's `configuration` field contains invalid JSON

If multiple listeners exist, only the first listener is evaluated for MCP configuration.
