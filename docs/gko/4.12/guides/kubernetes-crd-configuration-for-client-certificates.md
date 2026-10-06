---
description: The Application CRD holds several client certificates for mTLS plans in the Gravitee Kubernetes Operator 4.12. Rotate them without downtime.
---

# Kubernetes CRD Configuration for Client Certificates

## Overview

The `Application` resource supports a `clientCertificates` list under `spec.settings.tls`, so an application holds several client certificates for mTLS plans at once. This lets you rotate a certificate without downtime: add the new certificate, wait for the operator to register it with APIM, then remove the old one.

The single `clientCertificate` field is **deprecated** but remains supported for backward compatibility.

This feature requires GKO 4.11 or later and APIM 4.11 or later. GKO sends the certificates to APIM, which validates them, computes their status from their dates, and copies the active ones into the mTLS subscriptions of the application. For the statuses, the grace period, and the automatic revocation, see [mTLS certificate management for applications](https://documentation.gravitee.io/apim/secure-and-expose-apis/applications/mtls-certificate-management-for-applications-overview-and-concepts) in the APIM documentation.

## `clientCertificates` Field

Each entry in the `clientCertificates` list is a `ClientCertificate` object with the following fields:

| Field      | Type             | Required      | Description                                                                      |
| ---------- | ---------------- | ------------- | -------------------------------------------------------------------------------- |
| `name`     | string           | No            | Label for this certificate. Defaults to `<application name>-<index>`, where the index starts at 0. |
| `content`  | string           | XOR `ref`     | Inline PEM or Base64 certificate content, or a `[[ ]]` template notation.        |
| `ref`      | CertificateRef   | XOR `content` | Reference to a Secret or ConfigMap containing the certificate.                   |
| `startsAt` | string (RFC3339) | No            | Optional start date of the certificate validity period.                          |
| `endsAt`   | string (RFC3339) | No            | Optional end date of the certificate validity period.                            |
| `encoded`  | bool             | No            | If `true`, content is base64-encoded and is decoded before it's sent to APIM.    |

{% hint style="info" %}
A certificate with no end date stays active until you remove it from the list.
{% endhint %}

{% hint style="warning" %}
Neither GKO nor APIM rejects a certificate whose own expiration date is earlier than its `endsAt`, or a certificate that has already expired. APIM computes the status of a certificate from `startsAt` and `endsAt` only, so keep both dates within the validity period of the certificate.
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

When using refs, the operator resolves the certificate content when the resource is admitted and on each reconciliation.

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

Template compilation is handled by the operator's existing template engine. This mode requires templating to be enabled on the operator, which is the default (`manager.templating.enabled` in the Helm chart).

## Certificate Rotation

To rotate certificates without downtime:

1. **Add** the new certificate to the `clientCertificates` list (keeping the old one).
2. **Apply** the updated Application. The operator reconciles and registers both certificates with APIM.
3. **Verify** the new certificate works by calling the gateway with it.
4. **Remove** the old certificate from the list.
5. **Apply** again. The operator removes the old certificate from APIM.

To bound the overlap instead of removing the old certificate by hand, set its `endsAt` date in step 1. Both certificates stay active until that date. The scheduled job of the APIM Management API then revokes the old certificate at its next run after the date, every day at midnight by default, and updates the mTLS subscriptions of the application. Remove the entry from the list once the date has passed.

## Updates and APIM

On each update, APIM compares the list with the certificates it holds for the application: it creates the certificates that are missing, updates the name and the dates of the certificates that changed, and deletes the certificates that are no longer in the list. Deleting a certificate updates the mTLS subscriptions of the application.

Starting with APIM 4.12.20 and 4.13.0, APIM matches a certificate you send with the stored one by its SHA-256 fingerprint. In earlier versions, it matches by the exact PEM text, so a certificate whose PEM text differs from the stored copy, for example in its line breaks, is treated as a new certificate and the update fails with the message `Client certificate with fingerprint [<fingerprint>] is already used by another active application.`

## Validation Rules

GKO checks the following rules when the resource is admitted:

* `clientCertificate` (singular) and `clientCertificates` (plural) **cannot be used together**. Choose one or the other.
* Each entry must have **either** `content` **or** `ref`, but not both (and not neither).
* The `ref.kind` must be `secrets` or `configmaps`.
* An `Application` update is rejected when a `Subscription` of the application to an mTLS plan has an `endingAt` date that is later than every certificate `endsAt` date. When at least one certificate has no `endsAt`, the rule doesn't apply.
* A `Subscription` to an mTLS plan is rejected when the application has no client certificate, and when its `endingAt` date is later than every certificate `endsAt` date, unless at least one certificate has no `endsAt`.

APIM checks the following rules when GKO sends the certificates:

* The certificate must be a valid PEM certificate.
* The certificate cannot be a CA certificate.
* If the PEM contains several certificates (for example, a certificate chain), only the first certificate is used.
* `startsAt` must be before `endsAt`.
* Every certificate in the list must have a different content.
* A certificate whose SHA-256 fingerprint is already used by a certificate that isn't revoked on another active application of the environment is rejected.

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
