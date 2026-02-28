# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6339 -->
#### **Certificate Fallback for JWT Signing**

* Access Management now supports domain-level fallback certificates for JWT signing operations, improving service resilience when a client's primary certificate fails to load or sign a token.
* The system follows a three-tier hierarchy: client-specific certificate, domain fallback certificate, and default HMAC certificate (if enabled).
* Configure fallback certificates via the Management API at `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/certificate-settings` using the `fallbackCertificate` property.
* Fallback certificates must belong to the current domain (or be accessible for master domains) and cannot match the primary certificate ID to prevent infinite loops.
* Requires `DOMAIN_SETTINGS[UPDATE]` permission; changes propagate to gateway nodes without restart.
<!-- /PIPELINE:AM-6339 -->

## Improvements

## Bug Fixes
