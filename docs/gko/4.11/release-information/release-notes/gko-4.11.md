# GKO 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:GKO-2006 -->
#### **mTLS Client Certificate Management**

* GKO Application CRD now support multiple client certificate with validity and rotation management for application-level mutual TLS.
* Administrators can now upload, validate, and rotate authentication directly through the Management Console (for application managed outside of GKO)
* Supports PKCS7 certificate bundles, scheduled certificate activation, and grace-period rotation to prevent downtime during certificate updates.
* Certificates are validated on upload (SHA-256 fingerprint, uniqueness) and progress through lifecycle states: Scheduled, Active, Active with End Date, and Revoked.
* Requires APIM 4.11 or above and a TLS-enabled gateway endpoint with an mTLS plan configured for the application.
<!-- /PIPELINE:GKO-2006 -->

## Improvements

## Bug Fixes
