### Overview

Client Certificate Management enables API platform administrators to manage TLS certificates for applications that consume APIs secured with mTLS plans. Administrators can create, update, and delete certificates through REST API endpoints, with support for certificate rotation via grace periods to ensure zero-downtime transitions. This feature addresses the operational challenge of certificate expiration by allowing multiple active certificates per application.

### Certificate lifecycle states

Certificates transition through four states based on their validity windows. The gateway evaluates both `startsAt` and `endsAt` timestamps to determine the current state.

| Status | Condition |
|:-------|:----------|
| `ACTIVE` | Certificate is available, no end date set |
| `ACTIVE_WITH_END` | Certificate is available but will be removed when `endsAt` is reached |
| `SCHEDULED` | Certificate is not yet active (`startsAt` not yet passed) |
| `REVOKED` | Certificate has expired (`endsAt` has passed) |

### Certificate uniqueness

Each certificate is identified by a SHA-256 fingerprint computed from its DER-encoded form. A fingerprint cannot be reused across active applications within the same environment. This prevents accidental certificate sharing and enforces isolation. Certificates with `REVOKED` status and applications with `ARCHIVED` status are excluded from this uniqueness check.
