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
A `TLSContext` used for TLS origination needs a certificate in `secret` or `cert_chain_file`, even when the upstream service doesn't ask for one. In this case, generate and provide a self-signed certificate. A `TLSContext` that sets `upstream: true` and a certificate authority (CA) to trust doesn't need a certificate. For more information, see [Validate the upstream server certificate](tls-origination.md#validate-the-upstream-server-certificate).
{% endhint %}

### Validate the upstream server certificate

{% hint style="info" %}
Upstream server certificate validation requires Ambassador Edge Stack 3.15.0 or later. The `upstream`, `verify_server_hostname`, and `system_root_certs` fields exist only in `getambassador.io/v3alpha1`.
{% endhint %}

When the `TLSContext` of a `Mapping` sets `upstream: true` and a certificate authority (CA) to trust, Ambassador Edge Stack validates the certificate that the upstream service presents. It checks that the certificate chains to the CA. With `verify_server_hostname: true`, it also checks that the certificate matches the expected hostname. No client certificate is needed. If a check fails, the TLS handshake fails and the client gets a `503` response.

The `TLSContext` takes these fields for upstream server certificate validation:

| Property | Description | Default | Required |
| -------- | ----------- | ------- | -------- |
| `upstream` | Marks the `TLSContext` for TLS origination. Required for `verify_server_hostname` and `system_root_certs`, and for `ca_secret` or `cacert_chain_file` without a client certificate. Can't be combined with a non-empty `hosts` list, and a `Host` can't use a `TLSContext` that sets it. | `false` | No |
| `ca_secret` | The name of a Kubernetes Secret that holds the CA certificate to trust in its `tls.crt` key. | - | No |
| `cacert_chain_file` | The path of a CA certificate file in the Ambassador Edge Stack container. | - | No |
| `system_root_certs` | Set to `true` to trust the system CA bundle in the Ambassador Edge Stack container. Can't be combined with `ca_secret`, `cacert_chain_file`, or `crl_secret`. | `false` | No |
| `verify_server_hostname` | Set to `true` to also check that the certificate's subject alternative names match the expected hostname. Requires a CA to trust, such as `ca_secret`, `cacert_chain_file`, or `system_root_certs`. | `false` | No |

{% hint style="warning" %}
The CA must be in the `tls.crt` key of the Secret that `ca_secret` names. Ambassador Edge Stack doesn't read a `ca.crt` key.
{% endhint %}

To validate the upstream server certificate against your own CA, follow these steps:

1.  Create a Kubernetes Secret that holds the CA certificate, in the namespace of the `TLSContext`. Replace `ca.pem` with the file of the CA that signed the upstream service's certificate:

    ```bash
    kubectl create secret generic upstream-ca --from-file=tls.crt=ca.pem
    ```
2.  Create a `TLSContext` that trusts the CA and checks the hostname:

    ```yaml
    ---
    apiVersion: getambassador.io/v3alpha1
    kind: TLSContext
    metadata:
      name: upstream-validation
    spec:
      upstream: true
      ca_secret: upstream-ca
      sni: api.example.com
      verify_server_hostname: true
    ```
3.  Set the `tls` field of the `Mapping` to the name of the `TLSContext`:

    ```yaml
    ---
    apiVersion: getambassador.io/v3alpha1
    kind: Mapping
    metadata:
      name: upstream-mapping
    spec:
      hostname: "*"
      prefix: /upstream/
      service: api.example.com
      tls: upstream-validation
    ```

    Ambassador Edge Stack now accepts the upstream service's certificate only when it chains to the CA in `upstream-ca` and its subject alternative names match `api.example.com`.

{% hint style="info" %}
You don't need `https://` on `service` when the `Mapping` sets `tls`. Ambassador Edge Stack originates TLS for a `Mapping` whose `tls` names a valid `TLSContext`, and connects to port `443` unless `service` names another port.
{% endhint %}

To also present a client certificate to the upstream service, add `secret` to the `TLSContext` with the name of the Secret that holds the client certificate.

#### Expected hostname

With `verify_server_hostname: true`, Ambassador Edge Stack expects the first of these values that's set:

1. The `sni` field of the `TLSContext`. Ambassador Edge Stack also sends this value as the server name in the TLS handshake.
2. The `host_rewrite` field of the `Mapping`, without its port.
3. The host in the `service` field of the `Mapping`.

When the expected hostname is an IP address, Ambassador Edge Stack looks for it in the IP addresses of the certificate's subject alternative names instead of the DNS names.

Recommended: Set `sni` to the hostname in the upstream service's certificate. Without `sni`, Ambassador Edge Stack doesn't set a server name for the TLS handshake, but hostname verification still checks `host_rewrite` or the host in `service`. Servers that host several hostnames use the server name in the TLS handshake to choose which certificate to present. When the certificate they present doesn't match the expected hostname, the TLS handshake fails and the client gets a `503` response.

#### Trust the system CA bundle

To validate an upstream service whose certificate comes from a public CA, trust the system CA bundle in the Ambassador Edge Stack container instead of your own CA:

```yaml
---
apiVersion: getambassador.io/v3alpha1
kind: TLSContext
metadata:
  name: public-upstream
spec:
  upstream: true
  system_root_certs: true
  sni: api.example.com
  verify_server_hostname: true
```

To use a CA bundle from another path in the container, set the [`AMBASSADOR_SYSTEM_ROOT_CERTS_FILE`](../../edge-stack-user-guide/deployment/ambassador-edge-stack-environment-variables-and-ports.md#ambassador_system_root_certs_file) environment variable. If the bundle is missing, Ambassador Edge Stack rejects the `TLSContext`.

#### Rejected configurations

Ambassador Edge Stack rejects a `TLSContext` in each of these cases:

* It sets `upstream: true` and a non-empty `hosts` list.
* It sets `verify_server_hostname: true` without `upstream: true`.
* It sets `system_root_certs: true` without `upstream: true`.
* It sets `verify_server_hostname: true` without a CA to trust.
* It sets `system_root_certs: true` together with `ca_secret`, `cacert_chain_file`, or `crl_secret`.
* It sets `ca_secret` or `cacert_chain_file` without `upstream: true` and without a certificate in `secret` or `cert_chain_file`.
* Its `ca_secret` can't be loaded.
* Its `cacert_chain_file` doesn't exist in the Ambassador Edge Stack container.
* It sets `system_root_certs: true`, and the system CA bundle is missing.
* Its `crl_secret` can't be loaded.
* It sets no certificate, private key, CA, or certificate revocation list. For example, it only sets `sni` or `min_tls_version`.
* Its `secret` can't be loaded.
* The Secret that `secret` names has no private key.
* It sets both `secret` and `cert_chain_file`.
* It sets `cert_chain_file` without `private_key_file`.
* Its `cert_chain_file` or `private_key_file` doesn't exist in the Ambassador Edge Stack container.

When the `tls` field of a `Mapping` names a `TLSContext` that doesn't exist or that Ambassador Edge Stack rejected, and the `Mapping` uses the default Kubernetes Service Resolver, Ambassador Edge Stack doesn't connect to the upstream service. Requests to the `Mapping` get a `503` response until the `TLSContext` exists and is valid.

Ambassador Edge Stack logs each rejection. It logs a warning when a CA, a CA file, a certificate revocation list, or the system CA bundle can't be loaded, when `verify_server_hostname: true` has no CA, and when a `Mapping` names a `TLSContext` that doesn't exist or that it rejected.

#### Verification

To verify that Ambassador Edge Stack validates the upstream server certificate, follow these steps:

1.  Send a request through the `Mapping`. Replace `<ambassador-host>` with the hostname of your Ambassador Edge Stack:

    ```bash
    curl -i https://<ambassador-host>/upstream/
    ```

    The upstream service answers the request.
2.  Generate a CA certificate that didn't sign the upstream service's certificate:

    ```bash
    openssl req -x509 -newkey rsa:2048 -nodes -keyout other-ca.key -out other-ca.pem -days 1 -subj "/CN=other-ca"
    ```
3.  Store the certificate in a Kubernetes Secret in the namespace of the `TLSContext`:

    ```bash
    kubectl create secret generic other-ca --from-file=tls.crt=other-ca.pem
    ```
4.  Set `ca_secret` in the `TLSContext` to `other-ca`, and apply the `TLSContext`.
5.  Send the same request again. The response status is `503`, because the upstream service's certificate doesn't chain to the CA in `other-ca`.
6.  Set `ca_secret` back to `upstream-ca`, apply the `TLSContext`, and delete the `other-ca` Secret.
