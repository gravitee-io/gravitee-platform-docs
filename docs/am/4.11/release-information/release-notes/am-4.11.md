# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6321 -->
#### **Protected Resource Secret Management and Certificate-Based Authentication**

* Protected Resources now support client secret lifecycle management with automatic rotation, expiration dates, and secure storage. Multiple secrets can be active simultaneously for zero-downtime rotation.
* Protected Resources can reference certificates for JWT signature verification during token introspection, enabling asymmetric cryptography workflows where tokens are validated against the authorization server's public key.
* MCP Server context automatically restricts Protected Resources to `client_credentials` and token exchange grant types, with authentication methods limited to `client_secret_basic`, `client_secret_post`, and `client_secret_jwt`.
* Requires AM 4.11.0 or later and `PROTECTED_RESOURCE[CREATE]` and `PROTECTED_RESOURCE[UPDATE]` permissions to manage secrets and certificates.
<!-- /PIPELINE:AM-6321 -->

## Improvements

## Bug Fixes
