# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6321 -->
#### **Protected Resource Secret and Certificate Management**

* Protected Resources now support multiple client secrets for authentication, with automatic generation, expiration tracking, and renewal capabilities.
* Administrators can bind certificates to Protected Resources for mTLS authentication scenarios, with validation to prevent deletion of referenced certificates.
* Protected Resources participate in token introspection workflows by resolving audience claims, enabling integration with token exchange scenarios and MCP Server configurations.
* Each Protected Resource requires at least one active secret and receives default OAuth 2.0 settings (client credentials grant, basic authentication) when created without explicit configuration.
* MCP Server-type Protected Resources are restricted to three token endpoint authentication methods: `client_secret_basic`, `client_secret_post`, and `client_secret_jwt`.
<!-- /PIPELINE:AM-6321 -->

## Improvements

## Bug Fixes
