Protected Resources support secret management, certificate-based authentication, and membership controls. These features enable secure token introspection, audience validation, and role-based access to Protected Resource configurations.

### Protected Resource Secrets

Protected Resources can maintain multiple client secrets for authentication. Each secret is generated server-side and can be renewed or deleted independently. Secrets share a common `secretSettings` configuration (algorithm, expiration) via a `settingsId` reference, allowing multiple secrets to reuse the same cryptographic parameters. On creation, the plaintext secret is returned once. Subsequent API calls return only safe (redacted) metadata (ID, algorithm, creation date).

### Certificate-Based Authentication

Protected Resources can reference a domain certificate for JWT signature verification during token introspection. When a token's `aud` claim matches a Protected Resource's `clientId`, the introspection service retrieves the associated certificate ID to validate the token signature. If no certificate is configured, HMAC-based validation is used. Certificate deletion is blocked if any Protected Resource references it.

### MCP Server Context Restrictions

Protected Resources with type `MCP_SERVER` are restricted to `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange` grant types. Token endpoint authentication methods are limited to `client_secret_basic`, `client_secret_post`, and `client_secret_jwt`. Methods requiring asymmetric keys (`private_key_jwt`, `tls_client_auth`, `self_signed_tls_client_auth`) and `none` are excluded from the UI and validation logic.

### Prerequisites for Secret Management

* Domain with OAuth 2.0 settings configured
* `PROTECTED_RESOURCE[CREATE]` permission to create resources
* `PROTECTED_RESOURCE[UPDATE]` permission to manage secrets and certificates
* `PROTECTED_RESOURCE[READ]` permission to view resource configurations

### Prerequisites for Certificate-Based Authentication

* Valid domain certificate uploaded
* `PROTECTED_RESOURCE[UPDATE]` permission to assign certificates

### Prerequisites for Membership Controls

* User or group memberships defined
* `PROTECTED_RESOURCE_MEMBER[LIST]` permission to view members
* `PROTECTED_RESOURCE_MEMBER[CREATE]` permission to assign roles
* `PROTECTED_RESOURCE_MEMBER[DELETE]` permission to remove members
