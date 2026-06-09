# MCP Proxy API Documentation: Troubleshooting and Reference

## Troubleshooting

**Empty install URL:** If the install component displays an empty or incorrect URL, verify that the API has at least one configured entrypoint and that the first entrypoint URL is accessible. Check that `api.mcp.mcpPath` is populated by confirming the first listener's first entrypoint has type `mcp` or `mcp-proxy`.

**Widget placeholder:** If the component renders "Provide a server name and URL, or use stdio inputs for a local MCP server," ensure the `name` attribute and either `url` (for HTTP/SSE) or `command` (for stdio) are provided in the component markup.

**Tag stripped:** If the `<gmd-install-mcp>` tag is removed after saving a portal page, verify that all attributes are from the allowlisted set (`name`, `transport`, `url`, `headers`, `command`, `args`, `env`, `clients`). The HTML sanitizer preserves only these attributes.

## Restrictions

- The `<gmd-install-mcp>` component and its attributes (`name`, `transport`, `url`, `headers`, `command`, `args`, `env`, `clients`) are allowlisted by the HTML sanitizer and will not be stripped from stored portal pages.
- If the first listener has no entrypoints, or no entrypoint has type `mcp` or `mcp-proxy`, the `api.mcp` template variable will be an empty map.
- The MCP install component uses only the first entrypoint URL from `api.entrypoints` in the default template.
- If `args` or `env` inputs are provided as strings but cannot be parsed as JSON, the component falls back to comma-separated parsing for `args` and returns `undefined` for `env`.
- Default page seeding is skipped if the API navigation item already has a child page.


## Related Changes

### New API Types

- The portal now accepts three additional API types: `MCP_PROXY`, `LLM_PROXY`, and `A2A_PROXY` (in addition to `PROXY`, `MESSAGE`, and `NATIVE`). Only `MCP_PROXY` triggers MCP-specific Overview page seeding.

### HTML Sanitizer Updates

- The HTML sanitizer allowlist was extended to preserve the `<gmd-install-mcp>` element and its attributes in stored Gravitee Markdown content.

### Implementation References

- These changes were introduced in [APIM-14224](https://gravitee.atlassian.net/browse/APIM-14224) (component, sanitizer, template variables, API types) and [APIM-14225](https://gravitee.atlassian.net/browse/APIM-14225) (default page seeding).

### Additional Resources

- For additional context on securing MCP proxies, see the [Secure MCP Proxy with OAuth2](https://documentation.gravitee.io/apim/ai-agent-management/secure-mcp-proxy-with-oauth2) documentation.
