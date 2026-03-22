# GKO 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:GKO-2006 -->
#### **Multi-Certificate mTLS Support for Applications**

* Applications can now authenticate with multiple client certificates instead of a single certificate, enabling certificate rotation, gradual migration, and multi-environment deployments.
* Each certificate includes lifecycle status (ACTIVE, ACTIVE_WITH_END, SCHEDULED, REVOKED) and optional start/end dates for scheduled rotation.
* The gateway uses SHA-256 fingerprints to match incoming TLS client certificates to subscriptions, with support for PKCS7 certificate bundles that are automatically parsed and indexed.
* The Console UI displays a banner when an application has multiple active certificates, showing the most recently created certificate by default.
* API plans must be configured to require mTLS authentication, and client certificates must be provided in PEM or PKCS7 format.
<!-- /PIPELINE:GKO-2006 -->

## Improvements

## Bug Fixes
