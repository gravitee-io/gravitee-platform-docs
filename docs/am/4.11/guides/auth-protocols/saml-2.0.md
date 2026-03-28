# SAML 2.0

## Overview

[The Security Assertion Markup Language (SAML)](http://docs.oasis-open.org/security/saml/Post2.0/sstc-saml-tech-overview-2.0.html) standard defines an XML-based framework for describing and exchanging security information between online business partners.

Gravitee Access Management (AM) supports the SAML protocol and can serve both as Identity Provider (IdP) and Service Provider (SP):

* [Configure AM as SAML Identity Provider](saml-2.0.md#enable-saml-2.0-identity-provider-support)
* [Configure AM as SAML Service Provider](../identity-providers/enterprise-identity-providers/saml-2.0.md)

## Participants

At a minimum, SAML exchanges take place between system entities referred to as a SAML asserting party and a SAML relying party. In many SAML use cases, a user, perhaps running a web browser or executing a SAML-enabled application, is also a participant, and may even be the asserting party.

**Service provider (SP)**

A relying party that uses assertions it has received from the Identity Provider (IdP) to grant the principal access to local resources.

**Identity provider (IdP)**

An entity that authenticates users and provides to service providers (SP) an authentication assertion that indicates a principal has been authenticated.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-devguide-protocols-saml-overview.png" alt=""><figcaption><p>SAML diagram</p></figcaption></figure>

## Enable SAML 2.0 Identity Provider support

Currently, AM supports the following SAML bindings:

* HTTP-Redirect
* HTTP-POST

and the following options:

* Web Browser SSO Profile
* Single Logout Profile
* SP-Initiated flow
* Support for signed SAML assertions (SAML Request and SAML Response)

{% hint style="info" %}
Support for encrypted SAML assertions will be provided in a future version of the SAML 2.0 IdP protocol plugin.
{% endhint %}

### Activate SAML 2.0 IdP

{% hint style="info" %}
Be sure to have your SAML 2.0 IdP protocol plugin and your license key installed in your environment before configuring the connection.
{% endhint %}

1. Log in to AM Console.
2. Click **Settings > SAML 2.0**.
3. Enable **SAML 2.0 IdP support**.
4. Enter your IdP Entity ID.
5. Select your certificate to sign the SAML Response assertion.
6. Click **Save**.

{% hint style="info" %}
If you choose to not use a certificate, the SAML Response assertion will not be signed.
{% endhint %}

{% hint style="warning" %}
SAML cannot currently be configured at the Organization level.
{% endhint %}

### Test the connection

To connect your applications to the AM SAML 2.0 IdP, you need at least the following information:

* **SingleSignOnService**, the SAML IdP Sign In URL: `https://AM_GATEWAY/{domain}/saml2/idp/SSO`
* **SingleLogoutService**, the SAML IdP Sign Out URL: `https://AM_GATEWAY/{domain}/saml2/idp/logout`
* **Signing certificate**, the public signing certificate (encoded in PEM)

{% hint style="info" %}
SAML IdP metadata information can be found here: `https://AM_GATEWAY/{domain}/saml2/idp/metadata`
{% endhint %}

You can test your SAML 2.0 connection using a web application created in AM.

1. In AM Console, create a new web application.
2. Click **Settings > SAML 2.0**.
3. Verify/update the SAML 2.0 application settings.
4. Select an identity provider to connect your users.
5. Call the Login page (the /saml/idp/SSO?SAMLRequest=…​ endpoint).
6. Enter username/password and click **Sign in**.
7. If everything is OK, your user will be redirected to the application **attribute consume service URL** with the SAML Response assertion as a parameter.

{% hint style="info" %}
SAML 2.0 IdP protocol is compatible out of the box with all the existing features of AM just like the OAuth 2.0/OpenID Connect protocol, such as passwordless, MFA, social login, etc.
{% endhint %}

## SAML Identity Provider Configuration

SAML Identity Provider configuration supports automated metadata retrieval via URL or inline XML file, eliminating manual entry of IdP endpoints and certificates. Administrators can configure SAML IdPs by referencing a metadata endpoint or uploading metadata XML directly.

### Metadata Provider Types

SAML IdP metadata can be supplied through three methods: manual configuration (legacy), metadata URL, or metadata file. Manual configuration requires explicit entry of all IdP endpoints, certificates, and protocol bindings. Metadata URL retrieves IdP configuration from an HTTP(S) endpoint serving SAML metadata XML. Metadata file accepts inline XML content containing the IdP's SAML metadata descriptor.

| Provider Type | Property | Description |
|:--------------|:---------|:------------|
| Manual | N/A | Legacy method requiring explicit endpoint and certificate configuration |
| Metadata URL | `idpMetadataUrl` | HTTP(S) endpoint serving IdP metadata XML (e.g., `https://.../saml2/idp/metadata`) |
| Metadata File | `idpMetadataFile` | Inline XML document containing IdP metadata descriptor |

### Certificate References

When using metadata URL or metadata file providers, the `graviteeCertificate` property references a certificate ID used to sign SAML AuthnRequests. The certificate must be pre-configured in the domain's certificate store using Java Keystore format. The IdP's signing certificate is extracted from the metadata XML and used to validate SAML assertions and responses.

### Attribute Mapping

SAML attributes returned in assertions are mapped to user profile fields using the `attributeMapping` configuration object. Keys are SAML attribute URNs (e.g., `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress`) and values are target user profile field names (e.g., `email`, `firstname`, `lastname`). Mappings apply regardless of metadata provider type.

### Prerequisites

* Access Management domain with SAML 2.0 IdP plugin installed (`gravitee-am-idp-saml2` version 5.0.0-alpha.3 or later)
* Valid certificate configured in domain certificate store (Java Keystore format) when using metadata URL or metadata file providers
* IdP metadata endpoint accessible via HTTP(S) when using metadata URL provider
* IdP metadata XML containing `IDPSSODescriptor` and `SingleSignOnService` elements

### Gateway Configuration

#### SAML IdP Metadata Provider

| Property | Description | Example |
|:---------|:------------|:--------|
| `idpMetadataProvider` | Metadata source type: `METADATA_URL` or `METADATA_FILE` | `METADATA_URL` |
| `idpMetadataUrl` | HTTP(S) endpoint serving IdP metadata XML (required when provider is `METADATA_URL`) | `https://am.example.com/domain-hrid/saml2/idp/metadata` |
| `idpMetadataFile` | Inline XML metadata content (required when provider is `METADATA_FILE`) | `<?xml version="1.0"?><EntityDescriptor...` |
| `graviteeCertificate` | Certificate ID for signing AuthnRequests (required for metadata URL/file providers) | `cert-abc123` |
| `requestSigningAlgorithm` | Algorithm URI for signing SAML AuthnRequests | `http://www.w3.org/2001/04/xmldsig-more#rsa-sha256` |
| `entityId` | SAML entity identifier for the IdP | `saml-idp-production` |

#### SAML Protocol Bindings

| Property | Description | Example |
|:---------|:------------|:--------|
| `protocolBinding` | SAML protocol binding for authentication requests | `urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect` |
| `responseBinding` | SAML response binding method | `HTTP-POST` |
| `nameIDFormat` | SAML NameID format URN | `urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified` |

#### Signature Configuration

| Property | Description | Example |
|:---------|:------------|:--------|
| `wantAssertionsSigned` | Require signed SAML assertions (typically `true` for SP applications, `false` for client IdPs) | `true` |
| `wantResponsesSigned` | Require signed SAML responses | `false` |
| `signatureAlgorithm` | Signature algorithm for SAML messages | `RSA_SHA256` |
| `digestAlgorithm` | Digest algorithm for SAML signatures | `SHA256` |

#### Certificate Store (Java Keystore)

| Property | Description | Example |
|:---------|:------------|:--------|
| `jks` | Base64-encoded Java Keystore content | `MIIKZgIBAzCCCh8GCSqGSIb3...` |
| `storepass` | Keystore password | `letmein` |
| `alias` | Certificate alias within keystore | `mytestkey` |
| `keypass` | Private key password | `changeme` |

### Creating a SAML Identity Provider

1. Choose `METADATA_URL` to fetch metadata from an HTTP(S) endpoint, or `METADATA_FILE` to provide inline XML.
2. Set `entityId` to the IdP's SAML entity identifier.
3. For metadata URL, specify `idpMetadataUrl` pointing to the IdP's metadata endpoint; for metadata file, paste the XML content into `idpMetadataFile`.
4. Reference a pre-configured certificate via `graviteeCertificate` for signing AuthnRequests.
5. Configure `attributeMapping` to map SAML attributes to user profile fields.

The domain's SyncManager polls for certificate events every 5 seconds; allow 10-30 seconds for certificate loading before testing authentication flows.

### Configuring Service Provider Applications

1. Set `entityId` to the application's client ID.
2. Specify `singleSignOnServiceUrl` and `singleLogoutServiceUrl` using the domain's gateway URL and HRID (e.g., `{AM_GATEWAY_URL}/{domain-hrid}/saml2/sp/SSO`).
3. Enable `wantAssertionsSigned` if the application requires signed assertions from the IdP.
4. Set `responseBinding` to `HTTP-POST` or the binding method expected by the application.
5. Provide the application's public certificate in PEM format via the `certificate` property for validating signed requests.

### Restrictions

* Metadata URL endpoint must be accessible at configuration time; temporary IdP unavailability causes configuration failures
* Inline metadata file XML is stored as a JSON string and may exceed database column limits for very large metadata documents
* When IdP metadata specifies `WantAuthnRequestsSigned=true`, the client domain must have a valid certificate configured via `graviteeCertificate`; missing or invalid certificates cause authentication failures
* Metadata XML validation checks for `IDPSSODescriptor` and `SingleSignOnService` elements but does not perform full XML schema validation against SAML metadata XSD
* Metadata URL must match pattern `^https?://.+/saml2/idp/metadata$`
* Metadata file XML must match pattern `^<[?]?xml|^<[A-Za-z]`

### Related Changes

The SAML 2.0 IdP plugin (`gravitee-am-idp-saml2`) has been upgraded from version 4.0.3 to 5.0.0-alpha.3 to support metadata URL and metadata file providers. Legacy manual configuration remains supported for backward compatibility. JSON schema validation for `oneOf` constructs now detects when default values have been pre-filled by the validator, improving efficiency and reducing redundant processing.
