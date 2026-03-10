# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6339 -->
#### **Domain-Level Certificate Fallback**

* Administrators can configure a fallback certificate at the domain-level to prevent authentication failures when a certificate that is explicitly configured for an application cannot be used.
* When an application's certificate fails to load (e.g., external provider unavailable), the system automatically uses the domain's fallback certificate to sign OAuth and ID tokens.
* Fallback certificates are configured using the Management API (`/domains/{domain}/certificate-settings`) and require `DOMAIN_SETTINGS[UPDATE]` permission.
* Certificates configured as domain fallback cannot be deleted until removed from the fallback configuration.
<!-- /PIPELINE:AM-6339 -->

## Improvements

## Bug Fixes
