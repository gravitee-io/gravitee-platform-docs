# Multi-Certificate mTLS: Overview and Concepts

## Overview

Multi-certificate mTLS support enables applications to authenticate with multiple client certificates instead of a single certificate. This feature supports certificate rotation, gradual migration, and multi-environment deployments where different certificates are active at different times. It is designed for API platform administrators managing application subscriptions and developers integrating with mTLS-protected APIs.

## Key Concepts

### Client Certificates

A client certificate is an X.509 certificate stored in PEM or PKCS7 format that authenticates an application to an API. Each certificate has a lifecycle status and metadata including subject, issuer, fingerprint, and validity dates. Applications can register multiple certificates, each with optional start and end dates to support scheduled rotation.

**Client Certificate Properties**

| Property | Description | Example |
|:---------|:------------|:--------|
| `name` | Optional label for the certificate | `"Production Cert 2024"` |
| `content` | PEM-encoded certificate or PKCS7 bundle | `"-----BEGIN CERTIFICATE-----\n..."` |
| `startsAt` | RFC3339 timestamp when certificate becomes valid | `"2024-01-29T00:00:00Z"` |
| `endsAt` | RFC3339 timestamp when certificate expires | `"2027-01-29T23:59:59Z"` |
| `fingerprint` | SHA-256 hash of the certificate (computed) | `"u21dNKud2YsKNJn3HQTTon1_qSoZi8IrBTsLiZCFQLg"` |
| `status` | Lifecycle state | `ACTIVE`, `ACTIVE_WITH_END`, `SCHEDULED`, `REVOKED` |

### PKCS7 Certificate Bundles

PKCS7 bundles allow multiple certificates to be packaged in a single Base64-encoded payload. The platform parses PKCS7 bundles automatically, extracting each certificate and generating individual SHA-256 fingerprints. If PKCS7 parsing fails, the system falls back to treating the content as a single PEM certificate. Each certificate in a bundle is indexed separately for subscription lookups.

### Certificate Fingerprints and Subscription Lookup

The platform uses SHA-256 fingerprints to match incoming TLS client certificates to subscriptions. When a request arrives, the gateway extracts the client certificate from the TLS session, computes its SHA-256 fingerprint, and queries the subscription cache using the key format `{apiId}.{planId}.{fingerprint}`. For PKCS7 bundles, each certificate generates a separate cache entry, allowing any certificate in the bundle to authenticate the subscription.

### Certificate Status Lifecycle

**Certificate Status Lifecycle**

| Status | Meaning |
|:-------|:--------|
| `ACTIVE` | Certificate is currently valid with no end date |
| `ACTIVE_WITH_END` | Certificate is valid but has a future expiration date |
| `SCHEDULED` | Certificate validity starts in the future |
| `REVOKED` | Certificate has been revoked |

### Application Settings UI

The Console UI displays a banner when an application has multiple active certificates: `"This application has {count} active certificates. The one displayed is the most recently created."` The banner appears only when `certificate_count > 1`.

## Gateway Configuration

No new gateway configuration properties are required. The feature uses existing subscription and certificate infrastructure.
