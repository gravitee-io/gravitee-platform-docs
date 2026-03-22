# Configuring Multi-Certificate mTLS for Applications

## Certificate Status Lifecycle

| Status | Meaning |
|:-------|:--------|
| `ACTIVE` | Certificate is currently valid with no end date |
| `ACTIVE_WITH_END` | Certificate is valid but has a future expiration date |
| `SCHEDULED` | Certificate validity starts in the future |
| `REVOKED` | Certificate has been revoked |

## Gateway Configuration

No new gateway configuration properties are required. The feature uses existing subscription and certificate infrastructure.
