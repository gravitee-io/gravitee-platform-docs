# Gateway Configuration for mTLS Certificate Management

## Certificate Validation

Uploaded certificates are validated before storage. The certificate must be an X.509 certificate and cannot be a CA certificate. If the uploaded PEM contains a certificate chain, only the first certificate is used. The platform extracts the subject, issuer, expiration date, and generates a SHA-256 fingerprint. The fingerprint is checked for uniqueness within the environment to prevent duplicate uploads: the certificate is rejected if an active or scheduled certificate with the same fingerprint is bound to an active application.

## Prerequisites

* APIM version 4.11 or above
* Application with mTLS plan configured
* Valid X.509 certificates in PEM format
* TLS-enabled gateway endpoint


## Certificate Management

Application owners can upload and manage client certificates through the Developer Portal when the **mTLS** certificate management feature is enabled by administrators. For details on uploading, rotating, and managing certificates through the Developer Portal UI, see the **mTLS** Certificate Management for Applications documentation.

For Kubernetes-managed certificate configuration, see Kubernetes CRD Configuration for Client Certificates.
