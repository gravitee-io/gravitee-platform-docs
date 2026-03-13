# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6297 -->
#### **OAuth 2.0 Token Exchange (RFC 8693)**

* Enables secure token transformation and delegation for multi-hop architectures, AI agents, and distributed services by exchanging an existing token for a new token with reduced scope, different type, or delegated authority.
* Supports both impersonation mode (acting as the user without intermediary identity) and delegation mode (acting on behalf of the user with auditable actor chain via nested `act` claims).
* Provides two scope resolution modes: downscoping (default, subject token scopes act as ceiling) and permissive (ignores subject token scopes for external issuer compatibility).
* Allows integration with external identity providers through trusted issuer configuration with JWKS URL or PEM certificate validation and optional scope mapping.
* Requires enabling `urn:ietf:params:oauth:grant-type:token-exchange` grant type on client applications and configuring domain-level token exchange settings including allowed token types, delegation depth limits, and scope handling mode.
<!-- /PIPELINE:AM-6297 -->

## Improvements

## Bug Fixes
