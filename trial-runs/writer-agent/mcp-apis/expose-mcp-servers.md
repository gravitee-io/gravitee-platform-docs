---
description: Learn how to expose MCP servers through the Gravitee Gateway.
---

# Expose MCP Servers

## Overview

This guide explains how to expose Model Context Protocol (MCP) servers via the Gravitee Gateway. MCP is an emerging standard that enables AI agents to understand and interact with external tools and data. By exposing your MCP servers through Gravitee API Management (APIM), you can maintain governance, observability, and security over interactions between AI agents and your backend services.

You can expose two types of MCP servers:

* **Unsecured MCP server:** The backend MCP server doesn't require its own authentication. Gravitee adds a layer of governance, observability, and control.
* **Secured MCP server:** The backend MCP server requires OAuth authentication. The Gravitee Gateway proxies the authentication flow between the MCP client and server.

## Prerequisites

* A running Gravitee APIM installation
* An MCP server to proxy (or use the example server provided in [Test the proxy](expose-mcp-servers.md#test-the-proxy))

## Expose an unsecured MCP server

Use this procedure to publish an existing MCP server that doesn't require its own authentication. The Gravitee Gateway adds governance, observability, and access control to the backend server.

1. Log in to your APIM Console.
2. Click **APIs** from the left nav, then click **+ Add API**.
3. Start the V4 API creation process.
4. Enter your API name and version.
5. For **Architecture**, select **AI Gateway**.
6. For **Proxy Type**, select **MCP Proxy**.
7. Configure the entrypoint by defining an access path. For example, `/mcp-proxy`.
8. Configure the endpoint by entering the URL of your target MCP server.
9. For security, proceed with a **Keyless** plan for this example.
10. Validate the creation and deploy the API.

<!-- NEED CLARIFICATION: Missing screenshot for API creation wizard showing MCP Proxy selection -->

### Monitor MCP traffic

After you deploy the API, you can monitor MCP server usage in the APIM Console:

* **Logs screen:** Track exchanges between the MCP server and MCP clients.
* **API Traffic screen:** View a dashboard that displays MCP server usage, the methods and tools used, and any errors encountered by the server.

## Test the proxy

If you don't have an MCP server, you can test your configuration with the official MCP example server.

1.  Start the example server by running the following command:

    ```bash
    npx @modelcontextprotocol/server-everything streamableHttp
    ```

    The server starts on port 3001 by default.
2. In your Gravitee API configuration, set the backend endpoint URL to `http://localhost:3001/mcp`.
3. Save and deploy the API.

{% hint style="info" %}
For more information about the example server, see the [MCP Servers Everything repository](https://github.com/modelcontextprotocol/servers/tree/main/src/everything).
{% endhint %}

## Expose a secured MCP server

Exposing a secured MCP server through a proxy requires the backend server and the MCP client to strictly adhere to the MCP specification for OAuth authentication.

### Authentication flow

For the connection to work through the Gravitee Gateway, the following authentication flow must occur:

1. **Initial challenge:** The MCP server rejects the unauthenticated request with a `401 Unauthorized` response code.
2. **WWW-Authenticate header:** The 401 response includes a `WWW-Authenticate` header containing `resource_metadata`. This header points to a metadata resource URL, such as `http://mcpserver.com/.well-known/oauth-protected-resource`.
3. **Auth discovery:** The MCP client calls the `.well-known/oauth-protected-resource` URL to obtain information about the authentication server.
4. **Token retrieval:** The client authenticates with the authorization server and retrieves a token to retry the initial request.

{% hint style="warning" %}
If the MCP client or server doesn't follow this authentication flow, the Gravitee Gateway can't relay the authentication natively. Both ends must comply with the MCP specification.
{% endhint %}

### Compatibility

Support for this authentication specification is still being adopted across MCP implementations.

* **Test server:** You can test this flow with the GitHub Copilot API at `https://api.githubcopilot.com/mcp/`.
* **Compatible client:** VS Code (via the Copilot extension) is one of the only major clients that correctly implements this part of the MCP specification.

## Next steps

* To control which tools, resources, and prompts are accessible through your MCP proxy, see [MCP ACL Policy](mcp-acl-policy.md).
* To secure an unsecured MCP server using Gravitee Access Management, see [Secure an MCP Server with Gravitee AM](secure-mcp-server-with-am.md).
