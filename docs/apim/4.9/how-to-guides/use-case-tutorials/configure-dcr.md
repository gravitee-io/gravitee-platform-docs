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
2. Provide a **Name** and **Description** for the provider.

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

    <figure><img src="../../.gitbook/assets/apim-dcr-step-04.jpg" alt="AM client registration settings with DCR enabled"><figcaption></figcaption></figure>

### Create AM Client Registration Provider Application

1. Select **Applications** in the sidebar and then select the **+ icon** in the bottom right.

    <figure><img src="../../.gitbook/assets/apim-dcr-step-05.png" alt="AM application creation wizard showing application types"><figcaption></figcaption></figure>

2. Select **Backend to Backend** and then **Next**.
3. Provide a **Name** and **Description** for your app, leave everything else as default, and click **Create**.

    <figure><img src="../../.gitbook/assets/apim-dcr-step-06.png" alt="AM application creation form with name and description fields"><figcaption></figcaption></figure>

### Retrieve OpenID endpoint and client credentials

1. Select **Endpoints** from the inner sidebar and scroll down to the **OpenID Configuration endpoint**.

    <figure><img src="../../.gitbook/assets/apim-dcr-step-07.png" alt="AM endpoints page showing OpenID configuration endpoint"><figcaption></figcaption></figure>

2. Copy the endpoint and paste it into APIM under **OpenID Connect Discovery Endpoint**.

    <figure><img src="../../.gitbook/assets/apim-dcr-step-08.png" alt="APIM DCR provider configuration with OpenID endpoint field"><figcaption></figcaption></figure>

### Enable scopes and retrieve client credentials

1. In AM, select **Settings** in the inner sidebar.
2. Select the **OAuth 2.0 / OIDC** tab and then select the **Scopes** tab on the lower navigation menu.

    <figure><img src="../../.gitbook/assets/apim-dcr-step-09.png" alt="AM OAuth scopes configuration page"><figcaption></figcaption></figure>

3. Select **+ Add Scopes**, search for **dcr_admin**, select the **Client_registration_admin** scope, and click **Add**.
4. Click **Save**.

    <figure><img src="../../.gitbook/assets/apim-dcr-step-10.png" alt="AM add scopes dialog with dcr_admin scope selected"><figcaption></figcaption></figure>

5. In APIM, add the `dcr_admin` scope to the DCR Provider configuration page.

    <figure><img src="../../.gitbook/assets/apim-dcr-step-11.png" alt="APIM DCR provider configuration with dcr_admin scope field"><figcaption></figcaption></figure>

    {% hint style="info" %}
    Alternatively, you can make the `dcr_admin` scope a default scope in the "DCR Application" of your IdP.
    {% endhint %}

6. In AM, click the **General** tab to return to the homepage of your AM application.

    <figure><img src="../../.gitbook/assets/apim-dcr-step-12.png" alt="AM application general settings showing client ID and secret"><figcaption></figcaption></figure>

7. Copy the **Client ID** and **Client Secret** and paste them in the respective inputs inside the APIM client registration provider configuration page.
8. Scroll down and click **Create**.

    <figure><img src="../../.gitbook/assets/apim-dcr-step-13.png" alt="APIM DCR provider configuration with client credentials fields"><figcaption></figcaption></figure>

You have now configured a DCR provider and are ready to create advanced applications inside of APIM.

<figure><img src="../../.gitbook/assets/apim-dcr-step-14.png" alt="APIM client registration providers list showing configured provider"><figcaption></figcaption></figure>

## Create an advanced APIM app in the Developer Portal

1. Access the Developer Portal by selecting it from the top menu bar.

    <figure><img src="../../.gitbook/assets/apim-dcr-step-15.png" alt="APIM top navigation showing Developer Portal link"><figcaption></figcaption></figure>

    {% hint style="info" %}
    **Accessing the Developer Portal**

    In the default Docker installation, you won't see this link. By default, the Developer Portal is running at `localhost:8085`. You can add this link by providing the URL of the Developer Portal under **Settings > Settings > Scroll to Portal Section > Portal URL**. Make sure you scroll to the bottom and click **Save** after adding the URL.
    {% endhint %}

2. Select **Application** in the top nav and then select **+ Create an App**.

    <figure><img src="../../.gitbook/assets/apim-dcr-step-16.png" alt="Developer Portal applications page with create app button"><figcaption></figcaption></figure>

3. Provide a **Name** and **Description**, then select **Next**.
4. Select **Backend to Backend** then select **Next**.

    <figure><img src="../../.gitbook/assets/apim-dcr-step-17.png" alt="Developer Portal application creation wizard showing application type selection"><figcaption></figcaption></figure>

5. Click **Next** on the **Subscription** page.
6. Confirm your API details and select **Create The App**.

    <figure><img src="../../.gitbook/assets/apim-dcr-step-18.png" alt="Developer Portal application creation confirmation page"><figcaption></figcaption></figure>

If you return to AM and select **Applications** in the sidebar, you should see the brand new application you just created in the Developer Portal.

<figure><img src="../../.gitbook/assets/apim-dcr-step-19.png" alt="AM applications list showing newly created application"><figcaption></figcaption></figure>

## Expose an MCP server with OAuth2 authentication

This section explains how to secure an unsecured MCP server using Gravitee APIM and an OAuth2 plan with Gravitee Access Management.

{% hint style="warning" %}
If the MCP server itself is already secured, this configuration will not work.
{% endhint %}

### Prerequisites

Before you expose an MCP server with OAuth2 authentication, ensure you have:

* An AM domain and the rights to configure it
* An MCP client (for example, VS Code) that properly supports the MCP protocol with this type of authentication

### Prepare the API proxy in APIM

1. In APIM, create a new API and name it "API MCP Proxy".
2. Create a simple Keyless plan.
3. Deploy the API and test that it works correctly to proxy the MCP server without authentication.

### Configure the MCP server in AM

1. In AM, access the desired domain and create an entity "MCP Servers" (or the equivalent of "MCP server resource").
2. Fill in a name for this resource.
3. Add the APIM API endpoint in the **MCP Resource Identifier** field.
4. Let AM generate a ClientID and a Client Secret, or provide your own. Keep these credentials as they will be needed later.

### Configure DCR in AM (recommended)

To avoid manually creating an Application in AM and specifying its Client ID in the MCP client (for example, VS Code), enable DCR.

1. In AM, navigate to **Settings > Client Registration**.
2. Enable DCR.

    If DCR is enabled, the MCP client (for example, VS Code) should automatically create the application in AM and also register the ClientID / Client Secret.

    If DCR is not enabled, you will need to manually create an Application in AM for the MCP client and correctly configure the redirect URLs according to it. You will also need to configure the MCP client with the ClientID/Client Secret.

### Enable user registration in AM (optional)

For this guide, it is recommended to enable client user registration (sign up).

1. In AM, navigate to **Settings > Login > User Registration**.
2. Enable the registration option.

### Finalize configuration in APIM

1. In your API MCP Proxy in APIM, add a resource of type **Gravitee.io AM Authorization Server**.
2. Configure it by linking it to your AM instance and using the ClientID and Client Secret previously created in AM for the "API MCP Proxy" resource.
3. Save.
4. Add an OAuth2 plan in APIM using the AM resource that was just added.
5. Delete the Keyless plan.
6. Redeploy the API.

The MCP client, upon connection, should now use the OAuth2 server configured in APIM. You will be redirected to the AM login page, where you can use an existing AM user or create one (if the registration option was enabled). Once successfully logged in via AM, a redirection is performed to the MCP client. The MCP client retrieves the ClientID and Client Secret in the background, and creates a token to use the MCP API, now secured in APIM.

{% hint style="info" %}
**VS Code note**

If you are using VS Code and want to delete the ClientIDs registered by dynamic registration, use the command palette:

`Cmd+Shift+P` (or `Ctrl+Shift+P` on Windows/Linux)

Search for and use the action: `>Authentication: Remove Dynamic Authentication Providers`
{% endhint %}

<!-- ASSETS USED (copy/rename exactly):
- screenshots/Screenshot 2023-11-14 at 9.29.06 AM (1).jpg -> trial-runs/.gitbook/assets/apim-dcr-step-01.jpg | alt: "Client registration settings showing DCR enabled"
- screenshots/Screenshot 2023-11-14 at 9.48.56 AM (1).png -> trial-runs/.gitbook/assets/apim-dcr-step-02.png | alt: "Add provider form with name and description fields"
- screenshots/Screenshot 2023-11-14 at 10.32.02 AM (1).png -> trial-runs/.gitbook/assets/apim-dcr-step-03.png | alt: "AM domain selection dropdown"
- screenshots/Screenshot 2023-11-14 at 10.33.29 AM (1).jpg -> trial-runs/.gitbook/assets/apim-dcr-step-04.jpg | alt: "AM client registration settings with DCR enabled"
- screenshots/Screenshot 2023-11-14 at 10.39.11 AM (1).png -> trial-runs/.gitbook/assets/apim-dcr-step-05.png | alt: "AM application creation wizard showing application types"
- screenshots/Screenshot 2023-11-14 at 10.40.39 AM (1).png -> trial-runs/.gitbook/assets/apim-dcr-step-06.png | alt: "AM application creation form with name and description fields"
- screenshots/Screenshot 2023-11-14 at 10.46.20 AM (1).png -> trial-runs/.gitbook/assets/apim-dcr-step-07.png | alt: "AM endpoints page showing OpenID configuration endpoint"
- screenshots/Screenshot 2023-11-14 at 10.45.08 AM (1).png -> trial-runs/.gitbook/assets/apim-dcr-step-08.png | alt: "APIM DCR provider configuration with OpenID endpoint field"
- screenshots/Screenshot 2023-11-14 at 10.50.26 AM (1).png -> trial-runs/.gitbook/assets/apim-dcr-step-09.png | alt: "AM OAuth scopes configuration page"
- screenshots/Screenshot 2023-11-14 at 10.53.32 AM (1).png -> trial-runs/.gitbook/assets/apim-dcr-step-10.png | alt: "AM add scopes dialog with dcr_admin scope selected"
- screenshots/image (38) (3).png -> trial-runs/.gitbook/assets/apim-dcr-step-11.png | alt: "APIM DCR provider configuration with dcr_admin scope field"
- screenshots/Screenshot 2023-11-14 at 10.53.48 AM (1).png -> trial-runs/.gitbook/assets/apim-dcr-step-12.png | alt: "AM application general settings showing client ID and secret"
- screenshots/Screenshot 2023-11-14 at 10.55.35 AM (1).png -> trial-runs/.gitbook/assets/apim-dcr-step-13.png | alt: "APIM DCR provider configuration with client credentials fields"
- screenshots/Screenshot 2023-11-14 at 10.58.26 AM (1).png -> trial-runs/.gitbook/assets/apim-dcr-step-14.png | alt: "APIM client registration providers list showing configured provider"
- screenshots/Screenshot 2023-11-14 at 11.01.30 AM (1).png -> trial-runs/.gitbook/assets/apim-dcr-step-15.png | alt: "APIM top navigation showing Developer Portal link"
- screenshots/Screenshot 2023-11-14 at 11.05.21 AM (1).png -> trial-runs/.gitbook/assets/apim-dcr-step-16.png | alt: "Developer Portal applications page with create app button"
- screenshots/Screenshot 2023-11-14 at 11.07.23 AM (1).png -> trial-runs/.gitbook/assets/apim-dcr-step-17.png | alt: "Developer Portal application creation wizard showing application type selection"
- screenshots/Screenshot 2023-11-14 at 11.18.39 AM (1).png -> trial-runs/.gitbook/assets/apim-dcr-step-18.png | alt: "Developer Portal application creation confirmation page"
- screenshots/Screenshot 2023-11-14 at 11.20.02 AM (1).png -> trial-runs/.gitbook/assets/apim-dcr-step-19.png | alt: "AM applications list showing newly created application"
- screenshots/new-mcp-server-form.png -> trial-runs/.gitbook/assets/apim-dcr-step-20.png | alt: "New MCP server form showing server settings fields"
- screenshots/gravitee-hold-nothing-back-banner.png -> trial-runs/.gitbook/assets/apim-dcr-step-21.png | alt: "Gravitee Hold Nothing Back banner"
-->