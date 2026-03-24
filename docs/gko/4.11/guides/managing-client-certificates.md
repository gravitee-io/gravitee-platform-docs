# Managing Client Certificates

## Creating Client Certificates

To add a certificate, navigate to the application's certificate management card and select "Add Certificate." Upload a PEM-formatted certificate file or paste the content directly. The platform validates the certificate and extracts metadata (subject, issuer, expiration). Provide a name (up to 256 characters) and optionally set an "Active until" date. If active certificates already exist, specify a grace period end date to enable rotation — both certificates will authenticate requests until the grace period expires. Review the summary and confirm to save the certificate.

## Managing Certificates

### Viewing Certificates

The certificate management card displays the most recently created active certificate. If multiple active certificates exist, a warning banner indicates the total count. Use the certificate list to view all certificates for the application, including scheduled and revoked entries.

### Revoking Certificates

To revoke a certificate, select it from the list and choose "Revoke." Revoked certificates immediately stop authenticating requests and cannot be reactivated. The certificate remains in the list with a `REVOKED` status for audit purposes.

### Kubernetes CRD Configuration

For Kubernetes-managed applications, define certificates in the `Application` CRD under `spec.tlsSettings.clientCertificates`. Each certificate requires a `name` and either inline `content` or a `ref` to a Kubernetes Secret or ConfigMap. Optionally specify `startsAt` and `endsAt` dates for scheduled activation and expiration. The `clientCertificate` field (singular) is deprecated and cannot be used alongside `clientCertificates`.

```yaml
clientCertificates:
  - name: "prod-cert"
    ref:
      kind: "secrets"
      name: "app-tls"
      key: "tls.crt"
      namespace: "default"
    startsAt: "2025-01-01T00:00:00Z"
    endsAt: "2025-12-31T23:59:59Z"
    encoded: false
```
