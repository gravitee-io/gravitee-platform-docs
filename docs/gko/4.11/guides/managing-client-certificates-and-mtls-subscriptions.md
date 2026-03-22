# Managing Client Certificates and mTLS Subscriptions

## Creating Client Certificates

To add client certificates to an application:

1. Navigate to the application's TLS settings.
2. Populate the `clientCertificates` array with one or more certificate entries:
   * For inline certificates, set the `content` field to a PEM-encoded certificate or base64-encoded string. If using base64, set `encoded: true`.
   * For Kubernetes-managed certificates, set the `ref` field with the Secret or ConfigMap name and optional key.
3. Optionally specify `startsAt` and `endsAt` in RFC3339 format to define the validity window.
4. Save the application. The backend computes the SHA-256 fingerprint for each certificate and stores it in the `client_certificates` table.
5. Subscribe the application to an mTLS-enabled plan. The gateway caches the subscription using keys in the format `{apiId}.{planId}.{sha256(certificate)}` for each certificate.

## Subscribing to mTLS Plans

When an application with multiple certificates subscribes to an mTLS plan:

1. The subscription service retrieves all certificates for the application from the `client_certificates` table.
2. For each certificate, the gateway computes the SHA-256 thumbprint and creates a cache entry with the key `{apiId}.{planId}.{sha256(certificate)}`.
3. If the certificate is in PKCS7 format, the gateway extracts all certificates in the bundle and creates a separate cache entry for each.
4. When the subscription is updated (for example, a certificate is added or removed), the gateway evicts old cache keys and registers new ones.
5. To unsubscribe, the gateway removes all cache entries from `cacheBySubscriptionId`, `cacheByApiClientId`, `cacheByClientCertificate`, and `cacheKeysByApiId`.

## End-User Configuration

## Related Changes

The UI now displays a warning banner when `certificate_count > 1`, showing "This application has {certificate_count} active certificates. The one displayed is the most recently created."
