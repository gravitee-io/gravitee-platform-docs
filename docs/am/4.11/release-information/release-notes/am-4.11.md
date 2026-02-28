# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6339 -->
#### **Certificate Fallback for JWT Signing**

* Automatically switches to a backup certificate when the primary certificate fails to load or sign JWTs, improving service availability during certificate rotation or expiration.
* Configure a domain-wide fallback certificate via the `/certificate-settings` API endpoint without triggering a domain reload.
* Follows a strict priority order: client-specific certificate, domain fallback certificate, default HMAC certificate (if enabled), then fails with an error.
* Requires `DOMAIN_SETTINGS[UPDATE]` permission and at least one valid certificate configured in the domain.
* Configuration changes propagate immediately to all gateway nodes via domain events.
<!-- /PIPELINE:AM-6339 -->

## Improvements

## Bug Fixes
