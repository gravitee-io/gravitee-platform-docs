---
description: Overview of Why Ambassador Edge Stack.
hidden: true
noIndex: true
---

# Why Ambassador Edge Stack?

Ambassador Edge Stack gives platform engineers a comprehensive, self-service edge stack for managing the boundary between end-users and Kubernetes. Built on the [Envoy Proxy](https://www.envoyproxy.io) and fully Kubernetes-native, Ambassador Edge Stack is made to support multiple, independent teams that need to rapidly publish, monitor, and update services for end-users. A true edge stack, Ambassador Edge Stack can also be used to handle the functions of an API Gateway, a Kubernetes ingress controller, and a layer 7 load balancer (for more, see [this page](https://www.getambassador.io/products/edge-stack/api-gateway)).

## How Does Ambassador Edge Stack work?

Ambassador Edge Stack is a Kubernetes-native [microservices API gateway](core-concepts/microservices-api-gateways.md) built on the open core of Emissary-ingress and the [Envoy Proxy](https://www.envoyproxy.io). Ambassador Edge Stack is built from the ground up to support multiple, independent teams that need to rapidly publish, monitor, and update services for end-users. Ambassador Edge Stack can also be used to handle the functions of a Kubernetes ingress controller and load balancer (for more, see [this page](https://www.getambassador.io/products/edge-stack/api-gateway)).

## Cloud-native applications today

Traditional cloud applications were built using a monolithic approach. These applications were designed, coded, and deployed as a single unit. Today's cloud-native applications, by contrast, consist of many individual (micro)services. This results in an architecture that is:

* **Heterogeneous**: Services are implemented using multiple (polyglot) languages, they are designed using multiple architecture styles, and they communicate with each other over multiple protocols.
* **Dynamic**: Services are frequently updated and released (often without coordination), which results in a constantly-changing application.
* **Decentralized**: Services are managed by independent product-focused teams, with different development workflows and release cadences.

### Heterogeneous services

Ambassador Edge Stack is commonly used to route traffic to a wide variety of services. It supports:

* configuration on a _per-service_ basis, enabling fine-grained control of timeouts, rate limiting, authentication policies, and more.
* a wide range of L7 protocols natively, including HTTP, HTTP/2, gRPC, gRPC-Web, and WebSockets.
* Can route raw TCP for services that use protocols not directly supported by Ambassador Edge Stack.

### Dynamic services

Service updates result in a constantly changing application. The dynamic nature of cloud-native applications introduces new challenges around configuration updates, release, and testing. Ambassador Edge Stack:

* Enables [progressive delivery](core-concepts/progressive-delivery.md), with support for canary routing and traffic shadowing.
* Exposes high-resolution observability metrics, providing insight into service behavior.
* Uses a zero downtime configuration architecture, so configuration changes have no end-user impact.

### Decentralized workflows

Independent teams can create their own workflows for developing and releasing functionality that are optimized for their specific service(s). With Ambassador Edge Stack, teams can:

* Leverage a [declarative configuration model](core-concepts/the-ambassador-operating-model-gitops-and-continuous-delivery.md), making it easy to understand the canonical configuration and implement GitOps-style best practices.
* Independently configure different aspects of Ambassador Edge Stack, eliminating the need to request configuration changes through a centralized operations team.

## Ambassador Edge Stack is engineered for Kubernetes

Ambassador Edge Stack takes full advantage of Kubernetes and Envoy Proxy.

* All of the state required for Ambassador Edge Stack is stored directly in Kubernetes, eliminating the need for an additional database.
* The Ambassador Edge Stack team has added extensive engineering efforts and integration testing to ensure optimal performance and scale of Envoy and Kubernetes.

## For more information

[Deploy Ambassador Edge Stack today](README.md) and join the community [Slack Channel](http://a8r.io/slack).

Interested in learning more?

* [Ambassador Edge Stack Architecture overview](core-concepts/ambassador-edge-stack-architecture.md)
