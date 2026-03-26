# GKO 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:GKO-2006 -->
#### **mTLS Client Certificate Management**

* The GKO Application CRD now supports multiple client certificates with validity and rotation management for application-level mutual TLS.
* Administrators can now upload, validate, and rotate client certificates directly through the Management Console (for applications managed outside of GKO).
* Supports scheduled certificate activation and grace-period rotation to prevent downtime during certificate updates.
* Certificates are validated on upload (SHA-256 fingerprint, uniqueness) and progress through lifecycle states: Scheduled, Active, Active with End Date, and Revoked.
* Requires APIM 4.11 or above and an API with an mTLS plan subscribed for the application.
<!-- /PIPELINE:GKO-2006 -->

## Improvements

## Bug Fixes
