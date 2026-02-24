# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6339 -->
#### **Certificate Fallback for JWT Signing**

* Administrators can now configure a domain-level fallback certificate that automatically activates when a client's primary certificate fails during JWT signing operations.
* The system follows a three-tier selection hierarchy: client certificate → domain fallback certificate → domain HMAC certificate (if enabled), preventing service disruption during certificate rotation or temporary outages.
* Configure fallback certificates via the Management API (`PUT /domains/{domain}/certificate-settings`) with the `fallbackCertificate` property—changes propagate to all gateway nodes in real time without requiring domain restarts.
* Master domains can access certificates from all domains to support cross-domain introspection, while regular domains are restricted to their own certificates for security isolation.
<!-- /PIPELINE:AM-6339 -->

## Improvements

## Bug Fixes
