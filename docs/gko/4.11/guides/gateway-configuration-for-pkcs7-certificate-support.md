# Gateway Configuration for PKCS7 Certificate Support

### Certificate Status Lifecycle

| Status | Meaning |
|:-------|:--------|
| `ACTIVE` | Certificate is currently valid with no defined end date |
| `ACTIVE_WITH_END` | Certificate is valid but has a configured expiration date |
| `SCHEDULED` | Certificate validity begins in the future |
| `REVOKED` | Certificate has been revoked and will not authenticate |
