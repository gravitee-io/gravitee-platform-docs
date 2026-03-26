# proxy unsecured mcp server.writer output

## Overview

This guide explains how to proxy an existing Model Context Protocol (MCP) server that doesn't require authentication through Gravitee. Proxying the MCP server adds a layer of governance, observability, and control through API Management (APIM), even when the backend is open.

## Prerequisites

Before you proxy an unsecured MCP server, ensure the following:

* You have access to the Gravitee APIM Console
* You have the URL of your target MCP server
* The MCP server is accessible from your Gravitee Gateway

{% hint style="info" %}
If you don't have an MCP server yet, you can use the official MCP example server for testing. See [Test with the example MCP server](proxy-unsecured-mcp-server.writer-output.md#test-with-the-example-mcp-server) for setup instructions.
{% endhint %}

## Create the MCP proxy API

{% stepper %}
{% step %}
### Log in and start

Log in to the APIM Console and select **APIs** from the left menu. Click **+ Add API** and select **V4 API**.
{% endstep %}

{% step %}
### Name and version

Enter a name and version for your API, then click **Next**.
{% endstep %}

{% step %}
### Select architecture

Select **AI Gateway** as the architecture type.
{% endstep %}

{% step %}
### Select proxy type

Select **MCP Proxy** as the proxy type.
{% endstep %}

{% step %}
### Define access path

Define the access path for the entrypoint. For example, `/mcp-proxy`.
{% endstep %}

{% step %}
### Configure backend

Enter the URL of your target MCP server in the backend endpoint field.
{% endstep %}

{% step %}
### Choose security plan

Select **Keyless** as the security plan.
{% endstep %}

{% step %}
### Review and deploy

Review your configuration and click **Create and Deploy**.
{% endstep %}
{% endstepper %}

## Monitor MCP traffic

After deploying the API, you can monitor interactions between MCP clients and your server.

### View exchange logs

{% stepper %}
{% step %}
Navigate to your API in the APIM Console.
{% endstep %}

{% step %}
Select **Analytics > Logs** from the left menu.
{% endstep %}

{% step %}
Review the exchange logs between the MCP server and MCP clients.
{% endstep %}
{% endstepper %}

### View usage analytics

{% stepper %}
{% step %}
Navigate to your API in the APIM Console.
{% endstep %}

{% step %}
Select **Analytics > Dashboard** from the left menu.
{% endstep %}

{% step %}
Review the MCP server usage metrics, including:

* Methods and tools used
* Error rates
* Traffic patterns
{% endstep %}
{% endstepper %}

## Test with the example MCP server

To test your MCP proxy configuration without a production server, use the official MCP example server.

{% stepper %}
{% step %}
Install and start the example server:

{% code title="Start example MCP server" %}
```bash
npx @modelcontextprotocol/server-everything streamableHttp
```
{% endcode %}
{% endstep %}

{% step %}
Configure your Gravitee API with the following backend URL:

```
http://localhost:3001/mcp
```
{% endstep %}

{% step %}
Deploy the API and connect an MCP client to verify the proxy is working.
{% endstep %}
{% endstepper %}

## Next steps

* [Configure MCP access control](/broken/pages/da691a21aeae4af95403dab81a9b3707dec466ca)
* [Secure an MCP server with Access Management](/broken/pages/34e029d160ee033a8f9950ebde0f7edd19c12eec)
