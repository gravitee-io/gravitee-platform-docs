---
noIndex: true
---

# Ambassador Edge Stack Architecture

## Ambassador Edge Stack is a control plane

Ambassador Edge Stack is a specialized [control plane for Envoy Proxy](https://www.getambassador.io/blog/envoy-nginx-haproxy-comparison-why-edge-stack-chose-envoy). In this architecture, Ambassador Edge Stack translates configuration (in the form of Kubernetes Custom Resources) to Envoy configuration. All actual traffic is directly handled by the high-performance [Envoy Proxy](https://www.envoyproxy.io).

<figure><img src="../.gitbook/assets/00 aes 4.png" alt=""><figcaption></figcaption></figure>

## Details

1. The service owner defines configuration in Kubernetes manifests.
2. When the manifest is applied to the cluster, the Kubernetes API notifies Ambassador Edge Stack of the change.
3. Ambassador Edge Stack parses the change and transforms the configuration into a semantic intermediate representation. Envoy configuration is generated from this IR.
4. The new configuration is passed to Envoy via the gRPC-based Aggregated Discovery Service (ADS) API.
5. Traffic flows through the reconfigured Envoy, without dropping any connections.

## Scaling and availability

Ambassador Edge Stack relies on Kubernetes for scaling, high availability, and persistence. All Ambassador Edge Stack configuration is stored directly in Kubernetes; there is no database. Ambassador Edge Stack is packaged as a single container that contains both the control plane and an Envoy Proxy instance. By default, Ambassador Edge Stack is deployed as a Kubernetes `deployment` and can be scaled and managed like any other Kubernetes deployment.

### Stateless architecture

By design, Ambassador Edge Stack is an entirely stateless architecture. Each individual Ambassador Edge Stack instance operates independently of other instances. These Ambassador Edge Stack instances rely on Kubernetes to coordinate the configuration between the different Ambassador Edge Stack instances. This enables Ambassador Edge Stack to sidestep the need to engineer a safe, highly available centralized control plane (and if you don't think that this is hard, check out [Jepsen](https://jepsen.io)). By contrast, other control plane architectures rely on a single centralized control plane to manage multiple instances of the data plane. This means that these control plane architectures must engineer resilience and availability into their central control plane.

## Envoy Proxy

Ambassador Edge Stack closely tracks Envoy Proxy releases. A stable branch of Envoy Proxy is maintained that enables the team to cherry-pick specific fixes into Ambassador Edge Stack.
