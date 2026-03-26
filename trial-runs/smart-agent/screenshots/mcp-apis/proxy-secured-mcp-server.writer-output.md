# proxy secured mcp server.writer output

## Overview

This guide explains how to proxy a Model Context Protocol (MCP) server that implements its own OAuth authentication through Gravitee. For the proxy to work correctly, both the backend MCP server and the MCP client must comply with the MCP authentication specification.

{% hint style="warning" %}
Support for the MCP authentication specification is still being adopted. Not all MCP clients and servers implement this flow correctly.
{% endhint %}

## Prerequisites

Before you proxy a secured MCP server, ensure the following:

* You have access to the Gravitee APIM Console
* The MCP server implements the MCP OAuth authentication specification
* The MCP client supports the MCP OAuth authentication flow

## MCP authentication flow

For the proxy to function correctly, the following authentication flow must occur:

1. **Initial challenge**: The MCP server rejects the unauthenticated request with a `401 Unauthorized` response.
2.  **WWW-Authenticate header**: The 401 response contains a `WWW-Authenticate` header that includes a `resource_metadata` URL. For example:

    ```
    http://mcpserver.com/.well-known/oauth-protected-resource
    ```
3. **Auth discovery**: The MCP client calls the `.well-known/oauth-protected-resource` URL to retrieve information about the authorization server.
4. **Token retrieval**: The MCP client authenticates with the authorization server and retrieves a token to retry the initial request.

{% hint style="danger" %}
If the MCP client or server doesn't implement this authentication flow correctly, the API proxy cannot relay authentication natively.
{% endhint %}

## Create the MCP proxy API

{% stepper %}
{% step %}
### Log in and start

Log in to the APIM Console and select **APIs** from the left menu.

Click **+ Add API** and select **V4 API**.
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

Define the access path for the entrypoint.
{% endstep %}

{% step %}
### Backend endpoint

Enter the URL of your secured MCP server in the backend endpoint field.
{% endstep %}

{% step %}
### Security plan

Configure the security plan according to your requirements.
{% endstep %}

{% step %}
### Review and deploy

Review your configuration and click **Create and Deploy**.
{% endstep %}
{% endstepper %}

## Test with a compatible server and client

To test the secured MCP proxy flow:

* **Compatible server**: GitHub Copilot API at `https://api.githubcopilot.com/mcp/`
* **Compatible client**: VS Code with the Copilot extension

{% hint style="info" %}
VS Code with the Copilot extension is currently one of the few major clients that correctly implements the MCP authentication specification.
{% endhint %}

## Next steps

* [Configure MCP access control](/broken/pages/da691a21aeae4af95403dab81a9b3707dec466ca)
