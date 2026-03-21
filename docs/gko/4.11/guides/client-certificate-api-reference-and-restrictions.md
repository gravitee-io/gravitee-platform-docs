# Client Certificate API Reference and Restrictions

## Restrictions

- PKCS7 bundles must contain at least one valid X.509 certificate unless `allowEmpty` is explicitly enabled in internal API calls.
- Certificate fingerprints use SHA-256 hashing. MD5 digests are no longer supported.
- Kubernetes CRD validation rejects certificates with both `content` and `ref` fields set.
- `startsAt` and `endsAt` timestamps must conform to RFC3339 format.
- Repository queries for certificates by status return empty results if the status list is null or empty.
- The UI warning banner appears only when `certificateCount > 1`. Single-certificate applications display normally.
- Pagination in the client certificate repository is 1-indexed in the API but 0-indexed in the database layer. The page number is decremented before querying the database.

## Related Changes

The Application General Info UI component displays a warning banner when multiple certificates are active. The banner shows the certificate count and notes that only the most recently created certificate appears in the detail view.

The subscription cache key format changed from `{api}.{clientCertificate}.{plan}` to `{api}.{plan}.{sha256Hash}` to support multiple certificates per subscription.

BouncyCastle's `bcpkix-jdk18on` dependency moved from test scope to compile scope to enable PKCS7 parsing in production code.
