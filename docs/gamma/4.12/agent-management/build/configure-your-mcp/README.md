---
hidden: false
noIndex: false
---

# Configure your MCP proxy
<!-- GAP-STRUCTURAL: Missing procedural content source -->

After creating an MCP Proxy, configure how it handles upstream authentication. These settings control how the proxy authenticates with upstream MCP servers on behalf of your users and agents.

## Upstream Authentication

Securing third-party MCP servers (HubSpot, Salesforce, GitHub, Slack, Jira) is one of the most important problems the MCP Proxy solves. The MCP Proxy handles authentication by injecting the necessary credentials before forwarding the request to the upstream server.

The MCP Proxy currently supports injecting static credentials into the request headers.

## Configure Upstream Authentication

1. Navigate to your MCP Proxy in the Gravitee console.
2. Open the **Upstream Authentication** section for the server.
3. Select an authentication method:
   * **Static credential**: Inject a static credential into a request header on every call.
   * **No upstream auth**: Call the upstream without injecting credentials (passthrough).
4. If you chose **Static credential**, select the **Credential type**:
   * **API key**: Enter the Header name (e.g., `x-api-key`) and the API key value.
   * **Bearer token**: Enter the token value (injected as `Authorization: Bearer <token>`).
   * **Basic auth**: Enter the Username and Password (injected as `Authorization: Basic <base64>`).
   * **Custom secret**: Enter a Custom Header name and the secret value.
5. Save your configuration.

## Next steps

* [Add policies to your MCP server](add-policies-to-mcp-server.md) — Apply fine-grained authorization at the tool level.
