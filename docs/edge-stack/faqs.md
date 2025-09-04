---
noIndex: true
---

# FAQs

## Frequently Asked Questions

### Why Ambassador Edge Stack?

Kubernetes shifts application architecture for microservices, as well as the development workflow for a full-cycle development. Ambassador Edge Stack is designed for the Kubernetes world with:

* Sophisticated traffic management capabilities (thanks to its use of [Envoy Proxy](https://www.envoyproxy.io)), such as load balancing, circuit breakers, rate limits, and automatic retries.
* API management capabilities such as a developer portal and OpenID Connect integration for Single Sign-On.
* A declarative, self-service management model built on Kubernetes Custom Resource Definitions, enabling GitOps-style continuous delivery workflows.

We've written about [the history of Ambassador Edge Stack](https://www.getambassador.io/blog/envoy-nginx-haproxy-comparison-why-edge-stack-chose-envoy), [Why Ambassador Edge Stack In Depth](why-ambassador-edge-stack.md), [Features and Benefits](features-and-benefits.md) and about the [evolution of API Gateways](core-concepts/microservices-api-gateways.md).

### What's the difference between Emissary-ingress and Ambassador Edge Stack?

Emissary-ingress is a CNCF Incubating project and provides the open-source core of Ambassador Edge Stack. Originally we called Emissary-ingress the "Ambassador API Gateway", but as the project evolved, we realized that the functionality we were building had extended far beyond an API Gateway. In particular, the Ambassador Edge Stack is intended to provide all the functionality you need at the edge -- hence, an "edge stack." This includes an API Gateway, ingress controller, load balancer, developer portal, and more.

### How is Ambassador Edge Stack licensed?

The core Emissary-ingress is open source under the Apache Software License 2.0. The GitHub repository for the core is [https://github.com/emissary-ingress/emissary](https://github.com/emissary-ingress/emissary). Some additional features of the Ambassador Edge Stack (e.g., Single Sign-On) are not open source and available under a proprietary license.

### Can I use the add-on features for Ambassador Edge Stack for free?

Yes! For more details please see the [Ambassador Edge Stack Licenses](ambassador-edge-stack-licenses.md) page.

### How does Ambassador Edge Stack use Envoy Proxy?

Ambassador Edge Stack uses [Envoy Proxy](https://www.envoyproxy.io) as its core proxy. Envoy is an open-source, high-performance proxy originally written by Lyft. Envoy is now part of the Cloud Native Computing Foundation.

### Is Ambassador Edge Stack production ready?

Yes. Thousands of organizations, large and small, run Ambassador Edge Stack in production. Public users include Chick-Fil-A, ADP, Microsoft, NVidia, and AppDirect, among others.

### What is the performance of Ambassador Edge Stack?

There are many dimensions to performance. We published a benchmark of [Ambassador Edge Stack performance on Kubernetes](https://www.getambassador.io/resources/envoyproxy-performance-on-k8s). Our internal performance regressions cover many other scenarios; we expect to publish more data in the future.

### What's the difference between a service mesh (such as Istio) and Ambassador Edge Stack?

Service meshes focus on routing internal traffic from service to service ("east-west"). Ambassador Edge Stack focuses on traffic into your cluster ("north-south"). While both a service mesh and Ambassador Edge Stack can route L7 traffic, the reality is that these use cases are quite different. Many users will integrate Ambassador Edge Stack with a service mesh. Production customers of Ambassador Edge Stack have integrated with Consul, Istio, and Linkerd2.

## Common Configurations

### How do I disable the 404 landing page?

See the [Controlling the Ambassador Edge Stack 404 Page](controlling-the-edge-stack-404-page.md) how-to.

### How do I disable the default Admin mappings?

See the [Protecting the Diagnostics Interface](protecting-access-to-the-diagnostics-interface.md) how-to.

## Troubleshooting

### How do I get help for Ambassador Edge Stack?

We have an online [Slack community](http://a8r.io/slack) with thousands of users. We try to help out as often as possible, although we can't promise a particular response time. If you need a guaranteed SLA, we also have commercial contracts. [Contact sales](https://www.getambassador.io/contact-us) for more information.

### What do I do when I get the error `no healthy upstream`?

This error means that Ambassador Edge Stack could not connect to your backend service. Start by verifying that your backend service is actually available and responding by sending an HTTP response directly to the pod. Then, verify that Ambassador Edge Stack is routing by deploying a test service and seeing if the mapping works. Then, verify that your load balancer is properly routing requests to Ambassador Edge Stack. In general, verifying each network hop between your client and backend service is critical to finding the source of the problem.

### What is the difference between the v3alpha1 and v1alpha1 CRDs?

There are two different CRD versions supported by Ambassador Edge Stack. The first are the `getambassador.io/v3alpha1` CRDs which were introduced with Ambassador Edge Stack 2.x. These are still supported and are not deprecated. As of Ambassador Edge Stack 3.12.6, the new `gateway.getambassador.io/v1alpha1` CRDs have also been introduced. The `v1alpha1` CRDs have not only a new version, but also a new apigoup so that way they can be installed alongside the older CRDs without causing any conflicts.

The `v1alpha1` CRDs are only available for the `Filter`, `FilterPolicy`, `WebApplicationFirewall`, and `WebApplicationFirewallPolicy` resources, and are the next generation of the CRDs that Ambassador Edge Stack will support. We are introducing them now to allow users to try them out without needing to stop using the `v3alpha1` CRDs. You can use `v1alpha1` and `v3alpha1` CRDs in the same cluster at the same time, but `FilterPolicies` are not able to reference `Filters` that do not match their CRD version.
