# GKO 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:GKO-2006 -->
#### **Multi-Certificate mTLS Support for Applications**

* Applications can now register multiple client certificates for mutual TLS authentication, enabling certificate rotation and lifecycle management without service interruption.
* Each certificate supports independent validity periods with ACTIVE, SCHEDULED, and REVOKED states, allowing planned certificate transitions and immediate revocation when needed.
* Supports both single PEM certificates and PKCS7 certificate bundles, with SHA-256 fingerprint-based authentication and automatic certificate extraction from bundles.
* Requires Gravitee APIM 4.10 or later for SHA-256 fingerprint support; certificates can be provided inline or referenced from Kubernetes Secrets/ConfigMaps.
<!-- /PIPELINE:GKO-2006 -->

## Improvements

## Bug Fixes
