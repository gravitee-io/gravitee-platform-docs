# Gravitee as an Ingress Controller

## Overview

In this section, we will walk you through the steps needed to deploy the Gravitee gateway as an ingress runtime along with the Gravitee Kubernetes Operator acting as an Ingress controller.

### Limitations

When using the `graviteeio` ingress class, some features defined in the Kubernetes Ingress specification are not supported at this time. Here is the list of unsupported features:

* [Resource Backends](https://kubernetes.io/docs/concepts/services-networking/ingress/#resource-backend)
* [Hostname Wildcards](https://kubernetes.io/docs/concepts/services-networking/ingress/#hostname-wildcards)

## Deployment

The Gravitee gateway will be deployed in the `gravitee-ingress` namespace and will be available at the `graviteeio.example.com` domain name.

Our backend service(s) routed and made available through our ingress(es) will be deployed in the `gravitee-apis` namespace.

Finally, the APIM components used to gather analytics or review our configuration will be deployed in the `gravitee-apim` namespace.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/kubernetes/gko-architecture-4-ingress.png" alt=""><figcaption><p>Sample Kubernetes cluster</p></figcaption></figure>

### Prerequisites

A basic knowledge of [helm](https://helm.sh/docs/) and [kubectl](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands) command line tools is required to follow the steps described in the next sections.

For the sake of brevity, we will assume that [`external-dns`](https://github.com/kubernetes-sigs/external-dns) has been configured to handle domain name resolution on your cluster.

### Configure your deployment

In the next step, we will install the Gateway that will act as our Ingress runtime using the [Gravitee Helm charts.](../../getting-started/install-guides/install-on-kubernetes/configure-helm-chart.md)

Here is the minimum set of properties that your Helm values should contain to make the Gateway act as an Ingress runtime on your Kubernetes cluster.

{% code title="values.yml" %}
```yaml
gateway:
  services:
    sync:
      kubernetes:
        enabled: true
  ingress:
    enabled: false
  service:
    type: LoadBalancer
    annotations:
      external-dns.alpha.kubernetes.io/hostname: graviteeio.example.com
    externalPort: 443
```
{% endcode %}

In the values, you can see that the ingress is disabled. We do not want NGINX to act as an Ingress runtime as the gateway will be handling inbound traffic.

The `external-dns.alpha.kubernetes.io/hostname` instructs `external-dns` to create a DNS entry matching the load balancer service IP using your external DNS provider.

### Deploy your gateway

We can now install the gateway using the following command:

```sh
helm upgrade --install gravitee-ingress \
  -n gravitee-ingress \
  -f values.yml \
  graviteeio/apim3
```

### Deploy the Gravitee Kubernetes Operator

Just like we did for the Gateway, we can install the Gravitee Kubernetes Operator that will act as our Ingress controller using the gravitee.io helm charts. You can find the operator helm chart documentation [here](../../getting-started/install-guides/install-on-kubernetes/install-gravitee-kubernetes-operator.md).

```sh
helm upgrade --install gravitee-gko \
  -n gravitee-ingress \
  graviteeio/gko
```

### Add a test backend

To be able to test our installation, we will deploy [`go-httpbin`](https://github.com/mccutchen/go-httpbin) as a backend service routed through our ingress resource. The following snippet defines the minimum resources required to get our backend service up and running.

{% code title="httpbin.yaml" %}
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: httpbin
  labels:
    type: httpbin
spec:
  replicas: 1
  selector:
    matchLabels:
      type: httpbin
  template:
    metadata:
      labels:
        type: httpbin
    spec:
      containers:
        - name: httpbin
          image: mccutchen/go-httpbin
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8080
          env:
            - name: USE_REAL_HOSTNAME
              value: "true"
---
apiVersion: v1
kind: Service
metadata:
  name: httpbin
  labels:
    type: httpbin
spec:
  ports:
    - port: 8080
      targetPort: 8080
  selector:
    type: httpbin
```
{% endcode %}

Apply the resources on your cluster using the following command:

```sh
kubectl apply -f httpbin.yaml
```

### Define your ingress

Once the `httpbin` service created, it can be used as a reference in one or more ingress resources. The example below specifies the rules for routing traffic to your backend service. The Gravitee Kubernetes Operator’s ingress controller will then interpret this ingress resource and publish a new API on the Gravitee Gateway. The Gateway will act as a runtime ingress, handling traffic and forwarding it to your backend service.

{% code title="httpbin-ingress.yaml" %}
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: httpbin-ingress
  annotations:
    kubernetes.io/ingress.class: graviteeio
spec:
  rules:
    - http:
        paths:
          - path: /httpbin
            pathType: Prefix
            backend:
              service:
                name: httpbin
                port:
                  number: 8000
```
{% endcode %}

Apply the Ingress on your cluster using the following command:

```sh
kubectl apply -f httpbin-ingress.yaml
```

### Test your installation

You can now test your installation by sending a request to your ingress resource. Having these settings, you should be able to call the gateway and your ingress in a secured way.

```sh
curl -i https://graviteeio.example.com/httpbin/hostname
```
