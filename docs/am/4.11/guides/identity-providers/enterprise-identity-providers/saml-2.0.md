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
Before you begin, obtain this information from your SAML IdP administrator and make a note of it for later use. Alternatively, if your IdP publishes metadata at a stable URL or provides metadata as a downloadable XML file, you can use metadata-based configuration to automatically extract signing certificates, SSO endpoints, and protocol bindings.
{% endhint %}

## Prerequisites

Before configuring a SAML identity provider, complete the following steps:

* Configure an Access Management domain with a client application
* Upload a certificate to the Access Management certificate repository (for signing AuthnRequests when using metadata-based modes) and note its ID
* Ensure SAML identity provider metadata is accessible via HTTPS URL or available as an XML file (for metadata-based modes)
* Verify network connectivity from Access Management gateway to the IdP metadata endpoint (for `METADATA_URL` mode)

## Certificate roles

Two certificate types are used in SAML flows:

* **Gravitee certificate** (`graviteeCertificate` property): A certificate stored in Access Management's certificate repository, referenced by ID, and used by the client application to sign outbound SAML AuthnRequests when the IdP's metadata indicates `WantAuthnRequestsSigned=true`.
* **IdP signing certificate**: Extracted from metadata (in metadata-based modes) or manually configured via the `signingCertificate` property (in manual mode), and used to verify signed SAML assertions and responses from the identity provider.

Certificate synchronization between the client application and the provider domain is required when using metadata-based configuration.

## Create a SAML 2.0 connector

1. Log in to AM Console.
2. Click **Settings > Providers**.
3. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
4. Select **SAML 2.0** as your identity provider type and click **Next**.
5. Give your identity provider a name.
6. Select the metadata provider mode:
   * If using metadata URL mode, set `idpMetadataProvider` to `METADATA_URL` and provide the `idpMetadataUrl` pointing to the IdP's metadata endpoint (for example, `https://gateway.example.com/provider-domain/saml2/idp/metadata`). Metadata URL must match pattern `^https?://.+/saml2/idp/metadata$`.
   * If using metadata file mode, set `idpMetadataProvider` to `METADATA_FILE` and paste the IdP's metadata XML into `idpMetadataFile`. Metadata XML must match pattern `^<[?]?xml|^<[A-Za-z]` (starts with XML declaration or element tag).
   * If using manual mode, configure the settings (EntityID, Sign In URL, Sign Out URL, Signing certificate).
7. Set `graviteeCertificate` to the certificate ID from the prerequisites.
8. Configure `entityId` to match the SAML entity identifier (for example, `saml-idp-provider-domain`).
9. Optionally customize `requestSigningAlgorithm` and `attributeMapping`.
10. Click **Create**.

{% hint style="info" %}
The connector includes some advanced settings such as protocol binding (HTTP-REDIRECT or HTTP-POST), NameId format and Request Signing options to connect to your SAML 2.0 IdP. If you need more information on how to configure these settings, check with your SAML IdP administrator.

Make a note of the URL in **1. Configure the Redirect URI** on the right-hand side of the page. This is the SAML 2.0 Assertion Consumer Service URL you need to provide to the SAML 2.0 IdP to register your Access Management instance.

From AM version 3.7, SAML IdP servers may ask you to share the SAML SP Metadata endpoint to register your AM instance. This endpoint can be found at: `https://AM_GW_HOST/:domain/saml2/sp/metadata/:providerId`.

From SAML IdP plugin v1.4.0, encrypted assertion responses can be handled and decrypted. We decided to only publish KeyDescriptor with use="encryption" if the 'wantAssertionsEncrypted' option is enabled.
{% endhint %}

## Attribute mapping

SAML attribute URIs from IdP assertions are mapped to user profile fields using the `attributeMapping` object. Default mappings include:

* `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress` → `email`
* `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname` → `firstname`
* `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname` → `lastname`

Administrators can override these mappings to align with their IdP's attribute schema.

## Authenticating users

Users authenticate via SAML by initiating login at the client application, which redirects to `/{clientDomain.hrid}/login/callback` with the SAML provider selected.

1. The client generates a signed SAML AuthnRequest using the certificate referenced in `graviteeCertificate` and the algorithm specified in `requestSigningAlgorithm`.
2. The user is redirected to the IdP (provider domain) and authenticates using inline identity provider credentials.
3. The IdP generates a SAML Response with assertions, signing them if `wantAssertionsSigned=true` in the client's service provider configuration.
4. The client validates the SAML Response using the IdP's signing certificate (extracted from metadata or manually configured).
5. User attributes are mapped to profile fields using `attributeMapping`, and an OAuth 2.0 authorization code matching pattern `^[a-zA-Z0-9_-]+$` is issued.
6. The user is redirected to the client application with the authorization code.

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

## Restrictions

* SAML metadata URL must be publicly accessible from the Access Management gateway at configuration time. Firewall rules or network segmentation may prevent metadata retrieval when using `idpMetadataProvider=METADATA_URL`.
* Metadata URL must match pattern `^https?://.+/saml2/idp/metadata$`.
* Metadata XML must match pattern `^<[?]?xml|^<[A-Za-z]` (starts with XML declaration or element tag).
* Certificate synchronization between client application and provider domain is required when using metadata-based configuration.

