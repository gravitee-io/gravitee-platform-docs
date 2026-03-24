# Gateway Configuration for mTLS Certificate Management

## Certificate Validation

Uploaded certificates are validated before storage. The platform extracts the subject, issuer, expiration date, and generates a SHA-256 fingerprint. Certificates with expiration dates in the past are rejected. The fingerprint is checked for uniqueness within the environment to prevent duplicate uploads.

## Prerequisites

* APIM version 4.11 or above
* Application with mTLS plan configured
* Valid X.509 certificate in PEM format (or PKCS7 bundle)
* TLS-enabled gateway endpoint


## Certificate Management

For certificate upload and management workflows, see [Managing Client Certificates](../../../../gko/4.11/guides/managing-client-certificates.md).
