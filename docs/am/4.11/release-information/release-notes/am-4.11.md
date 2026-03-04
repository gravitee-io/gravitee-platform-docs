# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6321 -->
#### **Protected Resource Secret Management and Token Exchange Support**

* Protected Resources now support multiple client secrets with independent lifecycle management, enabling secure credential rotation without service interruption.
* Token introspection validates JWT audiences against both OAuth clients and Protected Resources, supporting token exchange and client credentials flows for machine-to-machine communication.
* MCP Server Protected Resources enforce restricted grant types (`client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange`) and authentication methods, excluding certificate-based authentication.
* Secrets reference shared `secretSettings` entries for algorithm configuration and are generated server-side with plaintext returned only once at creation.
* Requires `PROTECTED_RESOURCE[CREATE]`, `PROTECTED_RESOURCE[UPDATE]`, `PROTECTED_RESOURCE[DELETE]` permissions for secret operations and AM 4.11.0 or later.
<!-- /PIPELINE:AM-6321 -->

## Improvements

## Bug Fixes
