# GKO 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:GKO-2006 -->
#### **mTLS Client Certificate Management**

* Applications can now authenticate API requests using X.509 client certificates with automatic validation and rotation support.
* Configure multiple certificates per application with validity windows (startsAt/endsAt) that automatically transition through SCHEDULED, ACTIVE, ACTIVE_WITH_END, and REVOKED statuses.
* The gateway validates certificate SHA-256 fingerprints against subscriptions during TLS handshake, with fingerprints indexed by API, plan, and certificate for fast lookup.
* Certificates can be defined inline as PEM/Base64 content or referenced from Kubernetes Secrets/ConfigMaps using the `settings.tls.clientCertificates` array.
* The deprecated single-certificate property (`settings.tls.clientCertificate`) remains supported but is mutually exclusive with the new multi-certificate configuration.
<!-- /PIPELINE:GKO-2006 -->

## Improvements

## Bug Fixes
