# Exposing a Secured MCP Server via Gravitee APIM

## Overview

This guide explains how to expose a secured Model Context Protocol (MCP) server through Gravitee APIM. It covers the MCP OAuth authentication flow, client and server specification compliance requirements, and compatibility constraints.

{% hint style="warning" %}
Both the MCP client and server must strictly adhere to the MCP specification for the proxy to function correctly. Support for this authentication specification is still being adopted across the ecosystem.
{% endhint %}

## Prerequisites

Before you expose a secured MCP server, ensure the following:

* You have a Gravitee APIM installation with the MCP proxy plugin installed
* Your MCP server implements the OAuth authentication flow as defined in the MCP specification
* Your MCP client supports the MCP OAuth authentication flow

## MCP authentication flow

For a secured MCP server to work through a Gravitee proxy, the following authentication mechanism must occur:

1. **Initial challenge:** The MCP server rejects the unauthenticated request with a `401 Unauthorized` status code.
2. **WWW-Authenticate header:** The `401` response includes a `WWW-Authenticate` header containing `resource_metadata`. This header provides a URL to the OAuth protected resource metadata endpoint.

    Example header:

    ```
    WWW-Authenticate: Bearer realm="example", resource_metadata="http://mcpserver.com/.well-known/oauth-protected-resource"
    ```

3. **Auth discovery:** The MCP client calls the `.well-known/oauth-protected-resource` URL to retrieve information about the authentication server.
4. **Token retrieval:** The client authenticates with the authorization server and obtains an access token.
5. **Retry with token:** The client retries the original request, including the access token in the `Authorization` header.

{% hint style="danger" %}
If either the MCP client or server does not implement this negotiation flow correctly, the Gravitee proxy cannot relay authentication natively. The API proxy will fail to establish the connection.
{% endhint %}

## Compatibility and testing

As of the draft date, support for the MCP OAuth authentication specification is still being adopted across the ecosystem.

### Recommended test server

You can test the MCP OAuth authentication flow using the GitHub Copilot API:

```
https://api.githubcopilot.com/mcp/
```

### Compatible client

Currently, VS Code with the Copilot extension is one of the few major clients that correctly implements the MCP OAuth authentication specification.

## Next steps

After successfully exposing your secured MCP server through Gravitee APIM, you can:

* Configure access control policies to restrict which clients can access specific MCP tools
* Monitor MCP server usage through Gravitee analytics
* Apply rate limiting and quota policies to control consumption