# create-mcp-server.md

## Overview

This guide explains how to create and configure an MCP (Model Context Protocol) server in Gravitee Access Management. MCP servers enable AI agents and LLMs to discover and interact with your APIs as tools, providing a standardized way to expose backend functionality to conversational agents.

By exposing your APIs as MCP servers through Gravitee, you maintain governance, observability, and security over interactions between AI agents and your backend services.

## Prerequisites

Before you create an MCP server, ensure you have:

* Access to Gravitee Access Management with appropriate permissions
* An existing Gravitee APIM API that you want to expose as an MCP server
* The APIM API endpoint URL

## Create an MCP server

1. Navigate to **Access Management** in the Gravitee Console.

2. Select your environment from the **Environment** dropdown.

3. Click **MCP Servers** in the left navigation menu.

4. Click **New MCP server** to open the configuration form.

    ![New MCP server form showing server settings fields](.gitbook/assets/apim-mcp-server-step-01.png)

5. Configure the MCP server settings:

    * **Domain**: The security domain for the MCP server. This field is pre-populated with `/agentic` by default.
    * **Name**: Enter a descriptive name for your MCP server.
    * **MCP Resource Identifier**: Enter the canonical resource identifier for your MCP server. This should be the URL where the MCP server will be accessible (for example, `https://banking.example.com`).
    * **Description**: (Optional) Enter a description of the MCP server's purpose and functionality.

6. Click **Save** to create the MCP server.

    Access Management generates a Client ID and Client Secret for the MCP server. These credentials are required for OAuth2 authentication when securing the server.

## Configure tools

After creating the MCP server, you can define which tools (API operations) the server provides:

1. In the **Tools Configuration** section, click **Add tool**.

    ![Tools Configuration section with Add tool button](.gitbook/assets/apim-mcp-server-step-02.png)

2. Configure each tool by specifying:

    * The API operations to expose
    * Access scopes for the tool
    * Any additional metadata

    {% hint style="info" %}
    Tools can be tied to specific scopes to control which consumers can access them. This enables fine-grained access control based on OAuth2 scopes.
    {% endhint %}

3. Click **Save** after adding each tool.

## Verification

To verify your MCP server configuration:

1. Navigate to **MCP Servers** in Access Management.

2. Locate your newly created server in the list.

3. Verify that:
    * The server name and resource identifier are correct
    * The Client ID and Client Secret are displayed
    * Any configured tools appear in the Tools Configuration section

## Next steps

After creating your MCP server, you can:

* [Secure the MCP server with OAuth2](secure-mcp-server.md)
* [Control access to MCP tools using ACL policies](control-mcp-access.md)
* [Proxy an existing MCP server through Gravitee APIM](proxy-mcp-server.md)
* Configure MCP clients to connect to your server
* Monitor MCP server usage through APIM analytics

<!-- ASSETS USED (copy/rename exactly):
- screenshots/mcp-server-form.png -> trial-runs/.gitbook/assets/apim-mcp-server-step-01.png | alt: "New MCP server form showing server settings fields"
- screenshots/mcp-tools-config.png -> trial-runs/.gitbook/assets/apim-mcp-server-step-02.png | alt: "Tools Configuration section with Add tool button"
-->