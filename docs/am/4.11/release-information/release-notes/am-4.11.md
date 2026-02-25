# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6339 -->
#### **Certificate Fallback for JWT Signing**

* Domains can now specify a backup certificate for JWT signing operations, improving resilience during certificate rotation or temporary availability issues.
* When the primary certificate fails to load or sign a token, the gateway automatically attempts the fallback certificate before resorting to the default HMAC certificate.
* Certificate fallback settings can be updated via the Management API or Console UI without triggering a domain reload, allowing administrators to adjust behavior during certificate rotation without downtime.
* Master domains can reference certificates from any domain in the organization for cross-domain introspection; non-master domains are restricted to their own domain scope.
<!-- /PIPELINE:AM-6339 -->

## Improvements

## Bug Fixes
