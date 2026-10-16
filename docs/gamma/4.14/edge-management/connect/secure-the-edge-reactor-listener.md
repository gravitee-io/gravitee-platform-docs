---
hidden: false
noIndex: false
description: The Gamma Edge Reactor listener is plain HTTP by default. Learn how to run it over TLS and ask the Edge Daemons for a client certificate in gravitee.yml or the Helm chart.
---

# Secure the Edge Reactor listener

## Overview

The Edge Reactor listens on its own port on the gateway, `18093` by default, separate from the port that serves your APIs. By default, the listener is plain HTTP and asks no daemon for a certificate.

The mTLS plan of daemon authentication only matches a daemon whose certificate reaches the Edge Reactor. Run the listener over TLS and ask the daemons for a certificate, or, when TLS ends at a proxy in front of the gateway, have that proxy forward the certificate. See [Configure daemon authentication](configure-daemon-authentication.md).

The listener reads its settings from the `edge` block of the gateway's `gravitee.yml`, or from `gateway.edge` in the Helm chart.

## Configure the listener in gravitee.yml

Add an `edge` block to the `gravitee.yml` of the gateway:

```yaml
edge:
  port: 18093
  secured: true
  ssl:
    clientAuth: request
    keystore:
      type: pem
      certificates:
        - cert: ${gravitee.home}/security/edge-server.pem
          key: ${gravitee.home}/security/edge-server.key
    truststore:
      type: pem
      path: ${gravitee.home}/security/edge-fleet-ca.pem
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
| `ssl.truststore.path`       | The truststore file, which holds the certificate authority of your fleet. See [Trust the certificate authority of your fleet](#trust-the-certificate-authority-of-your-fleet).                         | -         |
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
      clientAuth: request
      keystore:
        type: pem
        certificates:
          - cert: /opt/graviteeio-gateway/security/edge-server.pem
            key: /opt/graviteeio-gateway/security/edge-server.key
      truststore:
        type: pem
        path: /opt/graviteeio-gateway/security/edge-fleet-ca.pem
```

Mount the keystore and the truststore files into the gateway pods, or point `ssl.keystore.secret` and `ssl.truststore.secret` at Kubernetes secrets instead of files, for example `secret://kubernetes/apim-gateway-edge-tls`.

To expose the listener outside the cluster, see [Configure Edge Ingress](configure-edge-ingress.md).

## Choose how the listener asks for a certificate

`ssl.clientAuth` decides what happens to a daemon, depending on the certificate it presents:

| Value      | Outcome                                                                                                                                                                                                                                                                                                       |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `none`     | The listener never asks for a certificate, so the mTLS plan matches no daemon. While the keyless plan is published, it serves every daemon, even one that holds an enrolled certificate. Once the keyless plan is closed, every daemon is refused.                                                           |
| `request`  | The listener asks for a certificate and accepts a daemon that has none. A daemon that presents no certificate is served by the keyless plan while it's published. A daemon that presents an enrolled certificate is served by the mTLS plan. A daemon that presents a certificate that isn't enrolled is refused, even while the keyless plan is published. |
| `required` | The TLS handshake fails for a daemon that presents no certificate, so the keyless plan serves no daemon. A daemon that presents an enrolled certificate is served by the mTLS plan, and one that presents a certificate that isn't enrolled is refused.                                                       |

Gravitee recommends `request` on development and test environments, and `required` in production.

When the settings let no client certificate reach the listener, the gateway logs a warning at startup that begins with `No client certificate can ever reach the Edge server`.

## Trust the certificate authority of your fleet

The truststore holds the certificate authority that signs the certificates of your fleet, not the enrolled certificates themselves. TLS checks that a daemon's certificate chains to that authority, and the mTLS plan then matches the exact certificate against the ones enrolled on the **Daemon authentication** page.

Recommended: Use a dedicated intermediate certificate authority for your fleet. With a corporate-wide one, more certificates complete the TLS handshake with the listener.

## Terminate TLS in front of the gateway

When a proxy in front of the gateway ends TLS, such as an Ingress or a load balancer, the daemon's certificate stops at that proxy. For the mTLS plan to match it, have the proxy forward the certificate in a request header, and name that header in the gateway's HTTP settings with `http.ssl.clientAuthHeader.name`. Only a header in the form that NGINX sets works.

The Edge Reactor reads the certificate from the same header as the rest of the gateway. Set it only when the proxy writes that header on every request, so that no daemon sends its own.

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
