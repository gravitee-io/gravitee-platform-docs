# GKO 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:GKO-2006 -->
#### **Multi-Certificate mTLS Support for Applications**

* Applications can now authenticate to APIs using multiple client certificates in a single subscription, enabling certificate rotation and multi-environment deployments without service interruption.
* The gateway validates incoming requests against all registered certificates by computing SHA-256 fingerprints and matching them to the TLS session peer certificate.
* Supports PKCS7 certificate bundles and individual PEM certificates with optional validity windows (`startsAt`, `endsAt`) for scheduled activation and expiration.
* Certificates can be stored inline (PEM or Base64) or referenced from Kubernetes Secrets/ConfigMaps using the `settings.tls.clientCertificates` array in the Application CRD.
* The UI displays a warning banner when multiple certificates are active, showing the count and indicating which certificate is displayed (most recently created).
<!-- /PIPELINE:GKO-2006 -->

## Improvements

## Bug Fixes
