# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6321 -->
#### **Protected Resource Secret Management and Certificate-Based Authentication**

* Protected Resources now support multiple client secrets with independent lifecycle management, including creation, renewal, and deletion via the Management API.
* Certificate-based JWT verification is available for token introspection when a certificate is associated with the Protected Resource.
* Secret expiration tracking integrates with the platform notification system, triggering events on secret lifecycle changes.
* MCP Server contexts restrict Protected Resources to `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange` grant types with limited authentication methods.
* Token introspection validates audience claims against both Applications and Protected Resources, supporting single-audience and multi-audience tokens per RFC 8707.
<!-- /PIPELINE:AM-6321 -->

## Improvements

## Bug Fixes
