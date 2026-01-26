# mcp-proxy-setup.md.writer-output.md

# Configure MCP Proxy

## Overview

This guide explains how to configure Gravitee API Management (APIM) to proxy Model Context Protocol (MCP) servers. MCP is a protocol that enables AI agents to interact with external tools and data sources. By proxying MCP servers through Gravitee, you can add governance, observability, and access control to agent-to-tool interactions.

This guide covers three primary scenarios:

* Exposing an unsecured MCP server with Gravitee-managed authentication
* Exposing a secured MCP server that implements its own authentication
* Controlling access to MCP tools using access control lists (ACLs)

## Prerequisites

Before configuring an MCP proxy, ensure you have:

* Gravitee APIM 4.9 or later installed and running
* Access to the APIM Console with API creation permissions
* An MCP server endpoint (either local or remote)
* For secured scenarios: Gravitee Access Management (AM) configured with an appropriate domain

## Expose an unsecured MCP server

This scenario demonstrates how to proxy an existing MCP server that does not implement its own authentication. Gravitee adds a layer of governance, observability, and access control through APIM.

### Create the MCP proxy API

1. Navigate to **APIs** in the APIM Console and click **+ Add API**.

2. Select **Create a V4 API** and click **Next**.

3. Configure the API general settings:
   * Enter a name for your API (for example, "MCP Proxy API")
   * Enter a version (for example, "1.0")
   * Optionally, enter a description

4. Select **AI Gateway** as the architecture type and click **Next**.

5. Select **MCP Proxy** as the proxy type and click **Next**.

6. Configure the entrypoint:
   * Enter the context path where the API will be accessible (for example, `/mcp-proxy`)
   * Click **Next**

7. Configure the endpoint:
   * Enter the URL of your target MCP server
   * For local testing, use `http://localhost:3001/mcp`
   * Click **Next**

8. Configure security:
   * Select **Keyless (public)** to create an open plan
   * Click **Next**

9. Review your configuration and click **Create API**.

10. Deploy the API by clicking **Deploy API** in the banner notification.

### Verify the configuration

Verify that your MCP proxy is working correctly by:

* Navigating to **APIs > [Your API] > Logs** to view request and response exchanges between the MCP client and server
* Navigating to **APIs > [Your API] > Analytics** to view usage metrics, including tool invocations, method calls, and error rates

### Test with the example MCP server

If you don't have an MCP server available, you can test using the official MCP example server:

1. Install and start the example server:

    ```bash
    npx @modelcontextprotocol/server-everything streamableHttp
    ```

    The server starts on port 3001 by default.

2. Configure your MCP proxy API endpoint to use `http://localhost:3001/mcp`.

3. Deploy the API and test the connection using an MCP client such as VS Code with the Copilot extension.

## Expose a secured MCP server

Exposing a secured MCP server through Gravitee requires both the server and client to implement the MCP authentication specification defined in RFC 9728. This flow enables OAuth 2.0-based authentication for MCP tool access.

### Authentication flow

The MCP authentication flow works as follows:

1. **Initial challenge**: The MCP server rejects unauthenticated requests with a `401 Unauthorized` response.

2. **WWW-Authenticate header**: The 401 response includes a `WWW-Authenticate` header containing `resource_metadata` that points to an OAuth 2.0 protected resource metadata endpoint (for example, `http://mcpserver.com/.well-known/oauth-protected-resource`).

3. **Auth discovery**: The MCP client calls the `.well-known/oauth-protected-resource` endpoint to discover the authorization server configuration.

4. **Token retrieval**: The client authenticates with the authorization server and retrieves an access token.

5. **Authenticated request**: The client retries the original request with the access token in the `Authorization` header.

{% hint style="warning" %}
If either the MCP client or server does not implement this authentication flow correctly, the proxy cannot relay authentication natively. Ensure both components support RFC 9728.
{% endhint %}

### Compatibility and testing

As of APIM 4.9, support for the MCP authentication specification is still being adopted across the ecosystem.

**Recommended test server**: GitHub Copilot API at `https://api.githubcopilot.com/mcp/`

**Compatible client**: VS Code with the Copilot extension is currently one of the only major clients that correctly implements this part of the MCP specification.

To test this flow:

1. Create an MCP proxy API in Gravitee pointing to `https://api.githubcopilot.com/mcp/`.

2. Configure the API with a Keyless plan initially to verify connectivity.

3. Use VS Code with the Copilot extension as your MCP client.

4. Verify that the authentication flow completes successfully and that the client can access MCP tools through the proxy.

## Secure an unsecured MCP server with Gravitee

This scenario demonstrates how to add OAuth 2.0 authentication to an unsecured MCP server using Gravitee APIM and Gravitee Access Management (AM).

{% hint style="danger" %}
This configuration only works if the upstream MCP server does not implement its own authentication. If the server is already secured, use the flow described in [Expose a secured MCP server](mcp-proxy-setup.md#expose-a-secured-mcp-server).
{% endhint %}

### Configure the MCP proxy API

1. Create an MCP proxy API following the steps in [Expose an unsecured MCP server](mcp-proxy-setup.md#expose-an-unsecured-mcp-server).

2. Create a Keyless plan and deploy the API.

3. Test that the API correctly proxies requests to the MCP server without authentication.

### Configure the MCP server in Access Management

1. Navigate to your AM domain in the Access Management Console.

2. Navigate to **MCP Servers** and click **+ Add MCP Server**.

    <figure><img src=".gitbook/assets/apim-mcp-proxy-step-01.png" alt="New MCP server configuration form showing domain, name, resource identifier, and description fields"><figcaption></figcaption></figure>

3. Configure the MCP server:
   * Enter a name for the MCP server resource
   * In the **MCP Resource Identifier** field, enter the APIM API endpoint URL (for example, `https://api.example.com/mcp-proxy`)
   * Optionally, enter a description

4. Click **Create**.

5. Note the generated **Client ID** and **Client Secret**. You will need these credentials to configure the APIM resource.

### Configure Dynamic Client Registration (recommended)

Dynamic Client Registration (DCR) allows MCP clients to automatically register themselves with AM without manual application creation.

1. Navigate to **Settings > Client Registration** in your AM domain.

2. Enable **Dynamic Client Registration**.

3. Configure any additional DCR settings as needed for your security requirements.

{% hint style="info" %}
If DCR is not enabled, you must manually create an application in AM for each MCP client and configure the client with the application's Client ID and Client Secret.
{% endhint %}

### Enable user registration (optional)

To allow users to create accounts during the authentication flow:

1. Navigate to **Settings > Login > User Registration** in your AM domain.

2. Enable **User Registration**.

3. Configure any additional registration settings as needed.

### Configure OAuth 2.0 in APIM

1. Navigate to your MCP proxy API in the APIM Console.

2. Navigate to **Backend Services > Resources** and click **+ Add Resource**.

3. Select **Gravitee.io AM Authorization Server** as the resource type.

4. Configure the resource:
   * Enter a name for the resource
   * Enter your AM instance URL
   * Enter the **Client ID** from the MCP server configuration in AM
   * Enter the **Client Secret** from the MCP server configuration in AM
   * Configure any additional OAuth 2.0 settings as needed

5. Click **Save**.

6. Navigate to **Plans** and click **+ Add Plan**.

7. Select **OAuth 2.0** as the security type.

8. Configure the plan:
   * Enter a name for the plan
   * Select the AM Authorization Server resource you created
   * Configure any additional plan settings as needed

9. Click **Save**.

10. Delete the Keyless plan.

11. Deploy the API.

### Verify the configuration

1. Configure an MCP client (such as VS Code with the Copilot extension) to connect to your MCP proxy API endpoint.

2. When the client attempts to connect, it should be redirected to the AM login page.

3. Log in with an existing AM user or create a new account if user registration is enabled.

4. After successful authentication, the client should be redirected back and receive an access token.

5. Verify that the client can now access MCP tools through the authenticated proxy.

{% hint style="info" %}
**VS Code users**: To remove dynamically registered authentication providers, open the command palette (`Cmd+Shift+P` on macOS or `Ctrl+Shift+P` on Windows/Linux) and run **Authentication: Remove Dynamic Authentication Providers**.
{% endhint %}

## Control access to MCP tools

The MCP Access Control List (ACL) policy allows you to restrict which MCP tools, resources, and prompts are accessible through the proxy. This enables fine-grained control over agent capabilities.

### Default behavior (implicit deny)

When you add the MCP ACL policy without configuring any rules, the system adopts a "deny all" approach by default.

1. Navigate to your MCP proxy API in the APIM Console.

2. Navigate to **Policy Studio**.

3. Add the **MCP Access Control List** policy to the request flow.

4. Save and deploy the API.

**Result**: All MCP server functionalities are inaccessible. MCP clients can connect to the server through the Gateway, but the lists of tools, resources, and prompts appear empty.

### Allow tool listing only

To allow clients to view available tools without being able to execute them:

1. Open the MCP ACL policy configuration in the Policy Studio.

2. Click **+ Add Rule**.

3. Configure the rule:
   * Select **Tools** as the feature type
   * Check **tools/list**
   * Leave **Name Pattern Type** set to **ANY**

4. Save and deploy the API.

**Result**: MCP clients can list available tools, but any attempt to call (execute) them is rejected.

### Allow listing and calling a specific tool

To restrict access to a single specific tool (for example, `get_weather`):

1. Open the MCP ACL policy configuration in the Policy Studio.

2. Click **+ Add Rule**.

3. Configure the rule:
   * Select **Tools** as the feature type
   * Check both **tools/list** and **tools/call**
   * Set **Name Pattern Type** to **Literal**
   * Enter the exact tool name in **Name Pattern** (for example, `get_weather`)

4. Save and deploy the API.

**Result**: Only the specified tool is visible to MCP clients and can be called. All other tools remain hidden and inaccessible.

### Configure conditional access

Each ACL rule includes a **Trigger Condition** field that accepts Gravitee Expression Language (EL) expressions. This enables context-based access control.

**Example use case**: Grant access to specific tools based on a claim in the user's JWT token:

1. Open the MCP ACL policy configuration in the Policy Studio.

2. Click **+ Add Rule**.

3. Configure the rule:
   * Select **Tools** as the feature type
   * Check **tools/list** and **tools/call**
   * Set **Name Pattern Type** to **Literal**
   * Enter the tool name in **Name Pattern**
   * In **Trigger Condition**, enter an EL expression such as:
     ```
     {#context.attributes['jwt.claims']['role'] == 'admin'}
     ```

4. Save and deploy the API.

**Result**: The tool is only accessible when the condition evaluates to true (in this example, when the user's JWT contains a `role` claim with the value `admin`).

### Test ACL policies locally

To validate ACL configurations without impacting production, use the official MCP example server:

1. Install and start the example server:

    ```bash
    npx @modelcontextprotocol/server-everything streamableHttp
    ```

2. Configure your MCP proxy API endpoint to use `http://localhost:3001/mcp`.

3. Add and configure the MCP ACL policy as described above.

4. Deploy the API and test with an MCP client.

The "Everything" server exposes numerous tools by default, making it ideal for verifying that your ACL policy correctly filters visible and callable tools according to your rules.

## Next steps

After configuring your MCP proxy, consider the following next steps:

* Configure rate limiting policies to control tool invocation frequency
* Set up analytics dashboards to monitor MCP server usage
* Integrate with Gravitee Access Management for advanced authentication and authorization

<!-- ASSETS USED (copy/rename exactly):
- screenshot-01.png -> trial-runs/.gitbook/assets/apim-mcp-proxy-step-01.png | alt: "New MCP server configuration form showing domain, name, resource identifier, and description fields"
-->