# Kubernetes Gateway API

{% hint style="warning" %}
**Experimental:** Kubernetes Gateway API support in GKO is experimental and subject to change in future releases. The Gateway API controller is disabled by default.
{% endhint %}

## Overview

The Gravitee Kubernetes Operator (GKO) implements the [Kubernetes Gateway API](https://gateway-api.sigs.k8s.io/) specification, providing a standardized way to configure HTTP traffic routing through the Gravitee Gateway using Kubernetes-native resources.

Unlike the [Gravitee Ingress Controller](../gravitee-ingress-controller.md), which creates v2 API definitions, the Gateway API controller creates **v4 API definitions**. This is the recommended approach for new Kubernetes-native deployments.

GKO is officially recognized as a [partially conformant](https://gateway-api.sigs.k8s.io/implementations/) implementation of the Kubernetes Gateway API v1.3 standard channel.

## Supported resources

The following table lists the Gateway API resources that GKO supports:

| Resource | API group | API version | Status |
|----------|-----------|-------------|--------|
| GatewayClass | `gateway.networking.k8s.io` | v1 | Supported |
| Gateway | `gateway.networking.k8s.io` | v1 | Supported |
| HTTPRoute | `gateway.networking.k8s.io` | v1 | Supported (partial conformance) |
| ReferenceGrant | `gateway.networking.k8s.io` | v1beta1 | Supported (cross-namespace references) |
| GatewayClassParameters | `gravitee.io` | v1alpha1 | Supported (Gravitee extension) |
| KafkaRoute | `gravitee.io` | v1alpha1 | Experimental |

GRPCRoute, TCPRoute, TLSRoute, and UDPRoute are **not** supported.

## Prerequisites

Before enabling the Gateway API controller:

- Install GKO in **cluster-scoped mode**. The GatewayClass resource is cluster-scoped, so namespaced installations are not compatible with the Gateway API controller.
- Ensure `manager.scope.namespaces` is empty (`[]`).

## Enable the Gateway API controller

Set the following Helm values when installing or upgrading GKO:

```yaml
gatewayAPI:
  controller:
    enabled: true
manager:
  scope:
    cluster: true
    namespaces: []
```

GKO automatically installs the required Gateway API CRDs when the controller is enabled.

## Resource hierarchy

A Gateway API deployment in GKO follows this resource hierarchy:

```
GatewayClassParameters (Gravitee-specific configuration)
  └── GatewayClass (references GatewayClassParameters)
        └── Gateway (references GatewayClass, defines listeners)
              └── HTTPRoute (references Gateway, defines routing rules)
```

### GatewayClassParameters

The `GatewayClassParameters` custom resource is the Gravitee extension point for configuring Gateway API deployments. It controls licensing, Kafka support, custom gateway configuration, and Kubernetes deployment settings.

For a full reference, see [GatewayClassParameters CRD](../../overview/custom-resource-definitions/gatewayclassparameters.md).

### GatewayClass

The `GatewayClass` resource registers Gravitee as a Gateway API controller. Set `controllerName` to `apim.gravitee.io/gateway` and reference a `GatewayClassParameters` resource:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: GatewayClass
metadata:
  name: gravitee-gateway
spec:
  controllerName: apim.gravitee.io/gateway
  parametersRef:
    kind: GatewayClassParameters
    group: gravitee.io
    name: gravitee-gateway
    namespace: default
```

### Gateway

The `Gateway` resource defines listeners that accept traffic. GKO supports HTTP and HTTPS listeners:

{% code lineNumbers="true" %}
```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: gravitee-gateway
  annotations:
    cert-manager.io/cluster-issuer: self-signed
    cert-manager.io/usages: "server auth"
    cert-manager.io/subject-organizations: gravitee
spec:
  gatewayClassName: gravitee-gateway
  listeners:
    - name: http
      port: 80
      protocol: HTTP
    - name: https
      port: 443
      protocol: HTTPS
      hostname: '*.apis.example.dev'
      tls:
        certificateRefs:
          - group: ""
            kind: Secret
            name: "https-server"
```
{% endcode %}

When GKO reconciles a Gateway resource, it deploys a Gravitee Gateway instance in the cluster with the specified listener configuration.

## Minimal deployment example

This example deploys a Gravitee Gateway with an HTTPRoute that routes traffic to a backend service:

{% code lineNumbers="true" %}
```yaml
apiVersion: gravitee.io/v1alpha1
kind: GatewayClassParameters
metadata:
  name: gravitee-gateway
spec:
  kubernetes:
    deployment:
      template:
        spec:
          containers:
          - name: gateway
            image: graviteeio/apim-gateway
          securityContext:
            runAsNonRoot: true
            runAsUser: 1001
---
apiVersion: gateway.networking.k8s.io/v1
kind: GatewayClass
metadata:
  name: gravitee-gateway
spec:
  controllerName: apim.gravitee.io/gateway
  parametersRef:
    kind: GatewayClassParameters
    group: gravitee.io
    name: gravitee-gateway
    namespace: default
---
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: gravitee-gateway
spec:
  gatewayClassName: gravitee-gateway
  listeners:
    - name: http
      port: 80
      protocol: HTTP
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: http-route-demo
spec:
  parentRefs:
  - name: gravitee-gateway
    kind: Gateway
    group: gateway.networking.k8s.io
    namespace: default
  hostnames:
   - demo.apis.example.dev
  rules:
    - matches:
       - path:
           type: PathPrefix
           value: /bin
      backendRefs:
        - kind: Service
          group: ""
          name: httpbin-1
          namespace: default
          port: 8080
```
{% endcode %}

## What's next

* [HTTPRoute](httproute.md) — Configure path-based routing, header matching, traffic splitting, redirects, URL rewrites, and header modification.
* [GatewayClassParameters](../../overview/custom-resource-definitions/gatewayclassparameters.md) — Configure Gravitee-specific Gateway API settings including Kubernetes deployment options and autoscaling.
* [KafkaRoute](../../overview/custom-resource-definitions/kafkaroute.md) — Route Kafka traffic through the Gateway (experimental, requires Enterprise license).
