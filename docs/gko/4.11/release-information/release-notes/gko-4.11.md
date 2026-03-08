# GKO 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:GKO-2006 -->
#### **Client Certificate Management for Applications**

* Administrators can now create, update, and delete TLS client certificates for applications consuming mTLS-secured APIs through REST API endpoints.
* Certificates transition through lifecycle states (`ACTIVE`, `SCHEDULED`, `REVOKED`) based on configurable start and end dates, enabling zero-downtime certificate rotation via grace periods.
* Each certificate is uniquely identified by SHA-256 fingerprint and cannot be reused across active applications within the same environment.
* Requires `APPLICATION_DEFINITION[CREATE]`, `[UPDATE]`, or `[DELETE]` permissions depending on the operation.
<!-- /PIPELINE:GKO-2006 -->

## Improvements

## Bug Fixes
