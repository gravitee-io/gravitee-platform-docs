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

SAML IdP Metadata Configuration enables administrators to configure SAML 2.0 identity providers using metadata URLs or metadata files, simplifying integration with external SAML IdPs. Instead of manually entering individual SAML endpoints and settings, administrators can provide a metadata URL or upload a metadata XML file, and the system automatically extracts the IdP configuration.

## Get your SAML 2.0 IdP metadata

To connect your applications to a SAML 2.0 IdP, you need at least the following information:

* **SingleSignOnService**: the SAML IdP Sign-In URL
* **SingleLogoutService**: the SAML IdP Sign Out URL
* **Signing certificate**: the public signing certificate (encoded in PEM) provided by the identity provider

{% hint style="info" %}
Before you begin, obtain this information from your SAML IdP administrator and make a note of it for later use.
{% endhint %}

### Metadata Provider Modes

SAML IdP configuration supports three mutually exclusive modes:

* **Manual mode**: Requires entering individual SAML endpoints (sign-in URL, sign-out URL, single logout service URL) and settings.
* **Metadata URL mode**: Fetches IdP configuration from a remote metadata endpoint, automatically populating all required SAML settings. Set `idpMetadataProvider` to `"METADATA_URL"`.
* **Metadata File mode**: Accepts a complete IdP metadata XML document uploaded directly, extracting configuration from the XML content. Set `idpMetadataProvider` to `"METADATA_FILE"`.

Each mode requires the same certificate and attribute mapping configuration but differs in how core SAML endpoints are specified.

| Mode | Property | Value Type | Use Case |
|:-----|:---------|:-----------|:---------|
| Manual | N/A | Individual endpoint properties | Legacy configuration or IdPs without metadata support |
| Metadata URL | `idpMetadataProvider` | `"METADATA_URL"` | IdPs exposing a metadata endpoint |
| Metadata File | `idpMetadataProvider` | `"METADATA_FILE"` | IdPs providing downloadable metadata XML |

### SAML Entity and Certificates

The SAML entity identifier (`entityId`) uniquely identifies the IdP in SAML exchanges, typically formatted as `saml-idp-{domainSuffix}`. Certificate configuration varies by domain role:

* **Provider domain (acting as IdP)**: Requires a Java keystore certificate used by the `saml2-idp` plugin to sign SAML assertions.
* **Client domain (acting as SP)**: Requires a certificate for signing AuthnRequests when the IdP metadata specifies `WantAuthnRequestsSigned=true`, referenced via the `graviteeCertificate` property.
* **Service provider applications**: Provide their certificate as a PEM string, which the IdP uses to verify signed AuthnRequests.

### Attribute Mapping

Attribute mapping translates SAML assertion attributes to user profile fields. The system maps standard SAML claim URIs to internal user properties:

* `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress` maps to `email`
* `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname` maps to `firstname`
* `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname` maps to `lastname`

This mapping applies consistently across all metadata provider modes and enables user profile population from SAML assertions.

## Prerequisites

Before configuring SAML IdP metadata, ensure the following requirements are met:

* Provider domain configured and started (for IdP role)
* Client domain configured (for SP role)
* Java keystore certificate created in provider domain (type: `javakeystore-am-certificate`)
* Certificate created in client domain when using metadata URL/file mode with `WantAuthnRequestsSigned=true`
* Valid SAML IdP metadata URL or metadata XML file
* Network connectivity to metadata URL (for metadata URL mode)

## Create a SAML 2.0 connector

1. Log in to AM Console.
2. Click **Settings > Providers**.
3. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
4. Select **SAML 2.0** as your identity provider type and click **Next**.
5. Give your identity provider a name.
6. Select an **IdP Metadata Provider** mode:
   1. For **METADATA\_URL**, enter **Entity ID (SP)** and **Metadata URL** values. If the metadata contains multiple entities, **Entity ID (IdP)** is also required to select the correct one.
   2. For **METADATA\_FILE**, enter **Entity ID (SP)** and paste the metadata XML in **Metadata File**. If the metadata contains multiple entities, **Entity ID (IdP)** is also required to select the correct one.
   3. For **MANUAL**, configure the required settings: **Entity ID (SP)**, **Sign In URL**, and **Signing Certificate**.
7. Click **Create**.

{% hint style="info" %}
The connector includes advanced settings such as protocol binding (`HTTP-REDIRECT` or `HTTP-POST`), NameID format, and Request Signing options to connect to your SAML 2.0 IdP. If you need more information on how to configure these settings, check with your SAML IdP administrator.

Make a note of the URL in **1. Configure the Redirect URI** on the right-hand side of the page. This is the SAML 2.0 Assertion Consumer Service URL you need to provide to the SAML 2.0 IdP to register your Access Management instance.

From AM version 3.7, SAML IdP servers may ask you to share the SAML SP Metadata endpoint to register your AM instance. This endpoint can be found at: `https://AM_GW_HOST/:domain/saml2/sp/metadata/:providerId`.

From SAML IdP plugin v1.4.0, encrypted assertion responses can be handled and decrypted. `KeyDescriptor` elements with `use="encryption"` are only published if the `wantAssertionsEncrypted` option is enabled.
{% endhint %}

## Gateway Configuration

### Metadata URL Mode

To configure a SAML IdP using a metadata URL, create an identity provider of type `saml2-generic-am-idp` in the client domain. Set `idpMetadataProvider` to `"METADATA_URL"` and provide the `idpMetadataUrl` pointing to the IdP's metadata endpoint (for example, `https://gateway.example.com/provider-domain/saml2/idp/metadata`). Specify the `entityId` to uniquely identify the IdP. If the IdP metadata indicates `WantAuthnRequestsSigned=true`, reference a certificate via `graviteeCertificate` and set `requestSigningAlgorithm` to `http://www.w3.org/2001/04/xmldsig-more#rsa-sha256`. Configure `attributeMapping` to map SAML assertion attributes to user profile fields. The system fetches and parses the metadata XML, automatically extracting single sign-on and logout endpoints.

| Property | Description | Example |
|:---------|:------------|:--------|
| `idpMetadataProvider` | Metadata source type | `"METADATA_URL"` |
| `entityId` | SAML entity identifier | `saml-idp-client-domain` |
| `idpMetadataUrl` | URL to fetch IdP metadata from | `https://gateway.example.com/client-domain/saml2/idp/metadata` |
| `graviteeCertificate` | Certificate ID for signing AuthnRequests | Certificate UUID |
| `requestSigningAlgorithm` | Algorithm for signing SAML requests | `http://www.w3.org/2001/04/xmldsig-more#rsa-sha256` |
| `attributeMapping` | Maps SAML attributes to user profile fields | See Attribute Mapping section |

### Metadata File Mode

To configure a SAML IdP using a metadata file, create an identity provider of type `saml2-generic-am-idp` in the client domain. Set `idpMetadataProvider` to `"METADATA_FILE"` and provide the complete IdP metadata XML document in `idpMetadataFile`. Specify the `entityId` to uniquely identify the IdP. If the IdP metadata indicates `WantAuthnRequestsSigned=true`, reference a certificate via `graviteeCertificate` and set `requestSigningAlgorithm` to `http://www.w3.org/2001/04/xmldsig-more#rsa-sha256`. Configure `attributeMapping` to map SAML assertion attributes to user profile fields. The system parses the metadata XML, automatically extracting single sign-on and logout endpoints.

| Property | Description | Example |
|:---------|:------------|:--------|
| `idpMetadataProvider` | Metadata source type | `"METADATA_FILE"` |
| `entityId` | SAML entity identifier | `saml-idp-client-domain` |
| `idpMetadataFile` | Complete IdP metadata XML document | Full XML content |
| `graviteeCertificate` | Certificate ID for signing AuthnRequests | Certificate UUID |
| `requestSigningAlgorithm` | Algorithm for signing SAML requests | `http://www.w3.org/2001/04/xmldsig-more#rsa-sha256` |
| `attributeMapping` | Maps SAML attributes to user profile fields | See Attribute Mapping section |

### Manual Mode

| Property | Description | Example |
|:---------|:------------|:--------|
| `entityId` | SAML entity identifier | `saml-idp-client-domain` |
| `signInUrl` | IdP single sign-on endpoint | `https://gateway.example.com/client-domain/saml2/idp/SSO` |
| `signOutUrl` | IdP logout endpoint | `https://gateway.example.com/client-domain/saml2/idp/logout` |
| `singleLogoutServiceUrl` | IdP single logout service URL | `https://gateway.example.com/client-domain/saml2/idp/logout` |
| `wantAssertionsSigned` | Whether assertions must be signed | `false` |
| `wantResponsesSigned` | Whether responses must be signed | `false` |
| `protocolBinding` | SAML protocol binding | `urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect` |
| `signatureAlgorithm` | Signature algorithm | `RSA_SHA256` |
| `digestAlgorithm` | Digest algorithm | `SHA256` |
| `nameIDFormat` | NameID format | `urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified` |
| `signingCertificate` | PEM certificate for verifying IdP signatures | PEM-encoded X.509 certificate |
| `attributeMapping` | Maps SAML attributes to user profile fields | See Attribute Mapping section |

### Java Keystore Certificate

| Property | Description | Example |
|:---------|:------------|:--------|
| `jks` | Base64-encoded Java keystore containing certificate and private key | Base64 string |
| `storepass` | Keystore password | `letmein` |
| `alias` | Key alias within keystore | `mytestkey` |
| `keypass` | Private key password | `changeme` |

### Service Provider Configuration

| Property | Description | Example |
|:---------|:------------|:--------|
| `wantAssertionsSigned` | Whether SP requires signed assertions | `true` or `false` |
| `certificate` | X.509 PEM certificate of the SP for verifying signed AuthnRequests | PEM-encoded certificate |

## Restrictions

* Metadata provider modes are mutually exclusive — you can't combine manual properties with `METADATA_URL` or `METADATA_FILE`.
* Metadata URL must return HTTP 200 with valid XML containing `IDPSSODescriptor` and `SingleSignOnService` elements.
* Metadata file must be valid XML starting with an XML declaration or element tag, containing `IDPSSODescriptor` and `SingleSignOnService` elements.
* Provider domain must be fully started before fetching certificate PEM — the management API's `SyncManager` polls for certificate events every 5 seconds, requiring a 10–30 second wait for DEPLOY event processing.
* Certificate in the provider domain must be type `javakeystore-am-certificate`.
* Metadata URL must match the pattern `^https?:\/\/.+\/saml2\/idp\/metadata$`.

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

[Learn more about updating the Gateway configuration file.](../../../getting-started/configuration/configure-am-gateway/)
{% endhint %}