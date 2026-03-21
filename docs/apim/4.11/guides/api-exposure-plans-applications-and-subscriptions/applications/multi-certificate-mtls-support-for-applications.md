# Multi-Certificate mTLS Support for Applications

## Overview

Multi-Certificate mTLS Support enables applications to register multiple client certificates for mutual TLS authentication against API plans. Applications can manage certificate rotation and lifecycle by maintaining active, scheduled, and revoked certificates simultaneously. This feature supports both single PEM certificates and PKCS7 certificate bundles.

## Key Concepts

### Client Certificates

Applications can register multiple client certificates, each with its own validity period and lifecycle status. Each certificate is identified by a SHA-256 fingerprint and can be in one of four states:

* **ACTIVE**: Certificate with no end date
* **ACTIVE_WITH_END**: Certificate with an expiration timestamp
* **SCHEDULED**: Certificate with a future activation timestamp
* **REVOKED**: Certificate that has been invalidated

The system enforces fingerprint uniqueness across all active applications in an environment, preventing certificate reuse.

| Property | Description | Example |
|:---------|:------------|:--------|
| `id` | Unique certificate identifier | `cert-abc123` |
| `applicationId` | Owning application ID | `app-456` |
| `name` | User-defined certificate name | `cert-2026` |
| `startsAt` | Optional activation timestamp | `2024-01-01T00:00:00Z` |
| `endsAt` | Optional expiration timestamp | `2026-12-31T23:59:59Z` |
| `fingerprint` | SHA-256 certificate thumbprint | `u21dNKud2YsKNJn3HQTTon1_qSoZi8IrBTsLiZCFQLg` |
| `status` | Certificate lifecycle state | `ACTIVE`, `SCHEDULED`, `REVOKED` |

### PKCS7 Certificate Bundles

Subscriptions can use PKCS7-encoded certificate bundles containing multiple certificates. When a bundle is uploaded, each certificate is extracted and assigned an alias in the format `{subscriptionId}_{index}`. The system computes a SHA-256 fingerprint for each certificate in the bundle. If PKCS7 parsing fails, the system falls back to single PEM certificate parsing.

### Certificate Validation Flow

When a client connects with mTLS, the gateway extracts the peer certificate from the TLS session and computes its SHA-256 fingerprint. This fingerprint is used to create a security token and look up the corresponding subscription in the cache using the key `{api}.{plan}.{sha256(cert)}`. For PKCS7 bundles, each certificate in the bundle is indexed separately, allowing any certificate in the bundle to authenticate the subscription.

## Prerequisites

* Gravitee APIM 4.10 or later
* API with an mTLS-enabled plan
* Client certificates in PEM or PKCS7 format
* For Kubernetes deployments: [gravitee-kubernetes-operator](../../gko/4.11/overview/custom-resource-definitions/application.md) with Application CRD support

## Creating Client Certificates

To add client certificates to an application, use the `clientCertificates` array in the application's TLS settings. Each certificate requires either inline PEM content or a reference to a Kubernetes Secret or ConfigMap.

1. Specify a unique name for each certificate. If omitted, the system defaults to `app-name-{index}`.
2. Provide the certificate content directly as PEM or Base64, or use a `ref` object pointing to a Secret or ConfigMap.
3. Optionally set `startsAt` and `endsAt` timestamps in RFC3339 format to control certificate validity periods.
4. If using Base64-encoded content, set `encoded: true`.
5. For Secret/ConfigMap references, specify `kind` (secrets or configmaps), `name`, and optionally `key` (defaults to `tls.crt`) and `namespace` (defaults to Application namespace).

The system validates that each certificate has either content or a reference, but not both, and computes a SHA-256 fingerprint upon creation.

## Managing Certificate Lifecycle

Certificates transition through lifecycle states based on their validity periods and administrative actions.

1. Certificates with no `endsAt` timestamp are marked ACTIVE.
2. Certificates with a future `startsAt` timestamp are marked SCHEDULED until the activation time.
3. Certificates with an `endsAt` timestamp are marked ACTIVE_WITH_END and remain valid until expiration.
4. Administrators can manually revoke certificates by setting status to REVOKED, which excludes them from fingerprint uniqueness checks and subscription lookups.

The UI displays a warning banner when an application has multiple active certificates, showing the count and noting that the displayed certificate is the most recently created.

### Kubernetes Application CRD

For Kubernetes deployments, certificates can be specified using inline content, Secret/ConfigMap references, or template notation.

* **Inline certificates**: Use the `content` field with PEM or Base64 data.
* **References**: Use the `ref` object with `kind: secrets` or `kind: configmaps`, a `name`, and optional `key` and `namespace`.
* **Template notation**: Use the format `[[ secret 'secret-name/key' ]]` or `[[ configmap 'configmap-name/key' ]]`. Requires `ENABLE_TEMPLATING=true` in the operator configuration.

## End-User Configuration

## Restrictions

* Requires Gravitee APIM 4.10 or later
* Certificate fingerprints are now SHA-256 (previously MD5). Existing subscriptions using MD5 fingerprints will fail validation until re-registered.
* Existing cached subscriptions will be invalidated on upgrade due to cache key format change from `{api}.{clientCertificate}.{plan}` to `{api}.{plan}.{sha256(clientCertificate)}`.
