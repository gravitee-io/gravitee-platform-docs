---
description: Installation guide for Ambassador Edge Stack.
noIndex: true
---

# HTTP/3 Setup in Ambassador Edge Stack

HTTP/3 is the third version of the Hypertext Transfer Protocol (HTTP). It is built on the [QUIC](https://www.chromium.org/quic/) network protocol rather than Transmission Control Protocol (TCP) like previous versions.

## The changes and challenges of HTTP/3

Since the QUIC network protocol is built on UDP, most clients will require Ambassador Edge Stack to advertise its support for HTTP/3 using the `alt-svc` response header. This header is added to the response of the HTTP/2 and HTTP/1.1 connections. When the client sees the `alt-svc` it can choose to upgrade to HTTP/3 and connect to Ambassador Edge Stack using the QUIC protocol.

QUIC requires Transport Layer Security (TLS) version 1.3 to communicate. Otherwise, Ambassador Edge Stack will fall back to HTTP/2 or HTTP/1.1, both of which support other TLS versions if client does not support TLS v1.3. Due to this restriction, some clients also require valid certificatesand will not upgrade to HTTP/3 traffic with self-signed certificates.

Because HTTP/3 adoption is still growing and and changing, the Ambassador Edge Stack team will continue update this documentation as features change and mature.

## Setting up HTTP/3 with Ambassador Edge Stack

To configure Ambassador Edge Stack for HTTP/3 you need to do the following:

1. Configure `Listener` resources.
2. Configure a `Host`.
3. Have a valid certificate.
4. Setup an external load balancer.

### Configuring the Listener resources

To make Ambassador Edge Stack listen for HTTP/3 connections over the QUIC network protocol, you need to configure a `Listener` with `TLS`, `HTTP`, and `UDP` configured within `protocolStack`.

{% hint style="info" %}
The `protocolStack` elements need to be entered in the specific order of `TLS, HTTP, UDP.`
{% endhint %}

The `Listener` configured for HTTP/3 can be bound to the same address and port (`0.0.0.0:8443`) as the `Listener` that supports HTTP/2 and HTTP/1.1. This is not required, but it allows Ambassador Edge Stack to inject the default `alt-svc: h3=":443"; ma=86400, h3-29=":443"; ma=86400` header into the responses returned over the TCP connection with no additional configuration needed. **Most clients such as browsers require the `alt-svc` header to upgrade to HTTP/3**.

{% hint style="info" %}
The current default of `alt-svc: h3=":443"; ma=86400, h3-29=":443"; ma=86400` means that the external load balancer must be configured to accept traffic on port `:443` for the client to upgrade the request.
{% endhint %}

```yaml
# This is a standard Listener that leverages TCP to serve HTTP/2 and HTTP/1.1 traffic.
# It is bound to the same address and port (0.0.0.0:8443) as the UDP listener.
apiVersion: getambassador.io/v3alpha1
kind: Listener
metadata:
  name: edge-stack-https-listener
  namespace: ambassador
spec:
  port: 8443
  protocol: HTTPS
  securityModel: XFP
  hostBinding:
    namespace:
      from: ALL
---
# This is a Listener that leverages UDP and HTTP to serve HTTP/3 traffic.
# NOTE: Raw UDP traffic is not supported. UDP and HTTP must be used together.
apiVersion: getambassador.io/v3alpha1
kind: Listener
metadata:
  name: edge-stack-https-listener-udp
  namespace: ambassador
spec:
  port: 8443
  # Order is important here. HTTP is required.
  protocolStack:
    - TLS
    - HTTP
    - UDP
  securityModel: XFP
  hostBinding:
    namespace:
      from: ALL
```

### Configuring the Host resource

Because the QUIC network requires TLS, the certificate needs to be valid so the client can upgrade a connection to HTTP/3. See[the-host-resource.md](../../technical-reference/using-custom-resources/the-host-resource.md "mention") for more information on how to configure TLS for a `Host`.

### Certificate verification

Clients can only upgrade to an HTTP/3 connection with a valid certificate. If the client won’t upgrade to HTTP/3, verify that you have a valid TLS certificate and that your client can speak **TLS v1.3**. Your `Host` resource should be configured similar to the following:

```yaml
apiVersion: getambassador.io/v3alpha1
kind: Host
metadata:
  name: my-domain-host
spec:
  hostname: your-hostname
  # acme isn't required but just shown as an example of how to manage a valid TLS cert
  acmeProvider:
    email: your-email@example.com
    authority: https://acme-v02.api.letsencrypt.org/directory
  tls:
    # QUIC requires TLS v1.3 version. Verify your client supports it.
    min_tls_version: v1.3
    # Either protocol can be upgraded, but http/2 is recommended.
    alpn_protocols: h2,http/1.1
```

### External load balancers

The two most common service types to expose traffic outside of a Kubernetes cluster are:

* `LoadBalancer`: A load balancer controller generates and manages the cloud provider-specific external load balancer.
* `NodePort`: The platform administrator has to manually set up things like the external load balancer, firewall rules, and health checks.

#### LoadBalancer setup

The ideal setup would be to configure a single service of type `LoadBalancer`, but this comes with some current restrictions:

* You need version 1.24 or later of Kubernetes with the [`MixedProtocolLBService` feature enabled](https://kubernetes.io/docs/concepts/services-networking/service/#load-balancers-with-mixed-protocol-types).
* Your cloud service provider needs to support the creation of an external load balancer with mixed protocol types (TCP/UDP), port reuse, and port forwarding. Support for Kubernetes feature flags may vary between cloud service providers. Refer to your provider’s documentation to see if they support this scenario.

An example `LoadBalancer` configuration that fits the criteria listed above:

```yaml

# note: extra fields such as labels and selectors removed for clarity
apiVersion: v1
kind: Service
metadata:
  name: edge-stack
  namespace: ambassador
spec:
  ports:
    - name: http
      port: 80
      targetPort: 8080
      protocol: TCP
    - name: https
      port: 443
      targetPort: 8443
      protocol: TCP
    - name: http3
      port: 443
      targetPort: 8443
      protocol: UDP
  type: LoadBalancer
```

## Cloud service provider setup

Once you've completed the steps above, you need to configure HTTP/3 support through your cloud service provider. The configuration processes for each provider can be found here:

* HTTP/3 setup for Amazon Elastic Kubernetes Service (EKS): [http-3-with-eks.md](http-3-with-eks.md "mention")
* HTTP/3 setup for Azure Kubernetes Service (AKS): [http-3-with-aks.md](http-3-with-aks.md "mention")
* HTTP/3 setup for Google Kubernetes Engine (GKE): [http-3-with-gke.md](http-3-with-gke.md "mention")
