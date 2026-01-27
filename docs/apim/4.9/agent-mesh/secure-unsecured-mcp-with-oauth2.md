# Securing an Unsecured MCP Server with Gravitee AM OAuth2

## Overview

This guide explains how to add OAuth2 authentication to an unsecured Model Context Protocol (MCP) server using Gravitee API Management (APIM) and Gravitee Access Management (AM). The configuration includes Dynamic Client Registration (DCR) and user registration setup.

{% hint style="warning" %}
This configuration only works if the MCP server itself is not already secured. If your MCP server has its own authentication, this approach will not function correctly.
{% endhint %}

## Prerequisites

Before you secure an MCP server, complete the following steps:

* Ensure you have an AM domain with configuration rights.
* Ensure you have an MCP client that supports the MCP protocol with authentication, such as VSCode.

## Prepare the API proxy in APIM

To prepare your API proxy in APIM, complete the following steps:

1. Log in to your APIM Console.
2. Select **APIs** from the left nav.
3. Click **+ Add API**.
4. In the **Create New API** section, click **Create V4 API**.
5. Enter your API's name as "API MCP Proxy" and version number, then click **Validate my API details**.
6. Select **Proxy Generic Protocol** and click **Select my API architecture**.
7. Select **HTTP Proxy** and click **Select my entrypoints**.
8. Set a unique **Context-path**, then click **Validate my entrypoints**.
9. For the target URL, enter the URL of your MCP server.
10. Click **Validate my endpoints**.
11. By default, Gravitee adds a **Default keyless plan (UNSECURED)** to your API. Click **Validate my plans**.
12. Click **Save & Deploy**.
13. Test that the API works correctly to proxy the MCP server without authentication.

## Configure the MCP server in AM

To configure the MCP server in AM, complete the following steps:

1. Log in to your AM Console.
2. Navigate to the desired domain.
3. Create an entity named "MCP Servers".
4. Enter a name for this resource.
5. Add the APIM API endpoint in the **MCP Resource Identifier** field.
6. Let AM generate a ClientID and a Client Secret, or provide your own.
7. Save these credentials for later use.

## Configure DCR in AM

To avoid manually creating an Application in AM and specifying its Client ID in the MCP client, enable Dynamic Client Registration (DCR).

To configure DCR in AM, complete the following steps:

1. Log in to your AM Console.
2. Select **Settings** from the left nav.
3. Select **Client Registration** from the inner left nav.
4. Toggle **Enable Dynamic Client Registration** ON.

{% hint style="info" %}
If DCR is enabled, the MCP client (such as VSCode) automatically creates the application in AM and registers the ClientID and Client Secret. If DCR is not enabled, you must manually create an Application in AM for the MCP client and configure the redirect URLs. You must also configure the MCP client with the ClientID and Client Secret.
{% endhint %}

## Enable user registration in AM

To enable client user registration, complete the following steps:

1. Log in to your AM Console.
2. Select **Settings** from the left nav.
3. Select **Login** from the inner left nav.
4. Select **User Registration**.
5. Toggle **Enable user registration** ON.

## Finalize the configuration in APIM

To finalize the configuration in APIM, complete the following steps:

1. Log in to your APIM Console.
2. Select **APIs** from the left nav.
3. Select your API MCP Proxy.
4. Select **Configuration** from the inner left nav.
5. Select **Resources** from the inner left nav.
6. Click **+ Add resource**.
7. Select **Gravitee.io AM Authorization Server**.
8. Configure the resource by linking it to your AM instance and using the ClientID and Client Secret previously created in AM for the "API MCP Proxy" resource.
9. Click **Save**.
10. Select **Consumers** from the inner left nav.
11. Under the **Plans** tab, click **+ Add new plan**.
12. Select **OAuth2** from the drop-down menu.
13. Configure the OAuth2 plan using the AM resource that was just added.
14. Click **Save**.
15. Delete the Keyless plan.
16. Click **Save & Deploy**.

## Verification

The MCP client should now use the OAuth2 server configured in APIM. When connecting, you will be redirected to the AM login page, where you can use an existing AM user or create one if registration was enabled. After successfully logging in via AM, a redirection is performed to the MCP client. The MCP client retrieves the ClientID and Client Secret in the background and creates a token to use the MCP API, which is now secured in APIM.

## Next steps

{% hint style="info" %}
**VSCode users**

If you are using VSCode and want to delete the ClientIDs registered by dynamic registration, use the command palette. Press `Cmd+Shift+P` (or `Ctrl+Shift+P` on Windows/Linux), search for and use the action: **Authentication: Remove Dynamic Authentication Providers**.
{% endhint %}