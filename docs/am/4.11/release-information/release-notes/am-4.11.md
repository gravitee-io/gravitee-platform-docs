# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6321 -->
#### **Protected Resource Secret Management and Certificate-Based Authentication**

* Protected Resources now support multiple client secrets with independent lifecycle management (create, renew, delete) for secure token introspection and audience validation.
* Certificate-based JWT signature verification can be configured by associating a domain certificate with a Protected Resource, enabling asymmetric key validation during token introspection.
* MCP Server-type Protected Resources are automatically restricted to `client_credentials` and `token-exchange` grant types, with authentication methods limited to `client_secret_basic`, `client_secret_post`, and `client_secret_jwt`.
* Default OAuth settings are applied automatically when creating Protected Resources: `client_credentials` grant type, `code` response type, and `client_secret_basic` authentication method.
* Requires `PROTECTED_RESOURCE[CREATE]` and `PROTECTED_RESOURCE[UPDATE]` permissions; certificate deletion is blocked if referenced by any Protected Resource.
<!-- /PIPELINE:AM-6321 -->

## Improvements

## Bug Fixes
