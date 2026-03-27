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

SAML 2.0 identity provider configuration supports metadata-based setup through URL endpoints or inline XML files, simplifying integration with external IdPs. This feature includes enhanced JSON schema validation for oneOf constructs with improved default value handling.

## Metadata Provider Modes

SAML IdP configuration supports three metadata provider modes:

| Mode | Required Fields | Use Case |
|:-----|:----------------|:---------|
| `METADATA_URL` | `idpMetadataUrl`, `graviteeCertificate` | Dynamic metadata retrieval from IdP endpoint |
| `METADATA_FILE` | `idpMetadataFile`, `graviteeCertificate` | Static metadata embedded in configuration |
| Manual | `signInUrl`, `signOutUrl`, `signingCertificate` | Full manual endpoint and certificate setup |

**METADATA_URL** fetches IdP metadata from a runtime endpoint, requiring only the metadata URL and a Gravitee certificate reference. **METADATA_FILE** uses inline XML metadata provided directly in the configuration, also requiring a Gravitee certificate. **Manual configuration** (when `idpMetadataProvider` is not set) requires explicit specification of all IdP endpoints and the signing certificate in PEM format.

## Get your SAML 2.0 identity provider metadata

To connect your applications to a SAML 2.0 IdP, you need at least the following information:

* **SingleSignOnService**: the SAML IdP Sign-In URL
* **SingleLogoutService**: the SAML IdP Sign Out URL
* **Signing certificate**: the public signing certificate (encoded in PEM) provided by the identity provider

Alternatively, you can use metadata-based configuration by obtaining:

* **IdP Metadata URL**: the endpoint where the IdP publishes its SAML metadata
* **IdP Metadata File**: the complete XML metadata document from your IdP
* **Gravitee Certificate**: a valid X.509 certificate uploaded to the Gravitee certificate store

{% hint style="info" %}
Before you begin, obtain this information from your SAML IdP administrator and make a note of it for later use.
{% endhint %}

## Prerequisites

Before configuring SAML 2.0 identity provider integration:

* Gravitee Access Management domain configured and running
* SAML IdP metadata URL accessible from the client domain (for `METADATA_URL` mode)
* Valid X.509 certificate uploaded to Gravitee certificate store (for metadata-based modes)
* Java Keystore (JKS) file with signing certificate (for manual configuration in test environments)

{% hint style="warning" %}
Domain start operations include a 10-30 second synchronization delay to ensure the DEPLOY event is processed and the certificate provider is fully loaded before certificate PEM retrieval.
{% endhint %}

## Create a SAML 2.0 connector

1. Log in to AM Console.
2. Click **Settings > Providers**.
3. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
4. Select **SAML 2.0** as your identity provider type and click **Next**.
5. Give your identity provider a name.
6. Configure the settings using one of the following methods:
   * **Metadata URL mode**: Set **IdP Metadata Provider** to `METADATA_URL`, enter the IdP metadata URL (e.g., `https://gateway.example.com/domain/saml2/idp/metadata`), and select a certificate from the **Gravitee Certificate** dropdown.
   * **Metadata File mode**: Set **IdP Metadata Provider** to `METADATA_FILE`, paste the XML metadata content into the **IdP Metadata File** textarea, and select a certificate from the **Gravitee Certificate** dropdown.
   * **Manual mode**: Leave **IdP Metadata Provider** unset and configure EntityID, Sign In URL, Sign Out URL, and Signing certificate manually.
7. Click **Create**.

{% hint style="info" %}
The connector includes some advanced settings such as protocol binding (HTTP-REDIRECT or HTTP-POST), NameId format and Request Signing options to connect to your SAML 2.0 IdP. If you need more information on how to configure these settings, check with your SAML IdP administrator.

Make a note of the URL in **1. Configure the Redirect URI** on the right-hand side of the page. This is the SAML 2.0 Assertion Consumer Service URL you need to provide to the SAML 2.0 IdP to register your Access Management instance.

From AM version 3.7, SAML IdP servers may ask you to share the SAML SP Metadata endpoint to register your AM instance. This endpoint can be found at: `https://AM_GW_HOST/:domain/saml2/sp/metadata/:providerId`.

From SAML IdP plugin v1.4.0, encrypted assertion responses can be handled and decrypted. We decided to only publish KeyDescriptor with use="encryption" if the 'wantAssertionsEncrypted' option is enabled.
{% endhint %}

## Configuration Reference

### SAML Identity Provider Properties

| Property | Description | Example |
|:---------|:------------|:--------|
| `idpMetadataProvider` | Metadata source mode: `METADATA_URL`, `METADATA_FILE`, or omit for manual | `METADATA_URL` |
| `idpMetadataUrl` | URL endpoint for fetching IdP metadata (required when `idpMetadataProvider=METADATA_URL`) | `https://gateway.example.com/domain/saml2/idp/metadata` |
| `idpMetadataFile` | Inline XML metadata content (required when `idpMetadataProvider=METADATA_FILE`) | `<?xml version="1.0"?>\n<EntityDescriptor ...>` |
| `graviteeCertificate` | Certificate ID from Gravitee certificate store (required for metadata modes) | `cert-id-123` |
| `requestSigningAlgorithm` | Algorithm URI for signing AuthnRequests | `http://www.w3.org/2001/04/xmldsig-more#rsa-sha256` |
| `entityId` | SAML entity identifier for the IdP | `saml-idp-example` |
| `signInUrl` | SAML SSO endpoint URL (manual mode only) | `https://gateway.example.com/domain/saml2/idp/SSO` |
| `signOutUrl` | SAML logout endpoint URL (manual mode only) | `https://gateway.example.com/domain/saml2/idp/logout` |
| `singleLogoutServiceUrl` | SAML single logout service URL (manual mode only) | `https://gateway.example.com/domain/saml2/idp/logout` |
| `signingCertificate` | X.509 PEM certificate for verifying IdP signatures (manual mode only) | `-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----` |
| `wantAssertionsSigned` | Whether SAML assertions must be signed | `false` |
| `wantResponsesSigned` | Whether SAML responses must be signed | `false` |
| `protocolBinding` | SAML protocol binding URN | `urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect` |
| `signatureAlgorithm` | Signature algorithm for SAML messages | `RSA_SHA256` |
| `digestAlgorithm` | Digest algorithm for SAML signatures | `SHA256` |
| `nameIDFormat` | SAML NameID format URN | `urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified` |

### SAML Service Provider Properties

| Property | Description | Example |
|:---------|:------------|:--------|
| `singleLogoutServiceUrl` | SP logout service URL | `https://gateway.example.com/domain/logout` |
| `entityId` | SAML entity identifier for the SP (typically client ID) | `client-app-123` |
| `wantResponseSigned` | Whether SP requires signed SAML responses | `false` |
| `wantAssertionsSigned` | Whether SP requires signed SAML assertions | `true` |
| `responseBinding` | SAML response binding method | `HTTP-POST` |
| `certificate` | X.509 PEM certificate used by IdP to verify signed AuthnRequests from SP | `-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----` |

### Attribute Mapping

| SAML Claim URI | Mapped Attribute | Description |
|:---------------|:-----------------|:------------|
| `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress` | `email` | User email address |
| `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname` | `firstname` | User first name |
| `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname` | `lastname` | User last name |

## Restrictions

* SAML metadata URL must be accessible from the client domain at both configuration time and runtime
* Metadata URL must match the pattern `^https?:\/\/.+\/saml2\/idp\/metadata$`
* Metadata file XML must contain `IDPSSODescriptor` and `SingleSignOnService` elements
* Metadata file must start with `<?xml` or `<[A-Za-z]`
* Java Keystore (JKS) format is the only supported certificate format in test configurations
* JSON schema validation with `useDefaults` enabled mutates the original `JSONObject` instance in-place rather than creating a defensive copy
* everit validator processes all `allOf` subschemas regardless of intermediate failures, ensuring defaults are always injected

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

[Learn more about updating the Gateway configuration file](../../../getting-started/configuration/configure-am-gateway)
{% endhint %}

## Troubleshooting

### Missing 'Sign in with SAML 2.0' button

If the **Sign in with SAML 2.0** button does not appear on the login page, check the AM Gateway logs for identity provider configuration errors. Common issues include invalid metadata URLs, missing certificates, or incorrect endpoint configurations.

## Related Changes

The SAML 2.0 identity provider plugin (`gravitee-am-idp-saml2`) has been upgraded from version 4.0.3 to 5.0.0-alpha.3, introducing metadata provider selection in the configuration form. When **METADATA_URL** or **METADATA_FILE** is selected, the form hides manual endpoint fields (`signInUrl`, `signOutUrl`, `singleLogoutServiceUrl`, `signingCertificate`) and displays metadata-specific fields (**IdP Metadata URL** or **IdP Metadata File**, and **Gravitee Certificate** dropdown). Attribute mapping fields now include default mappings for common SAML claims (email, firstname, lastname). Existing manual configurations remain compatible but can be migrated to metadata-based modes by setting `idpMetadataProvider` and providing either `idpMetadataUrl` or `idpMetadataFile` along with a `graviteeCertificate` reference.
