
# mTLS Client Certificate Configuration Reference

## Gateway Configuration


### Application TLS Settings

Configure client certificates in the application's TLS settings. Use either the deprecated `clientCertificate` field (single certificate) or the new `clientCertificates` array (multiple certificates). The two fields are mutually exclusive.

| Property | Description | Example |
|:---------|:------------|:--------|
| `settings.tls.clientCertificate` | **Deprecated**. Single certificate (PEM or Base64). Cannot be used with `clientCertificates`. | `"-----BEGIN CERTIFICATE-----\n..."` |
| `settings.tls.clientCertificates` | Array of certificate objects. Cannot be used with `clientCertificate`. | `[{name: "prod-cert", content: "..."}, ...]` |
| `settings.tls.certificate_count` | Number of active certificates (UI display only, computed by backend). | `3` |

### ClientCertificate Object Schema

Each entry in the `clientCertificates` array must include either `content` (inline certificate) or `ref` (reference to external resource), but not both.

| Property | Description | Example |
|:---------|:------------|:--------|
| `name` | Optional label. Defaults to `{applicationName}-{index}`. | `"production-cert-2024"` |
| `content` | Inline certificate (PEM/Base64) or template `[[ ]]` notation. | `"-----BEGIN CERTIFICATE-----\n..."` |
| `ref` | Reference to Secret or ConfigMap. See CertificateRef schema below. | `{kind: "secrets", name: "app-cert"}` |
| `startsAt` | Start of validity period (RFC3339). | `"2024-01-01T00:00:00Z"` |
| `endsAt` | End of validity period (RFC3339). | `"2025-01-01T00:00:00Z"` |
| `encoded` | If true, `content` is base64-decoded before sending to APIM. | `false` |

### CertificateRef Object Schema

Use `ref` to load certificates from Kubernetes Secrets or ConfigMaps. The operator resolves the reference at sync time and validates the PEM format.

| Property | Description | Example |
|:---------|:------------|:--------|
| `kind` | Resource type. Enum: `secrets`, `configmaps`. | `"secrets"` |
| `name` | Name of the Secret or ConfigMap. | `"tls-client-cert"` |
| `key` | Key in the resource's `data` field. Defaults to `tls.crt`. | `"client.crt"` |
| `namespace` | Namespace of the resource. Defaults to application namespace. | `"production"` |

### Database Schema

The `client_certificates` table stores certificate metadata and content. The `certificate` column is an NCLOB to support large PKCS7 bundles.

| Column | Type | Description |
|:-------|:-----|:------------|
| `id` | nvarchar(64), PK | Unique certificate ID |
| `cross_id` | nvarchar(64) | Cross-environment identifier |
| `application_id` | nvarchar(64) | Parent application ID |
| `name` | nvarchar(512) | User-defined label |
| `starts_at` | timestamp | Validity start date |
| `ends_at` | timestamp | Validity end date |
| `certificate` | nclob | PEM or PKCS7 certificate content |
| `certificate_expiration` | timestamp | Extracted expiration from X.509 |
| `subject` | nvarchar(1024) | X.509 subject DN |
| `issuer` | nvarchar(1024) | X.509 issuer DN |
| `fingerprint` | nvarchar(256) | SHA-256 thumbprint |
| `status` | nvarchar(32) | Enum: `ACTIVE`, `ACTIVE_WITH_END`, `SCHEDULED`, `REVOKED` |
| `environment_id` | nvarchar(64) | Environment scope |
| `organization_id` | nvarchar(64) | Organization scope |

Indexes: `idx_client_certificates_application_id`, `idx_client_certificates_environment_id`, `idx_client_certificates_app_id_status`.
