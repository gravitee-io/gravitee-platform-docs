# Secure backend traffic with BackendTLSPolicy

## Overview

The `BackendTLSPolicy` resource configures TLS between the deployed Gravitee Gateway and your backend Services. Attach a policy to a Service to make the Gateway call that Service over HTTPS and validate its certificate against a CA bundle you provide. The Gateway also sends the hostname you configure as the `Host` header.

GKO supports `BackendTLSPolicy` `v1` from the Gateway API standard channel and installs its CRD together with the other Gateway API CRDs.

{% hint style="info" %}
BackendTLSPolicy support requires GKO 4.12.11 or later.
{% endhint %}

### How it works

The backend TLS flow works as follows:

1. You create a ConfigMap that contains the CA bundle under the `ca.crt` key.
2. You create a `BackendTLSPolicy` that targets the backend Service and references the ConfigMap.
3. GKO detects the policy and updates the APIs generated from the `HTTPRoute` resources that use the targeted Service as a backend.
4. The deployed Gateway calls the Service over HTTPS, trusts the referenced CA bundle, validates the server certificate, and sends the hostname from `spec.validation.hostname` as the `Host` header.

## Create the CA certificate ConfigMap

Store the CA bundle that signs the backend certificate in a ConfigMap, under the `ca.crt` key:

{% code lineNumbers="true" %}
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: backend-ca
data:
  ca.crt: |
    -----BEGIN CERTIFICATE-----
    ...
    -----END CERTIFICATE-----
```
{% endcode %}

Create the ConfigMap in the same namespace as the backend Service. When the policy references several ConfigMaps, the Gateway trusts the combined bundle.

## Create the policy

Target the backend Service in `targetRefs` and reference the ConfigMap in `validation.caCertificateRefs`:

{% code lineNumbers="true" %}
```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: BackendTLSPolicy
metadata:
  name: backend-tls
spec:
  targetRefs:
    - group: ""
      kind: Service
      name: api-backend
  validation:
    caCertificateRefs:
      - group: ""
        kind: ConfigMap
        name: backend-ca
    hostname: api-backend.example.com
```
{% endcode %}

Create the policy in the same namespace as the Service it targets. GKO watches `BackendTLSPolicy` resources, so applying, updating, or deleting a policy updates the APIs generated from the `HTTPRoute` resources that use the targeted Service.

## Target a specific Service port

To apply the policy to a single port of the Service, set `sectionName` to the name of that port in the Service definition:

{% code lineNumbers="true" %}
```yaml
spec:
  targetRefs:
    - group: ""
      kind: Service
      name: api-backend
      sectionName: https
```
{% endcode %}

A policy whose `sectionName` matches the port takes precedence over a policy that targets the whole Service.

## Send a client certificate to the backend

To authenticate the Gateway itself against backends that require mutual TLS, set `spec.tls.backend.clientCertificateRef` on the `Gateway` resource to a Secret that contains PEM-encoded `tls.crt` and `tls.key` data:

{% code lineNumbers="true" %}
```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: gravitee-gateway
spec:
  gatewayClassName: gravitee-gateway
  tls:
    backend:
      clientCertificateRef:
        group: ""
        kind: Secret
        name: gateway-client-cert
  listeners:
    - name: https
      port: 443
      protocol: HTTPS
      hostname: '*.apis.example.dev'
      tls:
        certificateRefs:
          - group: ""
            kind: Secret
            name: https-server
```
{% endcode %}

The Gateway presents this certificate when it calls backends covered by a `BackendTLSPolicy`. When the Secret reference omits a namespace, GKO reads the Secret from the Gateway's namespace.

## Constraints

* A policy applies to Services in the policy's own namespace.
* The `caCertificateRefs` entries reference ConfigMaps that contain a non-empty `ca.crt` key. A reference to another kind is rejected.
* The `wellKnownCACertificates` field isn't supported. A policy that sets it is rejected with the message `WellKnownCACertificates is not supported`.
* When two equivalent policies target the same Service, the oldest policy wins. The newer policy's `Accepted` condition is `False` with reason `Conflicted`.

## Verification

To verify the policy is working as expected, follow these steps:

1. Check the policy status conditions:

    ```sh
    kubectl describe backendtlspolicy backend-tls
    ```

    The `Accepted` condition reports `True` with the message `Policy has been accepted`, and the `ResolvedRefs` condition reports `True` with the message `All CA certificate references are valid`.

2. Send a request to a route backed by the targeted Service and confirm the backend responds:

    ```sh
    curl -i https://api.example.com/
    ```

## What's next

* [Gateway API overview](README.md): Set up GatewayClass, GatewayClassParameters, and Gateway resources.
* [Configure multi-domain TLS on a Gateway](multi-domain-tls.md): Serve several domains on the same port, each with its own TLS certificate.
* [Configure TLS with cert-manager](tls-with-cert-manager.md): Configure TLS certificate provisioning for Gateway HTTPS listeners.
* [HTTPRoute](httproute.md): Configure path-based routing, header matching, traffic splitting, redirects, URL rewrites, and header modification.
