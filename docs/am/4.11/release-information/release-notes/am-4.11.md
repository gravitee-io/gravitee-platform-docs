# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6321 -->
#### **Protected Resource Secret Management and Token Introspection**

* Protected Resources now support full secret lifecycle management with creation, renewal, deletion, and automatic expiration tracking via REST API.
* Token introspection validates audiences against both Applications and Protected Resources, with support for certificate-based JWT verification when configured.
* Protected Resources in MCP Server context are restricted to `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange` grant types with limited authentication methods (`client_secret_basic`, `client_secret_post`, `client_secret_jwt`).
* Secret expiration notifications are registered automatically based on domain-level expiration policies, with at least one secret required per Protected Resource.
* Default OAuth settings are applied automatically during creation, including `client_credentials` grant type and `client_secret_basic` authentication method.
<!-- /PIPELINE:AM-6321 -->

## Improvements

## Bug Fixes
