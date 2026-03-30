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

SAML 2.0 Identity Provider configuration supports metadata-driven setup via URL endpoints or inline XML files, eliminating manual entry of IdP endpoints and certificates. Administrators configure SAML IdPs by referencing a metadata URL or pasting XML metadata directly, with automatic extraction of SSO endpoints, logout URLs, and signing requirements.

## Get your SAML 2.0 identity provider metadata

Metadata for a SAML 2.0 identity provider (IdP) can be provided in one of three ways:

* **Metadata URL**—configuration is supplied by a remote SAML 2.0 metadata xml endpoint. This allows for the dynamic exchange of metadata while reducing the likelihood of configuration errors. Fetching and updating configuration of the IdP occurs at startup of the AM and its plugins.
* **Metadata File**—metadata is imported from an XML file. This is an alternative approach to hosting the metadata where security and versioning can be strictly controlled by static files, without a network dependency on startup.
* **Manual**—metadata values are supplied individually to AM.

{% hint style="info" %}
To connect your applications to a SAML 2.0 IdP manually, you need at least the following information:

* **SingleSignOnService**: the SAML IdP Sign-In URL
* **Signing certificate**: the public signing certificate (encoded in PEM) provided by the identity provider
{% endhint %}

## Create a SAML 2.0 connector

1. Log in to AM Console.
2. Click **Settings > Providers**.
3. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
4. Select **SAML 2.0** as your identity provider type and click **Next**.
5. Give your identity provider a name.
6. Configure the settings using one of the following methods:
   * **Metadata URL mode**: Set **IdP Metadata Provider** to `METADATA_URL` and enter the IdP's metadata endpoint URL (e.g., `https://gateway.example.com/my-domain/saml2/idp/metadata`). The system fetches IdP metadata and extracts SSO endpoints and signing requirements automatically.
   * **Metadata File mode**: Set **IdP Metadata Provider** to `METADATA_FILE` and paste the XML metadata document into the **IdP Metadata File** field. The system parses the metadata and extracts SSO endpoints and signing requirements automatically.
   * **Manual mode**: Leave **IdP Metadata Provider** empty and configure EntityID, Sign In URL, Sign Out URL, and Signing certificate manually.
7. (Optional) If the IdP requires signed AuthnRequests, select a certificate from the **Certificate for Signing Requests** dropdown. This certificate must exist in the client domain and will be used to sign AuthnRequests.
8. (Optional) Configure **Request Signing Algorithm** (default: `http://www.w3.org/2001/04/xmldsig-more#rsa-sha256`) to control the algorithm used to sign SAML AuthnRequests.
9. (Optional) Configure **Attribute Mapping** to map SAML attribute URIs to user profile fields (e.g., `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress` → `email`).
10. Click **Create**.

{% hint style="info" %}
The connector includes some advanced settings such as protocol binding (HTTP-REDIRECT or HTTP-POST), NameId format and Request Signing options to connect to your SAML 2.0 IdP. If you need more information on how to configure these settings, check with your SAML IdP administrator.

Make a note of the URL in **1. Configure the Redirect URI** on the right-hand side of the page. This is the SAML 2.0 Assertion Consumer Service URL you need to provide to the SAML 2.0 IdP to register your Access Management instance.

From AM version 3.7, SAML IdP servers may ask you to share the SAML SP Metadata endpoint to register your AM instance. This endpoint can be found at: `https://AM_GW_HOST/:domain/saml2/sp/metadata/:providerId`.

From SAML IdP plugin v1.4.0, encrypted assertion responses can be handled and decrypted. We decided to only publish KeyDescriptor with use="encryption" if the 'wantAssertionsEncrypted' option is enabled.
{% endhint %}

{% hint style="warning" %}
Metadata URL mode requires the IdP metadata endpoint to be accessible at configuration time and remain available for periodic refresh. Network failures or endpoint changes will break authentication. Metadata URL must match the pattern `^https?://.+/saml2/idp/metadata$`.

Metadata File mode uses static inline XML metadata. Administrators must manually update the configuration if the IdP's certificates, endpoints, or capabilities change. Metadata File XML must start with `<?xml` or `<` followed by an element name.

Metadata must contain `IDPSSODescriptor` and `SingleSignOnService` elements. Missing elements will cause validation failures.

When IdP metadata specifies `WantAuthnRequestsSigned=true`, a certificate must be configured via **Certificate for Signing Requests**. Failure to provide a valid certificate will result in authentication failures. Certificate must be created in the client domain and the domain must be started before retrieving the certificate in PEM format.
{% endhint %}

## Configuration reference

### SAML IdP metadata provider

| Property | Description | Example |
|:---------|:------------|:--------|
| **IdP Metadata Provider** | Metadata source type: `METADATA_URL`, `METADATA_FILE`, or empty for manual | `METADATA_URL` |
| **IdP Metadata URL** | URL endpoint for fetching IdP metadata (Metadata URL mode) | `https://gateway.example.com/my-domain/saml2/idp/metadata` |
| **IdP Metadata File** | Inline XML metadata content (Metadata File mode) | `<?xml version="1.0"?><EntityDescriptor ...>...</EntityDescriptor>` |
| **Certificate for Signing Requests** | Certificate ID for signing AuthnRequests | `cert-id-123` |
| **Request Signing Algorithm** | Algorithm for signing SAML AuthnRequests | `http://www.w3.org/2001/04/xmldsig-more#rsa-sha256` |

### SAML IdP endpoints (manual mode)

| Property | Description | Example |
|:---------|:------------|:--------|
| **Entity ID** | SAML entity identifier for the IdP | `saml-idp-example` |
| **Sign In URL** | SAML SSO endpoint URL | `https://gateway.example.com/my-domain/saml2/idp/SSO` |
| **Sign Out URL** | SAML logout endpoint URL | `https://gateway.example.com/my-domain/saml2/idp/logout` |
| **Single Logout Service URL** | SAML single logout service URL | `https://gateway.example.com/my-domain/saml2/idp/logout` |
| **Signing Certificate** | X.509 PEM certificate for verifying IdP signatures | `-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----` |

### SAML signature and assertion settings

| Property | Description | Example |
|:---------|:------------|:--------|
| **Want Assertions Signed** | Whether SAML assertions must be signed | `false` |
| **Want Responses Signed** | Whether SAML responses must be signed | `false` |
| **Protocol Binding** | SAML protocol binding | `urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect` |
| **Signature Algorithm** | Signature algorithm for SAML messages | `RSA_SHA256` |
| **Digest Algorithm** | Digest algorithm for SAML signatures | `SHA256` |
| **Name ID Format** | SAML NameID format | `urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified` |

### SAML attribute mapping

SAML assertions contain user attributes identified by URIs (e.g., `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress`). The **Attribute Mapping** configuration maps these URIs to local user profile fields. Standard mappings include `emailaddress` → `email`, `givenname` → `firstname`, and `surname` → `lastname`. Administrators configure mappings as key-value pairs in the IdP configuration form.

| Property | Description | Example |
|:---------|:------------|:--------|
| `attributeMapping` | Maps SAML attribute URIs to user profile fields | `{"http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress": "email"}` |

### Java keystore certificate configuration

| Property | Description | Example |
|:---------|:------------|:--------|
| `jks` | Base64-encoded JKS file content | `MIIKZgIBAzCCCh8GCSqGSIb3...` |
| `storepass` | Keystore password | `letmein` |
| `alias` | Key alias within keystore | `mytestkey` |
| `keypass` | Key password | `changeme` |

### SAML service provider settings

| Property | Description | Example |
|:---------|:------------|:--------|
| **Single Logout Service URL** | Application's single logout endpoint | `https://gateway.example.com/my-domain/logout` |
| **Entity ID** | SAML entity identifier for the application | `client-id-123` |
| `wantResponseSigned` | Whether application requires signed SAML responses | `false` |
| **Want Assertions Signed** | Whether application requires signed SAML assertions | `true` |
| **Response Binding** | SAML response delivery method | `HTTP-POST` |
| `certificate` | X.509 PEM certificate for verifying application's signed requests | `-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----` |

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
