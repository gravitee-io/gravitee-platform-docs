# mTLS Certificate Management for Applications: Overview and Concepts

## Overview

mTLS certificate management enables application owners to upload, rotate, and manage client certificates for mutual TLS authentication in the new Developer Portal. Administrators control feature availability via a portal settings toggle. Application owners with appropriate permissions can manage certificates through a dedicated UI section.

## Key Concepts

### Client Certificates

Client certificates authenticate applications using mutual TLS. Each certificate has a name, status, validity period, and metadata including subject, issuer, and fingerprint. Certificates are uploaded in PEM format and can be scheduled to activate at a future date or configured with an expiration date.

### Certificate Status

| Status | Description |
|:-------|:------------|
| Active | Certificate is currently active with no end date |
| Active with end | Certificate is active but has a scheduled end date |
| Scheduled | Certificate will become active in the future |
| Revoked | Certificate has been revoked or expired |

Active, Active with end, and Scheduled certificates appear in the Active Certificates tab. Revoked certificates appear in the Certificate History tab.

### Grace Period Rotation

When uploading a new certificate while an active certificate exists, both certificates remain active during a grace period to avoid downtime. The grace period end date must be specified for the current certificate and cannot exceed its expiration date. After the grace period, the old certificate transitions to revoked status.

## Prerequisites

Before managing mTLS certificates, ensure the following requirements are met:

* New Developer Portal must be enabled (`portal.next.enabled`)
* `APPLICATION_DEFINITION[READ]` permission to view certificates
* `APPLICATION_DEFINITION[UPDATE]` permission to create, update, or delete certificates
* Certificates must be in PEM format (`.pem`, `.crt`, or `.cer` file extensions)
