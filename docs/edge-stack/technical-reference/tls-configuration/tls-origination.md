---
description: Overview of TLS Origination.
noIndex: true
---

# TLS Origination

Sometimes you may want traffic from Ambassador Edge Stack to your services to be encrypted. For the cases where terminating TLS at the ingress is not enough, Ambassador Edge Stack can be configured to originate TLS connections to your upstream services.

### Basic configuration

Telling Ambassador Edge Stack to talk to your services over HTTPS is easily configured in the `Mapping` definition by setting `https://` in the `service` field.

```yaml
---
apiVersion: getambassador.io/v3alpha1
kind: Mapping
metadata:
  name: basic-tls
spec:
  hostname: "*"
  prefix: /
  service: https://example-service
```

### Advanced configuration using a `TLSContext`

If your upstream services require more than basic HTTPS support (for example, providing a client certificate or setting the minimum TLS version support) you must create a `TLSContext` for Ambassador Edge Stack to use when originating TLS. For example:

```yaml
---
apiVersion: getambassador.io/v3alpha1
kind: TLSContext
metadata:
  name: tls-context
spec:
  secret: self-signed-cert
  min_tls_version: v1.3
  sni: some-sni-hostname
```

{% hint style="info" %}
The Kubernetes Secret named by `secret` must contain a valid TLS certificate. If the environment variable `AMBASSADOR_FORCE_SECRET_VALIDATION` is set and the Secret contains an invalid certificate, Ambassador Edge Stack will reject the `TLSContext` and prevent its use; see [#certificates-and-secrets](tls-overview.md#certificates-and-secrets "mention") in the TLS overview.
{% endhint %}

Configure Ambassador Edge Stack to use this `TLSContext` for connections to upstream services by setting the `tls` attribute of a `Mapping`:

```yaml
---
apiVersion: getambassador.io/v3alpha1
kind: Mapping
metadata:
  name: mapping-with-tls-context
spec:
  hostname: "*"
  prefix: /
  service: https://example-service
  tls: tls-context
```

The `example-service` service must now support TLS v1.3 for Ambassador Edge Stack to connect.

{% hint style="warning" %}
The Kubernetes Secret named by `secret` must contain a valid TLS certificate. If the environment variable `AMBASSADOR_FORCE_SECRET_VALIDATION` is set and the Secret contains an invalid certificate, Ambassador Edge Stack will reject the `TLSContext` and prevent its use; see [#certificates-and-secrets](tls-overview.md#certificates-and-secrets "mention") in the TLS overview.
{% endhint %}

{% hint style="warning" %}
A `TLSContext` requires a certificate be provided, even in cases where the upstream service does not require it (for origination) and the `TLSContext` is not being used to terminate TLS. In this case, simply generate and provide a self-signed certificate.
{% endhint %}
