# Creating and Managing Client Certificates via Management API

### Subscription Cache

The gateway caches subscriptions by API ID, plan ID, and certificate SHA-256 hash. Cache keys follow the format `{apiId}.{planId}.{sha256Hash}`. When a client presents a certificate, the gateway computes its SHA-256 thumbprint and queries the cache. If multiple certificates exist in a PKCS7 bundle, each generates a separate cache entry pointing to the same subscription.

## Creating Client Certificates

Upload a certificate or PKCS7 bundle through the Management API. The system parses the content and extracts individual certificates. For each certificate, the gateway computes a SHA-256 thumbprint. 

For PKCS7 bundles, the gateway assigns aliases following the pattern `{subscriptionId}_0`, `{subscriptionId}_1`, and so on. Each certificate in the bundle is registered in the trust store.

Certificates receive status assignments based on their validity windows:
- Certificates with `startsAt` timestamps in the future receive `SCHEDULED` status
- Certificates with `endsAt` timestamps receive `ACTIVE_WITH_END` status
- Certificates without validity windows default to `ACTIVE` status

The gateway synchronizes certificates to the subscription cache during the next sync cycle, enabling mTLS validation.
