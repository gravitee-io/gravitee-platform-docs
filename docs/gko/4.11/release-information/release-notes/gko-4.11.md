# GKO 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:GKO-2006 -->
#### **Client Certificate Management for Applications**

* Attach X.509 certificates to applications for mutual TLS authentication with automatic lifecycle management based on validity periods.
* Certificates are identified by SHA-256 fingerprint and enforced unique per environment—preventing certificate sharing across active applications while enabling rotation.
* Each certificate receives a cross-environment identifier (`crossId`) to track the same logical certificate across development, staging, and production environments.
* Certificate body is immutable after creation—update name and validity dates via API, or delete and recreate to rotate certificates.
* Requires `APPLICATION_DEFINITION[CREATE]` permission and valid PEM-encoded X.509 certificates.
<!-- /PIPELINE:GKO-2006 -->

## Improvements

## Bug Fixes
