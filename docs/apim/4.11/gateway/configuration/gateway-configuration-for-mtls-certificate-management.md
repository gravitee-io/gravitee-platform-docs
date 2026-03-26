# Gateway Configuration for mTLS Certificate Management

## Certificate Validation

Uploaded certificates are validated before storage. It must a X.509 certificate that is not a CA. If it is certificate chain, only the first one is read. The platform extracts the subject, issuer, expiration date, and generates a SHA-256 fingerprint.  The fingerprint is checked for uniqueness within the environment to prevent duplicate uploads: it is rejected if an active or scheduled certificate is bound to an active application.

## Prerequisites

* APIM version 4.11 or above
* Application with mTLS plan configured
* Valid X.509 certificate in PEM format (or PKCS7 bundle)
* TLS-enabled gateway endpoint


## Certificate Management

For certificate upload and management workflows, see [Managing Client Certificates](../../../../gko/4.11/guides/managing-client-certificates.md).
