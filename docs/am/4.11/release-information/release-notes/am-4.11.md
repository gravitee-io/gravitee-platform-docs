# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6338 -->
#### **Magic Link Authentication**

* Enables passwordless login by sending users a time-limited authentication link via email, eliminating the need to enter passwords during sign-in.
* Users enter their email address at `/magic-link/login`, receive a JWT-based authentication link valid for 15 minutes (configurable), and are authenticated when they click the link.
* Requires email service configuration and must be enabled in domain or application login settings via the `magicLinkAuthEnabled` property.
* Generates `USER_MAGIC_LINK_LOGIN` audit events for successful authentications and supports analytics filtering via the `magic_link` field type.
* Token expiration time is configurable via `user.magic.link.login.time.value` and `user.magic.link.login.time.unit` gateway properties (defaults to 15 minutes).
<!-- /PIPELINE:AM-6338 -->
<!-- PIPELINE:AM-6339 -->
#### **Domain-Level Certificate Fallback**

* Administrators can configure a fallback certificate at the domain-level to prevent authentication failures when a certificate that is explicitly configured for an application cannot be used.
* When an application's certificate fails to load (e.g., external provider unavailable), the system automatically uses the domain's fallback certificate to sign OAuth and ID tokens.
* Fallback certificates are configured using the Management API (`/domains/{domain}/certificate-settings`) and require `DOMAIN_SETTINGS[UPDATE]` permission.
* Certificates configured as domain fallback cannot be deleted until removed from the fallback configuration.
<!-- /PIPELINE:AM-6339 -->
<!-- PIPELINE:AM-6321 -->
#### **Protected Resource OAuth 2.0 Client Management**

* Protected Resources now support full OAuth 2.0 client lifecycle management, including multiple client secrets with independent expiration dates and certificate-based authentication for JWT signature verification.
* Secret rotation is enabled through the Management API, with server-generated secrets returned only once during creation or renewal to ensure secure credential handling.
* Token introspection resolves audience claims against both Applications and Protected Resources, with automatic fallback to RFC 8707 resource identifiers for multi-audience JWTs.
* MCP Servers configured as Protected Resources are restricted to `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange` grant types, with authentication methods limited to `client_secret_basic`, `client_secret_post`, and `client_secret_jwt`.
* Requires AM 4.11.0+ with OAuth 2.0 enabled at the domain level; token exchange flows require `tokenExchangeSettings.enabled = true` in domain configuration.
<!-- /PIPELINE:AM-6321 -->
<!-- PIPELINE:AM-6322 -->
#### **Agent Application Type for Agentic OAuth Clients**

* Introduces a dedicated Agent application type for AI assistants and autonomous agents, enforcing stricter OAuth grant type constraints than traditional clients.
* Restricts agent applications to `authorization_code` and `client_credentials` grant types only, blocking implicit, password, and refresh token flows to align with agentic security requirements.
* Supports optional AgentCard metadata import via the A2A specification, allowing administrators to fetch and display agent capabilities, tools, and prompts from a publicly accessible URL.
* AgentCard fetching enforces SSRF protection, 512 KB size limits, and 5-second timeouts to prevent security risks and resource exhaustion.
<!-- /PIPELINE:AM-6322 -->


<!-- PIPELINE:AM-6297 -->
#### **OAuth 2.0 Token Exchange (RFC 8693)**

* Enables clients to exchange security tokens for new tokens, supporting impersonation (acting as another user) and delegation (acting on behalf of another user) scenarios.
* Supports access tokens, refresh tokens, and ID tokens as input and output, with configurable scope handling modes (downscoping or permissive) to control granted permissions.
* Allows administrators to configure trusted external JWT issuers with JWKS or PEM-based key resolution, scope mappings, and user binding rules via EL expressions.
* Impersonation is enabled by default; delegation requires explicit configuration via `allowDelegation` setting.
<!-- /PIPELINE:AM-6297 -->


<!-- PIPELINE:AM-6340 -->
#### **SAML Identity Provider Metadata Configuration**

* SAML identity providers can now be configured using metadata URL or metadata file upload, eliminating manual endpoint and certificate configuration.
* Three configuration modes are supported: Manual (individual endpoint specification), Metadata URL (remote endpoint fetch), and Metadata File (inline XML upload).
* Metadata-based modes automatically sign authentication requests when the IdP requires it, using certificates from the AM certificate store.
* The JSON schema validator now prevents duplicate default value injection in oneOf schemas, improving validation accuracy for complex configurations.
<!-- /PIPELINE:AM-6340 -->

## Improvements

## Bug Fixes
