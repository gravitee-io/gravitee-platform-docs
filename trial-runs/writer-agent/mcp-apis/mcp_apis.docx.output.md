```
mcp_apis.writer-output.md
```

---
description: Learn how to expose, secure, and control access to MCP servers through Gravitee APIM.
---

# Exposing Your MCP APIs in Gravitee

## Overview

This guide explains how to expose your APIs as tools directly usable by AI agents using the Model Context Protocol (MCP) within Gravitee. The MCP is an emerging standard that enables AI agents to understand and interact with external tools and data. By exposing your APIs as MCP servers through Gravitee, you allow large language models (LLMs) and conversational agents to discover and invoke your API operations intelligently, without requiring complex connectors.

Exposing your MCP servers through Gravitee API Management (APIM) allows you to maintain governance, observability, and security over interactions between AI agents and your backend services.

## Expose an unsecured MCP server

This section explains how to publish an existing MCP server that does not require its own authentication through Gravitee. This configuration adds a layer of governance, observability, and control through APIM, even when the backend is open.

### Create the MCP Proxy API

1. In the APIM Console, start the v4 API creation process.
2. Enter your API name and version.
3. Select **AI Gateway** as the architecture.
4. Select **MCP Proxy** as the proxy type.
5. Define the access path for the entrypoint. For example, `/mcp-proxy`.
6. Enter the URL of your target MCP server in the backend (endpoint) configuration.
7. Select a **Keyless** plan for this example.
8. Validate the creation and deploy the API.

### Monitor MCP traffic

After deployment, you can monitor MCP server interactions:

- In the **Logs** screen, you can track exchanges between the MCP server and the MCP client.
- In the **API Traffic** screen, a dashboard displays MCP server usage, the methods and main tools used, and any errors encountered by the server.

### Test with an example server

If you do not have an MCP server, you can use the official MCP example server to simulate a local environment.

1. Start the example server:

```bash
npx @modelcontextprotocol/server-everything streamableHttp
```

The server starts on port 3001.

2. In the backend configuration (step 6), use the following URL:

```
http://localhost:3001/mcp
```

## Expose a secured MCP server

Exposing a secured MCP server through a proxy requires the backend server and the client to adhere to specific parts of the MCP specification regarding OAuth authentication.

### MCP authentication flow

For the connection to work through the proxy, the following mechanism must occur:

1. **Initial challenge:** The MCP server rejects the unauthenticated request with a `401 Unauthorized` status code.
2. **WWW-Authenticate header:** The 401 response contains a header that includes `resource_metadata`. For example, a URL pointing to a metadata resource such as `http://mcpserver.com/.well-known/oauth-protected-resource`.
3. **Auth discovery:** The client (the AI agent) calls this `.well-known/oauth-protected-resource` URL to obtain information about the authentication server.
4. **Token retrieval:** The client authenticates and retrieves a token to retry the initial request.

{% hint style="warning" %}
If the client (the AI tool) or the server does not respect this negotiation flow specific to the MCP specification, the API Proxy cannot relay the authentication natively.
{% endhint %}

### Compatibility and testing

Support for this authentication specification is still being adopted.

- **Recommended test server:** You can test this flow with the GitHub Copilot API: `https://api.githubcopilot.com/mcp/`
- **Compatible client:** VS Code (via the Copilot extension) is one of the only major clients that correctly implements this part of the MCP specification.

## Control access to MCP server functionalities

You can control access to MCP server functionalities using an Access Control List (ACL) policy within Gravitee. On a Gravitee MCP Proxy API, you can add an ACL policy via the Policy Studio to restrict access to MCP features such as the list of tools, resources, and prompts.

### Default behavior (implicit deny)

If you add the ACL policy without specifying any rules, the system adopts a restrictive "Deny All" approach by default.

1. Add the ACL policy to an MCP API.
2. Save and deploy.

**Result:** All server functionalities are inaccessible. An MCP client can connect to the server via the Gateway, but the lists of tools, resources, and prompts appear empty.

### Authorize only tool listing

To allow a client to see available tools without being able to execute them:

1. Add a rule (ACL) in the policy configuration.
2. Select the **Tools** feature option.
3. Check the **tools/list** box.
4. Leave the **Name Pattern Type** field set to **ANY** (default value).
5. Save and deploy the API.

**Result:** The MCP client can only list available tools. Any attempt to call (execute) them is rejected.

### Authorize the call and listing of a specific tool

To restrict access and execution to a single specific tool (for example, `get_weather`):

1. Add or modify an ACL in the policy configuration.
2. In the **Tools** feature option:
   - Check **tools/list** and **tools/call**.
   - In the **Name Pattern Type** field, select **Literal**.
   - In the **Name Pattern** field, enter the exact name of the tool. For example: `get_weather`.
3. Save and deploy.

**Result:** Only the specified tool is visible to the MCP client and can be called. All other tools remain hidden and inaccessible.

### Advanced configuration with execution conditions

Each ACL rule has a **Trigger Condition** field. This field allows you to add conditional logic to determine if the rule should be applied or ignored. This is useful for applying context-based security policies.

For example, you can condition access to certain tools based on a specific property (claim) present in the user's token or a request attribute.

{% hint style="info" %}
The **Trigger Condition** field expects a Gravitee Expression Language (EL) expression.
{% endhint %}

### Test ACL configurations locally

To validate your ACL configurations without impacting a production environment, you can use the official MCP example server named "Everything." This server exposes a large number of functionalities, making it ideal for testing filters.

1. Start the server in HTTP mode (streamable):

```bash
npx @modelcontextprotocol/server-everything streamableHttp
```

2. In your Gravitee API configuration, set the API endpoint to point to the local URL of the server:

```
http://localhost:3001/mcp
```

3. Save and redeploy the API.

You can now test your ACL policy. The "Everything" server exposes many tools by default, allowing you to verify if your policy correctly filters visible and callable tools according to your rules.

## Secure an MCP server with Gravitee Access Management

This section explains how to secure an unsecured MCP server using Gravitee APIM and an OAuth2 plan with Gravitee Access Management (AM).

{% hint style="warning" %}
If the MCP server itself is already secured, this configuration does not work.
{% endhint %}

### Prerequisites

Before you secure an MCP server with Gravitee AM, complete the following:

- Have an AM domain and the rights to configure it.
- Use an MCP client (for example, VS Code) that properly supports the MCP protocol with this type of authentication.

### Prepare the API Proxy in APIM

1. In APIM, create a new API and name it "API MCP Proxy."
2. Create a **Keyless** plan.
3. Deploy the API and test that it correctly proxies the MCP server without authentication.

### Configure the MCP server in AM

1. In AM, access the desired domain.
2. Create an **MCP Servers** entity (or the equivalent of "MCP server resource").
3. Enter a name for this resource.
4. Add the APIM API endpoint in the **MCP Resource Identifier** field.
5. Let AM generate a Client ID and a Client Secret, or provide your own. Save these credentials for later use.

### Configure Dynamic Client Registration (DCR) in AM

<!-- UNCERTAIN: The draft recommends enabling DCR but does not specify if this step is required or optional. Clarify whether DCR is mandatory for this workflow. -->

To avoid manually creating an Application in AM and specifying its Client ID in the MCP client (for example, VS Code), enable DCR.

1. In AM, go to **Settings > Client Registration**.
2. Enable DCR.

**If DCR is enabled:** The MCP client (for example, VS Code) automatically creates the application in AM and registers the Client ID and Client Secret.

**If DCR is not enabled:** You must manually create an Application in AM for the MCP client, correctly configure the redirect URLs, and configure the MCP client with the Client ID and Client Secret.

### Enable user registration in AM (optional)

Enabling client user registration (sign up) allows users to create accounts during the authentication flow.

1. In AM, go to **Settings > Login > User Registration**.
2. Enable the registration option.

### Finalize configuration in APIM

1. In your API MCP Proxy in APIM, add a resource of type **Gravitee.io AM Authorization Server**.
2. Configure the resource by linking it to your AM instance and using the Client ID and Client Secret created in AM for the "API MCP Proxy" resource.
3. Save.
4. Add an **OAuth2** plan in APIM using the AM resource you added.
5. Delete the Keyless plan.
6. Redeploy the API.

### Verification

After configuration, the MCP client uses the OAuth2 server configured in APIM upon connection:

1. You are redirected to the AM login page.
2. Use an existing AM user or create one (if the registration option was enabled).
3. After successful login via AM, a redirection is performed to the MCP client.
4. The MCP client retrieves the Client ID and Client Secret in the background and creates a token to use the MCP API, now secured in APIM.

{% hint style="info" %}
**VS Code note:** To delete Client IDs registered by dynamic registration in VS Code, use the command palette:
- **Cmd+Shift+P** (macOS) or **Ctrl+Shift+P** (Windows/Linux)
- Search for and use the action: **Authentication: Remove Dynamic Authentication Providers**
{% endhint %}

---

```
mcp_apis.writer-notes.md
```

## Supplemental Notes

The following items require clarification before finalizing this documentation:

1. **Internal test server URL removed:** The draft included an internal Gravitee test server URL (`https://apim-tools-mcp-server.team-apim.gravitee.dev/mcp`) with a note not to include it in public documentation. This URL has been omitted from the output.

2. **DCR requirement:** The draft recommends enabling Dynamic Client Registration (DCR) but does not specify whether this step is required or optional for the secure MCP server workflow. Please clarify the requirement level.

3. **Screenshots and UI references:** The draft does not include specific screenshots or detailed UI navigation paths. If available, adding screenshots would improve user guidance, particularly for:
   - API creation workflow in APIM
   - Policy Studio ACL configuration
   - AM domain configuration screens

4. **MCP server resource entity:** The draft refers to creating an "MCP Servers" entity or "MCP server resource" in AM. Please confirm the exact terminology and navigation path for this feature in AM.

5. **Trigger Condition examples:** The draft mentions that the Trigger Condition field expects a Gravitee EL expression but does not provide specific examples. Consider adding example expressions for common use cases (for example, token claim-based conditions).