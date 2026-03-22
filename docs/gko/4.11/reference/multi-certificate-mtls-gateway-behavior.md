# Multi-Certificate mTLS Gateway Behavior

## Gateway Runtime Behavior

The gateway processes multi-certificate mTLS authentication using existing subscription and certificate infrastructure. No new gateway configuration properties are required.

### Subscription Lookup Flow

When a client connects with mTLS, the gateway:

1. Extracts the client certificate from the TLS session
2. Computes the SHA-256 fingerprint of the certificate
3. Queries the subscription cache using the key format `{apiId}.{planId}.{sha256(clientCertificate)}`

### PKCS7 Bundle Handling

When a subscription references a PKCS7 bundle:

- The gateway parses the bundle into individual certificates
- Each certificate generates a separate cache entry
- Any certificate in the bundle can authenticate the subscription

If PKCS7 parsing fails, the system treats the content as a single PEM certificate.

### Cache Key Format

Certificate cache keys use SHA-256 hashes of the full certificate content, not individual fingerprints. The subscription cache key format is `{apiId}.{planId}.{sha256(clientCertificate)}`.

### Validation Restrictions

- PKCS7 bundles with no valid certificates fail validation
- Duplicate fingerprints across active applications in the same environment are not allowed


