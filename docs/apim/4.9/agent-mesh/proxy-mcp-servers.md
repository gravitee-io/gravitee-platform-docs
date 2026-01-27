# Proxy MCP Servers

## Overview

This guide explains how to use Gravitee APIM to proxy Model Context Protocol (MCP) servers. MCP is a protocol that enables AI agents to interact with tools, resources, and prompts. By proxying MCP servers through Gravitee, you can add governance, observability, and access control to MCP-based agent workflows.

## Prerequisites

Before you proxy an MCP server, ensure you have:

* A Gravitee APIM instance (version 4.9 or later)
* Access to an MCP server (either your own or a test server)
* An MCP client that supports the MCP protocol (for example, VS Code with the Copilot extension, Claude Desktop, or Cursor)

## Proxy an unsecured MCP server

This section explains how to publish an existing MCP server that does not require authentication. The goal is to add governance, observability, and control through APIM, even if the backend is open.

### Create the API

1. Create a new API and start the V4 API creation process.
2. Enter your API name and version in the general configuration.
3. Select **AI Gateway** as the architecture choice.
4. Choose the **MCP Proxy** option as the proxy type.
5. Define the entrypoint access path (for example, `/mcp-proxy`).
6. Enter the URL of your target MCP server as the backend endpoint.
7. For this example, proceed with a Keyless plan for security.
8. Validate the creation and deploy the API.

### Monitor MCP traffic

After deploying the API, you can monitor MCP server usage:

* In the APIM logs screen, track exchanges between the MCP server and the MCP client.
* In the API Traffic screen, a dashboard visualizes MCP server usage, the methods and main tools used, and any errors encountered by the server.

### Test with the example MCP server

If you don't have an MCP server yet, you can simulate a local environment with the official example server.

1. Start the example server from the [MCP servers repository](https://github.com/modelcontextprotocol/servers/tree/main/src/everything):

    ```bash
    npx @modelcontextprotocol/server-everything streamableHttp
    ```

    The server will usually start on port 3001.

2. Configure Gravitee to use the following URL as the backend endpoint: `http://localhost:3001/mcp`

{% hint style="info" %}
An internal Gravitee testing tool is available for APIM development purposes. This tool is not intended for public documentation and may be removed at any time.
{% endhint %}

## Proxy a secured MCP server

Proxying a secured MCP server requires the backend server and the client to strictly adhere to the MCP specification for OAuth authentication.

### MCP authentication flow

For the connection to work through the proxy, the following mechanism must occur:

1. **Initial challenge**: The MCP server must reject the unauthenticated request with a `401 Unauthorized` status code.
2. **WWW-Authenticate header**: The `401` response must contain a specific header including `resource_metadata`. For example, a URL pointing to a metadata resource, such as `http://mcpserver.com/.well-known/oauth-protected-resource`.
3. **Auth discovery**: The client (the AI agent) then calls this `.well-known/oauth-protected-resource` URL to obtain information about the authentication server to use.
4. **Token retrieval**: The client authenticates and retrieves a token to retry its initial request.

{% hint style="warning" %}
If the client (the AI tool) or the server does not respect this negotiation flow specific to the MCP spec, the API Proxy will not be able to relay the authentication natively.
{% endhint %}

### Compatibility and testing

As of today, support for this authentication specification is still being adopted.

* **Recommended test server**: You can test this flow with the GitHub Copilot API: `https://api.githubcopilot.com/mcp/`
* **Compatible client**: Currently, VS Code (via the Copilot extension) is one of the only major clients correctly implementing this part of the MCP specification.

## Control access to MCP server features

This section explains how to control access to MCP server functionalities using an Access Control List (ACL) policy within Gravitee.

On a Gravitee MCP Proxy API, you can add an ACL policy via the Policy Studio. This policy restricts access to MCP features such as the list of tools, resources, and prompts.

### Default behavior (implicit deny)

If you add the ACL policy without specifying any rules, the system adopts a restrictive "Deny All" approach by default.

1. Add the policy to an MCP API, save, and deploy.

**Result**: All server functionalities will be inaccessible. An MCP client will be able to connect to the server via the Gateway, but the lists of tools, resources, and prompts will appear empty.

### Authorize only tool listing

To allow a client to see available tools without being able to execute them:

1. Add a rule (ACL) in the policy configuration.
2. Select the **Tools** feature option.
3. Check the **tools/list** box.
4. Leave the **Name Pattern Type** field on **ANY** (default value).
5. Save and deploy the API.

**Result**: If you configure an MCP client, it will only be able to list available tools, but any attempt to call (execute) them will be rejected.

### Authorize the call and listing of a specific tool

To restrict access and execution to a single specific tool (for example, `get_weather`):

1. Add or modify an ACL in the policy configuration.
2. In the **Tools** feature option:
    * Check **tools/list** AND **tools/call**.
    * In the **Name Pattern Type** field, select **Literal**.
    * In the **Name Pattern** field, enter the exact name of the tool (for example: `get_weather`).
3. Save and deploy.

**Result**: From now on, only this specific tool is visible to the MCP client and can be called. All other tools remain hidden and inaccessible.

### Advanced configuration: execution conditions

Each ACL rule has a **Trigger Condition** field. This field allows you to add conditional logic to determine if the rule should be applied or ignored. This is particularly useful for applying context-based security policies.

**Usage example**: You can condition access to certain tools based on a specific property (claim) present in the user's token or a request attribute.

{% hint style="info" %}
The field generally expects a Gravitee EL (Expression Language) expression.
{% endhint %}

### Test ACL configurations locally

To validate your ACL configurations without impacting a production environment, you can use the official example MCP server named "Everything." This server exposes a large number of functionalities, making it ideal for testing filters.

The source code is available in the [MCP servers repository](https://github.com/modelcontextprotocol/servers/tree/main/src/everything).

1. Launch the server in HTTP mode (streamable):

    ```bash
    npx @modelcontextprotocol/server-everything streamableHttp
    ```

2. Once the local server is launched, return to your Gravitee API configuration.
3. Configure the API Endpoint to point to the local URL of the created server: `http://localhost:3001/mcp`
4. Save and redeploy the API.

**Validation**: You can now test your ACL policy. As the "Everything" server exposes many tools by default, you will be able to effectively verify if your policy correctly filters visible and callable tools according to your rules.

## Secure an MCP server with Gravitee

This section explains how to secure an unsecured MCP server using Gravitee APIM and an OAuth2 plan with Gravitee Access Management (AM).

{% hint style="danger" %}
If the MCP server itself is already secured, this configuration will not work.
{% endhint %}

### Prerequisites

Before you secure an MCP server with Gravitee, ensure you have:

* An AM domain and the rights to configure it
* An MCP client (for example, VS Code) that properly supports the MCP protocol with this type of authentication

### Prepare the API proxy in APIM

1. In APIM, create a new API and name it "API MCP Proxy".
2. Start by creating a simple Keyless plan.
3. Once the API is created and deployed, test that it works correctly to proxy the MCP server without authentication.

### Configure the MCP server in AM

1. In AM, access the desired domain and create an entity "MCP Servers" (or the equivalent of "MCP server resource").
2. Fill in a name for this resource.
3. Add the APIM API endpoint in the **MCP Resource Identifier** field.
4. Let AM generate a ClientID and a Client Secret, or provide your own. Keep these credentials as they will be needed later.

### Configure DCR (Dynamic Client Registration) in AM

To avoid manually creating an Application in AM and specifying its Client ID in the MCP client (for example, VS Code), it is recommended to enable DCR.

1. In AM, go to **Settings > Client Registration**.
2. Enable DCR.

**If DCR is enabled**: The MCP client (for example, VS Code) should automatically create the application in AM and also register the ClientID / Client Secret.

**If DCR is not enabled**: You will need to manually create an Application in AM for the MCP client and correctly configure the redirect URLs according to it. You will also need to configure the MCP client with the ClientID/Client Secret.

### Activate user registration in AM (optional)

For this guide, it is recommended to enable client user registration (sign up).

1. In AM, go to **Settings > Login > User Registration**.
2. Enable the registration option.

### Finalize configuration in APIM

1. In your API MCP Proxy in APIM, add a resource of type **Gravitee.io AM Authorization Server**.
2. Configure it by linking it to your AM instance and using the ClientID and Client Secret previously created in AM for the "API MCP Proxy" resource.
3. Save.
4. Add an OAuth2 plan in APIM using the AM resource that was just added.
5. Delete the Keyless plan.
6. Redeploy the API.

### Verify the configuration

The MCP client, upon connection, should now use the OAuth2 server configured in APIM.

1. You will be redirected to the AM login page, where you can use an existing AM user or create one (if the registration option was enabled).
2. Once successfully logged in via AM, a redirection is performed to the MCP client.
3. The MCP client retrieves the ClientID and Client Secret in the background, and creates a token to use the MCP API, now secured in APIM.

{% hint style="info" %}
**VS Code note**: If you are using VS Code and want to delete the ClientIDs registered by dynamic registration, use the command palette:

* `Cmd+Shift+P` (or `Ctrl+Shift+P` on Windows/Linux)
* Search for and use the action: `>Authentication: Remove Dynamic Authentication Providers`
{% endhint %}