# GKO 4.10

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:GKO-2006 -->
#### **Client Certificate Management for Applications**

* Applications can now store X.509 client certificates for mutual TLS authentication, enabling secure API access with certificate-based identity verification.
* Certificates are validated for uniqueness within an environment using SHA-256 fingerprints and automatically transition through lifecycle states (SCHEDULED, ACTIVE, ACTIVE_WITH_END, REVOKED) based on validity periods.
* Manage certificates via REST API endpoints supporting CRUD operations, pagination, and automatic cleanup when applications are deleted.
* Requires `APPLICATION_DEFINITION[CREATE]` permission to add certificates and valid PEM-encoded X.509 format with no fingerprint conflicts across active applications in the same environment.
<!-- /PIPELINE:GKO-2006 -->

## Improvements

## Bug Fixes
