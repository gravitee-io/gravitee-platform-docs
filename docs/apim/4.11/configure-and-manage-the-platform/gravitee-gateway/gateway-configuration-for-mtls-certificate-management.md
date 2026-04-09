
# Gateway Configuration for mTLS Certificate Management

## Prerequisites


* APIM version 4.11 or above
* Application with mTLS plan configured
* Valid X.509 certificates in PEM format
* TLS-enabled gateway endpoint


## Certificate Management

For Kubernetes-managed certificate configuration, see [Kubernetes CRD Configuration for Client Certificates](kubernetes-crd-configuration-for-client-certificates.md).

Application owners can manage client certificates directly through the Developer Portal when `portal.next.mtls.enabled` is set to `true`. This allows uploading, configuring, and managing certificates through a dedicated UI. For details, see [mTLS Certificate Management for Applications](#certificate-management).
