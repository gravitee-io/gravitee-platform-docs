# Kubernetes CRD Configuration for Multi-Certificate mTLS

## Kubernetes Application CRD

For Kubernetes deployments, certificates can be specified using inline content, Secret/ConfigMap references, or template notation.

### Inline certificates

Use the `content` field with PEM or Base64-encoded data:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: Application
spec:
 settings:
 tls:
 clientCertificates:
 - name: "cert-2026"
 startsAt: "2024-01-01T00:00:00Z"
 endsAt: "2026-12-31T23:59:59Z"
 content: |
 -----BEGIN CERTIFICATE-----
 ...
 -----END CERTIFICATE-----
```

### Secret and ConfigMap references

Use the `ref` object to reference Kubernetes resources:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: Application
spec:
 settings:
 tls:
 clientCertificates:
 - name: "from-secret"
 ref:
 kind: secrets
 name: client-cert-secret
 key: tls.crt
 - name: "from-configmap"
 ref:
 kind: configmaps
 name: client-cert-configmap
 key: cert.pem
```

The `ref` object supports the following fields:

| Field | Type | Default | Description |
|:------|:-----|:--------|:------------|
| `kind` | string | `secrets` | Resource type: `secrets` or `configmaps` |
| `name` | string | | Name of the Secret or ConfigMap |
| `key` | string | `tls.crt` | Key within the resource containing the certificate |
| `namespace` | string | Application namespace | Namespace of the referenced resource |

### Template notation

Use template notation to reference Secrets or ConfigMaps:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: Application
spec:
 settings:
 tls:
 clientCertificates:
 - name: "from-secret-template"
 content: "[[ secret `client-cert-secret/tls.crt` ]]"
 - name: "from-configmap-template"
 content: "[[ configmap `client-cert-configmap/cert.pem` ]]"
```

Template notation requires `ENABLE_TEMPLATING=true` in the operator configuration.

## Restrictions

* Requires gravitee-kubernetes-operator [VERSION TBD] or later for Application CRD multi-certificate support
* Requires Gravitee APIM 4.10 or later (mTLS policy v2.0.0-alpha.1 minimum)

For breaking changes and migration considerations, see [Breaking Changes and Restrictions](multi-certificate-mtls-breaking-changes-and-restrictions.md).

## End-User Configuration

