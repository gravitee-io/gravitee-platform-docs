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

Metadata for a SAML 2.0 identity provider (IdP) can be provided in one of three ways:

* **Metadata URL**: configuration is supplied by a remote SAML 2.0 metadata XML endpoint. This allows for the dynamic exchange of metadata while reducing the likelihood of configuration errors. Fetching and updating configuration of the IdP occurs at startup of AM and its plugins.
* **Metadata File**: metadata is imported from an XML file. This is an alternative approach to hosting the metadata where security and versioning can be strictly controlled by static files, without a network dependency on startup.
* **Manual**: metadata values are supplied individually to AM.

### Metadata Provider Types

The `idpMetadataProvider` property determines how SAML IdP metadata is supplied to the client domain. Two provider types are supported:

| Provider Type | Configuration Source | Use Case |
|:--------------|:---------------------|:---------|
| `METADATA_URL` | Remote HTTP(S) endpoint | Dynamic IdP metadata served by provider domain |
| `METADATA_FILE` | Inline XML document | Static metadata copied from IdP |

`METADATA_URL` fetches metadata from a remote endpoint at runtime, while `METADATA_FILE` parses inline XML content provided during configuration. Both methods automatically extract IdP endpoints, signing certificates, and protocol bindings from the metadata document.

### Certificate Requirements

When IdP metadata sets `WantAuthnRequestsSigned=true`, the client domain must configure a `graviteeCertificate` to sign outbound SAML AuthnRequests. This certificate must be created in the client domain with type `javakeystore-am-certificate` before configuring the SAML IdP. The provider domain's signing certificate is automatically extracted from the metadata and used to verify inbound SAML assertions.

### Metadata Endpoint

The IdP metadata endpoint `/{domain.hrid}/saml2/idp/metadata` serves an XML document containing the `IDPSSODescriptor` element, `SingleSignOnService` endpoint, and domain HRID reference. This endpoint is used by client domains when configuring `idpMetadataProvider=METADATA_URL`.

{% hint style="info" %}
To connect your applications to a SAML 2.0 IdP manually, you need at least the following information:

* **SingleSignOnService**: the SAML IdP Sign-In URL
* **Signing certificate**: the public signing certificate (encoded in PEM) provided by the identity provider
{% endhint %}

## Prerequisites

Before configuring SAML IdP metadata, ensure the following:

* Access Management gateway deployed and accessible
* Provider domain configured with SAML 2.0 IdP capabilities
* Client domain created for SAML service provider configuration
* Certificate created in client domain (type `javakeystore-am-certificate`) if IdP requires signed AuthnRequests
* Network connectivity from client domain to provider domain metadata endpoint (for `METADATA_URL` provider type)

## Create a SAML 2.0 connector

1. Log in to AM Console.
2. Click **Settings > Providers**.
3. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
4. Select **SAML 2.0** as your identity provider type and click **Next**.
5. Give your identity provider a name.
6. Select **IdP Metadata Provider**:
   1. For **METADATA\_URL**, enter **Entity ID (SP)** and **Metadata URL** values. If the metadata contains multiple entities, then **Entity ID (IdP)** is also required in order to select the right one.
   2. For **METADATA\_FILE**, enter **Entity ID (SP)** and paste the metadata XML in **Metadata File**. If the metadata contains multiple entities, then **Entity ID (IdP)** is also required in order to select the right one.
   3. For **MANUAL**, configure the required settings: **Entity ID (SP)**, **Sign In URL**, **Sign Out URL** and **Signing Certificate**.
7. Click **Create**.

{% hint style="info" %}
The connector includes some advanced settings such as protocol binding (`HTTP-REDIRECT` or `HTTP-POST`), **Name ID format** and Request Signing options to connect to your SAML 2.0 IdP. If you need more information on how to configure these settings, check with your SAML IdP administrator.

Make a note of the URL in **1. Configure the Redirect URI** on the right-hand side of the page. This is the SAML 2.0 Assertion Consumer Service URL you need to provide to the SAML 2.0 IdP to register your Access Management instance.

From AM version 3.7, SAML IdP servers may ask you to share the SAML SP Metadata endpoint to register your AM instance. This endpoint can be found at: `https://AM_GW_HOST/:domain/saml2/sp/metadata/:providerId`.

From SAML IdP plugin v1.4.0, encrypted assertion responses can be handled and decrypted. `KeyDescriptor` elements with `use="encryption"` are only published if the **wantAssertionsEncrypted** option is enabled.
{% endhint %}

## Configuration properties

### SAML IdP Properties (Metadata URL)

| Property | Description | Example |
|:---------|:------------|:--------|
| `idpMetadataProvider` | Metadata source type | `METADATA_URL` |
| `entityId` | SAML entity identifier for the IdP | `saml-idp-{suffix}` |
| `idpMetadataUrl` | URL endpoint serving IdP metadata XML | `https://{AM_GATEWAY_URL}/{providerDomain.hrid}/saml2/idp/metadata` |
| `graviteeCertificate` | Certificate ID for signing AuthnRequests | `{certificate-id}` |
| `requestSigningAlgorithm` | Algorithm used to sign SAML AuthnRequests | `http://www.w3.org/2001/04/xmldsig-more#rsa-sha256` |
| `attributeMapping` | Mapping of SAML attributes to user profile fields | `{"http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress": "email"}` |

### SAML IdP Properties (Metadata File)

| Property | Description | Example |
|:---------|:------------|:--------|
| `idpMetadataProvider` | Metadata source type | `METADATA_FILE` |
| `entityId` | SAML entity identifier for the IdP | `saml-idp-{suffix}` |
| `idpMetadataFile` | Inline IdP metadata XML content | `<?xml version="1.0"?><EntityDescriptor...>` |
| `graviteeCertificate` | Certificate ID for signing AuthnRequests | `{certificate-id}` |
| `requestSigningAlgorithm` | Algorithm used to sign SAML AuthnRequests | `http://www.w3.org/2001/04/xmldsig-more#rsa-sha256` |
| `attributeMapping` | Mapping of SAML attributes to user profile fields | `{"http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress": "email"}` |

### SAML Provider Application Properties

| Property | Description | Example |
|:---------|:------------|:--------|
| `singleSignOnServiceUrl` | SP SSO endpoint | `{AM_GATEWAY_URL}/{domain.hrid}/saml2/sp/SSO` |
| `singleLogoutServiceUrl` | SP logout endpoint | `{AM_GATEWAY_URL}/{domain.hrid}/logout` |
| `entityId` | SAML entity identifier for the SP | `{clientId}` |
| `wantResponseSigned` | Whether SAML responses must be signed | `false` |
| `wantAssertionsSigned` | Whether SAML assertions must be signed | `true` |
| `responseBinding` | SAML response binding method | `HTTP-POST` |
| `certificate` | SP certificate used to verify signed AuthnRequests | `{PEM certificate}` |

### Manual SAML IdP Configuration

Administrators can continue to manually configure SAML IdP properties without using metadata. This approach requires explicit configuration of all endpoints and certificates.

| Property | Description | Example |
|:---------|:------------|:--------|
| `entityId` | SAML entity identifier for the IdP | `saml-idp-{suffix}` |
| `signInUrl` | IdP SSO endpoint | `{AM_GATEWAY_URL}/{providerDomain.hrid}/saml2/idp/SSO` |
| `signOutUrl` | IdP logout endpoint | `{AM_GATEWAY_URL}/{providerDomain.hrid}/saml2/idp/logout` |
| `singleLogoutServiceUrl` | IdP single logout service endpoint | `{AM_GATEWAY_URL}/{providerDomain.hrid}/saml2/idp/logout` |
| `wantAssertionsSigned` | Whether SAML assertions must be signed | `false` |
| `wantResponsesSigned` | Whether SAML responses must be signed | `false` |
| `protocolBinding` | SAML protocol binding for authentication requests | `urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect` |
| `signatureAlgorithm` | Signature algorithm for SAML assertions | `RSA_SHA256` |
| `digestAlgorithm` | Digest algorithm for SAML signatures | `SHA256` |
| `nameIDFormat` | SAML NameID format | `urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified` |
| `signingCertificate` | Public certificate of the IdP (PEM format) | `{PEM certificate}` |
| `attributeMapping` | Mapping of SAML attributes to user profile fields | `{"http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress": "email"}` |

## Test the connection

You can test your SAML 2.0 connection using a web application created in AM.

1.  In AM Console, click **Applications > App > Identity Providers** and select your SAML 2.0 connector.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-social-idp-list.png" alt=""><figcaption><p>Select SAML 2.0 IdP</p></figcaption></figure>
2.  Call the Login page (the `/oauth/authorize` endpoint). If the connection is working you will see a **Sign in with SAML 2.0** button.

    If the button is not visible, there may be a problem with the identity provider settings. Check the AM Gateway log for more information.
3.  Click **Sign in with SAML 2.0**. You will be redirected to your SAML 2.0 IdP login page to authenticate your user.

    If your user is already connected (SSO session), the user will be automatically redirected to your application with an OAuth 2.0 access token and Open ID Connect ID token, if requested.

{% hint style="info" %}
SAML responses can be very large. If you see an error message in the Gateway logs like this one: `Size exceeds allowed maximum capacity`

update the `http.maxFormAttributeSize` value in the `gravitee.yml` config file (set it to `-1` for infinite).

[Learn more about updating the Gateway configuration file](../../../getting-started/configuration/configure-am-gateway/)
{% endhint %}

## Restrictions

* IdP metadata fetched from `idpMetadataUrl` is not automatically refreshed; changes to IdP metadata require reconfiguration of the SAML IdP in the client domain
* Metadata XML is validated for presence of `IDPSSODescriptor` and `SingleSignOnService` elements, but full schema validation is not performed
* `idpMetadataUrl` must match the pattern `^https?://.+/saml2/idp/metadata$`
* `idpMetadataFile` must start with `<?xml` or `<[A-Za-z]`
* Manual SAML IdP configuration remains supported; metadata-based configuration is optional

## Related changes

The `gravitee-am-idp-saml2` plugin has been upgraded from version `4.0.3` to `5.0.0-alpha.3` to support metadata URL and metadata file configuration. The `gravitee-plugin-validator` dependency has been updated from `2.0.2` to `2.3.0`. JSON schema validation for `oneOf` constructs now detects when validators pre-fill default values via in-place mutation, preventing duplicate default injection. Administrators migrating from manual SAML IdP configuration can optionally adopt metadata-based configuration without breaking existing integrations.

