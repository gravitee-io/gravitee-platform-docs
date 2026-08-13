# Configure multi-domain TLS on a Gateway

## Overview

A single `Gateway` resource serves HTTPS traffic for several domains on the same port. Define one HTTPS listener per domain, each with its own hostname and TLS certificate. GKO configures the deployed Gravitee Gateway to present each listener's certificate to its matching domain using Server Name Indication (SNI).

{% hint style="info" %}
Multi-domain TLS requires GKO 4.12.11 or later. In earlier releases, only one certificate applies to each port: the certificate of the first accepted listener on that port.
{% endhint %}

### How it works

The multi-domain TLS flow works as follows:

1. You define several HTTPS listeners on the same port, each with a distinct hostname and its own `certificateRefs` entry.
2. GKO validates that each referenced Secret exists and contains PEM-encoded `tls.crt` and `tls.key` data.
3. GKO mounts each listener's certificate Secret into the Gateway pod as a read-only volume and enables SNI on the deployed Gravitee Gateway.
4. When a client opens a TLS connection, the Gravitee Gateway reads the requested server name and presents the certificate whose domain matches it. When no certificate matches the requested server name, the Gateway presents a fallback certificate from the configured set.

## Prerequisites

Before configuring multi-domain TLS, verify the following:

* Install GKO with the Gateway API controller enabled. See [Gateway API](README.md) for setup instructions.
* Verify a `GatewayClass` and `GatewayClassParameters` resource exist.
* Create a TLS Secret per domain, containing PEM-encoded `tls.crt` and `tls.key` data. To provision the certificates automatically, see [Configure TLS with cert-manager](tls-with-cert-manager.md).

## Define one HTTPS listener per domain

Each listener declares its own `hostname` and references its own TLS certificate. The following `Gateway` serves `api.example.com` and `portal.example.com` on port 443:

{% code lineNumbers="true" %}
```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: gravitee-gateway
spec:
  gatewayClassName: gravitee-gateway
  listeners:
    - name: api
      port: 443
      protocol: HTTPS
      hostname: api.example.com
      tls:
        certificateRefs:
          - group: ""
            kind: Secret
            name: api-example-com-tls
    - name: portal
      port: 443
      protocol: HTTPS
      hostname: portal.example.com
      tls:
        certificateRefs:
          - group: ""
            kind: Secret
            name: portal-example-com-tls
```
{% endcode %}

The following rules apply to listeners that share a port:

* Give each listener a distinct hostname. Two listeners with the same port and the same hostname conflict, and GKO rejects both.
* Use the same protocol for every listener on the port. Two listeners with the same port and different protocols conflict, and GKO rejects both.
* Reference exactly one certificate per listener. GKO rejects a listener with zero or several `certificateRefs` entries.
* Reference a Secret in another namespace only when a `ReferenceGrant` in that namespace permits it. Without a `ReferenceGrant`, GKO rejects the listener.

{% hint style="info" %}
When a port has a single TLS listener, SNI isn't enabled and the Gateway serves that listener's certificate directly from the referenced Secret.
{% endhint %}

## Attach routes to each domain

Declare each domain in the `hostnames` field of the `HTTPRoute` that serves it:

{% code lineNumbers="true" %}
```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: api-route
spec:
  parentRefs:
  - name: gravitee-gateway
    kind: Gateway
    group: gateway.networking.k8s.io
    namespace: default
  hostnames:
    - api.example.com
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /
      backendRefs:
        - kind: Service
          group: ""
          name: api-backend
          namespace: default
          port: 8080
```
{% endcode %}

To bind a route to a single listener instead, set `sectionName` in the route's `parentRefs` entry to the listener name. A route without a `hostnames` field that targets a listener through `sectionName` serves the hostname of that listener.

## Verification

To verify multi-domain TLS is working as expected, follow these steps:

1. Check that the Gateway is programmed and has an address:

    ```sh
    kubectl get gateway gravitee-gateway
    ```

    This command results in the following output:

    ```
    NAME               CLASS              ADDRESS        PROGRAMMED   AGE
    gravitee-gateway   gravitee-gateway   203.0.113.10   True         2m
    ```

2. Check that every listener is accepted:

    ```sh
    kubectl get gateway gravitee-gateway \
      -o jsonpath='{range .status.listeners[*]}{.name}{": "}{.conditions[?(@.type=="Accepted")].status}{"\n"}{end}'
    ```

    This command results in the following output:

    ```
    api: True
    portal: True
    ```

3. Retrieve the Gateway address:

    ```sh
    GATEWAY_IP=$(kubectl get gateway gravitee-gateway -o jsonpath='{.status.addresses[0].value}')
    ```

4. Confirm each domain is served with its own certificate:

    ```sh
    echo | openssl s_client -connect "$GATEWAY_IP":443 \
      -servername api.example.com 2>/dev/null \
      | openssl x509 -noout -subject
    ```

    ```sh
    echo | openssl s_client -connect "$GATEWAY_IP":443 \
      -servername portal.example.com 2>/dev/null \
      | openssl x509 -noout -subject
    ```

    The first command prints the subject of the `api.example.com` certificate, and the second command prints the subject of the `portal.example.com` certificate.

## What's next

* [Configure TLS with cert-manager](tls-with-cert-manager.md): Provision and renew the per-domain certificates automatically.
* [Configure DNS with external-dns](dns-with-external-dns.md): Configure DNS record creation for Gateway Services.
* [HTTPRoute](httproute.md): Configure path-based routing, header matching, traffic splitting, redirects, URL rewrites, and header modification.
