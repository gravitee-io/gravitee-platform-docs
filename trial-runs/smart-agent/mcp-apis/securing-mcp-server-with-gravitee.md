# securing mcp server with gravitee

## Overview

This guide explains how to secure an unsecured MCP (Model Context Protocol) server using Gravitee APIM and Gravitee Access Management (AM). By adding an OAuth2 plan to your MCP proxy API, you enforce authentication for all MCP client connections.

{% hint style="warning" %}
This configuration applies only to MCP servers that do not have their own authentication. If the MCP server is already secured, use the approach described in [Exposing a Secured MCP Server](/broken/pages/41f11fd9f156b274b9b28b9a90a9d605a67b4e45).
{% endhint %}

## Prerequisites

Before you secure an MCP server with Gravitee, complete the following steps:

* Install and configure Gravitee APIM 4.x or later
* Have access to a Gravitee AM domain with configuration permissions
* Have an MCP client that supports OAuth2 authentication (for example, VS Code)

## Create the MCP proxy API

{% stepper %}
{% step %}
Navigate to the **APIs** section in the APIM Console, and then click **Create API**.
{% endstep %}

{% step %}
Create a new V4 API with the MCP Proxy type as described in [Exposing an Unsecured MCP Server](/broken/pages/8d582e05da3b6e2c11183d7e46804547a5996266).
{% endstep %}

{% step %}
Create a **Keyless** plan for initial testing.
{% endstep %}

{% step %}
Deploy the API and verify that it proxies the MCP server correctly without authentication.
{% endstep %}
{% endstepper %}

## Configure the MCP server resource in AM

{% stepper %}
{% step %}
Navigate to your AM domain in the Access Management Console.
{% endstep %}

{% step %}
Create a new **MCP Server** resource.
{% endstep %}

{% step %}
Enter a name for the resource.
{% endstep %}

{% step %}
In the **MCP Resource Identifier** field, enter the APIM API endpoint URL.
{% endstep %}

{% step %}
Generate or provide a **Client ID** and **Client Secret** for this resource.

{% hint style="info" %}
Record the Client ID and Client Secret. You need these values when configuring the APIM resource.
{% endhint %}
{% endstep %}

{% step %}
Save the MCP server resource.
{% endstep %}
{% endstepper %}

## Enable Dynamic Client Registration (recommended)

{% stepper %}
{% step %}
In AM, navigate to **Settings** > **Client Registration**.
{% endstep %}

{% step %}
Enable **Dynamic Client Registration**.
{% endstep %}
{% endstepper %}

When DCR is enabled:

* MCP clients automatically create applications in AM
* Clients register their own Client ID and Client Secret
* No manual redirect URL configuration is required

When DCR is disabled:

* You must manually create an application in AM for each MCP client
* You must configure redirect URLs according to the client requirements
* You must provide the Client ID and Client Secret to the MCP client

## Enable user registration (optional)

{% stepper %}
{% step %}
In AM, navigate to **Settings** > **Login** > **User Registration**.
{% endstep %}

{% step %}
Enable the **User Registration** option.
{% endstep %}
{% endstepper %}

## Configure the OAuth2 plan in APIM

{% stepper %}
{% step %}
Navigate to your MCP proxy API in the APIM Console.
{% endstep %}

{% step %}
Add a new resource of type **Gravitee.io AM Authorization Server**.
{% endstep %}

{% step %}
Configure the resource with:

* Your AM instance connection details
* The Client ID from the MCP server resource created in AM
* The Client Secret from the MCP server resource created in AM
{% endstep %}

{% step %}
Save the resource.
{% endstep %}

{% step %}
Create a new **OAuth2** plan that uses the AM resource.
{% endstep %}

{% step %}
Delete or close the Keyless plan.
{% endstep %}

{% step %}
Redeploy the API.
{% endstep %}
{% endstepper %}

## Verification

{% stepper %}
{% step %}
Configure an MCP client to connect to your Gravitee Gateway endpoint.
{% endstep %}

{% step %}
When the client attempts to connect, confirm that you are redirected to the AM login page.
{% endstep %}

{% step %}
Log in with an existing AM user or create a new account if registration is enabled.
{% endstep %}

{% step %}
After successful authentication, confirm that you are redirected back to the MCP client.
{% endstep %}

{% step %}
Verify that the MCP client can now access the MCP server through the authenticated connection.
{% endstep %}
{% endstepper %}

{% hint style="info" %}
**VS Code users**: To remove dynamically registered authentication providers, open the command palette (Cmd+Shift+P on macOS or Ctrl+Shift+P on Windows/Linux) and run the command: `Authentication: Remove Dynamic Authentication Providers`
{% endhint %}

## Next steps

* [Controlling MCP Server Access](/broken/pages/04c5d28582ae357c408a77492c95aa9137501f4e) - Add ACL policies to restrict access to specific MCP tools and features
