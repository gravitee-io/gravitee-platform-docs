# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6321 -->
#### **Protected Resource Secret Management and Token Introspection**

* Protected Resources now support full secret lifecycle management, including creation, renewal, and deletion via REST API, with automatic expiration tracking based on domain-level policies.
* Token introspection validates audiences against both Applications and Protected Resources, with support for certificate-based JWT verification when configured.
* MCP Server contexts enforce OAuth constraints by restricting grant types to `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange`, and limiting token endpoint authentication methods to `client_secret_basic`, `client_secret_post`, and `client_secret_jwt`.
* Protected Resources require at least one active secret and appropriate permissions (`PROTECTED_RESOURCE[LIST|CREATE|UPDATE|DELETE]`) for secret operations.
<!-- /PIPELINE:AM-6321 -->

## Improvements

## Bug Fixes
