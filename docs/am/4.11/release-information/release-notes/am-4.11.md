# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6339 -->
#### **Certificate Fallback for JWT Signing**

* Administrators can now configure a domain-level fallback certificate that will be used when the primary certificate fails to load or sign JWTs, providing better control over certificate hierarchies before falling back to the default HMAC certificate.
* Certificate settings can be updated via the Management API without restarting the domain, with changes propagating across gateway nodes via the event bus.
* Master domains can access certificates from all domains to support cross-domain introspection scenarios, while regular domains remain restricted to their own certificates.
* The fallback certificate must belong to the same domain unless the domain is a master domain, and the system prevents infinite loops by filtering out the fallback if it matches the failed primary certificate.
<!-- /PIPELINE:AM-6339 -->

## Improvements

## Bug Fixes
