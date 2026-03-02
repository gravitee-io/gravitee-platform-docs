# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6339 -->
#### **Domain Certificate Fallback Configuration**

* Administrators can now configure a fallback certificate at the domain level that the Access Management gateway uses when a client-specific certificate is unavailable or fails to load, preventing authentication failures in multi-tenant environments.
* The gateway follows a certificate selection hierarchy: client-specific certificate → domain fallback certificate → default HMAC certificate (if legacy fallback is enabled) → error. The gateway logs warnings when falling back from a configured certificate.
* Configure fallback certificates via the REST API endpoint `PUT /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/certificate-settings`. The fallback certificate must belong to the same domain and cannot be deleted while configured as a fallback.
* Certificate settings updates trigger a `DOMAIN_CERTIFICATE_SETTINGS` event rather than a full domain reload, allowing configuration changes without service interruption.
* Master domains can access certificates from all domains to support cross-domain introspection workflows, while regular domains can only access certificates within their own domain scope.
<!-- /PIPELINE:AM-6339 -->

## Improvements

## Bug Fixes
