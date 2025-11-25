---
description: An overview about configure dynamic client registration with apim.
---

# Configure Dynamic Client Registration with APIM

## Overview

This tutorial will quickly showcase how to configure Dynamic Client Registration (DCR) with APIM and Gravitee Access Management (AM).

{% hint style="info" %}
**DCR Background**

[DCR](https://www.rfc-editor.org/rfc/rfc7591) is a protocol that allows OAuth client applications to register with an OAuth server through the OpenID Connect (OIDC) client registration endpoint. DCR allows API consumers to register applications with an OAuth server from Gravitee’s Developer Portal or Management Console. This outsources the issuer and management of application credentials to a third party, allowing for additional configuration options and compatibility with various OIDC features provided by the identity provider.
{% endhint %}

## Prerequisites <a href="#prerequisites-3" id="prerequisites-3"></a>

To participate in this tutorial, you must have an [Enterprise instance of APIM](../../overview/gravitee-apim-enterprise-edition/) 4.0 or later up and running.

You also need to have an authentication server supporting OIDC. We will be using [Gravitee Access Management (AM)](https://documentation.gravitee.io/am/overview/readme) as our provider, but you are free to use any authentication server supporting OIDC.

## APIM Setup <a href="#apim-setup-4" id="apim-setup-4"></a>

To start, let’s see what we need to configure inside of APIM.

### 1. Enable DCR <a href="#enable-dcr-5" id="enable-dcr-5"></a>

The first step is to enable DCR for your instance of APIM. To do this, go to **Settings > Client Registration** in the Console UI. Under **Allowed application types**, you want to disable **Simple** apps and enable all the other “advanced” application types.

Simple applications are not secure as they allow API consumers to define their own `client_id`. However, advanced applications only allow the client registration provider to create the `client_id` and `client_secret` for each application that registers. Therefore, for advanced applications to function, DCR must be enabled and configured.

Under **Client registration providers (DCR)**, toggle on **Enable client registration providers (DCR) for applications**.

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-14 at 9.29.06 AM.jpg" alt=""><figcaption></figcaption></figure>

### 2. Configure AM as DCR provider <a href="#configure-am-as-dcr-provider-6" id="configure-am-as-dcr-provider-6"></a>

With DCR enabled, we now need to configure AM (or any auth server supporting OIDC). Select **+ Add a provider** to begin the configuration process. Provide a **Name** and **Description**:

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-14 at 9.48.56 AM.png" alt=""><figcaption></figcaption></figure>

The **Configuration** section first requires you to provide an **OpenID Connect Discovery Endpoint** which is the URL where an OIDC-compatible authorization server publishes its metadata.

{% hint style="info" %}
**OpenID Connect Discovery Endpoint**

The authorization server metadata published to this endpoint is a JSON listing of the OpenID/OAuth endpoints, supported scopes and claims, public keys used to sign the tokens, and other details. This information can be used to construct a request to the authorization server. The field names and values are defined in the [OIDC Discovery Specification.](https://openid.net/specs/openid-connect-discovery-1_0.html)
{% endhint %}

You must also select an **Initial Access Token Provider**, and we will be using **Client Credentials**. Client credentials is an authorization grant flow that allows APIM to securely retrieve an access token from AM.

Leave this page open and open up AM to see how to retrieve the discovery endpoint and credentials.

## AM Setup <a href="#am-setup-7" id="am-setup-7"></a>

Now let’s configure AM.

### 1. Set security domain

The first step is to create or select the security domain that you want to use in AM. The security domain acts as the container to group related applications and configuration settings. Select your user in the top right and then either select an existing domain or **+ Create domain**.

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-14 at 10.32.02 AM.png" alt=""><figcaption></figcaption></figure>

Once you have a domain, select **Settings** in the sidebar, scroll down to the **Openid** section, and select **Client Registration**. Toggle on the **Enable/Disable Dynamic Client Registration** setting.

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-14 at 10.33.29 AM.jpg" alt=""><figcaption></figcaption></figure>

### 2. Create AM Client Registration Provider Application <a href="#create-am-client-registration-provider-application-8" id="create-am-client-registration-provider-application-8"></a>

Now we just need to create an application in AM. This application is essentially what we use in APIM as the client registration provider.

To create an app in AM, select **Applications** in the sidebar and then select the **+ icon** in the bottom right. This will open up the following application creation wizard:

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-14 at 10.39.11 AM.png" alt=""><figcaption></figcaption></figure>

Select **Backend to Backend** and then **Next**. Finally, provide a **Name** and **Description** for your app, leave everything else as default, and click **Create**.

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-14 at 10.40.39 AM.png" alt=""><figcaption></figcaption></figure>

### 3. Retrieve OpenID Endpoint and Client Credentials <a href="#retrieve-openid-endpoint-and-client-credentials-9" id="retrieve-openid-endpoint-and-client-credentials-9"></a>

Next, we need to retrieve the OpenId configuration endpoint and the client credentials. To retrieve the endpoint, select **Endpoints** from the inner sidebar and scroll down to the **OpenID Configuration endpoint**.

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-14 at 10.46.20 AM.png" alt=""><figcaption></figcaption></figure>

Copy the endpoint and paste it into APIM under **OpenID Connect Discovery Endpoint**.

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-14 at 10.45.08 AM.png" alt=""><figcaption></figcaption></figure>

### 4. Enable scopes and retrieve client credentials

Lastly, we need to enable the proper scopes for the app and retrieve the client credentials. Back in AM, select **Settings** in the inner sidebar. Next, select the **OAuth 2.0 / OIDC** tab and then select the **Scopes** tab on the lower navigation menu.

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-14 at 10.50.26 AM.png" alt=""><figcaption></figcaption></figure>

We need to add the `dcr_admin` scope to ensure the initial access token tied to this application has the proper permissions to create new applications. Select **+ Add Scopes**, search for **dcr\_admin**, select the **Client\_registration\_admin** scope that pops up, and click **Add**. After adding the scope, make sure you click **Save**.

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-14 at 10.53.32 AM.png" alt=""><figcaption></figcaption></figure>

The `dcr_admin` scope must also be added to the scope in the APIM DCR Provider configuration page.

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
Alternatively, you could make the `dcr_admin` scope a default scope in the "DCR Application" of your IdP
{% endhint %}

To obtain the client credentials, simply click the **General** tab to return to the homepage of your AM application.

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-14 at 10.53.48 AM.png" alt=""><figcaption></figcaption></figure>

Copy the **Client ID** and **Client Secret** and paste them in the respective inputs inside the APIM client registration provider configuration page. Scroll down and click **Create**.

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-14 at 10.55.35 AM.png" alt=""><figcaption></figcaption></figure>

Congrats! You have now configured a DCR provider and are ready to create advanced applications inside of APIM.

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-14 at 10.58.26 AM.png" alt=""><figcaption></figcaption></figure>

## Create an Advanced APIM App in the Developer Portal <a href="#create-an-advanced-apim-app-in-the-developer-portal-10" id="create-an-advanced-apim-app-in-the-developer-portal-10"></a>

To create the app, let’s head over to the Developer Portal since this is where your API consumers will generally be creating apps. The Developer Portal is essentially an API catalog and marketplace for API consumers.

To access the Developer Portal, select it from the top menu bar:

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-14 at 11.01.30 AM.png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
**Accessing the Developer Portal**

In the default docker installation, you won’t see this link. By default, the Developer Portal is running at `localhost:8085`. You can add this link by providing the URL of the Developer Portal under **Settings > Settings > Scroll to Portal Section > Portal URL**. Make sure you scroll to the bottom and click **Save** after adding the URL.
{% endhint %}

Inside the Developer Portal, select Application in the top nav and then select **+ Create an App**.

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-14 at 11.05.21 AM.png" alt=""><figcaption></figcaption></figure>

Inside the application creation wizard, provide a **Name** and **Description**, then select **Next**.

Let’s create a Backend to Backend application so we don’t have to worry about a Redirect URI. Select **Backend to Backend** then select **Next**.

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-14 at 11.07.23 AM.png" alt=""><figcaption></figcaption></figure>

We can ignore the **Subscription** page and just click **Next** again. Finally, confirm your API details and select **Create The App**.

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-14 at 11.18.39 AM.png" alt=""><figcaption></figcaption></figure>

Well done! If you return to AM and select **Applications** in the sidebar, you should see the brand new application you just created in the Developer Portal:

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-14 at 11.20.02 AM.png" alt=""><figcaption></figcaption></figure>
