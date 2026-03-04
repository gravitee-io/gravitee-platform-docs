# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6321 -->
#### **Protected Resource OAuth2 Client Capabilities**

* Protected resources now function as OAuth2 clients with full secret management, enabling server-to-server authentication scenarios including token exchange flows for MCP servers.
* Each protected resource maintains one or more client secrets with optional expiration dates, generated server-side and returned in plaintext only at creation or renewal.
* Protected resources authenticate at the token introspection endpoint using client credentials and can validate JWT tokens when the `aud` claim matches their `clientId`.
* Token exchange grant type (`urn:ietf:params:oauth:grant-type:token-exchange`) enables delegation scenarios where clients exchange existing tokens for new access tokens, with inherited expiration constraints.
* MCP servers support a restricted subset of grant types (`client_credentials`, token exchange) and authentication methods (`client_secret_basic`, `client_secret_post`, `client_secret_jwt`).
<!-- /PIPELINE:AM-6321 -->

## Improvements

## Bug Fixes
