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


## Get your SAML 2.0 identity provider metadata

To connect your applications to a SAML 2.0 IdP, you need at least the following information:

* **SingleSignOnService**: the SAML IdP Sign-In URL
* **SingleLogoutService**: the SAML IdP Sign Out URL
* **Signing certificate**: the public signing certificate (encoded in PEM) provided by the identity provider

{% hint style="info" %}
Before you begin, obtain this information from your SAML IdP administrator and make a note of it for later use.
{% endhint %}

### Metadata Provider Options

Administrators select how SAML IdP metadata is supplied using the **IdP Metadata Provider** field. Three options are available:

| Provider Type | Required Configuration | Use Case |
|:-------------|:----------------------|:---------|
| `METADATA_URL` | IdP Metadata URL, Gravitee Certificate | Fetch metadata from a live endpoint |
| `METADATA_FILE` | IdP Metadata File (XML), Gravitee Certificate | Upload inline XML metadata content |
| Manual | Sign-In URL, Sign-Out URL, Single Logout Service URL, Signing Certificate | Configure all endpoints individually |

When using `METADATA_URL` or `METADATA_FILE`, the system parses the XML to extract `IDPSSODescriptor` and `SingleSignOnService` endpoints automatically. Manual configuration requires explicit entry of all SAML endpoints and certificates.

### Certificate Configuration

SAML authentication requires certificates for signing and verification. The **Gravitee Certificate** field references a certificate stored in the client domain, used to sign AuthnRequests when the IdP requires signed requests (`WantAuthnRequestsSigned=true`). Certificates are stored as Java KeyStore (JKS) files with the following properties:

| Property | Description | Example |
|:---------|:------------|:--------|
| Type | Certificate type | `javakeystore-am-certificate` |
| JKS | Base64-encoded KeyStore file | (binary content) |
| Storepass | KeyStore password | `letmein` |
| Alias | Key alias within the KeyStore | `mytestkey` |
| Keypass | Key password | `changeme` |

The **Signing Certificate** field (manual configuration only) accepts a PEM-encoded X.509 certificate used to verify IdP signatures on SAML assertions.

### Attribute Mapping

SAML attributes from the IdP are mapped to user profile fields using standard claim URIs:

| SAML Attribute URI | Mapped Field |
|:------------------|:-------------|
| `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress` | `email` |
| `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname` | `firstname` |
| `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname` | `lastname` |

## Create a SAML 2.0 connector

1. Log in to AM Console.
2. Click **Settings > Providers**.
3. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
4. Select **SAML 2.0** as your identity provider type and click **Next**.
5. Give your identity provider a name.
6. Select how to provide IdP metadata using the **IdP Metadata Provider** field:
   * **METADATA_URL**: Enter the metadata endpoint URL in **IdP Metadata URL** and select a certificate from **Gravitee Certificate** to sign AuthnRequests.
   * **METADATA_FILE**: Paste the XML metadata content into **IdP Metadata File** and select a certificate from **Gravitee Certificate** to sign AuthnRequests.
   * **Manual**: Configure the settings (EntityID, Sign In URL, Sign Out URL, Single Logout Service URL, Signing certificate).
7. Configure **Request Signing Algorithm** (default: `http://www.w3.org/2001/04/xmldsig-more#rsa-sha256`).
8. Map SAML attributes to user profile fields in the attribute mapping section.
9. Click **Create**.

{% hint style="info" %}
The connector includes some advanced settings such as protocol binding (HTTP-REDIRECT or HTTP-POST), NameId format and Request Signing options to connect to your SAML 2.0 IdP. If you need more information on how to configure these settings, check with your SAML IdP administrator.

Make a note of the URL in **1. Configure the Redirect URI** on the right-hand side of the page. This is the SAML 2.0 Assertion Consumer Service URL you need to provide to the SAML 2.0 IdP to register your Access Management instance.

From AM version 3.7, SAML IdP servers may ask you to share the SAML SP Metadata endpoint to register your AM instance. This endpoint can be found at: `https://AM_GW_HOST/:domain/saml2/sp/metadata/:providerId`.

From SAML IdP plugin v1.4.0, encrypted assertion responses can be handled and decrypted. We decided to only publish KeyDescriptor with use="encryption" if the 'wantAssertionsEncrypted' option is enabled.
{% endhint %}

{% hint style="warning" %}
When using `idpMetadataProvider=METADATA_URL`, the IdP metadata endpoint must be accessible at configuration time and return valid XML containing `IDPSSODescriptor` and `SingleSignOnService` elements.

When IdP metadata specifies `WantAuthnRequestsSigned=true`, a certificate must be configured in the client domain via **Gravitee Certificate**.

`gravitee-am-idp-saml2` version `5.0.0-alpha.3` is a pre-release version and may contain instability.
{% endhint %}

## Configuring SAML Service Provider Applications

To configure a SAML service provider application:

1. Create or edit an application in the domain and set the application type to SAML.
2. Enter the **Single Sign-On Service URL**.
3. Enter the **Single Logout Service URL**.
4. Set the **Entity ID** to the client ID.
5. Configure signature requirements: set **Want Response Signed** to `false` and **Want Assertion Signed** to `true` (or as required by the IdP).
6. Set **Response Binding** to `HTTP-POST`.
7. Paste the SP certificate (PEM format) into the **Certificate** field.

The IdP uses this certificate to verify signed AuthnRequests from the SP.

## Configuration Reference

| Property | Description | Example |
|:---------|:------------|:--------|
| **IdP Metadata Provider** | How SAML IdP metadata is provided | `METADATA_URL`, `METADATA_FILE`, or manual |
| **IdP Metadata URL** | URL endpoint for fetching IdP metadata | `${AM_GATEWAY_URL}/${domain.hrid}/saml2/idp/metadata` |
| **IdP Metadata File** | Inline XML metadata content | (XML document) |
| **Gravitee Certificate** | Certificate ID for signing AuthnRequests | (certificate reference) |
| **Request Signing Algorithm** | Algorithm used to sign SAML AuthnRequests | `http://www.w3.org/2001/04/xmldsig-more#rsa-sha256` |
| **Entity ID** | SAML entity identifier for the IdP | `saml-idp-example` |
| **Sign-In URL** | SAML SSO endpoint URL (manual config) | `${AM_GATEWAY_URL}/${domain.hrid}/saml2/idp/SSO` |
| **Sign-Out URL** | SAML logout endpoint URL (manual config) | `${AM_GATEWAY_URL}/${domain.hrid}/saml2/idp/logout` |
| **Single Logout Service URL** | SAML single logout service URL (manual config) | `${AM_GATEWAY_URL}/${domain.hrid}/saml2/idp/logout` |
| **Want Assertions Signed** | Whether SAML assertions must be signed | `false` |
| **Want Responses Signed** | Whether SAML responses must be signed | `false` |
| **Protocol Binding** | SAML protocol binding | `urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect` |
| **Signature Algorithm** | Signature algorithm for SAML messages | `RSA_SHA256` |
| **Digest Algorithm** | Digest algorithm for SAML signatures | `SHA256` |
| **NameID Format** | SAML NameID format | `urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified` |
| **Signing Certificate** | Certificate used to verify IdP signatures (manual config) | (PEM-encoded X.509 certificate) |
| **Certificate** | SP certificate used by IdP to verify signed AuthnRequests | (PEM-encoded X.509 certificate) |
| **Response Binding** | SAML response binding method | `HTTP-POST` |

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
