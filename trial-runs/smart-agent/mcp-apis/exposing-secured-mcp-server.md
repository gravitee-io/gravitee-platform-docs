# exposing secured mcp server

## Overview

This guide explains how to expose an MCP (Model Context Protocol) server that has its own authentication requirements through a Gravitee APIM proxy. When proxying a secured MCP server, both the backend server and the client must adhere to the MCP specification for OAuth authentication.

{% hint style="warning" %}
If the MCP client or server does not implement the MCP authentication specification correctly, the API proxy cannot relay authentication natively.
{% endhint %}

## Prerequisites

Before you expose a secured MCP server, complete the following steps:

* Install and configure Gravitee APIM 4.x or later
* Have access to a secured MCP server endpoint that implements RFC 9728
* Have an MCP client that supports the MCP authentication specification

## Understand the MCP authentication flow

{% stepper %}
{% step %}
### Initial challenge

The MCP server rejects an unauthenticated request with a `401 Unauthorized` response.
{% endstep %}

{% step %}
### WWW-Authenticate header

The `401` response includes a header containing resource metadata. For example:

```
WWW-Authenticate: Bearer resource_metadata="http://mcpserver.com/.well-known/oauth-protected-resource"
```
{% endstep %}

{% step %}
### Auth discovery

The MCP client calls the `.well-known/oauth-protected-resource` URL to obtain information about the authentication server.
{% endstep %}

{% step %}
### Token retrieval

The client authenticates with the authorization server and retrieves a token.
{% endstep %}

{% step %}
### Authenticated request

The client retries the original request with the obtained token.
{% endstep %}
{% endstepper %}

## Create an MCP proxy API for a secured server

{% stepper %}
{% step %}
### Create a new API

Navigate to the **APIs** section in the APIM Console, and then click **Create API**.
{% endstep %}

{% step %}
### Select API flow

Select the **V4 API** creation flow.
{% endstep %}

{% step %}
### Configure general settings

Enter your API name and version in the **General Configuration** section.
{% endstep %}

{% step %}
### Choose architecture

Select **AI Gateway** as the architecture type.
{% endstep %}

{% step %}
### Choose proxy type

Select **MCP Proxy** as the proxy type.
{% endstep %}

{% step %}
### Define entrypoint

Define the entrypoint path for your API.
{% endstep %}

{% step %}
### Set backend endpoint

Enter the URL of your secured MCP server in the **Backend (Endpoint)** field.
{% endstep %}

{% step %}
### Configure plan

Configure an appropriate plan based on your security requirements.
{% endstep %}

{% step %}
### Create the API

Review your configuration, and then click **Create** to finalize the API.
{% endstep %}

{% step %}
### Deploy

Click **Deploy** to make the API available on the Gateway.
{% endstep %}
{% endstepper %}

## Verification

{% stepper %}
{% step %}
### Configure the client

Configure an MCP client that supports the MCP authentication specification to connect to your Gravitee Gateway endpoint.
{% endstep %}

{% step %}
### Confirm authentication flow

Confirm that the client receives the `401` challenge and successfully completes the authentication flow.
{% endstep %}

{% step %}
### Verify proxied requests

Verify that authenticated requests are proxied successfully to the backend MCP server.
{% endstep %}
{% endstepper %}

{% hint style="info" %}
Support for the MCP authentication specification (RFC 9728) is still being adopted across the ecosystem. VS Code with the GitHub Copilot extension is currently one of the few major clients that correctly implements this part of the MCP specification.
{% endhint %}

## Test with GitHub Copilot API

You can test the secured MCP proxy flow using the GitHub Copilot API:

1.  Configure your MCP proxy API endpoint to use:

    ```
    https://api.githubcopilot.com/mcp/
    ```
2. Use VS Code with the Copilot extension as your MCP client.

## Next steps

* [Controlling MCP Server Access](/broken/pages/04c5d28582ae357c408a77492c95aa9137501f4e) - Learn how to restrict access to specific MCP tools and features
* [Securing an MCP Server with Gravitee](/broken/pages/db79ab554282bba17c1e94ac6ca59ae7e37e3e39) - Add OAuth2 authentication using Gravitee Access Management
