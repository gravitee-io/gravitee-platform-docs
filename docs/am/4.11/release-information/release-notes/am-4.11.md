# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6339 -->
#### **Domain-Level Certificate Fallback**

* Administrators can now configure a fallback certificate at the domain level that is automatically used when a client or application does not have a specific certificate configured, preventing service interruptions during JWT signing operations.
* Certificate resolution follows a hierarchy: client-specified certificate → domain fallback certificate → default HMAC certificate → error if all options are exhausted.
* System certificates are now visible in certificate selection dialogs, allowing them to be designated as domain-level fallbacks.
* Certificates configured as domain fallbacks cannot be deleted until removed from the domain's certificate settings.
* Requires `DOMAIN_SETTINGS[UPDATE]` permission to configure fallback certificates via the Management API endpoint `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/certificate-settings`.
<!-- /PIPELINE:AM-6339 -->

## Improvements

## Bug Fixes
