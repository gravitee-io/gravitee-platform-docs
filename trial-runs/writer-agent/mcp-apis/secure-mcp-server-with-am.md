---
description: Learn how to secure an unsecured MCP server using Gravitee APIM and Access Management.
---

# Secure an MCP Server with Gravitee AM

## Overview

This guide explains how to secure an unsecured Model Context Protocol (MCP) server using Gravitee API Management (APIM) and an OAuth2 plan with Gravitee Access Management (AM).

{% hint style="warning" %}
This configuration only works with MCP servers that don't have their own authentication. If your MCP server is already secured, see [Expose MCP Servers](expose-mcp-servers.md#expose-a-secured-mcp-server) for information on proxying secured MCP servers.
{% endhint %}

## Prerequisites

* An AM domain with configuration rights
* An MCP client that supports the MCP protocol with OAuth2 authentication (for example, VS Code)

## Prepare the API proxy in APIM

1. Log in to your APIM Console.
2. Create a new API and name it "API MCP Proxy."
3. Create a **Keyless** plan as an initial configuration.
4. Deploy the API.
5. Test that the API correctly proxies the MCP server without authentication.

<!-- NEED CLARIFICATION: Missing screenshot for API creation with Keyless plan -->

## Configure the MCP server in AM

1. Log in to your AM Console.
2. Navigate to the desired domain.
3. Create an **MCP Servers** resource (or equivalent MCP server resource entity).
4. Enter a name for this resource.
5. In the **MCP Resource Identifier** field, add the APIM API endpoint URL.
6. Let AM generate a **Client ID** and **Client Secret**, or provide your own values.
7. Save the credentials. You need them for the APIM configuration.

<!-- NEED CLARIFICATION: Missing screenshot for AM MCP Server resource configuration -->

## Configure DCR in AM

Dynamic Client Registration (DCR) is recommended to avoid manually creating an Application in AM and specifying its Client ID in the MCP client.

1. In AM, navigate to **Settings > Client Registration**.
2. Enable **DCR**.

<!-- NEED CLARIFICATION: Missing screenshot for DCR settings in AM -->

{% hint style="info" %}
**With DCR enabled:** The MCP client (for example, VS Code) automatically creates the application in AM and registers the Client ID and Client Secret.

**Without DCR:** You must manually create an Application in AM for the MCP client, configure the redirect URLs, and configure the MCP client with the Client ID and Client Secret.
{% endhint %}

## Activate user registration in AM

(Optional) Enable user registration so that users can create accounts during the OAuth flow.

1. In AM, navigate to **Settings > Login > User Registration**.
2. Enable the registration option.

<!-- NEED CLARIFICATION: Missing screenshot for user registration settings in AM -->

## Finalize configuration in APIM

1. Open your API MCP Proxy in APIM.
2. Add a resource of type **Gravitee.io AM Authorization Server**.
3. Configure the resource by linking it to your AM instance and using the Client ID and Client Secret you created earlier for the MCP server resource in AM.
4. Save the resource configuration.
5. Add an **OAuth2** plan that uses the AM resource you added.
6. Delete the **Keyless** plan.
7. Redeploy the API.

<!-- NEED CLARIFICATION: Missing screenshot for AM Authorization Server resource configuration -->

## Verification

When an MCP client connects to the API:

1. The client is redirected to the AM login page.
2. The user authenticates with an existing AM user or creates a new account (if you enabled user registration).
3. After successful authentication, AM redirects the user back to the MCP client.
4. The MCP client retrieves the Client ID and Client Secret in the background.
5. The MCP client creates a token to access the MCP API, which is now secured through APIM.

## Troubleshooting

### Clear dynamic authentication providers in VS Code

If you use VS Code and want to delete Client IDs registered through dynamic registration:

1. Open the command palette with **Cmd+Shift+P** (macOS) or **Ctrl+Shift+P** (Windows/Linux).
2. Search for and run the command: **Authentication: Remove Dynamic Authentication Providers**.

## Next steps

* To learn how to expose MCP servers through the Gateway, see [Expose MCP Servers](expose-mcp-servers.md).
* To control which tools, resources, and prompts are accessible through your MCP proxy, see [MCP ACL Policy](mcp-acl-policy.md).
