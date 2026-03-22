# AM 4.11

## Highlights

## Breaking Changes

## New Features


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

* Enables clients to exchange security tokens for new access or ID tokens, supporting both impersonation (acting as the subject) and delegation (acting on behalf of the subject) workflows.
* Supports external JWT issuers via trusted issuer configurations, allowing cross-domain token translation with configurable scope mappings and user binding criteria.
* Provides two scope handling modes: `DOWNSCOPING` (default) prevents privilege escalation by capping granted scopes to the intersection of subject and actor token scopes, while `PERMISSIVE` mode allows clients to request any configured scope.
* Enforces delegation depth limits (1-100, default 25) to prevent unbounded delegation chains, with full audit trail preserved in the `act` claim of resulting tokens.
* Configured at the domain level with controls for allowed token types, impersonation/delegation permissions, and maximum delegation depth.
<!-- /PIPELINE:AM-6297 -->

## Improvements

## Bug Fixes
