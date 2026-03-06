# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6339 -->
#### **Domain Fallback Certificate Configuration**

* Administrators can now configure a domain-level fallback certificate that is automatically used when applications or identity providers do not have a specific certificate configured, preventing service interruptions for JWT signing and mTLS operations.
* The fallback certificate is selected from existing domain certificates via the Management API or Console UI, with master domains able to access certificates from all domains while regular domains are restricted to their own certificates.
* Certificate resolution follows a priority order: client-specified certificate, domain fallback certificate, default HMAC certificate (if enabled), or error if all options are exhausted, with each fallback attempt logged as a warning.
* Certificates configured as the domain fallback cannot be deleted, and the feature requires `DOMAIN_SETTINGS[UPDATE]` permission to configure.
* System certificates are now visible in the fallback certificate selection interface, and configuration changes trigger a lightweight update event without requiring a full domain reload.
<!-- /PIPELINE:AM-6339 -->

## Improvements

## Bug Fixes
