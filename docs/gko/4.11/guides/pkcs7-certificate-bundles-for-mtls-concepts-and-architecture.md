# PKCS7 Certificate Bundles for mTLS: Concepts and Architecture

## Overview

PKCS7 certificate bundle support enables applications to present multiple client certificates for mTLS authentication against a single subscription. Administrators can upload certificate bundles containing multiple X.509 certificates, and the gateway validates client connections against any certificate in the bundle using SHA-256 thumbprints.

This is an APIM feature.

## Prerequisites

- Gravitee API Management 4.x gateway and management API
- MongoDB or JDBC-compatible database with schema version 02 or later
- BouncyCastle cryptographic provider (bundled with gateway)
- Applications configured with mTLS-enabled plans

## Gateway Configuration

### Database Schema

The `client_certificates` table stores certificate metadata and content. Apply the schema migration before enabling multi-certificate support.


| Property | Description | Example |
|:---------|:------------|:--------|
| `${gravitee_prefix}client_certificates.id` | Unique certificate identifier | `cert-abc123` |
| `${gravitee_prefix}client_certificates.application_id` | Owning application ID (indexed) | `app-xyz789` |
| `${gravitee_prefix}client_certificates.fingerprint` | SHA-256 thumbprint for cache lookup | `u21dNKud2YsKNJn3HQTTon1_qSoZi8IrBTsLiZCFQLg` |

<!-- GAP: Table incomplete - additional columns from source draft required -->
