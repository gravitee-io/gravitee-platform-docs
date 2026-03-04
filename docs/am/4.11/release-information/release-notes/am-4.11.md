# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6321 -->
#### **Protected Resource Secret Management and Token Exchange**

* Protected Resources now support client secret lifecycle management with expiration policies, certificate-based JWT authentication, and membership controls for administrative permissions.
* Protected Resources can participate in OAuth 2.0 Token Exchange flows (RFC 8693) as clients, exchanging subject tokens (access, refresh, ID, or JWT) for new access tokens scoped to their identity.
* Secrets follow domain-level expiration settings and can be renewed or deleted independently. Certificate deletion is blocked if referenced by any Protected Resource to prevent broken authentication chains.
* Token exchange requires domain-level configuration of allowed subject token types. Exchanged tokens inherit subject token lifetime constraints and preserve the `gis` (grant issuer) claim for audit trails.
* Configure secret expiration via `domain.secretExpirationSettings` properties and allowed token types via `domain.tokenExchangeSettings.allowedSubjectTokenTypes` at the domain level.
<!-- /PIPELINE:AM-6321 -->

## Improvements

## Bug Fixes
