# exposing-your-mcp-apis-in-gravitee.writer-output.md

---

# Exposing Your MCP APIs in Gravitee

## Overview

This guide explains how to expose your APIs as Model Context Protocol (MCP) servers through Gravitee API Management (APIM). By publishing your APIs as MCP servers, you enable AI agents and large language models (LLMs) to discover and invoke your API operations directly.

Gravitee APIM provides governance, observability, and security for interactions between AI agents and your backend services.

## Prerequisites

Before you expose your MCP APIs in Gravitee, complete the following steps:

* Install and configure Gravitee APIM
* Deploy an MCP server accessible via HTTP

## Expose an unsecured MCP server

This section explains how to publish an MCP server that does not require authentication. Gravitee adds governance, observability, and control even when the backend is open.

1. In the Gravitee Console, start the V4 API creation process.

2. Enter your API name and version in the general configuration.

3. Select **AI Gateway** as the architecture.

4. Select **MCP Proxy** as the proxy type.

5. Define the entrypoint access path, for example `/mcp-proxy`.

6. Enter the URL of your target MCP server in the backend endpoint field.

7. Create a Keyless plan for this example.

8. Validate the creation and deploy the API.

### Verification

After deployment, verify your MCP proxy API is functioning:

* In the APIM logs screen, confirm that exchanges between the MCP server and the MCP client appear.
* In the API Traffic screen, review the dashboard to visualize MCP server usage, the methods and tools used, and any errors encountered.

### Test with an example MCP server

If you do not have an MCP server, you can use the official example server for testing.

1. Start the example server:

   ```bash
   npx @modelcontextprotocol/server-everything streamableHttp
   ```

   The server starts on port 3001 by default.

2. In Gravitee, configure the backend endpoint URL as `http://localhost:3001/mcp`.

## Expose a secured MCP server

Exposing a secured MCP server through Gravitee requires the backend server and the client to implement the MCP specification for OAuth authentication.

### MCP authentication flow

For the connection to work through the proxy, the following mechanism must occur:

1. **Initial challenge**: The MCP server rejects the unauthenticated request with a `401 Unauthorized` response.

2. **WWW-Authenticate header**: The 401 response contains a header with `resource_metadata` pointing to a metadata resource, such as `http://mcpserver.com/.well-known/oauth-protected-resource`.

3. **Auth discovery**: The client calls the `.well-known/oauth-protected-resource` URL to obtain information about the authentication server.

4. **Token retrieval**: The client authenticates and retrieves a token to retry the initial request.

{% hint style="warning" %}
If the client or server does not implement this negotiation flow as specified in the MCP specification, the API Proxy cannot relay the authentication natively.
{% endhint %}

### Compatibility

Support for this authentication specification is still being adopted. You can test this flow with the GitHub Copilot API at `https://api.githubcopilot.com/mcp/`. VS Code with the Copilot extension is currently one of the clients that correctly implements this part of the MCP specification.

---

# controlling-access-to-mcp-server.writer-output.md

---

# Controlling Access to the MCP Server

## Overview

This guide explains how to control access to MCP server functionalities using an Access Control List (ACL) policy in Gravitee.

On a Gravitee MCP Proxy API, you can add an ACL policy through the Policy Studio. This policy restricts access to MCP features such as tools, resources, and prompts.

## Default behavior

If you add the ACL policy without specifying any rules, the system adopts a restrictive deny-all approach by default.

1. Add the ACL policy to an MCP API.

2. Save and deploy the API.

**Result**: All server functionalities are inaccessible. An MCP client can connect to the server through the Gateway, but the lists of tools, resources, and prompts appear empty.

## Authorize tool listing only

To allow a client to view available tools without executing them:

1. Add a rule in the ACL policy configuration.

2. Select the **Tools** feature option.

3. Check the **tools/list** box.

4. Leave the **Name Pattern Type** field set to **ANY**.

5. Save and deploy the API.

**Result**: The MCP client can list available tools, but any attempt to execute them is rejected.

## Authorize listing and calling a specific tool

To restrict access and execution to a single tool, for example `get_weather`:

1. Add or modify an ACL rule in the policy configuration.

2. In the **Tools** feature option, check **tools/list** and **tools/call**.

3. In the **Name Pattern Type** field, select **Literal**.

4. In the **Name Pattern** field, enter the exact tool name, for example `get_weather`.

5. Save and deploy the API.

**Result**: Only the specified tool is visible to the MCP client and can be called. All other tools remain hidden and inaccessible.

## Execution conditions

Each ACL rule has a **Trigger Condition** field. This field allows you to add conditional logic to determine if the rule should be applied or ignored.

You can condition access to certain tools based on a specific property (claim) present in the user's token or a request attribute.

{% hint style="info" %}
The Trigger Condition field expects a Gravitee Expression Language (EL) expression.
{% endhint %}

## Test ACL configurations locally

To validate your ACL configurations without impacting a production environment, use the official example MCP server named "Everything." This server exposes a large number of functionalities, making it ideal for testing filters.

1. Start the server in HTTP mode:

   ```bash
   npx @modelcontextprotocol/server-everything streamableHttp
   ```

2. In your Gravitee API configuration, set the API endpoint to `http://localhost:3001/mcp`.

3. Save and redeploy the API.

4. Test your ACL policy to verify that it correctly filters visible and callable tools according to your rules.

---

# secure-mcp-server-with-gravitee.writer-output.md

---

# Secure an MCP Server with Gravitee

## Overview

This guide explains how to secure an unsecured MCP server using Gravitee API Management (APIM) and an OAuth2 plan with Gravitee Access Management (AM).

{% hint style="warning" %}
If the MCP server is already secured with its own authentication, this configuration does not apply.
{% endhint %}

## Prerequisites

Before you secure an MCP server with Gravitee, complete the following steps:

* Configure a Gravitee AM domain with the necessary permissions
* Install an MCP client that supports the MCP protocol with OAuth authentication, such as VS Code

## Prepare the API proxy in APIM

1. In APIM, create a new API named "API MCP Proxy".

2. Create a Keyless plan.

3. Deploy the API and test that it correctly proxies the MCP server without authentication.

## Configure the MCP server in AM

1. In AM, access the desired domain.

2. Create an MCP server resource.

3. Enter a name for the resource.

4. Add the APIM API endpoint in the **MCP Resource Identifier** field.

5. Allow AM to generate a Client ID and Client Secret, or provide your own. Save these credentials for later use.

<!-- NEED CLARIFICATION: The draft references a screenshot "assets/image-01.png" but the image was not provided. Please provide the screenshot or confirm it should be removed. -->

## Configure Dynamic Client Registration in AM

To avoid manually creating an Application in AM, enable Dynamic Client Registration (DCR).

1. In AM, navigate to **Settings > Client Registration**.

2. Enable DCR.

{% hint style="info" %}
If DCR is enabled, the MCP client automatically creates the application in AM and registers the Client ID and Client Secret.

If DCR is not enabled, you must manually create an Application in AM for the MCP client, configure the redirect URLs, and configure the MCP client with the Client ID and Client Secret.
{% endhint %}

## Enable user registration in AM

For testing purposes, enable client user registration.

1. In AM, navigate to **Settings > Login > User Registration**.

2. Enable the registration option.

## Finalize configuration in APIM

1. In your API MCP Proxy in APIM, add a resource of type **Gravitee.io AM Authorization Server**.

2. Configure the resource by linking it to your AM instance and entering the Client ID and Client Secret created earlier.

3. Save the configuration.

4. Add an OAuth2 plan using the AM resource.

5. Delete the Keyless plan.

6. Redeploy the API.

## Verification

After configuration, verify the secured MCP server:

1. Connect with an MCP client. The client uses the OAuth2 server configured in APIM.

2. The AM login page appears. Use an existing AM user or create one if registration is enabled.

3. After successful login, AM redirects to the MCP client.

4. The MCP client retrieves the Client ID and Client Secret and creates a token to access the secured MCP API.

{% hint style="info" %}
**VS Code users**: To delete Client IDs registered by dynamic registration, open the command palette with `Cmd+Shift+P` (macOS) or `Ctrl+Shift+P` (Windows/Linux) and select **Authentication: Remove Dynamic Authentication Providers**.
{% endhint %}

---

# exposing-your-mcp-apis-in-gravitee.writer-notes.md

## Supplemental Notes

* The draft included a reference to an internal Gravitee tool URL with instructions not to include it in public documentation. This URL has been removed from the output.
* The draft screenshot reference in the "Secure MCP Server" section (`assets/image-01.png`) was not provided. Please confirm whether the screenshot should be included or if the section should remain text-only.
* The draft used inconsistent heading levels and combined multiple distinct procedures into a single document. The output has been split into three logical articles as indicated by the H1 section breaks in the original draft.