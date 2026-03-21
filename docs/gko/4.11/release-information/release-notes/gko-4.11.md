# GKO 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:GKO-2006 -->
#### **PKCS7 Certificate Bundle Support for mTLS Subscriptions**

* Applications can now present multiple client certificates for mTLS authentication against a single subscription by uploading PKCS7 certificate bundles containing multiple X.509 certificates.
* The gateway automatically detects PKCS7 format, extracts individual certificates, and validates client connections against any certificate in the bundle using SHA-256 thumbprints.
* Each certificate in a bundle receives a unique alias and independent cache entry, enabling flexible certificate rotation without subscription changes.
* Requires database schema migration to add the `client_certificates` table (MongoDB or JDBC-compatible databases with schema version 02 or later).
* Certificate lifecycle management supports `ACTIVE`, `ACTIVE_WITH_END`, `SCHEDULED`, and `REVOKED` statuses for granular control over certificate validity windows.
<!-- /PIPELINE:GKO-2006 -->

## Improvements

## Bug Fixes
