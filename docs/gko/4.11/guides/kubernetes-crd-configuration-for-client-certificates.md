# Kubernetes CRD Configuration for Client Certificates

## Overview

The Application CRD supports a `clientCertificates` list field under `settings.tls`, enabling multiple client certificates for mTLS plans. This allows certificate rotation without downtime: add the new certificate, wait for propagation, then remove the old one.

The existing `clientCertificate` (singular) field is **deprecated** but remains supported for backward compatibility.

## `clientCertificates` Field

Each entry in the `clientCertificates` list is a `ClientCertificate` object with the following fields:

| Field      | Type             | Required      | Description                                                                      |
| ---------- | ---------------- | ------------- | -------------------------------------------------------------------------------- |
| `name`     | string           | No            | Label for this certificate. Defaults to `<appName>-<index>`.                     |
| `content`  | string           | XOR `ref`     | Inline PEM/Base64 certificate content, or a `[[ ]]` template notation.           |
| `ref`      | CertificateRef   | XOR `content` | Reference to a Secret or ConfigMap containing the certificate.                   |
| `startsAt` | string (RFC3339) | No            | Optional start date of the certificate validity period.                          |
| `endsAt`   | string (RFC3339) | No            | Optional end date of the certificate validity period.                            |
| `encoded`  | bool             | No            | If `true`, content is base64-encoded and will be decoded before sending to APIM. |

{% hint style="info" %}
A certificate with no end date is valid until the subscription ends.
{% endhint %}

{% hint style="warning" %}
Certificate expiration is not checked. It is the user's responsibility to ensure the certificate is valid beyond the end date (if set).
{% endhint %}

### CertificateRef

| Field       | Type   | Default         | Description                                                         |
| ----------- | ------ | --------------- | ------------------------------------------------------------------- |
| `kind`      | string | `secrets`       | Kind of resource: `secrets` or `configmaps`.                        |
| `name`      | string | (required)      | Name of the Secret or ConfigMap.                                    |
| `key`       | string | `tls.crt`       | Key in the resource's data map.                                     |
| `namespace` | string | (application's) | Namespace of the resource. Defaults to the Application's namespace. |

## Certificate Provisioning Modes

The three modes can be combined.

### 1. Inline Content

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

### 2. References (Secret / ConfigMap)

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

When using refs, the operator resolves the certificate content at reconciliation time.

If no namespace is specified in the `ref`, the Application's namespace is used.

The `ResolvedRefs` condition on the Application status reflects whether all refs were resolved successfully.

### 3. Template Notation

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

## Certificate Rotation

To rotate certificates without downtime:

1. **Add** the new certificate to the `clientCertificates` list (keeping the old one).
2. **Apply** the updated Application. The operator reconciles and registers both certificates with APIM.
3. **Verify** the new certificate works by calling the gateway with it.
4. **Remove** the old certificate from the list.
5. **Apply** again. The operator removes the old certificate from APIM.

## Validation Rules

* `clientCertificate` (singular) and `clientCertificates` (plural) **cannot be used together**. Choose one or the other.
* Each entry must have **either** `content` **or** `ref`, but not both (and not neither).
* The `ref.kind` must be `secrets` or `configmaps`.
* The certificate must be a valid PEM certificate.
* The certificate cannot be a CA certificate.
* If the PEM contains several certificates (e.g., a certificate chain), only the first certificate is used.

## Deprecation of `clientCertificate`

The `clientCertificate` (singular) field is deprecated. It continues to work for backward compatibility, but new configurations should use `clientCertificates` (plural).

**Migration:** Replace

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
