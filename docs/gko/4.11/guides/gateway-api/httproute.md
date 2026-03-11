# HTTPRoute

{% hint style="warning" %}
**Experimental:** Kubernetes Gateway API support in GKO is experimental and subject to change in future releases.
{% endhint %}

## Overview

The `HTTPRoute` resource defines rules for routing HTTP traffic from a Gateway listener to backend Kubernetes Services. GKO reconciles each HTTPRoute into a v4 API definition that the Gravitee Gateway uses to handle requests.

GKO is partially conformant with the Kubernetes Gateway API v1.3 HTTPRoute specification. This page covers the supported features and provides configuration examples.

## Supported features

GKO passes 32 out of 33 core conformance tests and 7 out of 7 extended conformance tests for HTTPRoute (tested against GKO 4.10.3, Gateway API v1.4.1).

### Core features

| Feature | Status |
|---------|--------|
| Path prefix matching | Supported |
| Exact path matching | Supported |
| Header exact matching | Supported |
| Header regex matching | Supported |
| Query parameter matching | Supported |
| Multiple backend references | Supported |
| Cross-namespace backend references (via ReferenceGrant) | Supported |
| Matching across routes | Not supported |

### Extended features

| Feature | Status |
|---------|--------|
| Path redirect (`ReplacePrefixMatch`, `ReplaceFullPath`) | Supported |
| URL rewrite (`ReplacePrefixMatch`, `ReplaceFullPath`) | Supported |
| Port redirect | Supported |
| Scheme redirect | Supported |
| Response header modification (`set`, `add`, `remove`) | Supported |
| Custom gateway port (for example, 8080) | Supported |

### Unsupported features

The following extended features are not supported in the current release:

- Method matching
- CORS
- Request mirroring
- Request timeout
- Backend timeout
- Backend TLS policy
- WebSocket backend protocol
- H2C backend protocol
- Host rewrite
- Destination port matching
- Backend request header modification

## Path-based routing

Route traffic to different backend Services based on the request path:

{% code lineNumbers="true" %}
```yaml
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

Supported path match types:

| Type | Description | Example |
|------|-------------|---------|
| `PathPrefix` | Matches requests with the specified path prefix | `/bin` matches `/bin`, `/bin/headers`, `/bin/anything` |
| `Exact` | Matches only the exact path | `/bin` matches `/bin` only |
| `RegularExpression` | Matches paths against a regular expression | `/bin/.*` matches `/bin/headers`, `/bin/anything` |

## Header-based routing

Route traffic based on HTTP header values. This example routes requests with the header `env: canary` to a separate backend:

{% code lineNumbers="true" %}
```yaml
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
    - matches:
       - path:
           type: PathPrefix
           value: /bin
         headers:
          - name: env
            type: Exact
            value: canary
      backendRefs:
        - kind: Service
          group: ""
          name: httpbin-2
          namespace: default
          port: 8080
```
{% endcode %}

When multiple rules match, GKO selects the most specific match. In this example, a request to `/bin` with the header `env: canary` is routed to `httpbin-2` because the header match is more specific.

## Traffic splitting

Distribute traffic across multiple backends using weights. This example sends 90% of traffic to `httpbin-1` and 10% to `httpbin-2`:

{% code lineNumbers="true" %}
```yaml
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
          weight: 90
        - kind: Service
          group: ""
          name: httpbin-2
          namespace: default
          port: 8080
          weight: 10
```
{% endcode %}

GKO uses weighted round-robin load balancing when multiple backends are specified with weights. Backends with a weight of `0` are excluded from routing.

## Header modification

Add, set, or remove HTTP headers on requests and responses using filters.

### Request header modification

{% code lineNumbers="true" %}
```yaml
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
      filters:
      - type: RequestHeaderModifier
        requestHeaderModifier:
          add:
            - name: x-tag
              value: kubernetes.io,gravitee.io
          set:
            - name: x-tag
              value: acme.io
          remove:
            - x-rm
      backendRefs:
        - kind: Service
          group: ""
          name: httpbin-1
          namespace: default
          port: 8080
```
{% endcode %}

### Response header modification

{% code lineNumbers="true" %}
```yaml
      filters:
      - type: ResponseHeaderModifier
        responseHeaderModifier:
          set:
            - name: x-modified
              value: "true"
          add:
            - name: date
              value: today
```
{% endcode %}

Header modification operations:

| Operation | Description |
|-----------|-------------|
| `add` | Appends a value to the header. If the header exists, the value is appended with a comma separator. |
| `set` | Overwrites the header value. If the header does not exist, it is created. |
| `remove` | Removes the header from the request or response. |

## Request redirects

Redirect requests to a different URL using the `RequestRedirect` filter.

### Prefix replacement

Redirect requests by replacing the path prefix. This example redirects `/bin/*` to `https://httpbin.org/anything/*` with a 301 status code:

{% code lineNumbers="true" %}
```yaml
    - matches:
       - path:
           type: PathPrefix
           value: /bin
      filters:
      - type: RequestRedirect
        requestRedirect:
          statusCode: 301
          hostname: httpbin.org
          scheme: https
          path:
            type: ReplacePrefixMatch
            replacePrefixMatch: /anything
```
{% endcode %}

### Full path replacement

Replace the entire path. This example redirects `/bin/*` to `https://api.gravitee.io/echo` with a 302 status code:

{% code lineNumbers="true" %}
```yaml
    - matches:
       - path:
           type: PathPrefix
           value: /bin
      filters:
      - type: RequestRedirect
        requestRedirect:
          statusCode: 302
          hostname: api.gravitee.io
          scheme: https
          path:
            type: ReplaceFullPath
            replaceFullPath: /echo
```
{% endcode %}

### Redirect using request scheme and host

Omit the `scheme` and `hostname` fields to redirect using the original request's scheme and host:

{% code lineNumbers="true" %}
```yaml
    - matches:
       - path:
           type: PathPrefix
           value: /bin
      filters:
      - type: RequestRedirect
        requestRedirect:
          path:
            type: ReplaceFullPath
            replaceFullPath: /404
```
{% endcode %}

Supported redirect fields:

| Field | Description | Default |
|-------|-------------|---------|
| `statusCode` | HTTP status code for the redirect response | `302` |
| `scheme` | Target URL scheme (`http` or `https`) | Original request scheme |
| `hostname` | Target hostname | Original request host |
| `port` | Target port | `80` for `http`, `443` for `https` |
| `path.type` | `ReplacePrefixMatch` or `ReplaceFullPath` | — |

## URL rewrite

Rewrite the request URL before forwarding to the backend, without sending a redirect response to the client:

{% code lineNumbers="true" %}
```yaml
    - matches:
       - path:
           type: PathPrefix
           value: /bin
      filters:
      - type: URLRewrite
        urlRewrite:
          path:
            type: ReplacePrefixMatch
            replacePrefixMatch: /anything
      backendRefs:
        - kind: Service
          group: ""
          name: httpbin-1
          namespace: default
          port: 8080
```
{% endcode %}

URL rewrite supports the same path replacement types as request redirects (`ReplacePrefixMatch` and `ReplaceFullPath`).

## Limitations

- **Matching across routes**: GKO does not support matching rules that span multiple HTTPRoute resources targeting the same Gateway listener. Each HTTPRoute is reconciled independently into its own v4 API definition.
- **Backend types**: Only Kubernetes `Service` backends are supported. Resource backends are not supported.
- **Single Gateway reference**: Each HTTPRoute references a single Gateway via `parentRefs`.

## What's next

* [Kubernetes Gateway API overview](README.md) — Set up GatewayClass, GatewayClassParameters, and Gateway resources.
* [GatewayClassParameters](../../overview/custom-resource-definitions/gatewayclassparameters.md) — Configure autoscaling, pod disruption budgets, and deployment strategies.
* [KafkaRoute](../../overview/custom-resource-definitions/kafkaroute.md) — Route Kafka traffic through the Gateway (experimental).
