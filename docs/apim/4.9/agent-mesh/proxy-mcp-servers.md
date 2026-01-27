# Exposing an Unsecured MCP Server via Gravitee APIM

## Overview

This guide explains how to create an MCP Proxy API in Gravitee to expose an existing unsecured MCP server. By proxying an MCP server through Gravitee APIM, you add governance and observability without requiring backend authentication.

## Prerequisites

Before you expose an unsecured MCP server, complete the following steps:

* Ensure you have access to Gravitee APIM Console with permissions to create APIs.
* Verify that your MCP server is running and accessible.
* Confirm that the MCP server does not require authentication.

## Create an MCP Proxy API

To create an MCP Proxy API in Gravitee, complete the following steps:

1. Log in to your APIM Console.
2. Select **APIs** from the left nav.
3. Click **+ Add API**.
4. In the **Create New API** section, click **Create V4 API**.
5. Enter your API name and version number, then click **Validate my API details**.
6. Select **AI Gateway** as the architecture type, then click **Select my API architecture**.
7. Select **MCP Proxy** as the proxy type, then click **Select my entrypoints**.
8. Set the entrypoint path. For example, `/mcp-proxy`.
9. Click **Validate my entrypoints**.
10. Configure the backend endpoint:
    * Enter the URL of your target MCP server in the **Target URL** field. For example, `http://localhost:3001/mcp`.
11. Click **Validate my endpoints**.
12. Select **Keyless** as the security plan, then click **Validate my plans**.
13. Click **Save & Deploy**.

{% hint style="success" %}
Your MCP Proxy API is now deployed and ready to use.
{% endhint %}

## Monitoring

After deploying your MCP Proxy API, you can monitor MCP server activity using the following features:

* **APIM logs screen**: Track exchanges between the MCP server and the MCP client.
* **API Traffic dashboard**: Visualize MCP server usage, including the methods and main tools used, as well as any errors encountered by the server.

## Test the MCP Proxy API

If you don't have an MCP server yet, you can simulate a local environment with the official example server.

To test your MCP Proxy API, complete the following steps:

1. Start the example server using the following command:

    ```bash
    npx @modelcontextprotocol/server-everything streamableHttp
    ```

    The server will start on port 3001 by default.

2. Configure your MCP Proxy API to use the following backend URL:

    ```
    http://localhost:3001/mcp
    ```

3. Test the connection by sending requests to your MCP Proxy API entrypoint.

{% hint style="warning" %}
For internal testing within APIM, you can use the following URL: `https://apim-tools-mcp-server.team-apim.gravitee.dev/mcp`. This is an internal Gravitee tool and should not be added to public documentation. This URL may be removed at any time.
{% endhint %}

## Next steps

* Configure access control for your MCP server. For more information, see the MCP ACL policy documentation.
* Add additional security plans to control access to your MCP Proxy API.
* Monitor MCP server usage and performance using APIM analytics.