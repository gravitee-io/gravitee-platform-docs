# Gravitee as an Ingress Controller

## Overview

This page details the steps to deploy the Gravitee Gateway as an ingress runtime and the Gravitee Kubernetes Operator (GKO) as an ingress controller:

{% hint style="info" %}
**Limitations**

The `graviteeio` ingress class does not currently support the following features defined in the Kubernetes Ingress specification:

* [Resource Backends](https://kubernetes.io/docs/concepts/services-networking/ingress/#resource-backend)
* [Hostname Wildcards](https://kubernetes.io/docs/concepts/services-networking/ingress/#hostname-wildcards)
{% endhint %}

## Deployment

The Gravitee Gateway will be deployed in the `gravitee-ingress` namespace and available at the `graviteeio.example.com` domain name.

A Gravitee backend service routed and made available through a Gravitee ingress will be deployed in the `gravitee-apis` namespace.

The APIM components used to gather analytics and review our configuration will be deployed in the `gravitee-apim` namespace.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/kubernetes/gko-architecture-4-ingress.png" alt=""><figcaption><p>Sample Kubernetes cluster</p></figcaption></figure>

### Prerequisites

* A basic knowledge of [helm](https://helm.sh/docs/) and [kubectl](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands) command-line tools.
* It is assumed that [`external-dns`](https://github.com/kubernetes-sigs/external-dns) has been configured to handle domain name resolution on your cluster.

### Configure your deployment

Next, use the [Gravitee Helm Chart](docs/apim/4.0/getting-started/install-and-upgrade-guides/install-on-kubernetes/apim-helm-install-and-configuration.md) to install the Gateway that will act as an Ingress runtime on your Kubernetes cluster. Below is the minimum set of properties that your Helm values should contain:

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

{% hint style="info" %}
For the Gravitee Gateway to handle inbound traffic, `ingress` must be disabled to prevent NGINX from acting as an ingress runtime.
{% endhint %}

The `external-dns.alpha.kubernetes.io/hostname` instructs `external-dns` to use your external DNS provider to create a DNS entry that matches the load balancer service IP.

### Deploy your Gateway

We can now install the Gravitee Gateway using the following command:

```sh
helm upgrade --install gravitee-ingress \
  -n gravitee-ingress \
  -f values.yml \
  graviteeio/apim
```

### Deploy the Gravitee Kubernetes Operator

The Gravitee Kubernetes Operator that will act as our Ingress controller can also be installed using the Gravitee Helm Chart. You can find the operator Helm Chart documentation [here](docs/apim/4.0/getting-started/install-and-upgrade-guides/install-on-kubernetes/architecture-overview.md).

```sh
helm upgrade --install gravitee-gko \
  -n gravitee-ingress \
  graviteeio/gko
```

### Add a test backend

To be able to test our installation, we will deploy [`go-httpbin`](https://github.com/mccutchen/go-httpbin) as a backend service routed through our ingress resource. The following snippet defines the minimum resources required to initialize the backend service:

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

Once the `httpbin` service is created, it can be used as a reference in one or more ingress resources.

The example below specifies the rules for routing traffic to your backend service. The GKO's ingress controller interprets this ingress resource and publishes a new API on the Gravitee Gateway. The Gateway acts as a runtime ingress, handling traffic and forwarding it to your backend service.

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

Apply the ingress on your cluster using the following command:

```sh
kubectl apply -f httpbin-ingress.yaml
```

### Test your installation

The above settings establish a secure way for you to call the Gateway and your ingress. You can now test your installation by sending a request to your ingress resource:

```sh
curl -i https://graviteeio.example.com/httpbin/hostname
```

### Secure your Gateway and ingress resources <a href="#user-content-secure-your-gateway-and-ingress-resources" id="user-content-secure-your-gateway-and-ingress-resources"></a>

To secure the connection between your client and the Gateway, you must modify the Gateway `ConfigMap`.

As a prerequisite, a keystore must be added to the cluster. You can create a keystore using the following command:

```sh
keytool -genkeypair -alias example.com -storepass changeme -keypass changeme \
-keystore gw-keystore.jks -dname "CN=example.com"
```

{% hint style="info" %}
Currently, Gravitee only supports the JKS keystore.
{% endhint %}

Next, add your keystore to your target namespace. This example uses the default namespace:

```sh
kubectl create secret generic gw-keystore \
--from-file=keystore=gw-keystore.jks
```

After the keystore is added to the cluster, you need to configure the Gateway to use it and enable HTTPS. Open the `ConfigMap` that includes the Gateway configuration and add the following to the `HTTP` or the `listeners.https` section of the `gravitee.yaml` file:

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

{% hint style="info" %}
You must also add this label to your Gateway `ConfigMap` to tell the controller where your Gateway configuration is located.
{% endhint %}

Restart the Gateway for the changes to take effect.

#### Modify keystore

There are two ways that the GKO can modify your keystore:

1\) Add the following label to your exiting Gateway `ConfigMap`:

```
gravitee.io/component=gateway
```

2\) Create a new Secret and provide the name of the Gateway keystore and its password:

```sh
kubectl create secret generic gw-keystore-config \
-n default \
--from-literal=name=gw-keystore \
--from-literal=password=changeme
```

You also need to label the Secret:

```
gravitee.io/gw-keystore-config=true
```

#### Add TLS to the ingress resources <a href="#user-content-add-tls-to-the-ingress-resources" id="user-content-add-tls-to-the-ingress-resources"></a>

Assuming you have a [keypair for your host and added it to the cluster](https://kubernetes.io/docs/concepts/configuration/secret/#tls-secrets), you can reference the Secret inside your ingress file, as shown below:

{% hint style="info" %}
The Secret must be in the same namespace.
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

The settings above provide a secure means for you to call the Gateway and your ingress:

```sh
curl -v https://foo.com/httpbin
```

Alternatively, run the following command for a self-signed certificate:

```sh
curl --insecure -v https://foo.com/httpbin
```

## Extending an ingress using an API definition template

Policies allow you to apply custom behaviors on requests issued to a backend service. This can be achieved using an API definition labeled as a template.

The examples below will build on the previous example in the deployment section, which uses the `httpbin` service.

### API definition template

A template is an API definition with the `gravitee.io/template` label set to `true`.

This example below creates a template that defines a [`cache` policy](docs/apim/4.0/reference/policy-reference/cache.md):

{% code title="ingress-cache-template.yaml" %}
```yaml
apiVersion: "gravitee.io/v1alpha1"
kind: "ApiDefinition"
metadata:
  name: "ingress-cache-template"
  annotations:
    gravitee.io/template: "true"
spec:
  name: "ingress-cache-template"
  version: "1"
  description: "This template can be used to implement caching on your ingresses"
  visibility: "PRIVATE"
  resources:
    - name: "simple-cache"
      type: "cache"
      enabled: true
      configuration:
        timeToIdleSeconds: 0
        timeToLiveSeconds: 600
        maxEntriesLocalHeap: 1000
  flows:
  - name: ""
    path-operator:
      path: "/"
      operator: "STARTS_WITH"
    condition: ""
    consumers: []
    methods: []
    pre:
    - name: "Cache"
      description: ""
      enabled: true
      policy: "cache"
      configuration:
        timeToLiveSeconds: 600
        cacheName: "simple-cache"
        methods:
        - "GET"
        - "OPTIONS"
        - "HEAD"
        scope: "APPLICATION"
    post: []
    enabled: true
  gravitee: "2.0.0"
  flow_mode: "DEFAULT"
```
{% endcode %}

You can apply this template with the following command:

```sh
kubectl apply -f ingress-cache-template.yml
```

### Reference the template

To apply the template policies to requests issued to the `httpbin` ingress, you must add the required label.

This is done by annotating the ingress, using the `gravitee.io/template` as the key and the API definition template name as the value.

{% hint style="info" %}
The template must exist in the same Kubernetes namespace as the ingress.
{% endhint %}

{% code title="httpbin-ingress.yaml" %}
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: httpbin-ingress
  annotations:
    kubernetes.io/ingress.class: graviteeio
    gravitee.io/template: ingress-cache-template
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

You can apply this change with the following command:

```sh
kubectl apply -f httpbin-ingress.yaml
```

### Testing your ingress

To test that the `cache` policy is enforced on the `httpbin` ingress, request the `/headers` endpoint of `httpbin` and pass a timestamp as a header:

```sh
curl `https://graviteeio.example.com/httpbin/headers -H  "X-Date: $(date)"`
```

Then send the same request again:

```sh
curl `https://graviteeio.example.com/httpbin/headers -H  "X-Date: $(date)"`
```

This will return the same value for the `X-Date` header until the 10-minute window of the `cache` policy has elapsed.
