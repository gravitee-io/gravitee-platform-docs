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

1. In the Gravitee console, navigate to **MCP Proxies** and open your MCP Proxy.
2. In the left menu under **General**, select **Endpoint**. This page contains the **Upstream authentication** section.
3. Select one of the following authentication methods:
   * **Static credential**. Inject a static credential into a request header on every call.
   * **No upstream auth**. Call the upstream without injecting credentials.
4. If you chose **Static credential**, open the **Credential type** list and select one of the following:
   * **API key**. Select an **Injection location** of **Authorization header**, **x-api-key header**, or **Custom header**. If you select **Custom header**, enter the **Header name**. Enter the key in the **Credential** field.
   * **Bearer token**. Enter the token in the **Credential** field. The Gateway injects it as `Authorization: Bearer <token>`.
   * **Basic auth**. Enter the **Username** and **Password / token**. The Gateway injects them as `Authorization: Basic <base64>`.
   * **Custom secret**. Select an **Injection location** of **Authorization header**, **x-api-key header**, or **Custom header**. If you select **Custom header**, enter the **Header name**. Enter the secret in the **Credential** field.
5. Click **Save changes**.

## Next steps

* [Add policies to your MCP server](add-policies-to-mcp-server.md) — Apply fine-grained authorization at the tool level.
