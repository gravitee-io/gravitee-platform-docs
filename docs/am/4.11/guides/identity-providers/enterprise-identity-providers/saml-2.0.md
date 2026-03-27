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

SAML IdP metadata can be supplied through three [IdP Metadata Provider options](#get-your-saml-20-identity-provider-metadata). Metadata URL and metadata file are the recommended approaches, as they automate configuration and reduce errors.

| Provider Type | Property | Description |
|:--------------|:---------|:------------|
| `METADATA_URL` | `idpMetadataUrl` | URL endpoint serving IdP metadata XML (must match pattern `^https?://.+/saml2/idp/metadata$`) — recommended for dynamic configuration |
| `METADATA_FILE` | `idpMetadataFile` | Inline XML document starting with `<?xml` or `<[A-Za-z]` — recommended for static, version-controlled configuration |
| Manual | `signInUrl`, `signOutUrl`, `signingCertificate` | Legacy explicit configuration (no `idpMetadataProvider` property) — deprecated in favor of metadata URL/file |

### Metadata URL configuration (recommended)

When using metadata URL, the system fetches the metadata XML at runtime and extracts the IdP's entity ID, SSO URL, logout URL, and signing certificate automatically. The `idpMetadataUrl` property must reference a URL endpoint serving IdP metadata XML. This method reduces configuration errors and allows for dynamic updates when the IdP's metadata changes.

### Metadata file configuration (recommended)

When using metadata file, the system parses the inline XML and extracts all IdP properties, including `IDPSSODescriptor` and `SingleSignOnService` elements. The `idpMetadataFile` property accepts inline XML content containing the full IdP descriptor. This method is ideal for environments where security and versioning must be strictly controlled by static files, without a network dependency on startup.

{% hint style="info" %}
Metadata URL/file configuration requires SAML 2.0 IdP plugin version `5.0.0-alpha.3` or later.
{% endhint %}

### Manual configuration (deprecated)

To connect your applications to a SAML 2.0 IdP manually, you need at least the following information:

* **SingleSignOnService**: the SAML IdP Sign-In URL
* **SingleLogoutService**: the SAML IdP Sign Out URL
* **Signing certificate**: the public signing certificate (encoded in PEM) provided by the identity provider

{% hint style="info" %}
Before you begin, obtain this information from your SAML IdP administrator and make a note of it for later use. Manual configuration is deprecated — use metadata URL or metadata file instead.
{% endhint %}

## Create a SAML 2.0 connector

### Manual configuration

1. Log in to AM Console.
2. Click **Settings > Providers**.
3. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
4. Select **SAML 2.0** as your identity provider type and click **Next**.
5. Give your identity provider a name.
6. Configure the settings (EntityID, Sign In URL, Sign Out URL, Signing certificate).
7. Click **Create**.

{% hint style="info" %}
The connector includes some advanced settings such as protocol binding (HTTP-REDIRECT or HTTP-POST), NameId format and Request Signing options to connect to your SAML 2.0 IdP. If you need more information on how to configure these settings, check with your SAML 2.0 IdP administrator.

Make a note of the URL in **1. Configure the Redirect URI** on the right-hand side of the page. This is the SAML 2.0 Assertion Consumer Service URL you need to provide to the SAML 2.0 IdP to register your Access Management instance.

From AM version 3.7, SAML IdP servers may ask you to share the SAML SP Metadata endpoint to register your AM instance. This endpoint can be found at: `https://AM_GW_HOST/:domain/saml2/sp/metadata/:providerId`.

From SAML IdP plugin v1.4.0, encrypted assertion responses can be handled and decrypted. We decided to only publish KeyDescriptor with use="encryption" if the 'wantAssertionsEncrypted' option is enabled.
{% endhint %}

### Metadata URL configuration

1. Create a certificate resource in the client domain with type `javakeystore-am-certificate`, providing the JKS content, storepass, alias, and keypass.
2. Create a SAML IdP in the client domain, setting `idpMetadataProvider` to `METADATA_URL` and `idpMetadataUrl` to the provider's metadata endpoint (e.g., `https://am.example.com/provider-domain/saml2/idp/metadata`).
3. Reference the certificate ID in `graviteeCertificate` and specify the `requestSigningAlgorithm` (typically `http://www.w3.org/2001/04/xmldsig-more#rsa-sha256`).
4. Configure attribute mappings to map SAML claims to user profile fields.

### Metadata file configuration

1. Create a certificate resource in the client domain with type `javakeystore-am-certificate`, providing the JKS content, storepass, alias, and keypass.
2. Fetch the IdP metadata XML from the provider's metadata endpoint and copy the full XML content.
3. Create a SAML IdP in the client domain, setting `idpMetadataProvider` to `METADATA_FILE` and pasting the XML content into `idpMetadataFile`.
4. Reference the certificate ID in `graviteeCertificate` and specify the `requestSigningAlgorithm`.
5. Configure attribute mappings as needed.

## Certificate management

When using metadata URL or metadata file, the `graviteeCertificate` property references a certificate resource used to sign SAML AuthnRequests. Certificates must be created with type `javakeystore-am-certificate` and include JKS content (base64-encoded), storepass, alias, and keypass. The certificate's public key is retrieved in PEM format and embedded in the Service Provider configuration. If the IdP metadata specifies `WantAuthnRequestsSigned=true`, the SP must sign all authentication requests using this certificate.

### Certificate properties (Java Keystore)

| Property | Description | Example |
|:---------|:------------|:--------|
| `jks` | Base64-encoded JKS keystore content | `MIIKZgIBAzCCCh8GCSqGSIb3...` |
| `storepass` | Keystore password | `letmein` |
| `alias` | Key alias within the keystore | `mytestkey` |
| `keypass` | Key password | `changeme` |

{% hint style="warning" %}
Certificate synchronization timing: the management API's `SyncManager` polls for certificate events every 5 seconds — the domain start wait period (10-30 seconds) serves as an implicit synchronization point to ensure the certificate provider is loaded before fetching the PEM certificate.
{% endhint %}

## Configure the Service Provider application

When a user initiates login, the client redirects to the IdP, which authenticates the user and returns a signed SAML assertion to the SP's SSO endpoint.

### Service Provider properties

| Property | Description | Example |
|:---------|:------------|:--------|
| `entityId` | SAML entity identifier for the SP (typically client ID) | `my-client-app` |
| `singleSignOnServiceUrl` | SP endpoint for receiving SAML assertions | `https://am.example.com/domain-hrid/login/callback` |
| `singleLogoutServiceUrl` | SP endpoint for logout requests | `https://am.example.com/domain-hrid/logout` |
| `wantResponseSigned` | Whether signed SAML responses are required | `false` |
| `wantAssertionsSigned` | Whether signed SAML assertions are required | `true` |
| `responseBinding` | SAML response binding method | `HTTP-POST` |
| `certificate` | PEM-encoded SP certificate for assertion signing | `-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----` |

## Gateway configuration

### SAML IdP properties (Metadata URL)

| Property | Description | Example |
|:---------|:------------|:--------|
| `idpMetadataProvider` | Set to `METADATA_URL` to enable metadata URL retrieval | `METADATA_URL` |
| `entityId` | SAML entity identifier for the IdP | `saml-idp-example` |
| `idpMetadataUrl` | URL endpoint serving IdP metadata XML | `https://am.example.com/domain-hrid/saml2/idp/metadata` |
| `graviteeCertificate` | Certificate ID for signing AuthnRequests | `cert-id-123` |
| `requestSigningAlgorithm` | Algorithm URI for signing SAML requests | `http://www.w3.org/2001/04/xmldsig-more#rsa-sha256` |
| `attributeMapping` | Map SAML attributes to user profile fields | `{"http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress": "email"}` |

### SAML IdP properties (Metadata File)

| Property | Description | Example |
|:---------|:------------|:--------|
| `idpMetadataProvider` | Set to `METADATA_FILE` to enable inline metadata XML | `METADATA_FILE` |
| `entityId` | SAML entity identifier for the IdP | `saml-idp-example` |
| `idpMetadataFile` | Inline XML metadata content | `<?xml version="1.0"?><EntityDescriptor ...>` |
| `graviteeCertificate` | Certificate ID for signing AuthnRequests | `cert-id-123` |
| `requestSigningAlgorithm` | Algorithm URI for signing SAML requests | `http://www.w3.org/2001/04/xmldsig-more#rsa-sha256` |
| `attributeMapping` | Map SAML attributes to user profile fields | `{"http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress": "email"}` |

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

* Metadata URL must match the pattern `^https?://.+/saml2/idp/metadata$`
* Metadata file must start with `<?xml` or `<[A-Za-z]`
* Metadata XML must contain `IDPSSODescriptor` and `SingleSignOnService` elements
* Metadata URL/file configuration requires SAML 2.0 IdP plugin version `5.0.0-alpha.3` or later
* Validator pre-filling detection relies on internal everit-json-schema behavior — if the library switches to snapshot-based validation, the optimization may silently break with no compile-time signal
