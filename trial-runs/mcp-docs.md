---
description: Expose Model Context Protocol (MCP) servers through Gravitee API Management (APIM).
---

# Expose MCP servers with Gravitee

## Overview

Model Context Protocol (MCP) is an emerging standard that enables AI agents and large language models (LLMs) to discover and invoke external tools and data. By exposing MCP servers through Gravitee API Management (APIM), you add governance, observability, and security controls in front of agent-to-tool traffic.

This guide covers the following scenarios:

* Proxy an existing MCP server that is already unsecured
* Proxy an existing MCP server that is already secured with OAuth and follows MCP authorization requirements (RFC 9728)
* Control which MCP features and tools are visible/callable by using an Access Control List (ACL) policy
* Secure an unsecured MCP server by fronting it with APIM and an OAuth2 plan backed by Gravitee Access Management (AM)

## Prerequisites

* Access to an APIM environment with permission to create and deploy v4 APIs.
* An MCP server you want to expose, or a local test MCP server.
* For the “Secure an unsecured MCP server” scenario, an AM domain and permission to configure it.

{% hint style="warning" %}
This guide describes how to expose and govern MCP servers through APIM. It does not document how to implement an MCP server.
{% endhint %}

## Proxy an existing unsecured MCP server

Use this scenario when your upstream MCP server does not require authentication, but you still want to apply APIM governance and observability.

### Create the MCP proxy API in APIM

1. Start the v4 API creation wizard.
2. Enter an API **name** and **version**.
3. Select **AI Gateway** as the API architecture.
4. Select **MCP Proxy** as the proxy type.
5. Configure the API entrypoint **access path** (for example, `/mcp-proxy`).
6. Configure the API backend **endpoint** with the URL of your MCP server.
7. Create and publish a **Keyless** plan.
8. Deploy the API.

### Test with the official example MCP server

If you do not have an MCP server, you can use the official “Everything” example server to test the proxy.

1. Start the example server:
```bash
npx @modelcontextprotocol/server-everything streamableHttp
```

2. Configure your APIM endpoint to point to the local MCP server:
```text
http://localhost:3001/mcp
```

3. Save and redeploy the API.

{% hint style="info" %}
The example server typically listens on port `3001`.
{% endhint %}

## Proxy an existing secured MCP server

Exposing a secured MCP server through a proxy requires both the MCP client and the upstream MCP server to follow MCP authorization requirements for OAuth-protected resources (RFC 9728).

### Understand the required negotiation flow

For APIM to relay authentication correctly, the upstream MCP server must implement the following behavior:

1. Reject unauthenticated requests with `401 Unauthorized`.
2. Include a `WWW-Authenticate` header in the `401` response that contains `resource_metadata`.
3. Provide a `resource_metadata` URL that the client can call to discover which authorization server to use (for example, `http://mcpserver.com/.well-known/oauth-protected-resource`).
4. After discovery, the MCP client authenticates, obtains an access token, and retries the original request with the token.

{% hint style="warning" %}
If either the MCP client or the upstream MCP server does not follow this negotiation flow, APIM cannot relay authentication natively.
{% endhint %}

### Compatibility and testing

Support for this authentication specification is still being adopted across MCP clients.

* A test server you can use to validate this flow is the GitHub Copilot MCP API: `https://api.githubcopilot.com/mcp/`.
* VS Code (with the Copilot extension) is one of the few major clients that currently implements this part of the MCP specification correctly.

## Control access to MCP features with an ACL policy

You can restrict access to MCP server features by adding an Access Control List (ACL) policy to an MCP Proxy API in Policy Studio. The ACL policy can control visibility and execution for MCP features such as:

* Tools
* Resources
* Prompts

### Default behavior

If you add the ACL policy without any rules, the behavior is “deny all”:

* An MCP client can connect to the MCP server through the Gateway.
* The MCP client receives empty lists for tools, resources, and prompts.

### Allow only tool listing

Use this configuration to allow discovery without allowing tool execution.

1. Add an ACL rule to the API.
2. In the **Tools** feature, enable `tools/list`.
3. Leave **Name pattern type** set to `ANY`.
4. Save and deploy the API.

Result: MCP clients can list tools, but calls to execute tools are rejected.

### Allow listing and calling a specific tool

Use this configuration to expose only a single tool (for example, `get_weather`).

1. Add or edit an ACL rule.
2. In the **Tools** feature, enable `tools/list` and `tools/call`.
3. Set **Name pattern type** to `Literal`.
4. Set **Name pattern** to the exact tool name (for example, `get_weather`).
5. Save and deploy the API.

Result: Only that tool is visible and callable. All other tools remain hidden.

### Use conditional execution

Each ACL rule supports a **Trigger condition**. Use Gravitee Expression Language (EL) to apply rules conditionally based on request context (for example, token claims or request attributes).

{% hint style="info" %}
The **Trigger condition** field expects a Gravitee EL expression.
{% endhint %}

### Validate ACL behavior locally

To validate ACL rules without impacting production, use the “Everything” MCP server as described in the unsecured scenario:

1. Start the example server:
```bash
npx @modelcontextprotocol/server-everything streamableHttp
```

2. Configure the API endpoint:
```text
http://localhost:3001/mcp
```

3. Save and redeploy the API.

## Secure an unsecured MCP server with APIM and AM

This scenario secures an unsecured upstream MCP server by using an OAuth2 plan in APIM backed by AM.

{% hint style="danger" %}
If the upstream MCP server is already secured, this configuration does not work.
{% endhint %}

### Step 1: Prepare the MCP proxy API in APIM

1. Create a new v4 API and name it `API MCP Proxy`.
2. Create and publish a **Keyless** plan.
3. Deploy the API.
4. Test that APIM successfully proxies the MCP server without authentication.

### Step 2: Configure the MCP server resource in AM

1. In AM, open the target domain.
2. Create an entity named `MCP Servers` (or the equivalent “MCP server resource” entity).
3. Name the resource.
4. In **MCP Resource Identifier**, set the APIM MCP proxy API endpoint.
5. Let AM generate a **Client ID** and **Client Secret**, or provide your own. Save these credentials.

### Step 3: Enable Dynamic Client Registration in AM (recommended)

Dynamic Client Registration (DCR) reduces manual client setup.

1. In AM, go to **Settings > Client Registration**.
2. Enable DCR.

Result:

* If DCR is enabled, an MCP client (for example, VS Code) can create the application in AM and register the Client ID and Client Secret automatically.
* If DCR is disabled, you must manually create an application in AM, configure the redirect URLs, and configure the MCP client with the Client ID and Client Secret.

### Step 4: Enable user registration in AM (optional)

1. In AM, go to **Settings > Login > User Registration**.
2. Enable user registration.

### Step 5: Finalize the API security configuration in APIM

1. In your `API MCP Proxy` API:
   * Add a resource of type `Gravitee.io AM Authorization Server`.
   * Configure it by linking to your AM instance and using the Client ID and Client Secret from the AM resource.
   * Save the API.
2. Create an **OAuth2** plan and select the AM resource you just configured.
3. Delete the Keyless plan.
4. Redeploy the API.

### Expected behavior

When an MCP client connects to the MCP proxy API:

* The client uses the OAuth2 server configured in APIM.
* The user is redirected to the AM login page to authenticate (and can create a user if registration is enabled).
* After login, AM redirects back to the MCP client.
* The MCP client retrieves credentials, obtains a token, and calls the MCP API through APIM.

### VS Code cleanup

If you use VS Code and want to delete Client IDs registered through dynamic registration:

1. Open the command palette:
   * macOS: `Cmd+Shift+P`
   * Windows/Linux: `Ctrl+Shift+P`
2. Run:
   * `Authentication: Remove Dynamic Authentication Providers`

## Monitor MCP traffic in APIM

APIM provides observability for MCP traffic:

* Use **Logs** to track exchanges between the MCP client and the upstream MCP server.
* Use **API Traffic** dashboards to visualize MCP server usage, common tools/methods, and server errors.
