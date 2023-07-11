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

### Secure your Gateway and Ingress Resources <a href="#user-content-secure-your-gateway-and-ingress-resources" id="user-content-secure-your-gateway-and-ingress-resources"></a>

To secure the connection between your client and the gateway, you need to modify the Gateway `ConfigMap`. But first, you need to add a keystore to the cluster. You can create a keystore using the following command:

{% hint style="info" %}
Please be aware that Gravitee only supports the JKS keystore at the moment.
{% endhint %}

```sh
keytool -genkeypair -alias example.com -storepass changeme -keypass changeme \
-keystore gw-keystore.jks -dname "CN=example.com"
```

Once you have your keystore, you must add it to your target namespace. This example uses the default namespace.

```sh
kubectl create secret generic gw-keystore \
--from-file=keystore=gw-keystore.jks
```

Once you added the keystore to the cluster, you must configure the Gateway to use this keystore and enable HTTPS. Open the `ConfigMap` that includes the Gateway configuration and add the following configuration to the `HTTP` or the `listeners.https` section of the `gravitee.yaml` file:

{% hint style="info" %}
You must also add this label to your Gateway `ConfigMap`to tell the controller where your Gateway configuration is located.
{% endhint %}

```yaml
 http:
   secured: true # Turns on the https
   ssl:
     keystore:
       type: jks
       kubernetes: /default/secrets/gw-keystore/keystore
       password: changeme
     sni: true
```

Next, restart the Gateway for the changes to take effect.

#### Modify keystore

There are two ways that the GKO can modify your keystore:

1\) Either add the following label to your exiting Gateway `ConfigMap`

```
gravitee.io/component=gateway
```

2\) Create a new secret and provide the name of the Gateway keystore and its password

```sh
kubectl create secret generic gw-keystore-config \
-n default \
--from-literal=name=gw-keystore \
--from-literal=password=changeme
```

You also need to label this new secret:

```
gravitee.io/gw-keystore-config=true
```

#### Add TLS to the ingress resources <a href="#user-content-add-tls-to-the-ingress-resources" id="user-content-add-tls-to-the-ingress-resources"></a>

Assuming you have a [keypair for your host and added it to the cluster](https://kubernetes.io/docs/concepts/configuration/secret/#tls-secrets), you can reference the secret inside your ingress file.&#x20;

{% hint style="info" %}
The secret must be in the same namespace.
{% endhint %}

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: tls-example
  annotations:
    kubernetes.io/ingress.class: graviteeio
spec:
  tls:
  - hosts:
      - foo.com
    secretName: foo.com
  rules:
  - host: foo.com
    http:
      paths:
      - path: /httpbin
        pathType: Prefix
        backend:
          service:
            name: svc-1
            port:
              number: 8080
```

With these settings, you are able to call the Gateway and your ingress in a secure fashion.

```sh
curl -v https://foo.com/httpbin
```

Or, if it is a self-signed certificate:

```sh
curl --insecure -v https://foo.com/httpbin
```
