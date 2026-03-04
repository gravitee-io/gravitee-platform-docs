# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6321 -->
#### **Protected Resource Secret Management and Token Introspection**

* Protected Resources now support multiple client secrets with independent lifecycles, enabling secret rotation without service disruption.
* Token introspection validates JWT tokens against both Applications and Protected Resources, with automatic certificate-based signature verification for matched clients.
* MCP Servers operate under restricted OAuth 2.0 settings, limiting grant types to `client_credentials` and `token-exchange`, with authentication methods restricted to secret-based flows.
* Secret lifecycle events (create, renew, delete) are published to the event bus for audit and notification purposes.
* Default OAuth 2.0 settings are automatically applied to Protected Resources on creation, including `client_credentials` grant type and `client_secret_basic` authentication method.
<!-- /PIPELINE:AM-6321 -->

## Improvements

## Bug Fixes
