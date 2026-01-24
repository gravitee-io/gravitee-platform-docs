# secure mcp server with am.writer output

## Overview

This guide explains how to secure an unsecured Model Context Protocol (MCP) server using Gravitee API Management (APIM) and an OAuth2 plan with Gravitee Access Management (AM).

{% hint style="danger" %}
This configuration only works for MCP servers that don't implement their own authentication. If the MCP server is already secured, use the [Proxy a secured MCP server](/broken/pages/1e99c37904639592705ea456a0d4e16aa74c0c01) guide instead.
{% endhint %}

## Prerequisites

Before you secure an MCP server with AM, ensure the following:

* You have access to an AM domain with configuration permissions
* You have an MCP Proxy API deployed in APIM
* You use an MCP client that supports the MCP protocol with OAuth authentication

## Steps

{% stepper %}
{% step %}
### Create and test the MCP proxy API

* Create a new MCP Proxy API in APIM named "API MCP Proxy."
* Create a Keyless plan for initial testing.
* Deploy the API.
* Test the API to verify it proxies the MCP server correctly without authentication.
{% endstep %}

{% step %}
### Configure the MCP server in AM

* Log in to the AM Console and navigate to your domain.
* Select **MCP Servers** from the left menu.
* Click **+ Add MCP Server**.
* Enter a name for the MCP server resource.
* Enter the APIM API endpoint URL in the **MCP Resource Identifier** field.
* (Optional) Provide your own Client ID and Client Secret, or allow AM to generate them.
* Click **Save** and record the Client ID and Client Secret for later use.
{% endstep %}

{% step %}
### Configure Dynamic Client Registration

Dynamic Client Registration (DCR) allows MCP clients to automatically create applications in AM without manual configuration.

{% hint style="info" %}
Enabling DCR is recommended. If DCR is enabled, the MCP client (for example, VS Code) automatically creates the application in AM and registers the Client ID and Client Secret.
{% endhint %}

* In the AM Console, navigate to **Settings > Client Registration**.
* Enable **Dynamic Client Registration**.
* Click **Save**.

If you don't enable DCR, you must:

* Manually create an application in AM for each MCP client
* Configure the redirect URLs according to the client requirements
* Provide the Client ID and Client Secret to each MCP client
{% endstep %}

{% step %}
### Enable user registration

To allow users to create accounts during the OAuth flow:

* In the AM Console, navigate to **Settings > Login**.
* Select the **User Registration** tab.
* Enable the registration option.
* Click **Save**.
{% endstep %}

{% step %}
### Configure the OAuth2 plan in APIM

* Navigate to your MCP Proxy API in the APIM Console.
* Select **Resources** from the left menu.
* Click **+ Add Resource** and select **Gravitee.io AM Authorization Server**.
* Configure the resource with:
  * Your AM instance URL
  * The Client ID created in AM for the MCP server
  * The Client Secret created in AM for the MCP server
* Click **Save**.
* Select **Plans** from the left menu.
* Click **+ Add Plan** and select **OAuth2**.
* Configure the plan to use the AM Authorization Server resource you created.
* Publish the OAuth2 plan.
* Close or delete the Keyless plan.
* Deploy the API.
{% endstep %}

{% step %}
### Verification

* Connect an MCP client to the secured API endpoint.
* Verify that you are redirected to the AM login page.
* Log in with an existing AM user or create a new account if registration is enabled.
* Confirm that after successful authentication, you are redirected back to the MCP client.
* Verify that the MCP client can access the MCP server through the secured proxy.

{% hint style="info" %}
**VS Code users**: To remove Client IDs registered through Dynamic Client Registration, open the command palette with `Cmd+Shift+P` (macOS) or `Ctrl+Shift+P` (Windows/Linux) and run the command **Authentication: Remove Dynamic Authentication Providers**.
{% endhint %}
{% endstep %}
{% endstepper %}

## Next steps

* [Configure MCP access control](/broken/pages/da691a21aeae4af95403dab81a9b3707dec466ca)
