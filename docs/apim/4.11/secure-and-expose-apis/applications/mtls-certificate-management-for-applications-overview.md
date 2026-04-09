# mTLS Certificate Management for Applications - Overview

## Overview

mTLS Certificate Management enables application owners to upload, rotate, and manage client certificates for mutual TLS authentication in the New Developer Portal. Administrators control feature availability via a console toggle, and application owners with appropriate permissions can manage certificates through a dedicated UI with support for certificate rotation and grace periods to avoid downtime.

## Key Concepts

### Client Certificates

Client certificates authenticate applications using mutual TLS. Each certificate has a name, status, optional validity dates, and metadata including subject, issuer, and fingerprint. Certificates transition through four statuses:

- **Active**: Currently valid with no end date
- **Active with End**: Valid until a specified date
- **Scheduled**: Not yet active
- **Revoked**: No longer valid and moved to history

### Certificate Rotation

Certificate rotation allows uploading a new certificate while maintaining an existing active certificate during a grace period. When rotating, both certificates remain active until the grace period end date, preventing authentication downtime. The grace period end date is required when active certificates exist and cannot exceed the current certificate's expiration date.

### Certificate Lifecycle

Certificates are organized into two views:

- **Active certificates**: Certificates with status Active, Active with End, or Scheduled
- **Certificate history**: Certificates with status Revoked

Application owners can delete certificates from either view, with special confirmation required when deleting the last active certificate to prevent unintended loss of authentication capability.

## Prerequisites

Before managing mTLS certificates, ensure the following requirements are met:

- New Developer Portal must be enabled
- `portal.next.mtls.enabled` configuration property must be set to `true`
- User must have `APPLICATION_DEFINITION[UPDATE]` permission to upload or delete certificates
- Valid PEM-formatted client certificate (`.pem`, `.crt`, or `.cer` file)

## Gateway Configuration

| Property | Description | Default |
|:---------|:------------|:--------|
| `portal.next.mtls.enabled` | Enables mTLS certificate management in the New Developer Portal | `false` |
