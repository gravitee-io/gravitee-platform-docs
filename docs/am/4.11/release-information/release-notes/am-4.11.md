# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6321 -->
#### **Protected Resource Secret Management and Token Exchange**

* Protected Resources now support multiple client secrets with independent lifecycles, including creation, renewal, and expiration management.
* Token introspection validates audience claims against both Applications and Protected Resources, with support for single-audience and multi-audience tokens per RFC 8707.
* MCP Server context restricts OAuth configuration to machine-to-machine grant types (`client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange`) with appropriate authentication methods.
* Protected Resources can use certificate-based authentication by associating a certificate ID during creation or update.
* Requires AM 4.11.0 or later with OAuth 2.0 enabled on the domain.
<!-- /PIPELINE:AM-6321 -->

## Improvements

## Bug Fixes
