# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6321 -->
#### **Protected Resource Secret Management and Certificate Authentication**

* Protected Resources now support multiple client secrets with expiration tracking, renewal workflows, and domain-level policy inheritance.
* Certificate-based authentication enables X.509 certificate binding for mutual TLS authentication on Protected Resources, with validation enforced on creation and update.
* Token introspection resolves JWT `aud` claims by checking Application client IDs, Protected Resource client IDs, and resource identifiers (RFC 8707) in sequence.
* MCP Server contexts restrict authentication methods to `client_secret_basic`, `client_secret_post`, and `client_secret_jwt`, with grant types limited to `client_credentials` and token exchange.
* At least one active secret must exist per Protected Resource; certificate deletion is blocked if any resource references it.
<!-- /PIPELINE:AM-6321 -->

## Improvements

## Bug Fixes
