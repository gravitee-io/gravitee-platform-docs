---
description: The AMCertificate custom resource declares a certificate of an Access Management security domain for the Gravitee Kubernetes Operator 4.13. See how the keystore and its passwords are set.
---

# AMCertificate

The `AMCertificate` custom resource declares a certificate of a security domain in Gravitee Access Management (AM). It names the [`AMSecurityDomain`](amsecuritydomain.md) it belongs to, and GKO creates, updates, and deletes the certificate under that domain, through the domain's [`AMContext`](amcontext.md).

## Overview

The `domainRef` is required, can't change, and must name an `AMSecurityDomain` in the same namespace as the certificate. In AM, the key of the certificate is the namespace and the name of the resource joined with a hyphen (e.g. `production-system-cert`). The rules of a domain key apply: lowercase letters, digits, and hyphens, up to 255 characters. A domain names the certificate by that key in `spec.certificateSettings.fallbackCertificate`.

You can apply the certificate before its domain. It's stored with a warning, its `ResolvedRefs` condition stays `False` until AM has created the domain, and GKO then creates the certificate. The domain owns the certificate: deleting the `AMSecurityDomain` deletes the certificate in AM and removes the `AMCertificate` resource.

The `type` names an AM certificate plugin, such as `pkcs12-am-certificate` or `javakeystore-am-certificate`, and `configuration` holds the settings of that plugin. For the plugins and their settings, see [Certificates](https://documentation.gravitee.io/am/guides/certificates) in the Access Management documentation. The `type` can't change once the resource is created. The keystore goes in the configuration as a JSON string with the `name` of the file and its base64 `content`, as in the example.

The passwords can come from a Kubernetes Secret through a template, which GKO resolves before it sends the certificate to AM. AM then stores them, and returns them masked, as `********`. GKO treats a masked value as unchanged when it compares the resource with AM. The passwords can also be AM secret expressions, which AM resolves itself when it loads the certificate. See [Domain Secrets](https://documentation.gravitee.io/am/getting-started/configuration/domain-secrets) in the Access Management documentation.

With `system: true`, the resource gives the domain the default certificate that AM builds from its own configuration. Only `domainRef` and `system` are needed then. The `name`, `type`, and `configuration` fields are ignored, with a warning when they're set, and the status shows the name and type AM gave the certificate. A domain has at most one system certificate. The `system` flag can't change once the resource is created.

Before the resource is stored, GKO asks AM to validate it without saving it, unless the domain isn't in AM yet. An error reported by AM rejects the resource, a warning is returned with it, and an AM that can't be reached rejects it. See [Admission validation](../admission-validation.md) and [Drift detection](../drift-detection.md).

Deleting the resource deletes the certificate in AM. GKO refuses the deletion while an `AMSecurityDomain` of the same namespace names the certificate in `spec.certificateSettings.fallbackCertificate`: the error gives the number of domains and a `kubectl` command that lists them. A domain that's being deleted doesn't count. AM refuses to delete a certificate that an application, an identity provider, or a protected resource still uses: the resource then stays, and its `Accepted` condition carries the message from AM. A certificate already deleted in AM, or deleted with its domain, doesn't block the deletion.

## Example

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: banking-signing
  namespace: banking
stringData:
  keystore.b64: <base64 PKCS#12 file>
  storepass: <password>
  keypass: <password>
---
apiVersion: gravitee.io/v1alpha1
kind: AMCertificate
metadata:
  name: signing
  namespace: banking
spec:
  domainRef:
    name: banking
  name: Token signing
  type: pkcs12-am-certificate
  configuration:
    content: '{"name":"keystore.p12","content":"[[ secret `banking-signing/keystore.b64` ]]"}'
    alias: signing
    storepass: "[[ secret `banking-signing/storepass` ]]"
    keypass: "[[ secret `banking-signing/keypass` ]]"
    algorithm: RS256
    use: [sig]
```

A domain of the `banking` namespace uses this certificate as its fallback with `fallbackCertificate: banking-signing`.

## Key fields

| Field | Description |
|:------|:------------|
| `spec.domainRef` | `name` of the `AMSecurityDomain`, in the same namespace. Required, and can't change |
| `spec.name` | Name of the certificate. Required unless `system` is `true` |
| `spec.type` | Certificate plugin. Required unless `system` is `true`, and can't change |
| `spec.configuration` | Settings of the plugin, as a free-form object. The keystore file field is a JSON string with `name` and `content`. Required unless `system` is `true` |
| `spec.system` | Whether the resource is the domain's system certificate, built by AM. Defaults to `false`, and can't change |

## Validation

* `spec.domainRef` is required, can't change, and names a domain in the same namespace.
* `spec.name`, `spec.type`, and `spec.configuration` are required unless `spec.system` is `true`.
* `spec.type` and `spec.system` can't change.
* The namespace and name of the resource give a key of lowercase letters, digits, and hyphens, up to 255 characters.
* A domain that doesn't exist, or that AM hasn't created yet, gives a warning. The certificate is created once the domain is.
* An error reported by AM rejects the resource. An AM that can't be reached rejects it too.
* A certificate that a domain of the same namespace names as its fallback certificate can't be deleted.

## Verification

List the certificates of a namespace:

```sh
kubectl get amcertificates -n banking
```

Next to each resource, the output shows the name and type AM stored, the domain the certificate belongs to, and when it expires, as AM reports it.
