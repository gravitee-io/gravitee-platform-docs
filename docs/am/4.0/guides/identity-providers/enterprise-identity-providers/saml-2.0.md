---
description: Overview of Security Assertion Markup Language.
---

# SAML 2.0

## Overview

SAML 2.0 stands for Security Assertion Markup Language 2.0. It is an XML-based open standard for transferring identity data between two parties:

* a SAML authority named an Identity Provider (IdP)
* a SAML consumer named a Service Provider (SP)

SAML 2.0 specifies a web browser SSO profile involving an identity provider (IdP), a service provider (SP), and a principal wielding an HTTP user agent (a browser) which is used by AM to create a bridge between your applications and a SAML 2.0 IdP (Microsoft ADFS, for example).

{% hint style="info" %}
In this scenario, the AM SAML 2.0 identity provider acts as the Service Provider (SP) via the SP-Initiated SSO flow.
{% endhint %}

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-social-idp-saml2.png" alt=""><figcaption><p>AM SAML flow</p></figcaption></figure>

## Get your SAML 2.0 identity provider (IdP) metadata

To connect your applications to a SAML 2.0 IdP, you need at least the following information:

* **SingleSignOnService**: the SAML IdP Sign-In URL
* **SingleLogoutService**: the SAML IdP Sign Out URL
* **Signing certificate**: the public signing certificate (encoded in PEM) provided by the identity provider

{% hint style="info" %}
Before you begin, obtain this information from your SAML IdP administrator and make a note of it for later use.
{% endhint %}

## Create a SAML 2.0 connector

1. Log in to AM Console.
2. Click **Settings > Providers**.
3. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
4. Select **SAML 2.0** as your identity provider type and click **Next**.
5. Give your identity provider a name.
6. Configure the settings (EntityID, Sign In URL, Sign Out URL, Signing certificate).
7. Click **Create**.

{% hint style="info" %}
The connector includes some advanced settings such as protocol binding (HTTP-REDIRECT or HTTP-POST), NameId format and Request Signing options to connect to your SAML 2.0 IdP. If you need more information on how to configure these settings, check with your SAML IdP administrator.

Make a note of the URL in **1. Configure the Redirect URI** on the right-hand side of the page. This is the SAML 2.0 Assertion Consumer Service URL you need to provide to the SAML 2.0 IdP to register your Access Management instance.

From AM version 3.7, SAML IdP servers may ask you to share the SAML SP Metadata endpoint to register your AM instance. This endpoint can be found at: `https://AM_GW_HOST/:domain/saml2/sp/metadata/:providerId`.

From SAML IdP plugin v1.4.0, encrypted assertion responses can be handled and decrypted. We decided to only publish KeyDescriptor with use="encryption" if the 'wantAssertionsEncrypted' option is enabled.
{% endhint %}

## Test the connection

You can test your SAML 2.0 connection using a web application created in AM.

1.  In AM Console, click **Applications > App > Identity Providers** and select your SAML 2.0 connector.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-social-idp-list.png" alt=""><figcaption><p>Select SAML 2.0 IdP</p></figcaption></figure>
2.  Call the Login page (the `/oauth/authorize` endpoint). If the connection is working you will see a **Sign in with SAML 2.0** button.

    If the button is not visible, there may be a problem with the identity provider settings. Check the AM Gateway log for more information.
3.  Click **Sign in with SAML 2.0**. You will be redirected your SAML 2.0 IdP login page to authenticate your user.

    If your user is already connected (SSO session), the user will be automatically redirected to your application with an OAuth 2.0 access token and Open ID Connect ID token, if requested.

{% hint style="info" %}
SAML responses can be very large. If you see an error message in the Gateway logs like this one: `Size exceeds allowed maximum capacity`

update the `http.maxFormAttributeSize` value in the `gravitee.yml` config file (set it to `-1` for infinite).

[Learn more about updating the Gateway configuration file](../../../getting-started/configuration/configure-am-gateway/)
{% endhint %}
