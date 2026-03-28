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

SAML IdP configuration in Access Management supports two metadata provisioning methods: fetching metadata from a URL endpoint or uploading an inline XML document. Both methods automatically populate IdP endpoints, certificates, and protocol bindings from the metadata, eliminating manual entry of configuration details.

Metadata for a SAML 2.0 identity provider (IdP) can be provided in one of three ways:

* **Metadata URL**—configuration is supplied by a remote SAML 2.0 metadata XML endpoint. This allows for the dynamic exchange of metadata while reducing the likelihood of configuration errors. Fetching and updating configuration of the IdP occurs at startup of the AM and its plugins.
* **Metadata File**—metadata is imported from an XML file. This is an alternative approach to hosting the metadata where security and versioning can be strictly controlled by static files, without a network dependency on startup.
* **Manual**—metadata values are supplied individually to AM.

{% hint style="info" %}
To connect your applications to a SAML 2.0 IdP manually, you need at least the following information:

* **SingleSignOnService**: the SAML IdP Sign-In URL
* **SingleLogoutService**: the SAML IdP Sign Out URL
* **Signing certificate**: the public signing certificate (encoded in PEM) provided by the identity provider

Before you begin, obtain this information from your SAML IdP administrator and make a note of it for later use.
{% endhint %}

### SAML IdP Metadata Providers

Access Management supports two methods for configuring SAML identity provider metadata:

| Provider Type | Configuration Source | Required Fields |
|:--------------|:---------------------|:----------------|
| `METADATA_URL` | Remote metadata endpoint | `idpMetadataUrl`, `graviteeCertificate` |
| `METADATA_FILE` | Inline XML document | `idpMetadataFile`, `graviteeCertificate` |

**Metadata URL** fetches IdP configuration dynamically from a metadata endpoint at runtime, requiring only the endpoint URL and a certificate for signing authentication requests. **Metadata File** uses an inline XML metadata document uploaded directly into the configuration, suitable for environments where the IdP metadata endpoint is not accessible or when offline configuration is required.

### SAML Certificate Roles

Two certificate types are used in SAML IdP configuration:

* **Gravitee Certificate**: A certificate created in the client domain and used to sign SAML AuthnRequests sent to the IdP. This certificate is required when the IdP metadata specifies `WantAuthnRequestsSigned=true`.
* **Signing Certificate**: The IdP's public certificate in PEM format, used by the client to verify signatures on SAML assertions and responses received from the IdP.

The Gravitee Certificate is stored as a Java KeyStore (JKS) with properties including the Base64-encoded JKS file, keystore password (`storepass`), certificate alias, and private key password (`keypass`).

### SAML Attribute Mapping

User profile attributes are mapped from SAML assertion attributes using URI-based identifiers. The default mapping extracts email, first name, and last name from standard SAML attribute URIs defined in the WS-Federation specification:

| SAML Attribute URI | User Profile Field |
|:-------------------|:-------------------|
| `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress` | `email` |
| `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname` | `firstname` |
| `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname` | `lastname` |

## Prerequisites

Before configuring a SAML IdP, ensure the following:

* Access Management server has network access to the IdP metadata endpoint (when using `METADATA_URL`)
* Certificate created in the client domain for signing AuthnRequests
* IdP metadata XML document or metadata endpoint URL
* IdP signing certificate in PEM format (if not included in metadata)

## Create a SAML 2.0 connector

1. Log in to AM Console.
2. Click **Settings > Providers**.
3. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
4. Select **SAML 2.0** as your identity provider type and click **Next**.
5. Give your identity provider a name.
6. Select **IdP Metadata Provider**:
   1. For **Metadata URL**, enter **Entity ID (SP)** and **Metadata URL** values. If the metadata contains multiple entities, then **Entity ID (IdP)** is also required in order to select the right one.
   2. For **Metadata File**, enter **Entity ID (SP)** and paste the metadata XML in **Metadata File**. If the metadata contains multiple entities, then **Entity ID (IdP)** is also required in order to select the right one.
   3. For **Manual**, configure the required settings: **Entity ID (SP)**, **Sign In URL**, **Sign Out URL**, and **Signing Certificate**.
7. Click **Create**.

{% hint style="info" %}
The connector includes some advanced settings such as protocol binding (`HTTP-REDIRECT` or `HTTP-POST`), **Name ID format** and Request Signing options to connect to your SAML 2.0 IdP. If you need more information on how to configure these settings, check with your SAML IdP administrator.

Make a note of the URL in **1. Configure the Redirect URI** on the right-hand side of the page. This is the SAML 2.0 Assertion Consumer Service URL you need to provide to the SAML 2.0 IdP to register your Access Management instance.

From AM version 3.7, SAML IdP servers may ask you to share the SAML SP Metadata endpoint to register your AM instance. This endpoint can be found at: `https://AM_GW_HOST/:domain/saml2/sp/metadata/:providerId`.

From SAML IdP plugin v1.4.0, encrypted assertion responses can be handled and decrypted. `KeyDescriptor` elements with `use="encryption"` are only published if the **wantAssertionsEncrypted** option is enabled.
{% endhint %}

## Gateway Configuration

### SAML IdP Configuration (Metadata URL)

| Property | Description | Example |
|:---------|:------------|:--------|
| `idpMetadataProvider` | Metadata provisioning method | `METADATA_URL` |
| `entityId` | SAML entity identifier | `saml-idp-${domainSuffix}` |
| `idpMetadataUrl` | URL endpoint for fetching IdP metadata | `${AM_GATEWAY_URL}/${providerDomain.hrid}/saml2/idp/metadata` |
| `graviteeCertificate` | Certificate ID for signing AuthnRequests | `${certificateId}` |
| `requestSigningAlgorithm` | Algorithm for signing SAML AuthnRequests | `http://www.w3.org/2001/04/xmldsig-more#rsa-sha256` |

### SAML IdP Configuration (Metadata File)

| Property | Description | Example |
|:---------|:------------|:--------|
| `idpMetadataProvider` | Metadata provisioning method | `METADATA_FILE` |
| `entityId` | SAML entity identifier | `saml-idp-${domainSuffix}` |
| `idpMetadataFile` | Inline XML metadata document | `<xml>...</xml>` |
| `graviteeCertificate` | Certificate ID for signing AuthnRequests | `${certificateId}` |
| `requestSigningAlgorithm` | Algorithm for signing SAML AuthnRequests | `http://www.w3.org/2001/04/xmldsig-more#rsa-sha256` |

### SAML Protocol Settings

| Property | Description | Example |
|:---------|:------------|:--------|
| `protocolBinding` | SAML protocol binding for SSO | `urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect` |
| `signatureAlgorithm` | Signature algorithm for SAML messages | `RSA_SHA256` |
| `digestAlgorithm` | Digest algorithm for SAML signatures | `SHA256` |
| `nameIDFormat` | SAML NameID format | `urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified` |
| `wantAssertionsSigned` | Whether SAML assertions must be signed | `true` (provider app), `false` (client IdP) |
| `wantResponsesSigned` | Whether SAML responses must be signed | `false` |

### Certificate Configuration (JKS)

| Property | Description | Example |
|:---------|:------------|:--------|
| `jks` | Base64-encoded Java KeyStore file | `<base64-encoded-jks>` |
| `storepass` | KeyStore password | `letmein` |
| `alias` | Certificate alias within KeyStore | `mytestkey` |
| `keypass` | Private key password | `changeme` |

## End-User Configuration

### SAML Provider Application Settings

| Property | Description | Example |
|:---------|:------------|:--------|
| `singleLogoutServiceUrl` | SAML single logout service URL | `${AM_GATEWAY_URL}/${domain.hrid}/logout` |
| `entityId` | SAML entity identifier | `${clientId}` |
| `wantResponseSigned` | Whether SAML responses must be signed | `false` |
| `wantAssertionsSigned` | Whether SAML assertions must be signed | `true` |
| `responseBinding` | SAML response binding method | `HTTP-POST` |
| `certificate` | Service provider certificate in PEM format | `${spCertificatePem}` |

## Restrictions

* SAML metadata URL must be accessible from the Access Management server at configuration time. Network failures prevent IdP configuration.
* SAML metadata file size is not explicitly limited. Extremely large XML documents may cause performance issues.
* `idpMetadataUrl` must match pattern: `^https?:\/\/.+\/saml2\/idp\/metadata$`
* `idpMetadataFile` must contain valid XML starting with `<?xml` or `<[A-Za-z]`
* Metadata XML must contain `IDPSSODescriptor` and `SingleSignOnService` elements

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
