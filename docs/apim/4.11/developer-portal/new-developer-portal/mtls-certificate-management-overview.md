# mTLS Certificate Management Overview

## Overview

mTLS Certificate Management enables application owners to upload, rotate, and manage client certificates for mutual TLS authentication in the new Developer Portal. Administrators control feature availability via a portal-level toggle, and application owners manage certificates through a dedicated UI with support for grace-period rotation to avoid downtime during certificate updates.

## Key Concepts

### Client Certificates

Client certificates authenticate applications using mutual TLS. Each certificate has a name, PEM-encoded content, optional validity dates (Active Until), and a lifecycle status. Certificates are considered active when their status is `ACTIVE`, `ACTIVE_WITH_END`, or `SCHEDULED`. The `REVOKED` status indicates expired or manually revoked certificates.

| Status | Description |
|:-------|:------------|
| `ACTIVE` | Certificate is currently active with no end date |
| `ACTIVE_WITH_END` | Certificate is active but has a scheduled end date |
| `SCHEDULED` | Certificate is scheduled to become active in the future |
| `REVOKED` | Certificate has been revoked or expired |

### Grace Period Rotation

When uploading a new certificate while active certificates exist, users specify a Grace Period End date for the currently active certificate. Both certificates remain active during the grace period, allowing seamless rotation without downtime. The old certificate transitions to `ACTIVE_WITH_END` status, and the grace period end date must not exceed the old certificate's expiration date.

### Certificate Lifecycle

Certificates are uploaded in PEM format (`.pem`, `.crt`, `.cer` files accepted) and validated server-side before creation. Application owners can set an Active Until date to schedule automatic expiration. Deleting the last active certificate requires a second confirmation and is blocked if active mTLS subscriptions exist.

## Prerequisites

Before managing mTLS certificates, ensure the following requirements are met:

* The new Developer Portal must be enabled
* `portal.next.mtls.enabled` must be set to `true` by an administrator
* `APPLICATION_DEFINITION[READ]` permission to view certificates
* `APPLICATION_DEFINITION[UPDATE]` permission to upload, update, or delete certificates
