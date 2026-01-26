# Secure an MCP server with Gravitee

## Overview

This guide explains how to secure an unsecured Model Context Protocol (MCP) server using Gravitee API Management (APIM) and an OAuth2 plan with Gravitee Access Management (AM).

{% hint style="warning" %}
This configuration only works with unsecured MCP servers. If the MCP server itself is already secured, this configuration will not work.
{% endhint %}

## Prerequisites

Before you secure an MCP server with Gravitee, complete the following steps:

* Ensure you have an AM domain and the rights to configure it
* Use an MCP client (for example, VSCode) that properly supports the MCP protocol with OAuth2 authentication

## Create an API proxy in APIM

1. In APIM, create a new API and name it "API MCP Proxy."
2. Create a Keyless plan.
3. Deploy the API.
4. Test that the API correctly proxies the MCP server without authentication.

## Configure the MCP server in AM

1. In AM, navigate to the desired domain.
2. Create an MCP server resource.
3. Enter a name for the resource.
4. In the **MCP Resource Identifier** field, add the APIM API endpoint.

    <figure><img src=".gitbook/assets/apim-mcp-oauth-step-01.png" alt="New MCP server form with name, resource identifier, and description fields"><figcaption></figcaption></figure>

5. Let AM generate a Client ID and Client Secret, or provide your own. Keep these credentials as they will be needed later.

## Configure Dynamic Client Registration in AM

To avoid manually creating an application in AM and specifying its Client ID in the MCP client (for example, VSCode), enable Dynamic Client Registration (DCR).

1. In AM, navigate to **Settings > Client Registration**.
2. Enable DCR.

{% hint style="info" %}
If DCR is enabled, the MCP client (for example, VSCode) automatically creates the application in AM and registers the Client ID and Client Secret. If DCR is not enabled, you must manually create an application in AM for the MCP client and correctly configure the redirect URLs. You must also configure the MCP client with the Client ID and Client Secret.
{% endhint %}

## Enable user registration in AM

For this guide, enable client user registration (sign up).

1. In AM, navigate to **Settings > Login > User Registration**.
2. Enable the registration option.

## Finalize configuration in APIM

1. In your API MCP Proxy in APIM, add a resource of type **Gravitee.io AM Authorization Server**.
2. Configure the resource by linking it to your AM instance and using the Client ID and Client Secret previously created in AM for the API MCP Proxy resource.
3. Save the resource.
4. Add an OAuth2 plan in APIM using the AM resource that was just added.
5. Delete the Keyless plan.
6. Redeploy the API.

## Verification

The MCP client, upon connection, should now use the OAuth2 server configured in APIM. You will be redirected to the AM login page, where you can use an existing AM user or create one (if the registration option was enabled). Once successfully logged in via AM, a redirection is performed to the MCP client. The MCP client retrieves the Client ID and Client Secret in the background, and creates a token to use the MCP API, now secured in APIM.

{% hint style="info" %}
If you are using VSCode and want to delete the Client IDs registered by dynamic registration, use the command palette: `Cmd+Shift+P` (or `Ctrl+Shift+P` on Windows/Linux), and search for and use the action: **Authentication: Remove Dynamic Authentication Providers**.
{% endhint %}

<!-- ASSETS USED (copy/rename exactly):
- screenshots/image1.png -> trial-runs/.gitbook/assets/apim-mcp-oauth-step-01.png | alt: "New MCP server form with name, resource identifier, and description fields"
-->