### Related Changes

- The API type enumeration now includes `MCP_PROXY` as a valid value.
- The HTML sanitizer allowlist permits the `gmd-install-mcp` element with attributes `name`, `transport`, `url`, `headers`, `command`, `args`, `env`, and `clients`.
- The Monaco editor hover provider safely handles component selectors without suggestion configurations.
- The default page seeding logic checks for the `MCP_PROXY` API type and uses the `api-overview-mcp-proxy-page-content.md` template instead of the standard overview template.

## Embedding Installation Instructions

Embed the `gmd-install-mcp` component in API documentation pages to provide one-click installation for MCP clients. The component requires a server name and either a URL (for HTTP/SSE transports) or a command (for stdio transports). Use the **Clients** attribute to control which installer options appear.

### Component Attributes

| Attribute | Type | Description | Example |
|:----------|:-----|:------------|:--------|
| `name` | `string` | MCP server name used in generated client configurations | `"weather"` |
| `transport` | `'http' \| 'sse' \| 'stdio'` | MCP transport protocol (default: `'http'`) | `"http"` |
| `url` | `string` | Remote MCP endpoint URL for `http` and `sse` transports | `"https://api.example.com/mcp"` |
| `headers` | `Record<string, string> \| string` | JSON object of headers for remote transports | `'{"X-API-Key":"abc123"}'` |
| `command` | `string` | Executable used to start a stdio MCP server | `"npx"` |
| `args` | `string[] \| string` | JSON array of stdio command arguments | `'["-y","@acme/weather-mcp"]'` |
| `env` | `Record<string, string> \| string` | JSON object of environment variables for stdio transports | `'{"API_KEY":"xyz"}'` |
| `clients` | `string` | Comma-separated list of installer IDs to display | `"cursor,vscode,claude-desktop"` |

### HTTP Transport Example

```html
<gmd-install-mcp name="weather" url="https://api.example.com/mcp" clients="cursor,vscode,claude-desktop" />
```
