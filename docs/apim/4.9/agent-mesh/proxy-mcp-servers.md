# create-mcp-server.md

## Overview

This guide explains how to expose your APIs as Model Context Protocol (MCP) servers using Gravitee APIM. By transforming your APIs into MCP-compatible tools, you enable AI agents and large language models (LLMs) to discover and invoke your API operations intelligently.

The Model Context Protocol (MCP) is an emerging standard that allows AI agents to understand and interact with external tools and data. Exposing your APIs as MCP servers via Gravitee maintains governance, observability, and security over interactions between AI agents and your backend services.

## Prerequisites

Before you create an MCP server, ensure you have:

* Access to Gravitee APIM 4.9 or later
* An existing API or MCP server to expose
* Appropriate permissions to create and deploy APIs in APIM

## Create an unsecured MCP server

This procedure publishes an existing MCP server that does not require authentication. Gravitee adds a layer of governance, observability, and control through APIM.

1. Navigate to **APIs** in the APIM Console, and then click **+ Add API**.

2. Select **Create a V4 API**.

3. Enter your API name and version in the **General** section.

4. Select **AI Gateway** as the architecture type.

5. Select **MCP Proxy** as the proxy type.

6. Define the entrypoint path (for example, `/mcp-proxy`).

7. Enter the URL of your target MCP server in the **Backend (Endpoint)** field.

    {% hint style="info" %}
    For local testing, you can use `http://localhost:3001/mcp` if running the example server described in the verification section.
    {% endhint %}

8. Select **Keyless** for the security plan.

9. Click **Create** to finalize the API creation.

10. Deploy the API.

## Verification

After deploying your MCP server API, verify that it works correctly:

1. Navigate to **APIs > [Your API] > Analytics** to view the API Traffic dashboard.

    The dashboard displays MCP server usage metrics, including the methods and tools used, as well as any errors encountered.

2. Navigate to **APIs > [Your API] > Logs** to track exchanges between the MCP server and MCP clients.

## Test with the example MCP server

If you don't have an MCP server available, you can test using the official example server:

1. Start the example server:

    ```bash
    npx @modelcontextprotocol/server-everything streamableHttp
    ```

    The server starts on port 3001 by default.

2. Configure your Gravitee API to use the backend URL `http://localhost:3001/mcp`.

3. Deploy the API and test the connection using an MCP-compatible client.

## Next steps

* [Secure an MCP server](secure-mcp-server.md)
* [Control access to MCP tools](control-mcp-access.md)
* [Monitor MCP server usage](../analytics/mcp-analytics.md)

<!-- ASSETS USED (copy/rename exactly):
- screenshots/mcp-server-creation.png -> trial-runs/.gitbook/assets/apim-mcp-server-step-01.png | alt: "New MCP server form showing server settings fields"
-->

---

# secure-mcp-server.md

## Overview

This guide explains how to secure an unsecured MCP server using Gravitee APIM and Gravitee Access Management (AM) with OAuth2 authentication.

{% hint style="warning" %}
This configuration only works for MCP servers that are not already secured. If your MCP server implements its own authentication, you must use the [MCP authentication flow](mcp-authentication-flow.md) instead.
{% endhint %}

## Prerequisites

Before you secure an MCP server, ensure you have:

* An existing unsecured MCP server API in APIM
* Access to a Gravitee Access Management domain
* Permissions to configure OAuth2 resources in both APIM and AM
* An MCP client that supports OAuth2 authentication (for example, VS Code with the appropriate extensions)

## Configure the MCP server in Access Management

1. Navigate to your AM domain.

2. Create a new **MCP Server** resource.

3. Enter a name for the MCP server resource.

4. In the **MCP Resource Identifier** field, enter the APIM API endpoint URL.

5. Generate or provide a Client ID and Client Secret.

    {% hint style="info" %}
    Save these credentials. You will need them when configuring the APIM resource.
    {% endhint %}

6. Click **Save**.

## Enable Dynamic Client Registration (recommended)

Dynamic Client Registration (DCR) allows MCP clients to automatically register with AM without manual application creation.

1. Navigate to **Settings > Client Registration** in your AM domain.

2. Enable **Dynamic Client Registration**.

3. Configure the registration settings according to your security requirements.

    {% hint style="info" %}
    If DCR is not enabled, you must manually create an application in AM for each MCP client and configure the redirect URLs.
    {% endhint %}

## Enable user registration (optional)

To allow users to create accounts during the authentication flow:

1. Navigate to **Settings > Login > User Registration** in your AM domain.

2. Enable the **User Registration** option.

3. Configure the registration form fields as needed.

4. Click **Save**.

## Configure the OAuth2 plan in APIM

1. Navigate to your MCP server API in APIM.

2. Click **Resources** in the left navigation menu.

3. Add a new resource of type **Gravitee.io AM Authorization Server**.

4. Configure the resource:
    * Enter the AM instance URL
    * Enter the Client ID from the MCP server resource created in AM
    * Enter the Client Secret from the MCP server resource created in AM

5. Click **Save**.

6. Navigate to **Plans** in the left navigation menu.

7. Click **+ Add new plan**.

8. Select **OAuth2** as the plan type.

9. Select the AM authorization server resource you created.

10. Configure the plan settings and click **Save**.

11. Delete the existing Keyless plan.

12. Deploy the API.

## Verification

When an MCP client connects to the secured server:

1. The client is redirected to the AM login page.

2. The user can log in with existing credentials or create a new account (if user registration is enabled).

3. After successful authentication, AM redirects back to the MCP client.

4. The MCP client retrieves the access token and uses it for subsequent API calls.

## Remove dynamic authentication providers in VS Code

If you are using VS Code and need to remove dynamically registered Client IDs:

1. Open the Command Palette (`Cmd+Shift+P` on macOS or `Ctrl+Shift+P` on Windows/Linux).

2. Search for and select **Authentication: Remove Dynamic Authentication Providers**.

3. Select the provider to remove.

## Next steps

* [Control access to MCP tools](control-mcp-access.md)
* [Configure MCP authentication flow](mcp-authentication-flow.md)
* [Monitor MCP server usage](../analytics/mcp-analytics.md)

<!-- ASSETS USED (copy/rename exactly):
- screenshots/am-mcp-server-config.png -> trial-runs/.gitbook/assets/apim-mcp-secure-step-01.png | alt: "Access Management MCP server configuration form"
- screenshots/apim-oauth2-resource.png -> trial-runs/.gitbook/assets/apim-mcp-secure-step-02.png | alt: "APIM OAuth2 resource configuration showing AM server details"
-->

---

# control-mcp-access.md

## Overview

This guide explains how to control access to MCP server functionalities using Access Control List (ACL) policies in Gravitee APIM. ACL policies restrict access to MCP features such as tools, resources, and prompts.

## Prerequisites

Before you configure access control, ensure you have:

* An existing MCP server API in APIM
* Permissions to modify API policies in the Policy Studio
* Understanding of the MCP tools, resources, and prompts your server exposes

## Default behavior (implicit deny)

When you add an ACL policy without specifying any rules, the system adopts a restrictive "Deny All" approach by default.

1. Navigate to **APIs > [Your API] > Policy Studio**.

2. Add the **ACL** policy to your API flow.

3. Save and deploy the API without configuring any rules.

    {% hint style="info" %}
    With no rules configured, all server functionalities are inaccessible. MCP clients can connect to the server via the Gateway, but the lists of tools, resources, and prompts appear empty.
    {% endhint %}

## Allow tool listing only

To allow clients to see available tools without executing them:

1. Navigate to **APIs > [Your API] > Policy Studio**.

2. Add or edit the **ACL** policy.

3. Add a new rule and select the **Tools** feature option.

4. Check the **tools/list** checkbox.

5. Leave the **Name Pattern Type** field set to **ANY**.

6. Save and deploy the API.

    MCP clients can now list available tools, but any attempt to execute them is rejected.

## Allow listing and execution of a specific tool

To restrict access to a single specific tool:

1. Navigate to **APIs > [Your API] > Policy Studio**.

2. Add or edit the **ACL** policy.

3. Add a new rule and select the **Tools** feature option.

4. Check both **tools/list** and **tools/call** checkboxes.

5. Set the **Name Pattern Type** field to **Literal**.

6. In the **Name Pattern** field, enter the exact tool name (for example, `get_weather`).

7. Save and deploy the API.

    Only the specified tool is visible to MCP clients and can be executed. All other tools remain hidden and inaccessible.

## Configure conditional access

Each ACL rule includes a **Trigger Condition** field that allows you to add conditional logic to determine whether the rule should be applied.

1. Navigate to **APIs > [Your API] > Policy Studio**.

2. Add or edit the **ACL** policy.

3. In the **Trigger Condition** field, enter a Gravitee Expression Language (EL) expression.

    For example, to restrict access based on a token claim:

    ```
    {#request.attributes['jwt.claims']['role'] == 'admin'}
    ```

4. Save and deploy the API.

    {% hint style="info" %}
    Conditional access is useful for applying context-based security policies, such as restricting certain tools based on user roles or request attributes.
    {% endhint %}

## Test ACL configurations locally

To validate your ACL configurations without impacting production, use the official example MCP server:

1. Start the example server:

    ```bash
    npx @modelcontextprotocol/server-everything streamableHttp
    ```

    The server exposes many tools by default, making it ideal for testing filters.

2. Configure your APIM API endpoint to point to `http://localhost:3001/mcp`.

3. Save and deploy the API.

4. Test your ACL policy using an MCP-compatible client.

    The example server's extensive tool set allows you to verify that your policy correctly filters visible and callable tools according to your rules.

## Next steps

* [Secure an MCP server](secure-mcp-server.md)
* [Configure MCP authentication flow](mcp-authentication-flow.md)
* [Monitor MCP server usage](../analytics/mcp-analytics.md)

<!-- ASSETS USED (copy/rename exactly):
- screenshots/acl-policy-config.png -> trial-runs/.gitbook/assets/apim-mcp-acl-step-01.png | alt: "ACL policy configuration showing tools feature options"
-->

---

# mcp-authentication-flow.md

## Overview

This article explains the MCP authentication flow for secured MCP servers. Understanding this flow is essential when exposing secured MCP servers through Gravitee APIM.

{% hint style="warning" %}
For the authentication flow to work through a proxy like Gravitee, both the backend MCP server and the client must strictly adhere to the MCP specification regarding OAuth authentication.
{% endhint %}

## Background

The Model Context Protocol defines a specific authentication mechanism for secured resources. This mechanism ensures that AI agents and MCP clients can authenticate with MCP servers in a standardized way, even when proxied through an API gateway.

## Authentication flow steps

The MCP authentication flow follows these steps:

1. **Initial challenge**: The MCP server rejects the unauthenticated request with a `401 Unauthorized` status code.

2. **WWW-Authenticate header**: The `401` response includes a `WWW-Authenticate` header containing `resource_metadata`.

    The header points to a metadata resource URL, such as `http://mcpserver.com/.well-known/oauth-protected-resource`.

3. **Auth discovery**: The MCP client calls the `.well-known/oauth-protected-resource` URL to obtain information about the authentication server.

4. **Token retrieval**: The client authenticates with the authorization server and retrieves an access token.

5. **Retry with token**: The client retries the initial request, including the access token in the `Authorization` header.

{% hint style="danger" %}
If the MCP client or server does not implement this negotiation flow according to the MCP specification, the API proxy cannot relay authentication natively.
{% endhint %}

## Compatibility and testing

As of APIM 4.9, support for this authentication specification is still being adopted across MCP implementations.

### Recommended test server

You can test the authentication flow with the GitHub Copilot API:

```
https://api.githubcopilot.com/mcp/
```

### Compatible clients

Currently, VS Code with the Copilot extension is one of the few major clients that correctly implements this part of the MCP specification.

## Use cases

The MCP authentication flow is useful when:

* Exposing secured MCP servers through Gravitee APIM
* Integrating with enterprise identity providers
* Enforcing fine-grained access control on MCP tools
* Maintaining audit trails of AI agent interactions

## Next steps

* [Secure an MCP server](secure-mcp-server.md)
* [Control access to MCP tools](control-mcp-access.md)
* [Create an MCP server](create-mcp-server.md)