# mTLS Certificate Management Overview

## Overview

mTLS Certificate Management enables application owners to upload, configure, and manage client certificates for mutual TLS authentication in the Developer Portal. Administrators control feature availability through a gateway configuration toggle, and application owners with appropriate permissions can manage certificates through a dedicated UI in the New Developer Portal.

## Key Concepts

### Client Certificates

Client certificates authenticate applications using mutual TLS. Each certificate includes a name, PEM-encoded certificate data, optional validity dates, and a status. Certificates transition through four statuses:

| Status | Description | Tab Location |
|:-------|:------------|:-------------|
| **Active** | Currently valid with no end date | Active certificates |
| **Active With End** | Currently valid with a configured expiration | Active certificates |
| **Scheduled** | Not yet valid based on start date | Active certificates |
| **Revoked** | Deleted or expired | Certificate history |

### Grace Period

When uploading a new certificate while an active certificate exists, a grace period allows both certificates to remain active simultaneously to avoid downtime. The grace period end date must fall between the current date and the active certificate's expiration date. During the grace period, both the new certificate and the existing certificate authenticate requests.

### Certificate Validation

Before creating a certificate, the system validates the PEM-encoded certificate data and extracts metadata including expiration date, subject, and issuer. Validation occurs automatically when the user proceeds from the Upload step to the Configure step in the Add Certificate dialog. Invalid certificates trigger an error message and prevent progression to the Configure step.

## Prerequisites

Before managing mTLS certificates, ensure the following requirements are met:

* New Developer Portal must be enabled
* `portal.next.mtls.enabled` must be set to `true` in gateway configuration
* User must have `APPLICATION_DEFINITION[UPDATE]` permission to upload or delete certificates

## Gateway Configuration

The mTLS certificate management feature is controlled by the following gateway configuration properties:

| Property | Description | Default |
|:---------|:------------|:--------|
| `portal.next.mtls.enabled` | Enables mTLS certificate management in the New Developer Portal | `false` |
| `portalNext.mtls.enabled` | Console WebUI toggle for mTLS feature availability | `false` |

The **Enable mTLS Certificate Management** toggle appears in the Management Console under Portal Settings → New Developer Portal section, immediately after the New Portal Enabled toggle.
