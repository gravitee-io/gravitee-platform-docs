# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6339 -->
#### **Certificate Fallback for JWT Signing**

* Access Management now supports domain-level fallback certificates for JWT signing operations, providing resilience when a client's primary certificate fails to load or sign tokens.
* When the primary certificate is unavailable, the system automatically attempts signing with the configured fallback certificate before falling back to the default HMAC certificate or failing the operation.
* Configure fallback certificates using the Management API endpoint `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/certificate-settings` without triggering a full domain reload.
* Fallback certificates must belong to the same domain unless the domain is configured as a master domain, and the system automatically skips the fallback if its ID matches the primary certificate ID.
<!-- /PIPELINE:AM-6339 -->

## Improvements

## Bug Fixes
