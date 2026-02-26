# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6339 -->
#### **Certificate Fallback for JWT Signing**

* Domains can now automatically switch to a backup certificate when the primary certificate fails to load or sign JWTs, improving service resilience without requiring domain restarts.
* Configure fallback certificates at the domain level via the Management API or Console—changes take effect immediately and are logged at WARN level when fallback is triggered.
* The fallback certificate must differ from the primary certificate to prevent infinite loops, and regular domains can only access certificates within their own scope (master domains can access certificates from any domain).
* Requires `DOMAIN_SETTINGS[UPDATE]` permission and at least one non-system certificate configured in the domain.
<!-- /PIPELINE:AM-6339 -->

## Improvements

## Bug Fixes
