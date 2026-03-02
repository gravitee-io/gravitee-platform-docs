# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6339 -->
#### **Domain-Level Certificate Fallback**

* Administrators can now configure a fallback certificate at the domain level that is automatically used when a client or application does not have a specific certificate assigned.
* The system follows a strict priority order: client-specific certificate, domain fallback certificate, default HMAC certificate (if enabled), or error if none are available.
* If JWT signing fails with the primary certificate, the system automatically retries with the fallback certificate before propagating the error.
* Fallback certificates must belong to the same domain (except for master domains) and cannot be deleted while configured as a domain's fallback certificate.
* Configure fallback certificates via the `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/certificate-settings` endpoint with `DOMAIN_SETTINGS[UPDATE]` permission.
<!-- /PIPELINE:AM-6339 -->

## Improvements

## Bug Fixes
