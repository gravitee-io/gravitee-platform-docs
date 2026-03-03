# GKO 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:GKO-2006 -->
#### **Client Certificate Management for Applications**

* Applications can now store and manage X.509 client certificates for mutual TLS authentication with backend services.
* Certificates transition automatically through lifecycle states (SCHEDULED, ACTIVE, ACTIVE_WITH_END, REVOKED) based on configured start and end dates.
* The platform enforces SHA-256 fingerprint uniqueness across active applications in the same environment to prevent accidental certificate reuse.
* Administrators can create, update metadata, list, and delete certificates via REST API endpoints under `/applications/{application}/certificates`.
* Requires `APPLICATION_DEFINITION[CREATE]`, `[UPDATE]`, or `[DELETE]` permissions depending on the operation.
<!-- /PIPELINE:GKO-2006 -->

## Improvements

## Bug Fixes
