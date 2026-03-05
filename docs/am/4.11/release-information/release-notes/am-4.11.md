# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6321 -->
#### **Protected Resource Secret Management and Token Introspection**

* Protected Resources now support multiple client secrets with independent lifecycle controls, including expiration dates and algorithm configuration.
* Token introspection validates JWT access tokens against both Applications and Protected Resources, using the matched entity's certificate for signature verification.
* MCP Server Protected Resources are restricted to `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange` grant types with limited authentication methods (`client_secret_basic`, `client_secret_post`, `client_secret_jwt`).
* Membership management allows assigning users or groups to Protected Resources with role-based permissions via REST API.
* Requires Access Management 4.11.0 or later with OAuth 2.0 enabled on the domain.
<!-- /PIPELINE:AM-6321 -->

## Improvements

## Bug Fixes
