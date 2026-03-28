# SAML Identity Provider Configuration Reference

## Gateway Configuration

### SAML Identity Provider Properties (Metadata URL Mode)

| Property | Description | Example |
|:---------|:------------|:--------|
| `idpMetadataProvider` | Metadata source type; set to `METADATA_URL` | `METADATA_URL` |
| `idpMetadataUrl` | URL endpoint serving IdP metadata XML; must match pattern `^https?://.+/saml2/idp/metadata$` | `https://gateway.example.com/provider-domain/saml2/idp/metadata` |
| `entityId` | SAML entity identifier for the identity provider | `saml-idp-provider-domain` |
| `graviteeCertificate` | Certificate ID from Access Management repository; used to sign AuthnRequests | `cert-abc123` |
| `requestSigningAlgorithm` | XML signature algorithm URI for signing SAML requests | `http://www.w3.org/2001/04/xmldsig-more#rsa-sha256` |
| `attributeMapping` | Maps SAML attribute URIs to user profile fields | `{"http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress": "email"}` |

### SAML Identity Provider Properties (Metadata File Mode)

| Property | Description | Example |
|:---------|:------------|:--------|
| `idpMetadataProvider` | Metadata source type; set to `METADATA_FILE` | `METADATA_FILE` |
| `idpMetadataFile` | Inline XML metadata document; must contain `IDPSSODescriptor` and `SingleSignOnService` elements; must match pattern `^<[?]?xml|^<[A-Za-z]` | `<EntityDescriptor>...</EntityDescriptor>` |
| `entityId` | SAML entity identifier for the identity provider | `saml-idp-provider-domain` |
| `graviteeCertificate` | Certificate ID from Access Management repository; used to sign AuthnRequests | `cert-abc123` |
| `requestSigningAlgorithm` | XML signature algorithm URI for signing SAML requests | `http://www.w3.org/2001/04/xmldsig-more#rsa-sha256` |
| `attributeMapping` | Maps SAML attribute URIs to user profile fields | `{"http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress": "email"}` |

### SAML Identity Provider Properties (Manual Mode)

| Property | Description | Example |
|:---------|:------------|:--------|
| `entityId` | SAML entity identifier for the identity provider | `saml-idp-provider-domain` |
| `signInUrl` | Single Sign-On service endpoint | `https://gateway.example.com/domain/saml2/idp/SSO` |
| `signOutUrl` | Single Logout service endpoint | `https://gateway.example.com/domain/saml2/idp/logout` |
| `singleLogoutServiceUrl` | Single Logout service URL | `https://gateway.example.com/domain/saml2/idp/logout` |
| `signingCertificate` | X.509 PEM certificate of the IdP for verifying signed assertions | `-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----` |
| `wantAssertionsSigned` | Whether the SP requires signed SAML assertions | `false` |
| `wantResponsesSigned` | Whether the SP requires signed SAML responses | `false` |
| `protocolBinding` | SAML protocol binding for authentication requests | `urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect` |
| `signatureAlgorithm` | Signature algorithm for SAML assertions | `RSA_SHA256` |
| `digestAlgorithm` | Digest algorithm for SAML signatures | `SHA256` |
| `nameIDFormat` | SAML NameID format | `urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified` |
| `attributeMapping` | Maps SAML attribute URIs to user profile fields | `{"http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress": "email"}` |

### Certificate Configuration

| Property | Description | Example |
|:---------|:------------|:--------|
| `type` | Certificate type for SAML signing | `javakeystore-am-certificate` |
| `jks` | Java KeyStore configuration object containing base64-encoded content, store password, key alias, and key password | `{"content": "...", "storepass": "letmein", "alias": "mytestkey", "keypass": "changeme"}` |


