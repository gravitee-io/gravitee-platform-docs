# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6321 -->
#### **Protected Resource Secret Management and Token Exchange Support**

* Protected Resources now support multiple client secrets with independent lifecycle management, enabling secure credential rotation without service interruption.
* Token introspection validates JWT audiences against Protected Resource client IDs in addition to OAuth clients, supporting machine-to-machine communication patterns including token exchange flows.
* MCP Server-type Protected Resources enforce restricted grant types (`client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange`) and authentication methods, excluding certificate-based authentication.
* Secret generation returns plaintext values once on creation; subsequent API calls return only metadata for security.
* Requires `PROTECTED_RESOURCE[CREATE/UPDATE/DELETE]` permissions for secret operations and AM 4.11.0 or later.
<!-- /PIPELINE:AM-6321 -->

## Improvements

## Bug Fixes
