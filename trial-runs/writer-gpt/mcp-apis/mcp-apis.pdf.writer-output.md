# MCP APIs.pdf.writer output

## Overview

The Model Context Protocol (MCP) is an emerging standard that enables AI agents to discover and interact with external tools and data. When you expose your APIs as MCP servers through Gravitee API Management (APIM), you let large language models (LLMs) and other agents discover and invoke API operations without building custom connectors.

Using APIM as the control point helps you apply governance, observability, and security to interactions between AI agents and your backend services.

This guide covers:

* Exposing an existing (unsecured) MCP server through an APIM MCP proxy
* Testing with the official MCP example server
* Proxying a secured MCP server that follows the MCP OAuth 2.0 negotiation flow (RFC 9728)
* Restricting MCP tools with an access control list (ACL) policy
* Securing an otherwise unsecured MCP server with an OAuth 2.0 plan backed by Gravitee Access Management (AM)

## Before you begin

You need:

* Access to an APIM environment where you can create and deploy v4 APIs
* The URL of an existing MCP server to proxy (or a local server for testing)
* If you secure an MCP server with AM: an AM domain and permissions to configure it

{% hint style="info" %}
This article uses UI labels and option names as they appear in the source materials (for example, **AI Gateway** and **MCP Proxy**). If your APIM version uses different labels, map the instructions to the equivalent options in your Console.
{% endhint %}

## Expose an unsecured MCP server

Use this approach when your upstream MCP server does not require its own authentication, but you still want governance and observability through APIM.

### Create the MCP proxy API

{% stepper %}
{% step %}
### Create the API

Start the v4 API creation flow in APIM.
{% endstep %}

{% step %}
### Name and version

Enter your API name and version.
{% endstep %}

{% step %}
### Architecture

For **Architecture**, select **AI Gateway**.
{% endstep %}

{% step %}
### Proxy type

For **Proxy type**, select **MCP Proxy**.
{% endstep %}

{% step %}
### Entrypoint

For the **Entrypoint**, set an access path (for example, `/mcp-proxy`).
{% endstep %}

{% step %}
### Backend endpoint

For the backend **Endpoint**, enter the URL of your target MCP server.
{% endstep %}

{% step %}
### Plan

Create a **Keyless** plan.
{% endstep %}

{% step %}
### Deploy

Validate the configuration and deploy the API.
{% endstep %}
{% endstepper %}

### Monitor MCP traffic

* Use the APIM logs to track exchanges between the MCP client and the MCP server.
* Use the **API Traffic** dashboard to visualize MCP usage, the methods and tools used, and server-side errors.

## Test with the official MCP example server

If you do not have an MCP server, you can test with the official example server named `everything`.

{% stepper %}
{% step %}
### Start the example server

```bash
npx @modelcontextprotocol/server-everything streamableHttp
```
{% endstep %}

{% step %}
### Confirm server

Confirm the server is running (it typically starts on port `3001`).
{% endstep %}

{% step %}
### Set backend endpoint

In your MCP proxy API, set the backend endpoint to:

http://localhost:3001/mcp
{% endstep %}
{% endstepper %}

{% hint style="warning" %}
Do not publish internal Gravitee-only test endpoints in public documentation. The source materials reference an internal test MCP server that can change or be removed without notice.
{% endhint %}

## Proxy a secured MCP server

Proxying a secured MCP server through APIM requires the MCP client and the upstream MCP server to follow the MCP OAuth 2.0 negotiation flow described in MCP Authorization (RFC 9728).

### Understand the negotiation flow

For authentication to work through the proxy, the upstream MCP server must:

{% stepper %}
{% step %}
Reject the initial unauthenticated request with `401 Unauthorized`.
{% endstep %}

{% step %}
Return a `WWW-Authenticate` header that includes a `resource_metadata` value.
{% endstep %}

{% step %}
Point `resource_metadata` to an OAuth-protected resource metadata URL (for example, `http://mcpserver.example/.well-known/oauth-protected-resource`).
{% endstep %}

{% step %}
Allow the MCP client to call the metadata URL to discover the authorization server to use.
{% endstep %}

{% step %}
Allow the client to authenticate, obtain a token, and retry the original request with the token.
{% endstep %}
{% endstepper %}

{% hint style="warning" %}
If the MCP client or the upstream MCP server does not follow this negotiation flow, APIM cannot relay authentication natively through the MCP proxy.
{% endhint %}

### Validate client compatibility

Support for this part of the MCP specification is still being adopted.

* You can test the flow against the GitHub Copilot MCP endpoint: https://api.githubcopilot.com/mcp/
* VS Code (with the Copilot extension) is one of the few major clients that implements this negotiation flow.

## Control MCP tool access with an ACL policy

You can restrict which MCP features are available through an APIM MCP proxy API using an ACL policy in Policy Studio. The ACL policy can restrict access to MCP features such as listing tools, calling tools, and accessing resources or prompts.

### Default behavior

If you add an ACL policy and define no rules, the policy applies an implicit deny all:

* The MCP client can connect through the Gateway.
* Lists of tools, resources, and prompts appear empty.
* The client cannot access MCP functionality.

### Allow tool listing only

To let the client list tools but prevent tool execution:

{% stepper %}
{% step %}
Add an ACL rule to the policy.
{% endstep %}

{% step %}
Select the **Tools** feature.
{% endstep %}

{% step %}
Enable `tools/list`.
{% endstep %}

{% step %}
Keep **Name pattern type** set to `ANY`.
{% endstep %}

{% step %}
Save and deploy the API.
{% endstep %}
{% endstepper %}

Result: the client can list tools, but any attempt to call them is rejected.

### Allow listing and calling a specific tool

To expose and allow execution of a single tool (for example, `get_weather`):

{% stepper %}
{% step %}
Add or edit an ACL rule.
{% endstep %}

{% step %}
Under **Tools**, enable both `tools/list` and `tools/call`.
{% endstep %}

{% step %}
Set **Name pattern type** to `Literal`.
{% endstep %}

{% step %}
Set **Name pattern** to the exact tool name (for example, `get_weather`).
{% endstep %}

{% step %}
Save and deploy the API.
{% endstep %}
{% endstepper %}

Result: only the specified tool is visible and callable. All other tools remain hidden and inaccessible.

### Add conditional execution rules

Each ACL rule includes a **Trigger condition** field. Use it to add conditional logic (for example, based on token claims or request attributes). This field typically expects a Gravitee Expression Language (EL) expression.

## Validate ACL rules locally

To test ACL configurations without impacting production, use the `everything` example MCP server because it exposes many tools by default.

{% stepper %}
{% step %}
Start the example server.

```bash
npx @modelcontextprotocol/server-everything streamableHttp
```
{% endstep %}

{% step %}
Set your API endpoint to http://localhost:3001/mcp.
{% endstep %}

{% step %}
Save and redeploy the API.
{% endstep %}

{% step %}
Connect an MCP client and verify that the ACL policy filters visible and callable tools as expected.
{% endstep %}
{% endstepper %}

## Secure an unsecured MCP server with AM

This section shows how to secure an unsecured MCP server using APIM and an OAuth 2.0 plan backed by AM.

{% hint style="warning" %}
If the MCP server itself is already secured, this configuration does not work.
{% endhint %}

### Prerequisites

* An AM domain and permissions to configure it
* An MCP client that supports the MCP authentication flow for OAuth 2.0 (for example, VS Code)

### Step 1: Prepare the MCP proxy API in APIM

{% stepper %}
{% step %}
Create a new API in APIM and name it `API MCP Proxy`.
{% endstep %}

{% step %}
Create a Keyless plan.
{% endstep %}

{% step %}
Deploy the API and verify it proxies the MCP server without authentication.
{% endstep %}
{% endstepper %}

### Step 2: Configure the MCP server resource in AM

{% stepper %}
{% step %}
In AM, open your domain and create an entity named `MCP Servers` (or the equivalent resource type for MCP servers).
{% endstep %}

{% step %}
Enter a name for the resource.
{% endstep %}

{% step %}
In **MCP Resource Identifier**, set the APIM API endpoint URL.
{% endstep %}

{% step %}
Let AM generate a client ID and client secret (or provide your own). Save these credentials.
{% endstep %}
{% endstepper %}

### Step 3: Enable Dynamic Client Registration in AM

To avoid manually creating an application in AM and configuring client credentials in your MCP client, enable Dynamic Client Registration (DCR).

{% stepper %}
{% step %}
In AM, go to **Settings > Client Registration**.
{% endstep %}

{% step %}
Enable DCR.
{% endstep %}
{% endstepper %}

If DCR is enabled, the MCP client can automatically create an AM application and register the client ID and client secret. If DCR is disabled, you must manually create an application in AM, configure redirect URLs, and configure the MCP client with the client credentials.

### Step 4: Enable user self-registration in AM (optional)

For this guide, enable user registration so test users can sign up.

{% stepper %}
{% step %}
In AM, go to **Settings > Login > User Registration**.
{% endstep %}

{% step %}
Enable the registration option.
{% endstep %}
{% endstepper %}

### Step 5: Finalize the OAuth 2.0 configuration in APIM

{% stepper %}
{% step %}
In your `API MCP Proxy` API, add a resource of type `Gravitee.io AM Authorization Server`.
{% endstep %}

{% step %}
Configure the resource to connect to your AM instance and use the client ID and client secret created for the `API MCP Proxy` resource in AM.
{% endstep %}

{% step %}
Save your API configuration.
{% endstep %}

{% step %}
Create an OAuth 2.0 plan that uses the AM authorization server resource.
{% endstep %}

{% step %}
Delete the Keyless plan.
{% endstep %}

{% step %}
Redeploy the API.
{% endstep %}
{% endstepper %}

### Verify the login flow

When an MCP client connects:

* The client redirects you to the AM login page.
* After login, AM redirects back to the MCP client.
* The client retrieves the client ID and client secret in the background, obtains a token, and calls the MCP API secured by APIM.

### VS Code cleanup

If you use VS Code and want to delete client IDs registered by dynamic registration:

{% stepper %}
{% step %}
Open the Command Palette (`Cmd+Shift+P` on macOS or `Ctrl+Shift+P` on Windows/Linux).
{% endstep %}

{% step %}
Run **Authentication: Remove Dynamic Authentication Providers**.
{% endstep %}
{% endstepper %}
