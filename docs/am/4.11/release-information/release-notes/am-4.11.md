# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6339 -->
#### **Certificate Fallback for JWT Signing**

* AM now supports domain-level fallback certificates for JWT signing operations, improving availability when a client's primary certificate fails to load.
* When a primary certificate is unavailable, the gateway attempts to use the configured fallback certificate before falling back to the default HMAC certificate or failing the operation.
* Configure the fallback certificate via the Management API at `/organizations/{orgId}/environments/{envId}/domains/{domain}/certificate-settings` with the `fallbackCertificate` property.
* Certificate settings updates propagate across gateway nodes in real time without requiring domain reloads.
* Requires `DOMAIN_SETTINGS[UPDATE]` permission and a pre-loaded backup certificate in the domain.
<!-- /PIPELINE:AM-6339 -->

## Improvements

## Bug Fixes
