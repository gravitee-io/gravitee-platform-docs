# mTLS Certificate Management Overview

## Overview

mTLS Certificate Management enables administrators to upload, validate, and rotate client certificates for application-level mutual TLS authentication. The feature supports multiple client certificates, scheduled certificate activation, and grace-period rotation to prevent downtime. It is available in APIM 4.11 and above.

## Key Concepts

### Client Certificate Lifecycle

Client certificates progress through four states: **Scheduled** (not yet active), **Active** (currently valid), **Active with End Date** (valid until a specified date), and **Revoked** (no longer valid). Certificates include metadata such as subject, issuer, fingerprint (SHA-256), and expiration date. Each certificate is scoped to a single application and environment.

| Status | Description |
|:-------|:------------|
| `ACTIVE` | Certificate is currently valid with no end date |
| `ACTIVE_WITH_END` | Certificate is valid until a specified end date |
| `SCHEDULED` | Certificate will become active at a future date |
| `REVOKED` | Certificate has been revoked and is no longer valid |

### Certificate Rotation

Certificate rotation allows administrators to upload a new certificate while an existing certificate remains active during a grace period. Both certificates authenticate requests during the overlap, preventing downtime. The grace period end date must not be in the past or exceed the active certificate's expiration.

### Certificate Validation

Uploaded certificates are validated before storage. The platform extracts the subject, issuer, expiration date, and generates a SHA-256 fingerprint. The fingerprint is checked for uniqueness within the environment to prevent duplicate uploads. The certificate must be in X.509 format and cannot be a CA certificate. If the uploaded PEM contains a certificate chain, only the first certificate is retained.

## Prerequisites

- APIM version 4.11 or above
- Application with mTLS plan configured
- Valid X.509 certificate in PEM format
- TLS-enabled gateway endpoint
