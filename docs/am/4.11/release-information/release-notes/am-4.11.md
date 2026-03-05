# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6321 -->
#### **Protected Resource Secret Management and Certificate-Based Authentication**

* Protected Resources now support multiple client secrets with independent lifecycle management, enabling secret rotation without service interruption.
* Certificate-based authentication allows Protected Resources to use JWT signature verification during token introspection when the JWT `aud` claim matches the resource's `clientId`.
* Token introspection validates Protected Resource audiences alongside traditional OAuth clients, enabling Protected Resources to act as first-class OAuth 2.0 clients.
* MCP Server-type Protected Resources have restricted OAuth 2.0 capabilities, supporting only `client_credentials` and `token-exchange` grant types with basic authentication methods.
* Certificate deletion is blocked if referenced by any Protected Resource, preventing broken authentication configurations.
<!-- /PIPELINE:AM-6321 -->

## Improvements

## Bug Fixes
