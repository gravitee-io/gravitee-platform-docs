# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6339 -->
#### **Certificate Fallback for JWT Signing**

* Configures a domain-level fallback certificate that the gateway uses when primary client certificates fail or become unavailable during JWT signing operations.
* Evaluates certificates in priority order: client-specific certificate, domain fallback certificate, default HMAC certificate (if enabled), or throws `TemporarilyUnavailableException` if none are available.
* Applies configuration changes immediately without requiring a domain reload and emits structured warning logs identifying both failed primary and fallback certificates used.
* Requires `DOMAIN_SETTINGS[UPDATE]` permission and at least one valid certificate uploaded to the domain or organization.
<!-- /PIPELINE:AM-6339 -->

## Improvements

## Bug Fixes
