# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6321 -->
#### **Protected Resource Secret Management and Token Exchange**

* Protected Resources now support multiple named secrets with independent lifecycles, enabling secure rotation and management of client credentials without service interruption.
* MCP Servers can perform RFC 8693 token exchange flows to delegate access tokens, inheriting the subject token's claims and expiration constraints for server-to-server authentication scenarios.
* Certificate binding allows Protected Resources to use mTLS authentication by associating domain certificates, with automatic validation to prevent deletion of certificates in use.
* Token exchange requires domain-level enablement via `tokenExchangeSettings.enabled` and restricts MCP Servers to `client_credentials` and token exchange grant types only.
<!-- /PIPELINE:AM-6321 -->

## Improvements

## Bug Fixes
