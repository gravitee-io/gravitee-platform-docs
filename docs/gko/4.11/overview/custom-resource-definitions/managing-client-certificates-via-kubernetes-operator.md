# Managing Client Certificates via Kubernetes Operator

## Managing Certificates via Kubernetes Operator

Define client certificates in the Application CRD under `spec.settings.tls.clientCertificates`. Each certificate entry supports inline PEM content, Kubernetes Secret/ConfigMap references, and optional validity windows.

1. Set `content` to a PEM-encoded certificate or use `ref` to reference a Secret or ConfigMap.
2. Specify `ref.kind` as `secrets` or `configmaps` (defaults to `secrets`), `ref.name` for the resource name, and `ref.key` for the data key (defaults to `tls.crt`).
3. Optionally set `startsAt` and `endsAt` as RFC3339 timestamps to control certificate validity windows.
4. Set `encoded: true` if the certificate content is Base64-encoded.

The operator validates that each certificate has either `content` or `ref` (not both) and parses timestamps before applying the resource. The deprecated `clientCertificate` field remains supported but triggers a warning banner in the Console when multiple certificates exist.

### Inline Content

Provide the PEM certificate directly in the `content` field:

```yaml
settings:
 tls:
 clientCertificates:
 - name: client1
 content: |
 -----BEGIN CERTIFICATE-----
 MIIBxTCCAW...
 -----END CERTIFICATE-----
 - name: client2
 content: |
 -----BEGIN CERTIFICATE-----
 MIICyDCCAb...
 -----END CERTIFICATE-----
```

### Secret or ConfigMap References

Point to existing Kubernetes resources using `ref`:

```yaml
settings:
 tls:
 clientCertificates:
 - name: client1
 ref:
 kind: secrets
 name: tls-client1
 key: tls.crt
 - name: client2
 ref:
 kind: configmaps
 name: tls-client2-cm
 key: tls.crt
```

When using refs, the operator resolves the certificate content at reconciliation time. If no namespace is specified in the `ref`, the Application's namespace is used. The `ResolvedRefs` condition on the Application status reflects whether all refs were resolved successfully.

### Template Notation

Use the existing `[[ secret ... ]]` / `[[ configmap ... ]]` template syntax:

```yaml
settings:
 tls:
 clientCertificates:
 - name: client1
 content: "[[ secret `tls-client1/tls.crt` ]]"
 - name: client2
 content: "[[ configmap `tls-client2-cm/tls.crt` ]]"
```

Template compilation is handled by the operator's existing template engine. The `EnableTemplating` feature flag must be enabled for this mode.

### Certificate Rotation

To rotate certificates without downtime:

1. Add the new certificate to the `clientCertificates` list (keeping the old one).
2. Apply the updated Application. The operator reconciles and registers both certificates with APIM.
3. Verify the new certificate works by calling the gateway with it.
4. Remove the old certificate from the list.
5. Apply again. The operator removes the old certificate from APIM.

### Validation Rules

- `clientCertificate` and `clientCertificates` can't be used together. Choose one or the other.
- Each entry must have either `content` or `ref`, but not both.
- If a subscription to an mTLS plan has `endingAt` set, at least one certificate must have `endsAt` after the subscription's `endingAt`.
- The `ref.kind` must be `secrets` or `configmaps`.
- The certificate must be a valid PEM certificate.
- The certificate can't be a CA certificate.
- If the PEM contains several certificates (e.g., a certificate chain), only the first certificate is used.

### Deprecation of `clientCertificate`

The `clientCertificate` field is deprecated. It continues to work for backward compatibility, but new configurations should use `clientCertificates`.

Migration: replace

```yaml
settings:
 tls:
 clientCertificate: "<PEM or template>"
```

with

```yaml
settings:
 tls:
 # When migrating, by setting "" one avoids a validation error.
 # Kubernetes will patch the existing resource resulting in both properties
 # being set, which is not allowed.
 clientCertificate: "" 
 clientCertificates:
 - content: "<PEM or template>"
```

## End-User Configuration

### Kubernetes Application CRD

| Property | Description | Example |
|:---------|:------------|:--------|
| `spec.settings.tls.clientCertificates[].name` | Certificate display name (defaults to `app-name-{index}`) | `prod-cert-1` |
| `spec.settings.tls.clientCertificates[].content` | Inline PEM certificate or template reference | `-----BEGIN CERTIFICATE-----...` |
| `spec.settings.tls.clientCertificates[].ref.name` | Secret or ConfigMap name | `app-tls-secret` |
| `spec.settings.tls.clientCertificates[].ref.key` | Data key within the referenced resource | `tls.crt` |
| `spec.settings.tls.clientCertificates[].ref.kind` | Resource type: `secrets` or `configmaps` (defaults to `secrets`) | `secrets` |
| `spec.settings.tls.clientCertificates[].ref.namespace` | Namespace of the referenced resource (defaults to Application namespace) | `default` |
| `spec.settings.tls.clientCertificates[].startsAt` | RFC3339 validity start timestamp | `2026-01-29T00:00:00Z` |
| `spec.settings.tls.clientCertificates[].endsAt` | RFC3339 validity end timestamp | `2027-01-29T23:59:59Z` |
| `spec.settings.tls.clientCertificates[].encoded` | If `true`, content is Base64-encoded and will be decoded before sending to APIM | `false` |
