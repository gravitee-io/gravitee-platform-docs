# Multi-Certificate mTLS Prerequisites and Restrictions

## PKCS7 Bundle Support

Certificates can be uploaded as PKCS7/CMS bundles containing multiple X.509 certificates. The gateway extracts all certificates from the bundle, computes individual SHA-256 fingerprints, and registers each certificate in the subscription trust store with alias `{subscriptionId}_{index}`. If PKCS7 parsing fails, the system falls back to PEM parsing for single-certificate data.

## Fingerprint-Based Subscription Lookup

The gateway indexes subscriptions by SHA-256 certificate fingerprint. During TLS handshake, the gateway computes the fingerprint of the presented client certificate and performs cache lookup using keys `{api}.{plan}.{fingerprint}` and `{api}.{fingerprint}` (plan-agnostic). Multiple certificates per subscription are supported, with each fingerprint mapping to the same subscription record.

## Prerequisites

Before configuring multi-certificate mTLS, ensure the following requirements are met:

* Gravitee APIM 4.11.x or above (plugin version 2.x)
* TLS-enabled gateway with client certificate authentication
* For Kubernetes deployments: gravitee-kubernetes-operator with Application CRD v1alpha1

## Gateway Configuration

### Database Schema

The `client_certificates` table stores certificate metadata and PEM-encoded content. Required indexes ensure efficient lookup by application and environment.

**JDBC Schema**:

| Column | Type | Constraints | Description |
|:-------|:-----|:------------|:------------|
| `id` | NVARCHAR(64) | PRIMARY KEY | Certificate identifier |
| `cross_id` | NVARCHAR(64) | NOT NULL | Cross-environment reference |
| `application_id` | NVARCHAR(64) | NOT NULL, INDEXED | Parent application |
| `name` | NVARCHAR(512) | NOT NULL | Certificate label |
| `certificate` | NCLOB | NOT NULL | PEM-encoded certificate |
| `fingerprint` | NVARCHAR(256) | — | SHA-256 thumbprint |
| `status` | NVARCHAR(32) | NOT NULL | Lifecycle state |
| `environment_id` | NVARCHAR(64) | NOT NULL, INDEXED | Environment scope |
| `starts_at` | TIMESTAMP | — | Validity start |
| `ends_at` | TIMESTAMP | — | Validity end |

**Required Indexes**:

* `idx_{prefix}client_certificates_application_id` on `application_id`
* `idx_{prefix}client_certificates_environment_id` on `environment_id`
* `idx_{prefix}client_certificates_app_id_status` on `(application_id, status)`

MongoDB deployments use the `client_certificates` collection with indexes on `applicationId` (alias `a1`) and `environmentId` (alias `e1`).

### Trust Store Configuration

The gateway automatically builds subscription trust stores from registered certificates. For each subscription, certificates are decoded from Base64, parsed as PKCS7 bundles (with PEM fallback), and added to a `KeyStore` instance. The trust store is registered with `SubscriptionTrustStoreLoaderManager` and indexed by SHA-256 fingerprint. When certificates change, old fingerprints are evicted from cache and new fingerprints are indexed.

## Managing Certificate Lifecycle

Certificates transition automatically based on validity windows: `SCHEDULED` certificates become `ACTIVE` or `ACTIVE_WITH_END` when `startsAt` is reached, and `ACTIVE_WITH_END` certificates remain valid until `endsAt`. To revoke a certificate, update its status to `REVOKED` via the Management API.  The `existsByFingerprintAndActiveApplication` repository method excludes `REVOKED` certificates when checking fingerprint uniqueness, allowing fingerprint reuse after revocation. Deleting an application cascades to all associated certificates via `deleteByApplicationId`.

## End-User Configuration

### Application TLS Settings

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `settings.tls.clientCertificate` | string | — | **Deprecated**. Single PEM/Base64 certificate. Mutually exclusive with `clientCertificates`. |
| `settings.tls.clientCertificates` | array | — | List of client certificates. Each entry supports inline content or external reference. |
| `settings.tls.certificate_count` | number | — | Read-only. Number of active certificates (UI display only). |

### ClientCertificate Object

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `name` | string | `{appName}-{index}` | Certificate label |
| `content` | string | — | Inline PEM/Base64 or template `[[ ]]` notation |
| `ref` | object | — | Reference to Secret or ConfigMap |
| `ref.kind` | string | `secrets` | Resource type: `secrets` or `configmaps` |
| `ref.name` | string | — | Resource name |
| `ref.key` | string | `tls.crt` | Data key in resource |
| `ref.namespace` | string | (app namespace) | Resource namespace |
| `startsAt` | string (RFC3339) | — | Validity start date |
| `endsAt` | string (RFC3339) | — | Validity end date |
| `encoded` | boolean | `false` | Whether content is base64-encoded |

### Management API

The `ClientCertificateRepository` interface provides pagination and filtering methods for certificate management.

| Method | Parameters | Returns | Description |
|:-------|:-----------|:--------|:------------|
| `findByApplicationId` | `applicationId`, `Pageable` | `Page<ClientCertificate>` | Paginated certificate list (1-based page numbers) |
| `findByApplicationIdAndStatuses` | `applicationId`, `Collection<Status>` | `Set<ClientCertificate>` | Filter by status (`ACTIVE`, `SCHEDULED`, etc.) |
| `existsByFingerprintAndActiveApplication` | `fingerprint`, `environmentId` | `boolean` | Check fingerprint uniqueness (excludes `REVOKED`) |
| `deleteByApplicationId` | `applicationId` | `void` | Delete all application certificates |

## Restrictions

* `clientCertificate` and `clientCertificates` fields cannot be used simultaneously (validation enforced at admission controller and API level)
* Requires Gravitee APIM 4.11.x or above for plugin version 2.x
* SHA-256 fingerprint algorithm is mandatory; MD5 digests from prior versions are incompatible and require subscription re-registration
* PKCS7 bundles must contain at least one certificate unless `allowEmpty=true` is set
* Fingerprint uniqueness is enforced per environment for active applications only (`REVOKED` certificates excluded)
* Pagination uses 1-based page numbers in API calls but 0-based indexing in repository layer (fixed in PR #15283)
* Template notation (`[[ secret ... ]]`) requires `ENABLE_TEMPLATING=true` environment variable in Kubernetes operator

## Related Changes


The Console UI now displays a warning banner when `certificateCount > 1`, indicating "This application has {count} active certificates. The one displayed is the most recently created." The deprecated `Client Certificate` field remains visible for backward compatibility.
 The mTLS policy error templates include three keys: `CLIENT_CERTIFICATE_MISSING` (no certificate provided), `CLIENT_CERTIFICATE_INVALID` (malformed certificate), and `SSL_SESSION_REQUIRED` (TLS session absent). Error templates are configured in API Console → Entrypoints → Response Templates for v4 APIs or Response Templates for v2 APIs. The Bouncycastle `bcpkix-jdk18on` dependency scope changed from `test` to `compile` to support PKCS7 parsing in production. Database migrations add the `client_certificates` table with three indexes for JDBC deployments and two indexes for MongoDB collections.
