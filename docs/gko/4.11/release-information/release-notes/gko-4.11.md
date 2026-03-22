# GKO 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:GKO-2006 -->
#### **Multi-Certificate mTLS Support for Applications**

* Applications can now authenticate with multiple client certificates per subscription, replacing the previous single-certificate limitation.
* Certificates can be uploaded as individual PEM files or PKCS7 bundles, with automatic SHA-256 fingerprint indexing for subscription lookup during TLS handshake.
* Each certificate includes lifecycle status tracking (`SCHEDULED`, `ACTIVE`, `ACTIVE_WITH_END`, `REVOKED`) and optional validity windows for automated rotation workflows.
* Requires APIM 4.11.x or above with TLS-enabled gateway and client certificate authentication configured.
<!-- /PIPELINE:GKO-2006 -->

## Improvements

## Bug Fixes
