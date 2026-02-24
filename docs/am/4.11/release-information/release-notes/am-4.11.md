# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6321 -->
#### **Protected Resource Secret Management**

* Protected Resources (MCP Servers) can now authenticate as OAuth2 clients with full secret lifecycle management, supporting token introspection and token exchange workflows.
* Multiple active secrets can exist simultaneously to enable zero-downtime rotation during credential updates.
* Certificate-based JWT verification is supported via an optional certificate field for custom signing key configuration.
* Protected Resources automatically receive OAuth2 defaults (`client_credentials` grant, `client_secret_basic` authentication) and can be resolved by either `clientId` or `resourceIdentifier`.
* Secret operations (create, renew, delete) are managed through the Management API and logged via the `PROTECTED_RESOURCE_SECRET` audit event type.
<!-- /PIPELINE:AM-6321 -->

## Improvements

## Bug Fixes
