# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6321 -->
#### **Protected Resource Secret Management and Token Exchange**

* Protected Resources now support secret lifecycle management with expiration policies, renewal capabilities, and automatic notifications to domain owners before expiration.
* Certificate-based JWT signature verification enables Protected Resources to validate tokens during introspection by referencing domain certificates.
* Token exchange grant type (`urn:ietf:params:oauth:grant-type:token-exchange`) allows MCP Servers to exchange subject tokens for new access tokens with inherited claims and controlled expiration.
* Membership controls restrict which users can access Protected Resources, with permissions enforced through `PROTECTED_RESOURCE` and `PROTECTED_RESOURCE_MEMBER` scopes.
* Domain-level `tokenExchangeSettings` configuration controls which subject token types are accepted for token exchange flows.
<!-- /PIPELINE:AM-6321 -->

## Improvements

## Bug Fixes
