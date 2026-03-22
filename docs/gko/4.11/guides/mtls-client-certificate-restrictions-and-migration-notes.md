# mTLS Client Certificate Restrictions and Migration Notes

## Restrictions

- Cannot use both `clientCertificate` and `clientCertificates` in the same application (mutually exclusive)
- Cannot use both `content` and `ref` in the same `ClientCertificate` object
- PKCS7 bundles must contain valid X.509 certificates; malformed bundles return `CLIENT_CERTIFICATE_INVALID` error
- TLS termination must occur at the gateway; requests without a TLS session return `SSL_SESSION_REQUIRED` error
- Requests without a peer certificate in the TLS session return `CLIENT_CERTIFICATE_MISSING` error
- Fingerprint computation uses SHA-256 (changed from MD5 in earlier versions)
- Pagination in the client certificate repository uses 0-based indexing internally; API consumers use 1-based page numbers
- Kubernetes operator validates RFC3339 format for `startsAt` and `endsAt` fields
- BouncyCastle library (`bcpkix-jdk18on`) is now a compile-time dependency (previously test-only)

## Related Changes

The UI now displays a warning banner when `certificate_count > 1`, showing "This application has {certificate_count} active certificates. The one displayed is the most recently created." The subscription cache service was updated to handle multiple certificates per subscription, evicting old cache keys when certificates are added or removed. The Kubernetes operator added validation to prevent simultaneous use of `clientCertificate` and `clientCertificates`, and to enforce mutual exclusion of `content` and `ref` in certificate objects. The repository layer fixed a pagination offset bug where API page numbers (1-based) were not converted to repository page numbers (0-based). BouncyCastle dependency scope changed from `test` to `compile` to support PKCS7 bundle parsing in production.
