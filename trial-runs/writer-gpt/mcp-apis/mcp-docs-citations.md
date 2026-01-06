---
description: Learn how to expose and secure MCP servers through Gravitee API Management (APIM) and Gravitee Access Management (AM).
---

# Expose Your MCP APIs in Gravitee

## Overview

The Model Context Protocol (MCP) is an emerging standard that lets AI agents, such as large language models (LLMs), discover and invoke external tools and data sources in a structured way. By exposing your MCP servers through Gravitee, you allow AI agents to call your backend capabilities while keeping governance, observability, and security under your control. :contentReference[oaicite:0]{index=0}

Gravitee Agent Mesh provides AI-native capabilities on top of Gravitee API Management (APIM). As part of Agent Mesh, Gravitee can act as:

* An MCP proxy that fronts an existing MCP server.
* A control point where you apply plans, policies, and analytics to MCP traffic. :contentReference[oaicite:1]{index=1}

This page focuses on the following use cases:

* Expose an **unsecured** MCP server via an MCP proxy in APIM.
* Expose a **secured** MCP server that implements OAuth 2.0 authorization for MCP.
* Secure an **unsecured** MCP server using Gravitee Access Management (AM) and an OAuth2 plan.
* Control which MCP tools, resources, and prompts are visible and callable through Gravitee.

## Prerequisites

Before you start, ensure the following:

* A Gravitee API Management environment where you can create v4 APIs and select the **AI Gateway** architecture with an **MCP Proxy** proxy type. :contentReference[oaicite:2]{index=2}  
* At least one MCP server reachable from the Gravitee Gateway.
* An MCP-compatible client, such as an IDE or desktop client that supports MCP.
* For the “Secure an unsecured MCP server with AM” flow:
  * A Gravitee Access Management domain that you can configure.
  * Ability to create AM applications and resources.
* For testing the standardized MCP authorization flow:
  * Access to a compliant MCP server, such as the GitHub Copilot MCP API.
  * A client that implements the MCP OAuth 2.0 Protected Resource Metadata flow (for example, Visual Studio Code with the Copilot extension). :contentReference[oaicite:3]{index=3} :contentReference[oaicite:4]{index=4}

## Expose an unsecured MCP server

In this scenario, the upstream MCP server does not require its own authentication. You use Gravitee APIM to front the server and add governance and observability without changing the MCP server itself. :contentReference[oaicite:5]{index=5}

### Create the MCP proxy API

1. Start creating a v4 API in APIM.

2. In the **General** configuration, set the API name and version. :contentReference[oaicite:6]{index=6}  

3. For **Architecture**, select **AI Gateway**. :contentReference[oaicite:7]{index=7}  

4. For **Proxy type**, select **MCP Proxy**. :contentReference[oaicite:8]{index=8}  

5. Configure the MCP entrypoint:

   * Set an access path, for example `/mcp-proxy`. :contentReference[oaicite:9]{index=9}  

6. Configure the MCP backend (endpoint):

   * Set the endpoint URL of your target MCP server. :contentReference[oaicite:10]{index=10}  

7. Configure security:

   * For an unsecured backend, start with a **Keyless** plan. :contentReference[oaicite:11]{index=11}  

8. Review and deploy:

   * Validate the configuration and deploy the API. :contentReference[oaicite:12]{index=12}  

### Monitor MCP traffic

After deployment, you can monitor MCP traffic and behavior:

* Use the **Logs** screen in APIM to review exchanges between the MCP server and the MCP client. :contentReference[oaicite:13]{index=13}  
* Use the **API Traffic** dashboard to visualize MCP server usage, methods and tools used, and any errors returned by the server. :contentReference[oaicite:14]{index=14}  

To inspect detailed runtime logs for a v4 proxy API:

1. From the **Dashboard**, click **APIs**.
2. Select the API you want to inspect.
3. Click **Logs** to open the list of logs for that API. :contentReference[oaicite:15]{index=15}  

Filters allow you to refine logs by period, entrypoint, HTTP method, and plan. :contentReference[oaicite:16]{index=16}  

## Expose a secured MCP server

In this scenario, the upstream MCP server is already secured using OAuth 2.0 in accordance with the MCP OAuth 2.0 Protected Resource Metadata (RFC 9728). Gravitee acts as an MCP proxy in front of this server. :contentReference[oaicite:17]{index=17}  

### Understand the MCP authorization flow

To work correctly through a proxy, the MCP client and server must implement the standardized authorization flow:

1. **Initial challenge**  
   The MCP client sends a request without a token.  
   The MCP server responds with `401 Unauthorized`. :contentReference[oaicite:18]{index=18} :contentReference[oaicite:19]{index=19}  

2. **WWW-Authenticate header**  
   The `401` response includes a `WWW-Authenticate` header that exposes **resource metadata**.  
   For example, a link to the OAuth 2.0 Protected Resource Metadata document:  
   `http://mcpserver.com/.well-known/oauth-protected-resource`. :contentReference[oaicite:20]{index=20} :contentReference[oaicite:21]{index=21}  

3. **Authorization server discovery**  
   The MCP client calls the `.well-known/oauth-protected-resource` URL to discover which authorization server to use and how to authenticate. :contentReference[oaicite:22]{index=22} :contentReference[oaicite:23]{index=23}  

4. **Token retrieval and retry**  
   The client authenticates the end user with the authorization server, obtains an OAuth 2.0 access token, and retries the original MCP request with this token. :contentReference[oaicite:24]{index=24} :contentReference[oaicite:25]{index=25}  

If either the MCP client or MCP server does not follow this negotiation flow, the Gravitee MCP proxy cannot relay authentication correctly. :contentReference[oaicite:26]{index=26}  

### Verify client and server compatibility

Support for this authorization specification is still in early adoption. You can verify compatibility using known test components:

* **Test server**: GitHub Copilot MCP API (`https://api.githubcopilot.com/mcp/`). :contentReference[oaicite:27]{index=27}  
* **Client**: Visual Studio Code with the Copilot extension, which correctly implements this part of the MCP specification. :contentReference[oaicite:28]{index=28}  

Once you confirm that your MCP client and server follow the standardized authorization flow, you can front them with a Gravitee MCP proxy as described in the previous section.

## Control access to tools, resources, and prompts

You can control which MCP capabilities are exposed to clients by applying an Access Control List (ACL) policy to your MCP proxy API in Policy Studio. This policy restricts access to specific MCP features such as tools, resources, and prompts. :contentReference[oaicite:29]{index=29}  

### Default behavior (implicit deny)

If you add the ACL policy without defining any rules:

* All server functionalities are denied.
* MCP clients can connect to the server through the Gateway, but the lists of tools, resources, and prompts are empty. :contentReference[oaicite:30]{index=30}  

This gives you a safe baseline where nothing is exposed until you explicitly allow it.

### Allow read-only tool listing

To allow clients to list available tools without being able to execute them:

1. In Policy Studio, add an ACL rule to your MCP proxy API.
2. For the rule, select the **Tools** feature.
3. Enable the `tools/list` option.
4. Leave **Name pattern type** set to **ANY**.
5. Save and redeploy the API. :contentReference[oaicite:31]{index=31}  

**Result**

* MCP clients can retrieve the list of available tools.
* Any attempt to call (execute) a tool is rejected. :contentReference[oaicite:32]{index=32}  

### Allow a specific tool

To allow discovery and execution of a single tool, such as `get_weather`:

1. In Policy Studio, add or edit an ACL rule.
2. For the rule, select the **Tools** feature.
3. Enable both `tools/list` and `tools/call`.
4. Set **Name pattern type** to **Literal**.
5. Set **Name pattern** to the exact tool name (for example, `get_weather`).
6. Save and redeploy the API. :contentReference[oaicite:33]{index=33}  

**Result**

* Only the specified tool is visible and callable for the MCP client.
* All other tools remain hidden and inaccessible. :contentReference[oaicite:34]{index=34}  

### Use trigger conditions for context-based rules

Each ACL rule includes a **Trigger condition** field. This field lets you add conditional logic to decide when the rule applies. :contentReference[oaicite:35]{index=35}  

For example:

* You can restrict access to certain tools based on a claim in the user’s token (such as a role or group) or a specific request attribute.
* The trigger condition expects a Gravitee Expression Language (EL) expression. :contentReference[oaicite:36]{index=36} :contentReference[oaicite:37]{index=37}  

This lets you implement fine-grained, context-aware authorization for MCP tools.

### Validate ACL rules with the Everything example server

To validate your ACL configuration without affecting a production MCP server, use the official **Everything** MCP example server. It exposes many tools and is well suited to testing filters. :contentReference[oaicite:38]{index=38}  

1. Start the Everything server:

   ```bash
   npx @modelcontextprotocol/server-everything streamableHttp
   ``` :contentReference[oaicite:39]{index=39}  

2. Confirm that the server is listening on port `3001`. :contentReference[oaicite:40]{index=40}  

3. In your Gravitee MCP proxy API configuration, set the backend endpoint URL to:

   ```text
   http://localhost:3001/mcp
   ``` :contentReference[oaicite:41]{index=41}  

4. Save and redeploy the API. :contentReference[oaicite:42]{index=42}  

You can now use your MCP client to verify that the ACL rules correctly control which tools are visible and callable. Because the Everything server exposes many tools, it makes it easy to confirm that restricted tools are hidden or blocked as expected. :contentReference[oaicite:43]{index=43}  

## Secure an unsecured MCP server with Gravitee Access Management

In some cases, your MCP server is not secured at all, but you want to enforce OAuth 2.0 authentication for MCP clients. You can use APIM together with AM to secure the MCP server, while keeping the backend MCP implementation unchanged. :contentReference[oaicite:44]{index=44}  

> **Important:** This flow applies only when the MCP server itself is **not** already secured. If the MCP server already implements its own OAuth 2.0 flow, use the “Expose a secured MCP server” approach instead. :contentReference[oaicite:45]{index=45}  

### Prerequisites for AM integration

Ensure that:

* You have an AM domain and enough permissions to configure it. :contentReference[oaicite:46]{index=46}  
* You use an MCP client (for example, Visual Studio Code) that properly supports the MCP protocol with this type of authentication. :contentReference[oaicite:47]{index=47}  

### Step 1: Prepare the MCP proxy API in APIM

1. In APIM, create a new API and name it, for example, **API MCP Proxy**.
2. Create an initial **Keyless** plan to validate proxying. :contentReference[oaicite:48]{index=48}  
3. Deploy the API and verify that it correctly proxies the unsecured MCP server without authentication. :contentReference[oaicite:49]{index=49}  

### Step 2: Configure the MCP server resource in AM

1. In AM, open the target domain.
2. Create a resource for MCP servers (for example, **MCP Servers**).
3. Set a name for the resource.
4. In the **MCP resource identifier** field, enter the endpoint of the APIM MCP proxy API that you created in the previous step.
5. Let AM generate a **Client ID** and **Client Secret**, or provide your own.
6. Store these credentials securely; you will use them later in APIM. :contentReference[oaicite:50]{index=50}  

### Step 3: Configure Dynamic Client Registration (recommended)

Dynamic Client Registration (DCR) allows MCP clients to register themselves with AM and obtain credentials automatically.

1. In AM, go to **Settings > Client Registration**.
2. Enable **Dynamic Client Registration** (DCR). :contentReference[oaicite:51]{index=51}  

**Behavior**

* If DCR is enabled, compatible MCP clients (for example, VS Code) can automatically create an application in AM and register their Client ID and Client Secret. :contentReference[oaicite:52]{index=52} :contentReference[oaicite:53]{index=53}  
* If DCR is not enabled, you must manually create an AM application for the MCP client, configure redirect URLs, and provide the Client ID and Client Secret to the client. :contentReference[oaicite:54]{index=54} :contentReference[oaicite:55]{index=55}  

### Step 4: (Optional) Enable user self-registration in AM

To allow end users to sign up during the login flow:

1. In AM, go to **Settings > Login > User registration**.
2. Enable user registration (sign-up). :contentReference[oaicite:56]{index=56}  

### Step 5: Finalize OAuth2 protection in APIM

1. In the **API MCP Proxy** API in APIM:
   * Add a resource of type **Gravitee.io AM Authorization Server**.
   * Configure it to point to your AM instance.
   * Provide the **Client ID** and **Client Secret** that you created for the MCP resource in AM.
   * Save the resource. :contentReference[oaicite:57]{index=57}  

2. Create an **OAuth2** plan for the API and configure it to use the AM Authorization Server resource. :contentReference[oaicite:58]{index=58}  

3. Remove the initial **Keyless** plan. :contentReference[oaicite:59]{index=59}  

4. Redeploy the API. :contentReference[oaicite:60]{index=60}  

### Resulting user and client experience

After this configuration:

* When an MCP client connects to your MCP proxy API, it is redirected to AM for user login. :contentReference[oaicite:61]{index=61}  
* The user logs in with an existing AM account or creates a new one if registration is enabled. :contentReference[oaicite:62]{index=62}  
* After successful login, AM redirects back to the MCP client.
* The MCP client uses the registered Client ID and Client Secret to obtain a token and call the MCP API, which is now secured in APIM by the OAuth2 plan. :contentReference[oaicite:63]{index=63}  

### Clean up dynamic registrations in Visual Studio Code

If you use Visual Studio Code and want to delete Client IDs that were created via dynamic registration:

1. Open the **Command Palette**:
   * macOS: `Cmd+Shift+P`
   * Windows/Linux: `Ctrl+Shift+P`
2. Run **Authentication: Remove Dynamic Authentication Providers**. :contentReference[oaicite:64]{index=64}  

## Troubleshooting and limitations

### MCP authorization flow limitations

* The MCP OAuth 2.0 Protected Resource Metadata flow (RFC 9728) is still being adopted by MCP servers and clients. :contentReference[oaicite:65]{index=65} :contentReference[oaicite:66]{index=66}  
* If either the MCP client or server does not follow the specified negotiation flow (401 challenge, `WWW-Authenticate` with resource metadata, discovery, token retrieval), Gravitee cannot relay authentication natively. :contentReference[oaicite:67]{index=67}  

### ACL policy gotchas

* If you add the ACL policy but configure no rules, all MCP tools, resources, and prompts will be hidden, even though the MCP client can still connect to the proxy. :contentReference[oaicite:68]{index=68}  
* When testing with the Everything server, make sure that the backend endpoint in APIM points to the correct local URL (`http://localhost:3001/mcp`). :contentReference[oaicite:69]{index=69}  

For broader context on Agent Mesh and MCP integration, see the Agent Mesh overview and MCP integration goals for release 4.10. :contentReference[oaicite:70]{index=70} :contentReference[oaicite:71]{index=71}
