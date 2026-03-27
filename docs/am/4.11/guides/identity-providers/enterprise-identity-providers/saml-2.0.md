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

## SAML metadata provider modes

SAML identity providers can be configured in three modes:

| Mode | Discriminator Value | Key Properties | Use Case |
|:-----|:-------------------|:---------------|:---------|
| Manual | (not set) | `signInUrl`, `singleLogoutServiceUrl`, `signingCertificate` | Full manual control of IdP configuration |
| Metadata URL | `METADATA_URL` | `idpMetadataUrl`, `graviteeCertificate` | IdP exposes public metadata endpoint |
| Metadata File | `METADATA_FILE` | `idpMetadataFile`, `graviteeCertificate` | IdP provides metadata XML offline |

Manual mode requires administrators to specify all IdP endpoints and certificates individually. Metadata URL mode fetches IdP configuration from a remote endpoint, automatically populating SSO URLs and certificates. Metadata File mode accepts inline XML metadata, useful when the IdP does not expose a public metadata endpoint.

### AuthnRequest signing

When using metadata-based configuration (URL or file), the SAML service provider signs authentication requests if the IdP metadata specifies `WantAuthnRequestsSigned=true`. The `graviteeCertificate` property references a certificate ID stored in the Access Management certificate store. The signing algorithm defaults to `http://www.w3.org/2001/04/xmldsig-more#rsa-sha256` and can be overridden via `requestSigningAlgorithm`. Manual mode does not require a certificate unless the IdP explicitly demands signed requests.

#### JSON Schema oneOf Default Injection

The JSON schema validator detects when the underlying `everit-json-schema` library has already injected default values into the target object during `oneOf` validation. If all required properties and `const` constraints of the selected subschema are satisfied, the validator skips manual default injection. This prevents duplicate defaults when the validator mutates the object in-place.

The selection algorithm:

1. First checks for discriminator properties matching `const` values
2. Falls back to the first subschema if no discriminator is present

## Get your SAML 2.0 identity provider (IdP) metadata

To connect your applications to a SAML 2.0 IdP, you need at least the following information:

* **SingleSignOnService**: the SAML IdP Sign-In URL
* **SingleLogoutService**: the SAML IdP Sign Out URL
* **Signing certificate**: the public signing certificate (encoded in PEM) provided by the identity provider

{% hint style="info" %}
Before you begin, obtain this information from your SAML IdP administrator and make a note of it for later use.
{% endhint %}

## Create a SAML 2.0 connector

Configure a SAML identity provider by selecting one of three modes:

1. **Manual mode**: Set `entityId`, `signInUrl`, `singleLogoutServiceUrl`, and `signingCertificate` properties directly in the identity provider configuration.
2. **Metadata URL mode**: Set `idpMetadataProvider` to `METADATA_URL`, provide the `idpMetadataUrl` pointing to the IdP's metadata endpoint, and reference a certificate via `graviteeCertificate` for signing authentication requests.
3. **Metadata file mode**: Set `idpMetadataProvider` to `METADATA_FILE`, paste the full metadata XML into `idpMetadataFile`, and reference a certificate via `graviteeCertificate`.

All modes support the same `attributeMapping` configuration to map SAML attributes to user profile fields.

To create a SAML 2.0 connector:

1. Log in to AM Console.
2. Click **Settings > Providers**.
3. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
4. Select **SAML 2.0** as your identity provider type and click **Next**.
5. Give your identity provider a name.
6. Select **IdP Metadata Provider**:
   * For `METADATA_URL`, enter **Entity ID (SP)** and **Metadata URL** values. If the metadata contains multiple entities, then **Entity ID (IdP)** is also required.
   * For `METADATA_FILE`, enter **Entity ID (SP)** and paste the metadata XML in **Metadata File**. If the metadata contains multiple entities, then **Entity ID (IdP)** is also required.
   * For manual configuration, configure the required settings: **Entity ID (SP)**, **Sign In URL**, and **Signing Certificate**.
7. Click **Create**.

{% hint style="info" %}
The connector includes some advanced settings such as protocol binding (HTTP-REDIRECT or HTTP-POST), NameId format and Request Signing options to connect to your SAML 2.0 IdP. If you need more information on how to configure these settings, check with your SAML 2.0 IdP administrator.

Make a note of the URL in **1. Configure the Redirect URI** on the right-hand side of the page. This is the SAML 2.0 Assertion Consumer Service URL you need to provide to the SAML 2.0 IdP to register your Access Management instance.

From AM version 3.7, SAML IdP servers may ask you to share the SAML SP Metadata endpoint to register your AM instance. This endpoint can be found at: `https://AM_GW_HOST/:domain/saml2/sp/metadata/:providerId`.

From SAML IdP plugin v1.4.0, encrypted assertion responses can be handled and decrypted. We decided to only publish KeyDescriptor with use="encryption" if the 'wantAssertionsEncrypted' option is enabled.
{% endhint %}

{% hint style="info" %}
For metadata URL mode, the metadata URL must point to a public endpoint that returns valid XML containing `IDPSSODescriptor` and `SingleSignOnService` elements.

For metadata file mode, the metadata file must contain valid XML starting with `<?xml` or an element tag.
{% endhint %}

## Gateway configuration

### SAML identity provider (manual mode)

| Property | Description | Example |
|:---------|:------------|:--------|
| `entityId` | SAML entity identifier for the IdP | `saml-idp-example` |
| `signInUrl` | Single Sign-On service endpoint | `https://idp.example.com/sso` |
| `signOutUrl` | Single Logout service endpoint (deprecated) | `https://idp.example.com/logout` |
| `singleLogoutServiceUrl` | Single Logout service endpoint | `https://idp.example.com/logout` |
| `signingCertificate` | X.509 PEM certificate for signature verification | `-----BEGIN CERTIFICATE-----\n...` |
| `wantAssertionsSigned` | Whether IdP requires signed assertions | `false` |
| `wantResponsesSigned` | Whether IdP requires signed responses | `false` |
| `protocolBinding` | SAML protocol binding | `urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect` |
| `signatureAlgorithm` | Signature algorithm for SAML messages | `RSA_SHA256` |
| `digestAlgorithm` | Digest algorithm for SAML signatures | `SHA256` |
| `nameIDFormat` | NameID format | `urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified` |
| `attributeMapping` | Maps SAML attributes to user profile fields | See attribute mapping defaults below |

{% hint style="warning" %}
`signOutUrl` is deprecated. Use `singleLogoutServiceUrl` instead.
{% endhint %}

### SAML identity provider (metadata URL mode)

| Property | Description | Example |
|:---------|:------------|:--------|
| `idpMetadataProvider` | Metadata provider mode | `METADATA_URL` |
| `entityId` | SAML entity identifier for the IdP | `saml-idp-example` |
| `idpMetadataUrl` | URL to fetch IdP metadata XML | `https://idp.example.com/metadata` |
| `graviteeCertificate` | Certificate ID for signing AuthnRequests | `cert-id-123` |
| `requestSigningAlgorithm` | Algorithm for signing AuthnRequests | `http://www.w3.org/2001/04/xmldsig-more#rsa-sha256` |
| `attributeMapping` | Maps SAML attributes to user profile fields | See attribute mapping defaults below |

### SAML identity provider (metadata file mode)

| Property | Description | Example |
|:---------|:------------|:--------|
| `idpMetadataProvider` | Metadata provider mode | `METADATA_FILE` |
| `entityId` | SAML entity identifier for the IdP | `saml-idp-example` |
| `idpMetadataFile` | Full IdP metadata XML document | `<EntityDescriptor>...</EntityDescriptor>` |
| `graviteeCertificate` | Certificate ID for signing AuthnRequests | `cert-id-123` |
| `requestSigningAlgorithm` | Algorithm for signing AuthnRequests | `http://www.w3.org/2001/04/xmldsig-more#rsa-sha256` |
| `attributeMapping` | Maps SAML attributes to user profile fields | See attribute mapping defaults below |

### Attribute mapping defaults

```json
{
  "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress": "email",
  "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname": "firstname",
  "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname": "lastname"
}
```

### Certificate configuration (Java Keystore)

| Property | Description | Example |
|:---------|:------------|:--------|
| `jks` | Base64-encoded Java Keystore file content | (base64 string) |
| `storepass` | Keystore password | `letmein` |
| `alias` | Key alias within the keystore | `mytestkey` |
| `keypass` | Private key password | `changeme` |

{% hint style="warning" %}
Certificate synchronization relies on a 5-second polling interval. The `waitForDomainStart()` completion requirement must be satisfied before calling `fetchCertificatePem()`.
{% endhint %}

## Authenticating with SAML

The client initiates login by redirecting to `/{client-domain-hrid}/oauth/authorize`, where the user selects the SAML identity provider. If using metadata URL mode, the client fetches IdP metadata from `idpMetadataUrl` and parses the `IDPSSODescriptor` and `SingleSignOnService` endpoints. If the IdP metadata specifies `WantAuthnRequestsSigned=true`, the client signs the AuthnRequest using the certificate identified by `graviteeCertificate` and the algorithm specified in `requestSigningAlgorithm`. The user authenticates at the IdP and submits credentials. The IdP signs the SAML assertion (if `wantAssertionsSigned=true`) using the configured signature and digest algorithms. The IdP returns the SAML response via HTTP POST to the client domain callback. The client validates the response signature using `signingCertificate` (manual mode) or the certificate from metadata, extracts attributes using `attributeMapping`, and issues an authorization code.

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
