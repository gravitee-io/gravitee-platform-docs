# configure-dcr.writer-output.md

---
description: Configure Dynamic Client Registration (DCR) with APIM and Gravitee Access Management (AM).
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/bGmDEarvnV52XdcOiV8o/how-to-guides/use-case-tutorials/configure-dcr
---

# Configure DCR

## Overview

This guide explains how to configure Dynamic Client Registration (DCR) with APIM and Gravitee Access Management (AM).

[DCR](https://www.rfc-editor.org/rfc/rfc7591) is a protocol that allows OAuth client applications to register with an OAuth server through the OpenID Connect (OIDC) client registration endpoint. DCR allows API consumers to register applications with an OAuth server from Gravitee's Developer Portal or Management Console. This outsources the issuer and management of application credentials to a third party, allowing for additional configuration options and compatibility with various OIDC features provided by the identity provider.

## Prerequisites

Before you configure DCR, ensure you have:

* An Enterprise instance of APIM 4.0 or later up and running
* An authentication server supporting OIDC (this guide uses Gravitee Access Management)

## Configure DCR in APIM

### Enable DCR

1. Navigate to **Settings > Client Registration** in the Console UI.
2. Under **Allowed application types**, disable **Simple** apps and enable all other "advanced" application types.

    {% hint style="info" %}
    Simple applications are not secure as they allow API consumers to define their own `client_id`. Advanced applications only allow the client registration provider to create the `client_id` and `client_secret` for each application that registers. For advanced applications to function, DCR must be enabled and configured.
    {% endhint %}

3. Under **Client registration providers (DCR)**, toggle on **Enable client registration providers (DCR) for applications**.

    <figure><img src="../../.gitbook/assets/apim-dcr-step-01.jpg" alt="Client registration settings showing DCR enabled"><figcaption></figcaption></figure>

### Configure AM as DCR provider

1. Select **+ Add a provider** to begin the configuration process.
2. Provide a **Name** and **Description**.

    <figure><img src="../../.gitbook/assets/apim-dcr-step-02.png" alt="Add provider form with name and description fields"><figcaption></figcaption></figure>

3. In the **Configuration** section, provide an **OpenID Connect Discovery Endpoint**, which is the URL where an OIDC-compatible authorization server publishes its metadata.

    {% hint style="info" %}
    **OpenID Connect Discovery Endpoint**

    The authorization server metadata published to this endpoint is a JSON listing of the OpenID/OAuth endpoints, supported scopes and claims, public keys used to sign the tokens, and other details. This information can be used to construct a request to the authorization server. The field names and values are defined in the [OIDC Discovery Specification](https://openid.net/specs/openid-connect-discovery-1_0.html).
    {% endhint %}

4. Select **Client Credentials** as the **Initial Access Token Provider**. Client credentials is an authorization grant flow that allows APIM to securely retrieve an access token from AM.

Leave this page open and proceed to configure AM.

## Configure AM

### Set security domain

1. Select your user in the top right and then either select an existing domain or **+ Create domain**.

    <figure><img src="../../.gitbook/assets/apim-dcr-step-03.png" alt="AM domain selection dropdown"><figcaption></figcaption></figure>

2. Select **Settings** in the sidebar, scroll down to the **Openid** section, and select **Client Registration**.
3. Toggle on the **Enable/Disable Dynamic Client Registration** setting.

    <figure><img src="../../.gitbook/assets/apim-dcr-step-04.jpg" alt="Client registration toggle in AM settings"><figcaption></figcaption></figure>

### Create AM Client Registration Provider Application

1. Select **Applications** in the sidebar and then select the **+ icon** in the bottom right.

    <figure><img src="../../.gitbook/assets/apim-dcr-step-05.png" alt="Application creation wizard in AM"><figcaption></figcaption></figure>

2. Select **Backend to Backend** and then **Next**.
3. Provide a **Name** and **Description** for your app, leave everything else as default, and click **Create**.

    <figure><img src="../../.gitbook/assets/apim-dcr-step-06.png" alt="Backend to Backend application form"><figcaption></figcaption></figure>

### Retrieve OpenID endpoint and client credentials

1. Select **Endpoints** from the inner sidebar and scroll down to the **OpenID Configuration endpoint**.

    <figure><img src="../../.gitbook/assets/apim-dcr-step-07.png" alt="OpenID Configuration endpoint in AM"><figcaption></figcaption></figure>

2. Copy the endpoint and paste it into APIM under **OpenID Connect Discovery Endpoint**.

    <figure><img src="../../.gitbook/assets/apim-dcr-step-08.png" alt="OpenID Connect Discovery Endpoint field in APIM"><figcaption></figcaption></figure>

### Enable scopes and retrieve client credentials

1. In AM, select **Settings** in the inner sidebar.
2. Select the **OAuth 2.0 / OIDC** tab and then select the **Scopes** tab on the lower navigation menu.

    <figure><img src="../../.gitbook/assets/apim-dcr-step-09.png" alt="OAuth scopes configuration in AM"><figcaption></figcaption></figure>

3. Select **+ Add Scopes**, search for **dcr_admin**, select the **Client_registration_admin** scope, and click **Add**.
4. Click **Save**.

    <figure><img src="../../.gitbook/assets/apim-dcr-step-10.png" alt="Adding dcr_admin scope"><figcaption></figcaption></figure>

    The `dcr_admin` scope must also be added to the scope in the APIM DCR Provider configuration page.

    <figure><img src="../../.gitbook/assets/image (38) (3).png" alt="Scope field in APIM DCR provider configuration"><figcaption></figcaption></figure>

    {% hint style="info" %}
    Alternatively, you could make the `dcr_admin` scope a default scope in the "DCR Application" of your IdP.
    {% endhint %}

5. Click the **General** tab to return to the homepage of your AM application.

    <figure><img src="../../.gitbook/assets/apim-dcr-step-11.png" alt="General tab showing client credentials"><figcaption></figcaption></figure>

6. Copy the **Client ID** and **Client Secret** and paste them in the respective inputs inside the APIM client registration provider configuration page.
7. Scroll down and click **Create**.

    <figure><img src="../../.gitbook/assets/apim-dcr-step-12.png" alt="Client credentials fields in APIM"><figcaption></figcaption></figure>

You have now configured a DCR provider and are ready to create advanced applications inside of APIM.

<figure><img src="../../.gitbook/assets/apim-dcr-step-13.png" alt="Configured DCR provider in APIM"><figcaption></figcaption></figure>

## Create an advanced APIM app in the Developer Portal

1. Access the Developer Portal by selecting it from the top menu bar.

    <figure><img src="../../.gitbook/assets/apim-dcr-step-14.png" alt="Developer Portal link in top navigation"><figcaption></figcaption></figure>

    {% hint style="info" %}
    **Accessing the Developer Portal**

    In the default Docker installation, you won't see this link. By default, the Developer Portal is running at `localhost:8085`. You can add this link by providing the URL of the Developer Portal under **Settings > Settings > Scroll to Portal Section > Portal URL**. Make sure you scroll to the bottom and click **Save** after adding the URL.
    {% endhint %}

2. Select **Application** in the top nav and then select **+ Create an App**.

    <figure><img src="../../.gitbook/assets/apim-dcr-step-15.png" alt="Create an App button in Developer Portal"><figcaption></figcaption></figure>

3. Provide a **Name** and **Description**, then select **Next**.
4. Select **Backend to Backend** then select **Next**.

    <figure><img src="../../.gitbook/assets/apim-dcr-step-16.png" alt="Backend to Backend application type selection"><figcaption></figcaption></figure>

5. Click **Next** on the **Subscription** page.
6. Confirm your API details and select **Create The App**.

    <figure><img src="../../.gitbook/assets/apim-dcr-step-17.png" alt="Application creation confirmation"><figcaption></figcaption></figure>

If you return to AM and select **Applications** in the sidebar, you should see the brand new application you just created in the Developer Portal.

<figure><img src="../../.gitbook/assets/apim-dcr-step-18.png" alt="New application visible in AM"><figcaption></figcaption></figure>

## Expose MCP APIs in Gravitee

This section explains how to expose your APIs as Model Context Protocol (MCP) servers via Gravitee, allowing AI agents and LLMs to discover and invoke your API operations.

### Overview

The Model Context Protocol (MCP) is an emerging standard enabling AI agents to understand and interact with external tools and data. By exposing your APIs as MCP servers via Gravitee, you allow LLMs and conversational agents to discover and invoke your API operations intelligently, without requiring complex connectors.

Exposing your MCP servers via Gravitee APIM allows you to maintain governance, observability, and security over interactions between AI agents and your backend services.

### Expose an unsecured MCP server

This procedure explains how to publish an existing MCP server (which does not require its own authentication) via Gravitee. The goal is to add a layer of governance, observability, and control through APIM, even if the backend is open.

1. Create a new API and start the V4 API creation process.
2. Enter your API name and version in the **General Configuration** section.
3. Select **AI Gateway** as the architecture choice.
4. Choose the **MCP Proxy** option as the proxy type.
5. Define the access path in the **Entrypoint** field (for example, `/mcp-proxy`).
6. Enter the URL of your target MCP server in the **Backend (Endpoint)** field.
7. For this example, proceed with a **Keyless** plan in the **Security** section.
8. Validate the creation and deploy the API.

#### Monitoring

* In the APIM logs screen, you can track exchanges between the MCP server and the MCP client.
* In the API Traffic screen, a dashboard allows you to visualize MCP server usage, the methods and main tools used, as well as any errors encountered by the server.

#### Test the configuration

If you don't have an MCP server yet, you can simulate a local environment with the official example server.

1. Start the example server from the [MCP servers repository](https://github.com/modelcontextprotocol/servers/tree/main/src/everything):

    ```bash
    npx @modelcontextprotocol/server-everything streamableHttp
    ```

    The server will usually start on port 3001.

2. In step 6 (Backend), use the following URL:

    ```
    http://localhost:3001/mcp
    ```

### Expose a secured MCP server

Exposing a secured MCP server via a proxy (like Gravitee) requires the backend server and the client to strictly adhere to certain parts of the MCP specification regarding OAuth/Auth authentication.

#### MCP authentication flow

For the connection to work through the proxy, the following mechanism must take place:

1. **Initial challenge**: The MCP server must reject the unauthenticated request with a `401 Unauthorized` code.
2. **WWW-Authenticate header**: The `401` response must contain a specific header including `resource_metadata`. For example, a URL pointing to a metadata resource, such as `http://mcpserver.com/.well-known/oauth-protected-resource`.
3. **Auth discovery**: The client (the AI agent) then calls this `.well-known/oauth-protected-resource` URL to obtain information about the authentication server to use.
4. **Token retrieval**: The client authenticates and retrieves a token to retry its initial request.

{% hint style="warning" %}
If the client (the AI tool) or the server does not respect this negotiation flow specific to the MCP spec, the API Proxy will not be able to relay the authentication natively.
{% endhint %}

#### Compatibility and testing

As of today, support for this authentication specification is still being adopted.

* **Recommended test server**: You can test this flow with the GitHub Copilot API: `https://api.githubcopilot.com/mcp/`
* **Compatible client**: Currently, VS Code (via the Copilot extension) is one of the only major clients correctly implementing this part of the MCP specification.

### Secure an MCP server with Gravitee

This procedure explains how to secure an unsecured MCP server using Gravitee (APIM) and an OAuth2 plan with Gravitee Access Management (AM).

{% hint style="info" %}
If the MCP server itself is already secured, this configuration will not work.
{% endhint %}

#### Prerequisites

* An AM domain and the rights to configure it
* An MCP client (for example, VS Code) that properly supports the MCP protocol with this type of authentication

#### Prepare the API proxy in APIM

1. In APIM, create a new API and name it "API MCP Proxy".
2. Create a simple **Keyless** plan.
3. Deploy the API and test that it works correctly to proxy the MCP server without authentication.

#### Configure the MCP server in AM

1. In AM, access the desired domain and create an entity "MCP Servers" (or the equivalent of "MCP server resource").
2. Fill in a name for this resource.
3. Add the APIM API endpoint in the **MCP Resource Identifier** field.
4. Let AM generate a ClientID and a Client Secret, or provide your own. Keep these credentials as they will be needed later.

#### Configure DCR in AM (recommended)

To avoid manually creating an Application in AM and specifying its Client ID in the MCP client (for example, VS Code), enable DCR.

1. In AM, navigate to **Settings > Client Registration**.
2. Enable DCR.

    * If DCR is enabled: The MCP client (for example, VS Code) should automatically create the application in AM and also register the ClientID / Client Secret.
    * If DCR is not enabled: You will need to manually create an Application in AM for the MCP client and correctly configure the redirect URLs according to it. You will also need to configure the MCP client with the ClientID/Client Secret.

#### Enable user registration in AM (optional)

For this guide, it is recommended to enable client user registration (sign up).

1. In AM, navigate to **Settings > Login > User Registration**.
2. Enable the registration option.

#### Finalize configuration in APIM

1. In your API MCP Proxy in APIM, add a resource of type **Gravitee.io AM Authorization Server**.
2. Configure it by linking it to your AM instance and using the ClientID and Client Secret previously created in AM for the "API MCP Proxy" resource.
3. Save.
4. Add an **OAuth2** plan in APIM using the AM resource that was just added.
5. Delete the **Keyless** plan.
6. Redeploy the API.

#### Verification

The MCP client, upon connection, should now use the OAuth2 server configured in APIM. You will be redirected to the AM login page, where you can use an existing AM user or create one (if the registration option was enabled). Once successfully logged in via AM, a redirection is performed to the MCP client. The MCP client retrieves the ClientID and Client Secret in the background, and creates a token to use the MCP API, now secured in APIM.

{% hint style="info" %}
**VS Code note**

If you are using VS Code and want to delete the ClientIDs registered by dynamic registration, use the command palette:

* `Cmd+Shift+P` (or `Ctrl+Shift+P` on Windows/Linux)
* Search for and use the action: `>Authentication: Remove Dynamic Authentication Providers`
{% endhint %}

## Control access to the MCP server

This section explains how to control access to MCP (Model Context Protocol) server functionalities using an Access Control List (ACL) policy within Gravitee.

On a Gravitee MCP Proxy API, you can add an ACL (Access Control List) policy via the Policy Studio. This policy restricts access to MCP features such as the list of tools, resources, and prompts.

### Default behavior (implicit deny)

If you add the ACL policy without specifying any rules, the system adopts a restrictive "Deny All" approach by default.

1. Add the policy to an MCP API.
2. Save and deploy.

All server functionalities will be inaccessible. An MCP client will be able to connect to the server via the Gateway, but the lists of tools, resources, and prompts will appear empty.

### Authorize only tool listing

To allow a client to see available tools without being able to execute them:

1. Add a rule (ACL) in the policy configuration.
2. Select the **Tools** feature option.
3. Check the **tools/list** box.
4. Leave the **Name Pattern Type** field on **ANY** (default value).
5. Save and deploy the API.

If you configure an MCP client, it will only be able to list available tools, but any attempt to call (execute) them will be rejected.

### Authorize the call and listing of a specific tool

To restrict access and execution to a single specific tool (for example, `get_weather`):

1. Add or modify an ACL in the policy configuration.
2. In the **Tools** feature option:
    * Check **tools/list** AND **tools/call**.
    * In the **Name Pattern Type** field, select **Literal**.
    * In the **Name Pattern** field, enter the exact name of the tool (for example: `get_weather`).
3. Save and deploy.

From now on, only this specific tool is visible to the MCP client and can be called. All other tools remain hidden and inaccessible.

### Advanced configuration: Execution conditions

Each ACL rule has a **Trigger Condition** field. This field allows you to add conditional logic to determine if the rule should be applied or ignored. This is particularly useful for applying context-based security policies.

You can condition access to certain tools based on a specific property (claim) present in the user's token or a request attribute.

{% hint style="info" %}
The field generally expects a Gravitee EL (Expression Language) expression.
{% endhint %}

### Test locally

To validate your ACL configurations without impacting a production environment, you can use the official example MCP server named "Everything." This server exposes a large number of functionalities, making it ideal for testing filters.

#### Prerequisites and installation

The source code is available in the [MCP Servers Everything repository](https://github.com/modelcontextprotocol/servers/tree/main/src/everything).

To launch the server in HTTP mode (streamable):

```bash
npx @modelcontextprotocol/server-everything streamableHttp
```

#### API configuration

1. Once the local server is launched, return to your Gravitee API configuration.
2. Configure the API Endpoint to point to the local URL of the created server:

    ```
    http://localhost:3001/mcp
    ```

3. Save and redeploy the API.

#### Verification

You can now test your ACL policy. As the "Everything" server exposes many tools by default, you will be able to effectively verify if your policy correctly filters visible and callable tools according to your rules.

<!-- ASSETS USED (copy/rename exactly):
- screenshots/Screenshot 2023-11-14 at 9.29.06 AM (1).jpg -> ../../.gitbook/assets/apim-dcr-step-01.jpg | alt: "Client registration settings showing DCR enabled"
- screenshots/Screenshot 2023-11-14 at 9.48.56 AM (1).png -> ../../.gitbook/assets/apim-dcr-step-02.png | alt: "Add provider form with name and description fields"
- screenshots/Screenshot 2023-11-14 at 10.32.02 AM (1).png -> ../../.gitbook/assets/apim-dcr-step-03.png | alt: "AM domain selection dropdown"
- screenshots/Screenshot 2023-11-14 at 10.33.29 AM (1).jpg -> ../../.gitbook/assets/apim-dcr-step-04.jpg | alt: "Client registration toggle in AM settings"
- screenshots/Screenshot 2023-11-14 at 10.39.11 AM (1).png -> ../../.gitbook/assets/apim-dcr-step-05.png | alt: "Application creation wizard in AM"
- screenshots/Screenshot 2023-11-14 at 10.40.39 AM (1).png -> ../../.gitbook/assets/apim-dcr-step-06.png | alt: "Backend to Backend application form"
- screenshots/Screenshot 2023-11-14 at 10.46.20 AM (1).png -> ../../.gitbook/assets/apim-dcr-step-07.png | alt: "OpenID Configuration endpoint in AM"
- screenshots/Screenshot 2023-11-14 at 10.45.08 AM (1).png -> ../../.gitbook/assets/apim-dcr-step-08.png | alt: "OpenID Connect Discovery Endpoint field in APIM"
- screenshots/Screenshot 2023-11-14 at 10.50.26 AM (1).png -> ../../.gitbook/assets/apim-dcr-step-09.png | alt: "OAuth scopes configuration in AM"
- screenshots/Screenshot 2023-11-14 at 10.53.32 AM (1).png -> ../../.gitbook/assets/apim-dcr-step-10.png | alt: "Adding dcr_admin scope"
- screenshots/Screenshot 2023-11-14 at 10.53.48 AM (1).png -> ../../.gitbook/assets/apim-dcr-step-11.png | alt: "General tab showing client credentials"
- screenshots/Screenshot 2023-11-14 at 10.55.35 AM (1).png -> ../../.gitbook/assets/apim-dcr-step-12.png | alt: "Client credentials fields in APIM"
- screenshots/Screenshot 2023-11-14 at 10.58.26 AM (1).png -> ../../.gitbook/assets/apim-dcr-step-13.png | alt: "Configured DCR provider in APIM"
- screenshots/Screenshot 2023-11-14 at 11.01.30 AM (1).png -> ../../.gitbook/assets/apim-dcr-step-14.png | alt: "Developer Portal link in top navigation"
- screenshots/Screenshot 2023-11-14 at 11.05.21 AM (1).png -> ../../.gitbook/assets/apim-dcr-step-15.png | alt: "Create an App button in Developer Portal"
- screenshots/Screenshot 2023-11-14 at 11.07.23 AM (1).png -> ../../.gitbook/assets/apim-dcr-step-16.png | alt: "Backend to Backend application type selection"
- screenshots/Screenshot 2023-11-14 at 11.18.39 AM (1).png -> ../../.gitbook/assets/apim-dcr-step-17.png | alt: "Application creation confirmation"
- screenshots/Screenshot 2023-11-14 at 11.20.02 AM (1).png -> ../../.gitbook/assets/apim-dcr-step-18.png | alt: "New application visible in AM"
-->