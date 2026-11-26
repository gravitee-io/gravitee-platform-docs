---
hidden: false
noIndex: false
description: The Gamma Edge Reactor listener is plain HTTP by default. Learn how to run it over TLS and ask the Edge Daemons for a client certificate in gravitee.yml or the Helm chart.
---

# Secure the Edge Reactor listener

## Overview

The Edge Reactor listens on its own port on the gateway, `18093` by default, separate from the port that serves your APIs. By default, the listener is plain HTTP and asks no daemon for a certificate.

mTLS, in daemon authentication, only authenticates a daemon whose certificate reaches the Edge Reactor. Run the listener over TLS and ask the daemons for a certificate, or, when TLS ends at a proxy in front of the gateway, have that proxy forward the certificate. See [Configure daemon authentication](configure-daemon-authentication.md).

Once the listener runs over TLS, the daemons reach it at an `https://` **Reactor URL**, and each daemon must trust the listener's certificate. When a private certificate authority signs that certificate, or when it's self-signed, install the daemons with `--reactor-ca`. See [Configure daemon authentication](configure-daemon-authentication.md#turn-on-mtls).

The listener reads its settings from the `edge` block of the gateway's `gravitee.yml`, or from `gateway.edge` in the Helm chart.

## Configure the listener in gravitee.yml

Add an `edge` block to the `gravitee.yml` of the gateway:

```yaml
edge:
  port: 18093
  secured: true
  ssl:
    clientAuth: request # for development and test. In production, use required.
    keystore:
      type: pem
      certificates:
        - cert: ${gravitee.home}/security/edge-server.pem
          key: ${gravitee.home}/security/edge-server.key
```

The following table describes each field:

| Property                    | Description                                                                                                                                                                                              | Default   |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- |
| `port`                      | The port the listener binds to.                                                                                                                                                                          | `18093`   |
| `host`                      | The address the listener binds to.                                                                                                                                                                       | `0.0.0.0` |
| `secured`                   | Runs the listener over TLS.                                                                                                                                                                              | `false`   |
| `ssl.clientAuth`            | Whether the listener asks a daemon for a client certificate: `none`, `request`, or `required`. See [Choose how the listener asks for a certificate](#choose-how-the-listener-asks-for-a-certificate).   | `none`    |
| `ssl.keystore.type`         | The format of the listener's own TLS identity: `jks`, `pem`, `pkcs12`, or `self-signed`.                                                                                                                 | `jks`     |
| `ssl.keystore.path`         | The keystore file, for the `jks` and `pkcs12` types.                                                                                                                                                     | -         |
| `ssl.keystore.certificates` | The certificate and key files, as `cert` and `key` pairs, for the `pem` type.                                                                                                                            | -         |
| `ssl.keystore.password`     | The password of the keystore.                                                                                                                                                                            | -         |
| `ssl.truststore.type`       | The format of the truststore: `jks`, `pem`, or `pkcs12`.                                                                                                                                                 | `jks`     |
| `ssl.truststore.path`       | Optional. A truststore file, which changes which certificates complete the TLS handshake. See [Trust the enrolled certificates](#trust-the-enrolled-certificates).                                    | -         |
| `ssl.truststore.password`   | The password of the truststore.                                                                                                                                                                          | -         |

## Configure the listener with Helm

In the Helm chart, the same settings go under `gateway.edge`. They take effect only when `gateway.edge.enabled` is `true`, and the chart passes the `ssl` block to the gateway as written:

```yaml
gateway:
  edge:
    enabled: true
    port: 18093
    secured: true
    ssl:
      clientAuth: request # for development and test. In production, use required.
      keystore:
        type: pem
        certificates:
          - cert: /opt/graviteeio-gateway/security/edge-server.pem
            key: /opt/graviteeio-gateway/security/edge-server.key
```

Mount the keystore files, and the truststore file if you use one, into the gateway pods, or point `ssl.keystore.secret` and `ssl.truststore.secret` at Kubernetes secrets instead of files, for example `secret://kubernetes/apim-gateway-edge-tls`.

To expose the listener outside the cluster, see [Configure Edge Ingress](configure-edge-ingress.md).

## Choose how the listener asks for a certificate

`ssl.clientAuth` decides what happens to a daemon, depending on the certificate it presents:

| Value      | Outcome                                                                                                                                                                                                                                                                                                                   |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `none`     | The listener never asks for a certificate. Unless a proxy forwards the certificate in a header, mTLS authenticates no daemon, even one that holds an enrolled certificate. While keyless is on, every daemon is then served, and while mTLS is the only method on, every daemon is refused.                              |
| `request`  | The listener asks for a certificate and accepts a daemon that has none. A daemon that presents no certificate is served while keyless is on. While mTLS is on, a daemon that presents a certificate is served only when that certificate is enrolled in the environment and active, even while keyless is on.             |
| `required` | The TLS handshake fails for a daemon that presents no certificate, even while keyless is on. It also fails for a certificate that the listener doesn't trust, and that daemon gets no HTTP answer. See [Trust the enrolled certificates](#trust-the-enrolled-certificates). While mTLS is on, a daemon that completes the handshake is served only when its certificate is enrolled in the environment and active. |

Gravitee recommends `request` on development and test environments, and `required` in production.

When the settings let no client certificate reach the listener, the gateway logs a warning at startup that begins with `No client certificate can ever reach the Edge server`.

## Trust the enrolled certificates

The listener trusts the certificates enrolled on the **Daemon authentication** page of every environment that the gateway serves, and no other certificate by default. Each certificate is trusted from the start of its validity until its end, and a replacement is trusted before the certificate it replaces is removed. Without a truststore, the listener trusts no certificate until an enrolled certificate is active, so with `required`, every daemon is refused at the TLS handshake until then.

Without a truststore, completing the handshake only proves that a certificate is enrolled in one of the environments. While mTLS is on in the environment that the daemon calls, each call is then served only when the certificate is enrolled in that environment and active. While mTLS is off there, the certificate is ignored.

A truststore is optional. With `required`, a certificate that one of its certificate authorities signed also completes the handshake, even when it isn't enrolled, and the call is then refused while mTLS is on. With `request`, a truststore makes the handshake fail for a certificate that neither the truststore nor the enrolled certificates trust.

Recommended: Leave out the truststore, or use a dedicated intermediate certificate authority for your fleet. With a corporate-wide one, more certificates complete the TLS handshake with the listener.

## Terminate TLS in front of the gateway

When a proxy in front of the gateway ends TLS, such as an Ingress or a load balancer, the daemon's certificate stops at that proxy. For mTLS to authenticate the daemon, have the proxy forward the certificate in a request header, and name that header in the gateway's HTTP settings with `http.ssl.clientAuthHeader.name`. A header in the form that Nginx sets works.

The Edge Reactor reads the certificate from the same header as the rest of the gateway. Set it only when the proxy writes that header on every request, so that no daemon sends its own.

## Serve several environments from one gateway

One gateway serves the Edge API of every environment that it deploys, and keeps the configuration of each environment apart. A daemon installed with the ID of its environment, as the command under **Install script** on the **Daemon deployment** page installs it, gets the configuration of that environment only. When that environment has no Edge API on the gateway, the Edge Reactor answers the daemon with `404`, and never serves another environment instead.

A daemon installed without an environment ID, such as a daemon installed with a 4.13 script, doesn't name its environment. `edge.server.default_environment`, in the `gravitee.yml` of the gateway, decides which environment serves it:

```yaml
edge:
  server:
    default_environment: <environment ID>
```

The following table describes each value:

| Value             | Environment that serves the daemons installed without an environment ID                                                                                      |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Not set (default) | The only environment whose Edge API the gateway deploys. Once the gateway deploys the Edge API of several environments, the environment whose ID is `DEFAULT`. |
| An environment ID | That environment only.                                                                                                                                       |
| `""`              | None. The Edge Reactor answers these daemons with `404`.                                                                                                     |

When the environment that the setting selects has no Edge API on the gateway, the Edge Reactor answers these daemons with `404`, and the gateway logs a warning that begins with `Unscoped Edge requests resolve to environment`.

The Helm chart doesn't render `edge.server.default_environment` from `gateway.edge`. Set it instead with the `GRAVITEE_EDGE_SERVER_DEFAULT_ENVIRONMENT` environment variable of the gateway, in `gateway.env`:

```yaml
gateway:
  env:
    - name: GRAVITEE_EDGE_SERVER_DEFAULT_ENVIRONMENT
      value: <environment ID>
```

With `value: ""`, the setting is `""` rather than not set, and the Edge Reactor answers these daemons with `404`.

## Deploy the Edge API on gateways with sharding tags

The Edge API of each environment carries the `gravitee-edge-configuration` sharding tag. An Edge API deployed before the upgrade to 4.14 carries it only once the Edge configuration of its environment is deployed again, for example when you save a change with **Save & Deploy**. A gateway that deploys only the APIs of some sharding tags deploys the Edge API when `gravitee-edge-configuration` is one of them. Add it to the sharding tags of each such gateway that serves the Edge Reactor. Without it, that gateway doesn't deploy the Edge API, and its Edge Reactor answers the daemons with `404`. A gateway without sharding tags deploys every API, the Edge API included. See [Configure sharding tags for your internal and external Gateways](https://documentation.gravitee.io/apim/configure-and-manage-the-platform/gravitee-gateway/sharding-tags#configure-sharding-tags-for-your-internal-and-external-gateways).

## Rename the port setting

`edge.server.port` is deprecated. Use `edge.port`. The gateway still reads `edge.server.port` when `edge.port` isn't set, and logs a warning at startup. When both are set, `edge.port` wins. In the Helm chart, use `gateway.edge.port` instead of `gateway.edge.server.port`.

## Fix a gateway that doesn't start

If the listener can't start, the gateway doesn't start either, and the startup fails with `Unable to start Edge HTTP server on port` followed by the port. This happens, for example, when the port is already in use, or when the keystore or the truststore can't be read.

* If the port is in use, free it, or set `edge.port` to another port.
* If a store can't be read, check its type, its path, and its password.

## Verification

To verify that the listener is secured as expected, follow these steps:

1. Restart the gateway.
2. Check that the gateway log reads `Edge HTTP server listening on port 18093 (secured: true, clientAuth: REQUEST)`, with your port and your `ssl.clientAuth` value.
3. Check that the gateway log carries no warning that begins with `No client certificate can ever reach the Edge server`.

## Next steps

* **Decide how the daemons authenticate.** See [Configure daemon authentication](configure-daemon-authentication.md).
* **Expose the listener on Kubernetes.** See [Configure Edge Ingress](configure-edge-ingress.md).
