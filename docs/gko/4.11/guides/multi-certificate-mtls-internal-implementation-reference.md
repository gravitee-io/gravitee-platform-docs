# Multi-Certificate mTLS: Internal Implementation Reference

## Related Changes

### Application Schema

The `Application.TLSSettings` schema includes a `certificate_count` field and deprecates the single `clientCertificate` field in favor of the `clientCertificates` array.

### UI Behavior

The UI displays a warning banner when `certificate_count > 1`, indicating that multiple certificates are active and only the most recent is shown.

### Subscription Cache Structure

The subscription cache maintains separate maps:

* `cacheByClientCertificate`: Maps `{api}.{plan}.{sha256(cert)}` to `Subscription`
* `cacheByApiClientId`: Maps `{api}.{plan}.{clientId}` to `Subscription`
* `cacheBySubscriptionId`: Maps `{subscriptionId}` to `Subscription`
* `cacheBySubscriptionIdAll`: Maps `{subscriptionId}` to `Set<Subscription>` for API Products

### Dependency Changes

The `org.bouncycastle:bcpkix-jdk18on` dependency was moved from test scope to compile scope to support runtime PKCS7 parsing.

### Database Schema

A new `client_certificates` table was added with the following indexes:

* `idx_client_certificates_application_id` on `application_id`
* `idx_client_certificates_environment_id` on `environment_id`
* `idx_client_certificates_app_id_status` on `(application_id, status)` for efficient status-based queries

### Cache Key Format

Subscription cache keys changed format from `{api}.{clientCertificate}.{plan}` to `{api}.{plan}.{sha256(cert)}`. Existing cached subscriptions are invalidated on upgrade.

### Pagination Correction

API pagination uses 1-based page numbers while the repository layer uses 0-based indexing. This was corrected in PR #15283.
