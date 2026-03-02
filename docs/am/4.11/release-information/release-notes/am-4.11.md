# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6339 -->
#### **Domain Certificate Fallback**

* Administrators can now configure a default certificate at the domain level that AM uses when applications or identity providers do not specify their own certificate, preventing service interruptions from missing or failed certificates.
* The fallback certificate applies to JWT signing, OAuth token generation, and client authentication flows, following a three-tier resolution: client-specified certificate, domain fallback certificate, then legacy HMAC certificate.
* Configure the fallback certificate via the Management API (`PUT /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/certificate-settings`) or the Admin Console under Domain Settings > Certificates.
* The fallback certificate must belong to the same domain and cannot be deleted while configured as the domain's fallback.
* System certificates (pre-installed certificates managed by AM) are now available for selection as fallback certificates alongside user-uploaded certificates.
<!-- /PIPELINE:AM-6339 -->

## Improvements

## Bug Fixes
