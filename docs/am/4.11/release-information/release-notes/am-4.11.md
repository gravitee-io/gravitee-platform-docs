# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6339 -->
#### **Domain Certificate Fallback**

* Administrators can now configure a domain-level fallback certificate that automatically serves as a backup when an application or identity provider's primary certificate fails during JWT signing operations.
* The fallback certificate applies to ID tokens, userinfo responses, and authorization responses, preventing service disruptions without manual intervention.
* System certificates are now eligible for selection as fallback certificates, allowing built-in certificates to serve as domain-wide defaults.
* Certificates configured as the domain fallback cannot be deleted until removed from the certificate settings.
* Configure via Management API endpoint `PUT /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/certificate-settings` with `DOMAIN_SETTINGS[UPDATE]` permission.
<!-- /PIPELINE:AM-6339 -->

## Improvements

## Bug Fixes
