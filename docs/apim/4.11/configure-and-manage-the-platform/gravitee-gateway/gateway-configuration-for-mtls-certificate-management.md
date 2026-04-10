# Gateway Configuration for mTLS Certificate Management

## Certificate Validation

Uploaded certificates are validated before storage. The certificate must be an X.509 certificate and cannot be a CA certificate. If the uploaded PEM contains a certificate chain, only the first certificate is used. The platform extracts the subject, issuer, expiration date, and generates a SHA-256 fingerprint. The fingerprint is checked for uniqueness within the environment to prevent duplicate uploads: the certificate is rejected if an active or scheduled certificate with the same fingerprint is bound to an active application.

## Prerequisites

* APIM version 4.11 or above
* Application with mTLS plan configured
* Valid X.509 certificates in PEM format
* TLS-enabled gateway endpoint


## Certificate Management

For Kubernetes-managed certificate configuration, see [Kubernetes CRD Configuration for Client Certificates](https://docs.gravitee.io/gko/4.11/guides/kubernetes-crd-configuration-for-client-certificates).

When the mTLS Certificate Management feature is enabled in the Developer Portal (`portal.next.mtls.enabled` set to `true`), application owners can upload and rotate client certificates directly through the Developer Portal UI. This feature supports grace-period rotation to avoid downtime during certificate updates. For details on enabling and using this feature, see the mTLS Certificate Management documentation.
