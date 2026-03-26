# exposing unsecured mcp server

## Overview

This guide explains how to expose an existing MCP (Model Context Protocol) server through Gravitee API Management (APIM). By proxying your MCP server through Gravitee, you add governance, observability, and control over interactions between AI agents and your backend services, even when the backend MCP server does not require authentication.

{% hint style="info" %}
The Model Context Protocol is an emerging standard that enables AI agents to understand and interact with external tools and data. Exposing your APIs as MCP servers via Gravitee allows LLMs and conversational agents to discover and invoke your API operations intelligently.
{% endhint %}

## Prerequisites

Before you expose an unsecured MCP server, complete the following steps:

* Install and configure Gravitee APIM 4.x or later
* Have access to an MCP server endpoint
* Have permissions to create APIs in Gravitee APIM

## Create an MCP proxy API

{% stepper %}
{% step %}
### Start API creation

Navigate to the **APIs** section in the APIM Console, and then click **Create API**. Select the **V4 API** creation flow.
{% endstep %}

{% step %}
### General configuration

Enter your API name and version in the **General Configuration** section.
{% endstep %}

{% step %}
### Architecture and proxy type

Select **AI Gateway** as the architecture type and **MCP Proxy** as the proxy type.
{% endstep %}

{% step %}
### Entrypoint path

Define the entrypoint path for your API. For example:

```
/mcp-proxy
```
{% endstep %}

{% step %}
### Backend endpoint

Enter the URL of your target MCP server in the **Backend (Endpoint)** field.
{% endstep %}

{% step %}
### Plan type

Select **Keyless** as the plan type to allow unrestricted access for initial setup.
{% endstep %}

{% step %}
### Create and deploy

Review your configuration, click **Create** to finalize the API, then click **Deploy** to make the API available on the Gateway.
{% endstep %}
{% endstepper %}

## Monitor MCP traffic

After deploying your MCP proxy API, you can monitor traffic in two ways:

* **Logs screen**: View detailed exchanges between the MCP server and MCP clients
* **API Traffic dashboard**: Visualize MCP server usage, including the methods and tools used, and any errors encountered by the server

## Verification

{% stepper %}
{% step %}
### Configure an MCP client

Configure an MCP client to connect to your Gravitee Gateway endpoint.
{% endstep %}

{% step %}
### List available tools

Confirm that the client can list available tools from the proxied MCP server.
{% endstep %}

{% step %}
### Execute a tool call

Execute a tool call and verify the response is returned successfully.
{% endstep %}
{% endstepper %}

## Test with a local MCP server

If you do not have an MCP server available, you can use the official MCP example server for testing.

{% stepper %}
{% step %}
### Start the example server

Run:

```bash
npx @modelcontextprotocol/server-everything streamableHttp
```

The server starts on port 3001 by default.
{% endstep %}

{% step %}
### Configure the Gravitee endpoint

Configure your Gravitee MCP proxy API endpoint to use the following URL:

```
http://localhost:3001/mcp
```
{% endstep %}

{% step %}
### Save and redeploy

Save and redeploy the API.
{% endstep %}
{% endstepper %}

## Next steps

* [Controlling MCP Server Access](/broken/pages/04c5d28582ae357c408a77492c95aa9137501f4e) - Learn how to restrict access to specific MCP tools and features
* [Securing an MCP Server with Gravitee](/broken/pages/db79ab554282bba17c1e94ac6ca59ae7e37e3e39) - Add OAuth2 authentication to your MCP proxy
