# Proxy MCP Servers

## Overview

This guide explains how to use Gravitee API Management (APIM) to proxy Model Context Protocol (MCP) servers. MCP is a protocol that enables AI agents to interact with external tools and data sources. By proxying MCP servers through Gravitee, you can add governance, observability, and access control to your MCP infrastructure.

Gravitee supports three primary MCP proxy scenarios:

* **Exposing an unsecured MCP server**: Add a layer of control and monitoring to an open MCP server
* **Exposing a secured MCP server**: Proxy MCP servers that implement OAuth-based authentication
* **Securing an unsecured MCP server**: Use Gravitee Access Management (AM) to add OAuth2 authentication to an open MCP server

## Prerequisites

Before you proxy an MCP server, ensure you have:

* Gravitee APIM 4.9 or later installed and running
* Access to the APIM Console with permissions to create and deploy APIs
* An MCP server endpoint (either local or remote)
* For OAuth scenarios: Gravitee Access Management (AM) configured with appropriate domain access

## Expose an unsecured MCP server

This scenario demonstrates how to proxy an existing MCP server that does not require authentication. Gravitee adds governance, observability, and control without modifying the backend server.

### Create the MCP proxy API

1. In the APIM Console, navigate to **APIs** and click **+ Add API**.

2. Select **V4 API** as the API type.

3. Configure the general settings:
    * Enter a name for your API (for example, "MCP Proxy")
    * Enter a version number
    * Select **AI Gateway** as the architecture type

4. Configure the proxy settings:
    * Select **MCP Proxy** as the proxy type
    * Define the entrypoint path (for example, `/mcp-proxy`)

5. Configure the backend endpoint:
    * Enter the URL of your target MCP server
    * For a local test server: `http://localhost:3001/mcp`

6. Configure security:
    * Select **Keyless** as the plan type for this example

7. Click **Create** to finalize the API configuration.

8. Deploy the API by clicking **Deploy** in the API details page.

### Monitor MCP traffic

After deploying your API, you can monitor MCP server interactions:

* **Request logs**: Navigate to **APIs > [Your API] > Logs** to view detailed request and response data between MCP clients and the server
* **Traffic analytics**: Navigate to **APIs > [Your API] > Analytics** to view MCP server usage metrics, frequently used methods and tools, and error rates

### Test with a local MCP server

If you don't have an MCP server available, you can test using the official MCP example server:

1. Install and start the example server:

    ```bash
    npx @modelcontextprotocol/server-everything streamableHttp
    ```

    The server starts on port 3001 by default.

2. Configure your Gravitee API endpoint to use `http://localhost:3001/mcp`.

3. Deploy the API and test the connection using an MCP client.

<!-- NEED CLARIFICATION: The source mentions an internal Gravitee tool URL (https://apim-tools-mcp-server.team-apim.gravitee.dev/mcp) that should NOT be included in public documentation. Should this be documented in internal-only materials? -->

## Expose a secured MCP server

Proxying a secured MCP server requires both the backend server and the client to implement the MCP specification's OAuth authentication flow as defined in RFC 9728.

### MCP authentication flow

The MCP authentication flow works as follows:

1. **Initial challenge**: The MCP server rejects unauthenticated requests with a `401 Unauthorized` response.

2. **Authentication discovery**: The `401` response includes a `WWW-Authenticate` header containing `resource_metadata` that points to an OAuth metadata endpoint (for example, `http://mcpserver.com/.well-known/oauth-protected-resource`).

3. **Metadata retrieval**: The MCP client calls the metadata endpoint to discover the authorization server details.

4. **Token acquisition**: The client authenticates with the authorization server and obtains an access token.

5. **Authenticated request**: The client retries the original request with the access token.

{% hint style="warning" %}
If either the MCP client or server does not implement this authentication flow correctly, the Gravitee proxy cannot relay authentication natively. Both components must strictly adhere to the MCP specification.
{% endhint %}

### Test with GitHub Copilot API

As of this writing, support for MCP OAuth authentication is still being adopted across the ecosystem. To test this flow:

* **Test server**: Use the GitHub Copilot API at `https://api.githubcopilot.com/mcp/`
* **Compatible client**: Use Visual Studio Code with the Copilot extension, which correctly implements the MCP authentication specification

## Control access to MCP tools

Gravitee provides an Access Control List (ACL) policy that restricts access to MCP server features such as tools, resources, and prompts.

### Default behavior (implicit deny)

When you add the ACL policy without configuring any rules, the system adopts a "deny all" approach:

1. Navigate to **APIs > [Your API] > Policy Studio**.

2. Add the **MCP ACL** policy to your API flow.

3. Save and deploy the API.

**Result**: All MCP server functionality becomes inaccessible. MCP clients can connect to the server through the Gateway, but the lists of tools, resources, and prompts appear empty.

### Allow tool listing only

To allow clients to view available tools without executing them:

1. In the ACL policy configuration, add a new rule.

2. Configure the rule:
    * Select **Tools** as the feature type
    * Check the **tools/list** checkbox
    * Leave **Name Pattern Type** set to **ANY**

3. Save and deploy the API.

**Result**: MCP clients can list available tools but cannot execute them. Any attempt to call a tool is rejected.

### Allow specific tool access

To restrict access to a single tool (for example, `get_weather`):

1. In the ACL policy configuration, add or modify a rule.

2. Configure the rule:
    * Select **Tools** as the feature type
    * Check both **tools/list** and **tools/call**
    * Set **Name Pattern Type** to **Literal**
    * Enter the exact tool name in **Name Pattern** (for example, `get_weather`)

3. Save and deploy the API.

**Result**: Only the specified tool is visible to MCP clients and can be executed. All other tools remain hidden and inaccessible.

### Configure conditional access

Each ACL rule includes a **Trigger Condition** field that accepts Gravitee Expression Language (EL) expressions. Use this field to apply context-based security policies.

**Example use case**: Condition tool access based on a claim in the user's token or a request attribute.

### Test ACL policies locally

To validate ACL configurations without affecting production, use the official MCP "Everything" example server, which exposes numerous tools ideal for testing filters.

1. Install and start the server:

    ```bash
    npx @modelcontextprotocol/server-everything streamableHttp
    ```

2. Configure your Gravitee API endpoint to use `http://localhost:3001/mcp`.

3. Save and deploy the API.

4. Test your ACL policy by connecting an MCP client and verifying that only the configured tools are visible and callable.

## Secure an MCP server with Gravitee

This scenario demonstrates how to add OAuth2 authentication to an unsecured MCP server using Gravitee APIM and Gravitee Access Management (AM).

{% hint style="warning" %}
This configuration only works if the MCP server itself does not already implement authentication. If the backend server is secured, use the "Expose a secured MCP server" scenario instead.
{% endhint %}

### Prerequisites

Before you begin, ensure you have:

* A configured AM domain with appropriate permissions
* An MCP client (for example, Visual Studio Code) that supports MCP OAuth authentication

### Create the MCP proxy API

1. In the APIM Console, create a new V4 API named "MCP Proxy".

2. Configure the API with:
    * Architecture type: **AI Gateway**
    * Proxy type: **MCP Proxy**
    * Backend endpoint: Your MCP server URL

3. Create a **Keyless** plan.

4. Deploy the API and verify that it successfully proxies the MCP server without authentication.

### Configure the MCP server in AM

1. In AM, navigate to your domain and create a new **MCP Server** resource.

2. Configure the MCP server:
    * Enter a name for the resource
    * In **MCP Resource Identifier**, enter your APIM API endpoint URL
    * Generate or provide a Client ID and Client Secret
    * Save the credentials for later use

### Enable Dynamic Client Registration (recommended)

Dynamic Client Registration (DCR) allows MCP clients to automatically register with AM without manual application creation.

1. In AM, navigate to **Settings > Client Registration**.

2. Enable DCR.

**Result**:
* **If DCR is enabled**: The MCP client automatically creates an application in AM and registers the Client ID and Client Secret
* **If DCR is not enabled**: You must manually create an application in AM for the MCP client and configure redirect URLs. You must also configure the MCP client with the Client ID and Client Secret.

### Enable user registration (optional)

To allow users to create accounts during the authentication flow:

1. In AM, navigate to **Settings > Login > User Registration**.

2. Enable the registration option.

### Configure OAuth2 in APIM

1. In your MCP Proxy API, navigate to **Resources**.

2. Add a new resource of type **Gravitee.io AM Authorization Server**.

3. Configure the resource:
    * Link it to your AM instance
    * Enter the Client ID and Client Secret from the MCP Server resource created in AM

4. Save the resource.

5. Navigate to **Plans** and add a new **OAuth2** plan using the AM resource.

6. Delete the Keyless plan.

7. Deploy the API.

### Verify the configuration

When an MCP client connects to the API:

1. The client is redirected to the AM login page.

2. The user logs in with an existing AM account or creates a new account (if registration is enabled).

3. After successful authentication, AM redirects back to the MCP client.

4. The MCP client retrieves the Client ID and Client Secret and creates a token to access the secured MCP API.

### Remove dynamic authentication providers in Visual Studio Code

If you're using Visual Studio Code and need to remove dynamically registered Client IDs:

1. Open the Command Palette (`Cmd+Shift+P` on macOS or `Ctrl+Shift+P` on Windows/Linux).

2. Search for and select **Authentication: Remove Dynamic Authentication Providers**.