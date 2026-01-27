# Secure MCP with AM

## Overview

This guide explains how to secure Model Context Protocol (MCP) servers using Gravitee Access Management (AM). By integrating AM with your MCP infrastructure, you can enforce OAuth 2.0 authorization, control tool access, and manage agent authentication across your MCP deployments.

MCP servers expose tools that agents and LLMs can invoke. Without proper authorization, any client can access these tools. Gravitee AM provides centralized identity and access management, allowing you to define which users, applications, or agents can discover and use specific MCP tools.

## Prerequisites

Before you secure MCP servers with AM, complete the following steps:

* Install and configure Gravitee Access Management 4.10 or later
* Deploy at least one MCP server (either a Gravitee MCP Tool Server or an existing MCP server proxied through Gravitee)
* Ensure your MCP clients support OAuth 2.0 authorization flows
* Have administrative access to both AM and your MCP server configuration

## Configure AM as the authorization server

1. Log in to the AM Console.

2. Navigate to **Settings** > **Providers**, and then click **Create Provider**.

3. Select **OAuth 2.0 / OpenID Connect** as the provider type.

4. Configure the provider settings:
   * **Name**: Enter a descriptive name for the MCP authorization provider
   * **Client ID**: Generate or provide a client identifier
   * **Client Secret**: Generate or provide a client secret
   * **Token Endpoint**: Specify the AM token endpoint URL
   * **Authorization Endpoint**: Specify the AM authorization endpoint URL

5. Click **Save**.

6. Navigate to **Applications**, and then click **Create Application**.

7. Configure the application settings:
   * **Name**: Enter a name for your MCP client application
   * **Type**: Select **Service** or **Web Application** depending on your MCP client type
   * **Grant Types**: Enable **Authorization Code** and **Refresh Token**
   * **Redirect URIs**: Add the callback URLs your MCP client will use

8. Click **Create**.

9. Note the **Client ID** and **Client Secret** displayed. You will need these values to configure your MCP server.

## Configure the MCP server for AM integration

1. Navigate to **Access Management** in the Gravitee Console.

2. Select **MCP Servers** from the left navigation menu.

3. Click on the MCP server you want to secure, or create a new one.

4. In the **MCP Server Settings** section, locate the **Domain** field.

    ![New MCP server form showing domain, name, resource identifier, and description fields](.gitbook/assets/apim-mcp-am-step-01.png)

5. Enter the AM security domain in the **Domain** field (for example, `/agentic`).

6. Complete the remaining required fields:
   * **Name**: Enter a descriptive name for the MCP server
   * **MCP Resource Identifier**: Provide the canonical resource identifier (for example, `https://banking.example.com`)
   * **Description**: Add an optional description

7. Scroll to the **Tools Configuration** section.

8. Click **Add tool** to define the tools this MCP server provides.

9. Configure tool-level access control:
   * **Tool Name**: Enter the name of the tool
   * **Scopes**: Define OAuth 2.0 scopes required to access this tool
   * **Description**: Provide a description of what the tool does

10. Click **Save** to apply the configuration.

## Implement RFC 9728 authorization flow

The MCP authorization flow follows RFC 9728 (OAuth 2.0 Protected Resource Metadata). When an MCP client attempts to use a tool without a valid token, the server responds with a 401 error and authorization metadata.

1. Configure your MCP server to return RFC 9728-compliant error responses:

    ```json
    {
      "error": "unauthorized",
      "error_description": "Authorization required",
      "authorization_endpoint": "https://am.example.com/oauth/authorize",
      "token_endpoint": "https://am.example.com/oauth/token",
      "scopes_supported": ["mcp:tools:read", "mcp:tools:execute"]
    }
    ```

2. Update your MCP client configuration to handle the authorization flow:
   * Parse the 401 response to extract authorization endpoints
   * Redirect the user to the authorization endpoint
   * Exchange the authorization code for an access token
   * Include the access token in subsequent MCP requests

3. Test the authorization flow:
   * Attempt to invoke an MCP tool without authentication
   * Verify that the server returns a 401 response with authorization metadata
   * Complete the OAuth 2.0 flow and obtain an access token
   * Retry the tool invocation with the access token

## Configure tool access control

1. Navigate to **MCP Servers** in the Gravitee Console.

2. Select the MCP server you want to configure.

3. Click **Authorization** in the left navigation menu.

4. Define access control rules:
   * **Consumer Type**: Select **Application**, **User**, or **Agent**
   * **Allowed Tools**: Select which tools this consumer can access
   * **Scopes**: Assign OAuth 2.0 scopes that grant specific permissions

5. Create multiple access control rules to define different permission levels for different consumer types.

6. Click **Save** to apply the access control configuration.

7. Test the access control:
   * Authenticate as a consumer with limited tool access
   * Attempt to invoke a tool that is not included in the consumer's allowed tools list
   * Verify that the request is denied with an appropriate error message

## Verification

To verify that your MCP server is properly secured with AM:

1. Attempt to connect to the MCP server without authentication. The connection should fail with a 401 error.

2. Complete the OAuth 2.0 authorization flow and obtain an access token.

3. Connect to the MCP server using the access token. The connection should succeed.

4. Invoke a tool that your consumer has permission to access. The invocation should succeed.

5. Attempt to invoke a tool that your consumer does not have permission to access. The invocation should fail with a 403 error.

6. Review the MCP analytics in the Gravitee Console to confirm that authorization events are being logged correctly.

## Next steps

After securing your MCP server with AM, consider the following additional configurations:

* Configure agent-to-agent (A2A) tool access control to manage interactions between multiple agents
* Set up MCP analytics to monitor tool usage and authorization patterns
* Implement token rate limiting to control resource consumption
* Explore MCP discovery mechanisms to allow agents to dynamically find and integrate tools

<!-- ASSETS USED (copy/rename exactly):
- screenshots/mcp-server-form.png -> trial-runs/.gitbook/assets/apim-mcp-am-step-01.png | alt: "New MCP server form showing domain, name, resource identifier, and description fields"
-->