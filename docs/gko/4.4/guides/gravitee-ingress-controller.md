# Gravitee Ingress Controller

## Overview

This page describes how to deploy, test, and secure the Gravitee Gateway as an ingress runtime and the Gravitee Kubernetes Operator (GKO) as an ingress controller, then how to extend an ingress using an API definition template.

* [Deploy the ingress runtime and controller](gravitee-ingress-controller.md#deploy-the-ingress-runtime-and-controller)
* [Extend an ingress using an API definition template](gravitee-ingress-controller.md#extending-an-ingress-using-an-api-definition-template)

{% hint style="info" %}
**Limitations**

The `graviteeio` ingress class does not currently support the following features defined in the Kubernetes Ingress specification:

* [Resource Backends](https://kubernetes.io/docs/concepts/services-networking/ingress/#resource-backend)
* [Hostname Wildcards](https://kubernetes.io/docs/concepts/services-networking/ingress/#hostname-wildcards)
{% endhint %}

## Deploy the ingress runtime and controller

* The Gravitee Gateway will be deployed in the `gravitee-ingress` namespace and available at the `graviteeio.example.com` domain name.
* A Gravitee backend service routed and made available through a Gravitee ingress will be deployed in the `gravitee-apis` namespace.
* The APIM components used to gather analytics and review our configuration will be deployed in the `gravitee-apim` namespace.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/kubernetes/gko-architecture-4-ingress.png" alt=""><figcaption><p>Sample Kubernetes cluster</p></figcaption></figure>

This section is divided into the following:

* [Prerequisites](gravitee-ingress-controller.md#prerequisites)
* [1. Configure your deployment](gravitee-ingress-controller.md#id-1.-configure-your-deployment)
* [2. Deploy your Gateway](gravitee-ingress-controller.md#id-2.-deploy-your-gateway)
* [3. Deploy the GKO](gravitee-ingress-controller.md#id-3.-deploy-the-gko)
* [4. Add a test backend](gravitee-ingress-controller.md#id-4.-add-a-test-backend)
* [5. Define your ingress](gravitee-ingress-controller.md#id-5.-define-your-ingress)
* [6. Test your installation](gravitee-ingress-controller.md#id-6.-test-your-installation)
* [7. Secure your Gateway and ingress resources](gravitee-ingress-controller.md#user-content-secure-your-gateway-and-ingress-resources)

### Prerequisites

* A basic knowledge of [helm](https://helm.sh/docs/) and [kubectl](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands) CLI tools
* [`external-dns`](https://github.com/kubernetes-sigs/external-dns) has been configured to handle domain name resolution on your cluster

### 1. Configure your deployment

Configure the Gravitee Helm Chart. Below is the minimum set of properties that your Helm values should contain:

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
For the Gateway to handle inbound traffic, `ingress` must be disabled to prevent NGINX from acting as an ingress runtime.
{% endhint %}

The `external-dns.alpha.kubernetes.io/hostname` instructs `external-dns` to use your external DNS provider to create a DNS entry that matches the load balancer service IP.

### 2. Deploy your Gateway

Use the Gravitee Helm Chart to install the Gateway that will act as an ingress runtime on your Kubernetes cluster:

```sh
helm upgrade --install gravitee-ingress \
  -n gravitee-ingress \
  -f values.yml \
  graviteeio/apim
```

### 3. Deploy the GKO

Use the Gravitee Helm Chart to install the Gravitee Kubernetes Operator that will act as your ingress controller:

```sh
helm upgrade --install gravitee-gko \
  -n gravitee-ingress \
  graviteeio/gko
```

{% hint style="info" %}
Refer to the [Helm Chart documentation](docs/gko/4.4/getting-started/installation/install-with-helm.md) for more information.
{% endhint %}

### 4. Add a test backend

To test the installation:

1.  Deploy [`go-httpbin`](https://github.com/mccutchen/go-httpbin) as a backend service routed through your ingress resource. The minimum resources required to initialize the backend service are defined below:

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
2.  Apply the resources on your cluster:

    ```sh
    kubectl apply -f httpbin.yaml
    ```

{% hint style="info" %}
Once the `httpbin` service is created, it can be used as a reference in one or more ingress resources.
{% endhint %}

### 5. Define your ingress

The example below specifies the rules for routing traffic to your backend service. The GKO's ingress controller interprets this ingress resource and publishes a new API on the Gravitee Gateway. The Gateway acts as a runtime ingress, handling traffic and forwarding it to your backend service.

1.  Configure `httpbin-ingress.yaml`:

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


2.  Apply the ingress on your cluster:

    ```sh
    kubectl apply -f httpbin-ingress.yaml
    ```

### 6. Test your installation

The above settings establish a secure way to call the Gateway and your ingress. You can test your installation by sending a request to your ingress resource:

```sh
curl -i https://graviteeio.example.com/httpbin/hostname
```

### 7. Secure your Gateway and ingress resources <a href="#user-content-secure-your-gateway-and-ingress-resources" id="user-content-secure-your-gateway-and-ingress-resources"></a>

To secure the connection between your client and the Gateway, you must modify the Gateway `ConfigMap`:

1.  As a prerequisite, create a keystore and add it to the cluster:

    ```sh
    keytool -genkeypair -alias example.com -storepass changeme -keypass changeme \
    -keystore gw-keystore.jks -dname "CN=example.com"
    ```



    {% hint style="info" %}
    Currently, Gravitee only supports the JKS keystore.
    {% endhint %}
2.  Add your keystore to your target namespace, e.g., the default namespace used below:

    ```sh
    kubectl create secret generic gw-keystore \
    --from-file=keystore=gw-keystore.jks
    ```
3.  To configure the Gateway to use the keystore and enable HTTPS, open the `ConfigMap` that includes the Gateway configuration and add the following to the `HTTP` or the `listeners.https` section of the `gravitee.yaml` file:

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
4. Restart the Gateway for the changes to take effect.

#### Modify keystore

There are two ways that the GKO can modify your keystore:

*   Add the following label to your exiting Gateway `ConfigMap`:

    ```bash
    gravitee.io/component=gateway
    ```
*   Create a new Secret and provide the name of the Gateway keystore and its password:

    ```sh
    kubectl create secret generic gw-keystore-config \
    -n default \
    --from-literal=name=gw-keystore \
    --from-literal=password=changeme
    ```

    Then label the Secret:

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

## Extend an ingress using an API definition template

Policies allow you to apply custom behaviors to requests issued to a backend service. This can be achieved using an API definition labeled as a template. The subsections below describe how to extend an ingress using an API definition template and the `httpbin` service:

1. [Create an API definition template](gravitee-ingress-controller.md#id-1.-create-an-api-definition-template)
2. [Reference the template](gravitee-ingress-controller.md#id-2.-reference-the-template)
3. [Test your ingress](gravitee-ingress-controller.md#id-3.-test-your-ingress)

### 1. Create an API definition template

A template is an API definition with the `gravitee.io/template` label set to `true`. To create a template that defines a `cache` policy:

1.  Configure the `ingress-cache-template.yaml` file:

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
2.  Apply this template:

    ```sh
    kubectl apply -f ingress-cache-template.yml
    ```

### 2. Reference the template

To apply the template policies to requests issued to the `httpbin` ingress:

1.  Add the required label by annotating the ingress, using the `gravitee.io/template` as the key and the API definition template name as the value:

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
2.  Apply this change:

    ```sh
    kubectl apply -f httpbin-ingress.yaml
    ```

### 3. Test your ingress

To test that the `cache` policy is enforced on the `httpbin` ingress:

1.  Request the `/headers` endpoint of `httpbin` and pass a timestamp as a header:

    ```sh
    curl `https://graviteeio.example.com/httpbin/headers -H  "X-Date: $(date)"`
    ```
2.  Resend this request to return the same value for the `X-Date` header until the 10-minute window of the `cache` policy has elapsed:

    ```sh
    curl `https://graviteeio.example.com/httpbin/headers -H  "X-Date: $(date)"`
    ```
