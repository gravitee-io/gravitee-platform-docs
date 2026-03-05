# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6321 -->
#### **Protected Resource Secret Management and Token Introspection**

* Protected Resources now support multiple client secrets with independent lifecycle management, including creation, renewal, and deletion operations.
* Token introspection validates audience claims against both Applications and Protected Resources, with support for single-audience and multi-audience tokens per RFC 8707.
* Certificate-based JWT verification is supported when a Protected Resource has an associated certificate uploaded to the domain.
* Protected Resources operating in MCP Server context are restricted to `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange` grant types.
* Secret expiration tracking integrates with the platform notification system, triggering events on secret creation, renewal, and deletion.
<!-- /PIPELINE:AM-6321 -->

## Improvements

## Bug Fixes
