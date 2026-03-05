# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6321 -->
#### **Protected Resource Management and Token Exchange**

* Manage OAuth 2.0 resource servers independently from client applications, with support for multiple resource identifiers, credential rotation, and certificate-based JWT verification.
* Enable MCP Server integrations using OAuth 2.0 Token Exchange (RFC 8693) to exchange subject tokens for access tokens scoped to specific resource servers.
* Configure resource identifiers that appear in the `aud` claim of access tokens, supporting RFC 8707 resource indicators for fine-grained access control.
* Assign certificates to Protected Resources for JWT signature verification during token introspection, with automatic validation to prevent deletion of in-use certificates.
* Restrict subject token types for token exchange flows via domain-level settings to control which token types (access, refresh, ID, JWT) can be exchanged.
<!-- /PIPELINE:AM-6321 -->

## Improvements

## Bug Fixes
