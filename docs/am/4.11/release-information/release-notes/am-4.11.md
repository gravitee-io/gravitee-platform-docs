# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6339 -->
#### **Certificate Fallback for JWT Signing**

* Automatically uses a backup certificate when the primary certificate fails during JWT signing operations, improving service resilience without manual intervention.
* Configure a domain-level fallback certificate that activates transparently when the client's primary certificate is unavailable or fails to load.
* Changes take effect immediately through event-driven updates without requiring domain restarts or service disruption.
* Master domains can access certificates from any domain for cross-domain introspection scenarios, while regular domains are restricted to their own certificate scope.
<!-- /PIPELINE:AM-6339 -->

## Improvements

## Bug Fixes
