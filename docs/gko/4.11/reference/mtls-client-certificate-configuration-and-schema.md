# mTLS Client Certificate Configuration and Schema

## Overview

mTLS Client Certificate Management enables applications to authenticate API requests using X.509 client certificates. Administrators can configure multiple certificates per application with validity windows and automatic rotation, while the gateway validates certificate fingerprints against subscriptions. This feature supports both single-certificate (deprecated) and multi-certificate configurations.

## Key Concepts

### Client Certificates

A client certificate is an X.509 certificate presented by an application during TLS handshake to authenticate API requests. Each certificate includes a name, PEM-encoded content, validity dates (`startsAt`/`endsAt`), and computed metadata (subject, issuer, SHA-256 fingerprint). Certificates transition through statuses: `SCHEDULED` (before `startsAt`), `ACTIVE` (within validity window), `ACTIVE_WITH_END` (active with defined `endsAt`), and `REVOKED` (manually disabled).

| Status | Display Label | Meaning |
|:-------|:--------------|:--------|
| `ACTIVE` | Active | Certificate valid, no end date defined |
| `ACTIVE_WITH_END` | Active (with end date) | Certificate valid with defined expiration |
| `SCHEDULED` | Scheduled | Certificate not yet valid (before `startsAt`) |
| `REVOKED` | Revoked | Certificate manually disabled |

### Certificate Fingerprints

The gateway computes a SHA-256 digest of the client certificate presented during TLS handshake and uses this fingerprint to look up the associated subscription. Fingerprints must be unique across all active applications (status != `REVOKED`) within an environment. The subscription cache indexes certificates by API, plan, and fingerprint for fast validation.

### PKCS7 Certificate Bundles

Multiple certificates can be packaged into a single PKCS7/CMS binary bundle. The gateway parses PKCS7 bundles into Java KeyStore objects for trust validation.

## Prerequisites

Before configuring client certificates, ensure the following requirements are met:

* TLS termination configured at the gateway or load balancer
* Client applications capable of presenting X.509 certificates during TLS handshake
* Certificate authority (CA) infrastructure for issuing client certificates
* For Kubernetes deployments: certificates stored in Secrets or ConfigMaps

## Gateway Configuration

### Application Certificate Settings

Configure client certificates in the application's TLS settings. Use either the deprecated single-certificate property or the multi-certificate array. Both cannot be set simultaneously.

| Property | Type | Description | Example |
|:---------|:-----|:------------|:--------|
| `settings.tls.clientCertificate` | `string` | **Deprecated**. Single PEM/Base64 certificate. Mutually exclusive with `clientCertificates`. | `"-----BEGIN CERTIFICATE-----\n..."` |
| `settings.tls.clientCertificates` | `ClientCertificate[]` | List of client certificates. Mutually exclusive with `clientCertificate`. | See Client Certificate Object |
| `settings.tls.certificate_count` | `number` | Read-only count of active certificates for the application. | `3` |

### Client Certificate Object

Each certificate in the `clientCertificates` array contains the following properties:

| Property | Type | Description | Example |
|:---------|:-----|:------------|:--------|
| `name` | `string` | Optional label. Defaults to `{appName}-{index}`. | `"prod-cert-2024"` |
| `content` | `string` | Inline PEM/Base64 certificate or template `[[ ]]` notation. Mutually exclusive with `ref`. | `"-----BEGIN CERTIFICATE-----\n..."` |
| `ref` | `CertificateRef` | Reference to Kubernetes Secret or ConfigMap. Mutually exclusive with `content`. | See Certificate Reference Object |
| `startsAt` | `string` | RFC3339 validity start date. Certificate becomes `ACTIVE` at this time. | `"2024-01-01T00:00:00Z"` |
| `endsAt` | `string` | RFC3339 validity end date. Certificate transitions to `REVOKED` after this time. | `"2025-01-01T00:00:00Z"` |
| `encoded` | `boolean` | Whether `content` is base64 encoded. Defaults to `false`. | `true` |

**Configuration restrictions:**

* Either `content` or `ref` must be set. Both cannot be set simultaneously.
* If `content` is provided, it must be valid PEM format or base64-encoded PEM.
* If `encoded` is `true`, `content` must be valid base64.
* `startsAt` and `endsAt` must use RFC3339 format.
* SHA-256 fingerprint must be unique across all active applications in the environment.

### Certificate Reference Object (Kubernetes)

When using `ref` instead of inline `content`, reference a Secret or ConfigMap:

| Property | Type | Description | Example |
|:---------|:-----|:------------|:--------|
| `kind` | `string` | Resource type. Enum: `secrets`, `configmaps`. | `"secrets"` |
| `name` | `string` | Name of Secret or ConfigMap. | `"app-tls-cert"` |
| `key` | `string` | Key in data map. Defaults to `"tls.crt"`. | `"client.crt"` |
| `namespace` | `string` | Namespace of referenced resource. Defaults to application namespace. | `"production"` |

### Database Schema

The gateway stores client certificates in the `client_certificates` table with the following columns:

| Column | Type | Description |
|:-------|:-----|:------------|
| `id` | `nvarchar(64)` | Primary key |
| `cross_id` | `nvarchar(64)` | Cross-environment identifier |
| `application_id` | `nvarchar(64)` | Owning application |
| `name` | `nvarchar(512)` | Certificate label |
| `starts_at` | `timestamp` | Validity start date |
| `ends_at` | `timestamp` | Validity end date |
| `created_at` | `timestamp` | Creation timestamp |
| `updated_at` | `timestamp` | Last update timestamp |
| `certificate` | `nclob` | PEM-encoded certificate content |
| `certificate_expiration` | `timestamp` | Parsed expiration from X.509 |
| `subject` | `nvarchar(1024)` | X.509 subject DN |
| `issuer` | `nvarchar(1024)` | X.509 issuer DN |
| `fingerprint` | `nvarchar(256)` | SHA-256 digest |
| `environment_id` | `nvarchar(64)` | Environment scope |
| `organization_id` | `nvarchar(64)` | Organization scope |
| `status` | `nvarchar(32)` | Certificate status enum |

Composite index `idx_client_certificates_app_id_status` on `(application_id, status)`.

## Creating Client Certificates

Configure certificates in the application's TLS settings by adding entries to the `clientCertificates` array:

1. Set the `name` property to a descriptive label or omit it to use the default `{appName}-{index}` format.
2. Provide the certificate content either inline via the `content` property (PEM or Base64) or by reference using `ref` to point to a Kubernetes Secret or ConfigMap.
3. Optionally define `startsAt` and `endsAt` in RFC3339 format to schedule certificate activation and expiration.
4. If using base64-encoded content, set `encoded: true`.

The gateway computes the SHA-256 fingerprint, subject, issuer, and expiration date automatically upon creation.

{% hint style="info" %}
When multiple certificates exist, the UI displays a banner: "This application has {count} active certificates. The one displayed is the most recently created."
{% endhint %}

## Validating Client Certificates

The gateway validates client certificates during API request processing. The validation flow extracts the TLS session from the request context, computes the SHA-256 fingerprint of the presented certificate, and looks up the associated subscription in the cache by API, plan, and fingerprint. If no TLS session is present, the gateway returns an `SSL_SESSION_REQUIRED` error. If no certificate is presented, the gateway returns a `CLIENT_CERTIFICATE_MISSING` error. If the fingerprint does not match an active subscription, the gateway returns a `CLIENT_CERTIFICATE_INVALID` error.

**PKCS7 bundle support:**

The gateway requires the BouncyCastle library (`bcpkix-jdk18on`) to parse PKCS7 certificate bundles. The library scope changed from `test` to `compile` to enable runtime bundle parsing into Java KeyStore objects.
