# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6339 -->
#### **Domain-Level Certificate Fallback**

* Administrators can now configure a fallback certificate at the domain level that automatically activates when client-specific certificates fail to load or are unavailable.
* The certificate manager resolves certificates in a three-tier hierarchy: client-specific certificate, domain fallback certificate, and default HMAC certificate (if enabled).
* Fallback certificates prevent service disruptions during certificate rotation or misconfiguration by providing a domain-wide safety net for JWT signing and client authentication operations.
* Configure fallback certificates via the Management API endpoint `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/certificate-settings` with `DOMAIN_SETTINGS[UPDATE]` permission.
* Regular domains can only use certificates that belong to the same domain, while master domains can access certificates across all domains for cross-domain introspection.
<!-- /PIPELINE:AM-6339 -->

## Improvements

## Bug Fixes
