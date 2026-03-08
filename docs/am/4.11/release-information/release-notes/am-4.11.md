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

## Improvements

## Bug Fixes
