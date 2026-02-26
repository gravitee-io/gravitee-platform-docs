# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6339 -->
#### **Certificate Fallback for JWT Signing**

* Access Management now supports automatic fallback to a domain-level certificate when a client's configured certificate fails to load, improving service availability during certificate rotation or expiration.
* Configure a fallback certificate in domain certificate settings via the Console UI or Management API—changes propagate immediately to all gateway nodes without requiring a domain restart.
* The system follows a deterministic hierarchy: client certificate → domain fallback certificate → default HMAC signature (if enabled) → failure, with automatic loop prevention when fallback and primary certificates match.
* Requires `DOMAIN_SETTINGS[UPDATE]` permission and at least one non-system certificate configured in the domain.
<!-- /PIPELINE:AM-6339 -->

## Improvements

## Bug Fixes
