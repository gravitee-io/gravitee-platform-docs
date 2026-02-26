# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6339 -->
#### **Certificate Fallback for Domain Security**

* Configure a domain-level fallback certificate that automatically activates when a client's primary JWT signing certificate becomes unavailable, preventing service disruptions.
* The system follows a deterministic resolution chain: primary certificate → fallback certificate → default certificate (if HMAC fallback enabled), ensuring maximum availability while maintaining security boundaries.
* Master domains can access certificates from any domain for cross-domain introspection scenarios, while regular domains are restricted to their own certificate scope.
* Configure fallback certificates via the Management Console or REST API (`PUT /organizations/{orgId}/environments/{envId}/domains/{domain}/certificate-settings`) without requiring domain restart.
* Monitor fallback usage through detailed log messages that identify which certificate was used for each signing operation.
<!-- /PIPELINE:AM-6339 -->

## Improvements

## Bug Fixes
