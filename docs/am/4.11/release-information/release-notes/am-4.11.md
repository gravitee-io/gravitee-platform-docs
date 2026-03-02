# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6339 -->
#### **Domain Certificate Fallback**

* Administrators can now configure a default certificate at the domain level that AM uses when an application or identity provider does not specify its own certificate, preventing service interruptions from missing or failed certificates.
* The system follows a three-tier resolution order: client-specified certificate, domain fallback certificate, then default HMAC certificate (if legacy fallback is enabled). Fallback usage is logged at WARN level.
* System certificates (pre-installed platform-managed certificates) are now available for selection as fallback certificates alongside user-created certificates.
* Certificates configured as domain fallback cannot be deleted. Non-master domains can only access certificates from their own domain, while master domains can access certificates from all domains.
* Configure fallback certificates via the Management API at `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/certificate-settings` with `DOMAIN_SETTINGS[UPDATE]` permission.
<!-- /PIPELINE:AM-6339 -->

## Improvements

## Bug Fixes
