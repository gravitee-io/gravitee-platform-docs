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

SAML 2.0 Identity Provider configuration enables Access Management to authenticate users via external SAML 2.0 identity providers. Administrators can configure SAML IdPs using metadata URLs, inline XML files, or manual endpoint entry.

## Get your SAML 2.0 Identity Provider Metadata

Metadata for a SAML 2.0 identity provider (IdP) can be provided in one of three ways:

* **Metadata URL**—configuration is supplied by a remote SAML 2.0 metadata xml endpoint. This allows for the dynamic exchange of metadata while reducing the likelihood of configuration errors. Fetching and updating configuration of the IdP occurs at startup of the AM and its plugins.
* **Metadata File**—metadata is imported from an XML file. This is an alternative approach to hosting the metadata where security and versioning can be strictly controlled by static files, without a network dependency on startup.
* **Manual**—metadata values are supplied individually to AM.

{% hint style="info" %}
To connect your applications to a SAML 2.0 IdP manually, you need at least the following information:

* **SingleSignOnService**: the SAML IdP Sign-In URL
* **SingleLogoutService**: the SAML IdP Sign Out URL
* **Signing certificate**: the public signing certificate (encoded in PEM) provided by the identity provider

Before you begin, obtain this information from your SAML IdP administrator and make a note of it for later use.
{% endhint %}

### Metadata Provider Options

SAML IdP configuration supports three metadata sources:

| Provider Type | Required Fields | Use Case |
|:-------------|:----------------|:---------|
| `METADATA_URL` | IdP Metadata URL, Gravitee Certificate | IdP metadata endpoint is accessible from gateway |
| `METADATA_FILE` | IdP Metadata File (XML), Gravitee Certificate | Metadata endpoint is not accessible; XML obtained out-of-band |
| Manual | Sign In URL, Sign Out URL, Signing Certificate | Legacy configurations or custom IdP setups |

**Metadata URL** fetches IdP configuration from a remote endpoint (e.g., `${AM_GATEWAY_URL}/${domain.hrid}/saml2/idp/metadata`), automatically populating SSO endpoints and certificates. **Metadata File** accepts inline XML metadata content, useful when the IdP metadata endpoint is not network-accessible. **Manual configuration** preserves legacy behavior, requiring explicit entry of all endpoints and certificates.

### Certificate Requirements

SAML authentication requires certificates for signing and verification. The **Gravitee Certificate** (referenced by ID) signs outbound AuthnRequests when the IdP requires signed requests (`WantAuthnRequestsSigned=true`). The **Signing Certificate** (PEM format) verifies SAML assertions returned by the IdP. The **SP Certificate** (PEM format) is used by the SAML IdP to verify signed AuthnRequests from the service provider.

### Attribute Mapping

SAML assertions contain user attributes identified by URIs. Attribute mapping translates SAML attribute URIs to Access Management user profile fields. Standard mappings include `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress` → `email`, `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname` → `firstname`, and `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname` → `lastname`.

## Prerequisites

Before configuring a SAML 2.0 identity provider, ensure the following:

* Access Management gateway deployed and accessible
* SAML 2.0 identity provider with metadata endpoint or XML metadata file
* Network connectivity from gateway to IdP metadata URL (for `METADATA_URL` provider)
* IdP signing certificate in PEM format (for manual configurations)

## Create a SAML 2.0 connector

1. Log in to AM Console.
2. Click **Settings > Providers**.
3. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
4. Select **SAML 2.0** as your identity provider type and click **Next**.
5. Give your identity provider a name.
6. Choose **Metadata Provider** type:
   * For `METADATA_URL`, enter the IdP metadata endpoint URL (e.g., `https://idp.example.com/saml2/idp/metadata`) and select a Gravitee Certificate from the dropdown.
   * For `METADATA_FILE`, paste the XML metadata content into the text area and select a Gravitee Certificate.
   * For manual configuration, configure the settings (EntityID, Sign In URL, Sign Out URL, Signing certificate).
7. Set the **Request Signing Algorithm** (default: `http://www.w3.org/2001/04/xmldsig-more#rsa-sha256`).
8. Configure attribute mappings to map SAML assertion attributes to user profile fields.
9. Click **Create**.

{% hint style="info" %}
The connector includes some advanced settings such as protocol binding (HTTP-REDIRECT or HTTP-POST), NameId format and Request Signing options to connect to your SAML 2.0 IdP. If you need more information on how to configure these settings, check with your SAML IdP administrator.

Make a note of the URL in **1. Configure the Redirect URI** on the right-hand side of the page. This is the SAML 2.0 Assertion Consumer Service URL you need to provide to the SAML 2.0 IdP to register your Access Management instance.

From AM version 3.7, SAML IdP servers may ask you to share the SAML SP Metadata endpoint to register your AM instance. This endpoint can be found at: `https://AM_GW_HOST/:domain/saml2/sp/metadata/:providerId`.

From SAML IdP plugin v1.4.0, encrypted assertion responses can be handled and decrypted. We decided to only publish KeyDescriptor with use="encryption" if the 'wantAssertionsEncrypted' option is enabled.
{% endhint %}

## Configuration Reference

### SAML IdP Metadata Configuration

| Property | Description | Example |
|:---------|:------------|:--------|
| **IdP Metadata Provider** | Metadata source: `METADATA_URL`, `METADATA_FILE`, or manual | `METADATA_URL` |
| **IdP Metadata URL** | URL endpoint for fetching IdP metadata XML | `${AM_GATEWAY_URL}/${domain.hrid}/saml2/idp/metadata` |
| **IdP Metadata File** | Inline XML content of IdP metadata document | `<EntityDescriptor ...>` |
| **Gravitee Certificate** | Certificate ID for signing SAML AuthnRequests | `cert-12345` |
| **Request Signing Algorithm** | Algorithm URI for signing SAML requests | `http://www.w3.org/2001/04/xmldsig-more#rsa-sha256` |

### Manual SAML IdP Configuration

| Property | Description | Example |
|:---------|:------------|:--------|
| **Entity ID** | SAML entity identifier for the identity provider | `saml-idp-${domainSuffix}` |
| **Sign In URL** | SAML SSO endpoint URL | `${AM_GATEWAY_URL}/${providerDomain.hrid}/saml2/idp/SSO` |
| **Sign Out URL** | SAML logout endpoint URL | `${AM_GATEWAY_URL}/${providerDomain.hrid}/saml2/idp/logout` |
| **Single Logout Service URL** | SAML single logout service URL | `${AM_GATEWAY_URL}/${providerDomain.hrid}/saml2/idp/logout` |
| **Want Assertions Signed** | Whether SAML assertions must be signed | `false` |
| **Want Responses Signed** | Whether SAML responses must be signed | `false` |
| **Protocol Binding** | SAML protocol binding | `urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect` |
| **Signature Algorithm** | Signature algorithm for SAML messages | `RSA_SHA256` |
| **Digest Algorithm** | Digest algorithm for SAML signatures | `SHA256` |
| **NameID Format** | SAML NameID format | `urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified` |
| **Signing Certificate** | X.509 PEM certificate for verifying IdP signatures | `-----BEGIN CERTIFICATE-----...` |

### SAML Service Provider Configuration

Configure SAML service provider settings for client applications:

| Property | Description | Example |
|:---------|:------------|:--------|
| **Single Sign-On Service URL** | Callback URL for SAML assertions | `${AM_GATEWAY_URL}/${domain.hrid}/login/callback` |
| **Single Logout Service URL** | Logout callback URL | `${AM_GATEWAY_URL}/${domain.hrid}/logout` |
| **Entity ID** | SAML entity identifier for the service provider | `${clientId}` |
| **Want Response Signed** | Whether SAML responses must be signed | `false` |
| **Want Assertions Signed** | Whether SAML assertions must be signed | `true` |
| **Response Binding** | SAML response binding method | `HTTP-POST` |
| **Certificate** | X.509 PEM certificate of the SP; used by saml2-idp to verify signed AuthnRequests | `-----BEGIN CERTIFICATE-----...` |

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

* SAML signing certificates for `graviteeCertificate` must be in Java KeyStore (JKS) format
* IdP signing certificates for `signingCertificate` must be in PEM format
* SP certificates for the `certificate` field in application configuration must be in PEM format
* The `idpMetadataUrl` must be accessible from the Access Management gateway at runtime; firewall rules must allow outbound HTTPS connections to the IdP metadata endpoint
* Metadata URL responses must contain `IDPSSODescriptor` and `SingleSignOnService` elements with valid XML structure
* Metadata file content must contain `IDPSSODescriptor` and `SingleSignOnService` elements with valid XML structure

## Related Changes

The SAML 2.0 identity provider plugin (`gravitee-am-idp-saml2`) has been upgraded from version 4.0.3 to 5.0.0-alpha.3, introducing metadata-based configuration support. The plugin validation framework (`gravitee-plugin-validator`) has been updated from 2.0.2 to 2.3.0. Existing manual SAML IdP configurations continue to function without modification.
