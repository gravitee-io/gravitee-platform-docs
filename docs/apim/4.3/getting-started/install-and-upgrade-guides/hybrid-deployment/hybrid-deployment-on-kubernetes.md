---
description: >-
  Tutorial on Installing a Gravitee Gateway with a Hybrid Deployment on
  Kubernetes.
---

# Installing a Gravitee Gateway with a Hybrid Deployment on Kubernetes

This section describes how to install an APIM hybrid deployment using Kubernetes Helm charts.

{% hint style="info" %}
We assume familiarity with Google Cloud Platform (GCP), Kubernetes (K8s), and Helm. We also recommend that you read the [Introduction to APIM hybrid deployment](README.md) first.
{% endhint %}

## Target architecture

In this example, we will demonstrate how to deploy APIM in two different GCP regions and two different K8s clusters:

* A **Management cluster** (pictured on the left of the diagram below) — running the management API, the two APIM UI components, and a bridge gateway
* A **Gateway cluster** (pictured on the right of the diagram below) — running APIM gateway

<figure><img src="https://docs.gravitee.io/images/apim/3.x/installation/hybrid/hybrid_deployment_k8s.png" alt=""><figcaption><p>Kubernetes hybrid deployment architecture diagram</p></figcaption></figure>

In this schema, we can see that:

* MongoDB is used for all the management data (API definitions, subscriptions, API keys, etc.)
* ElasticSearch is also deployed in the Management cluster
* Redis is used to manage rate limits and quota counters within the Gateway cluster

{% hint style="info" %}
Before you continue, keep in mind that the bridge Gateway (the red box in the left-hand region of the schema) is simply an APIM Gateway instance with additional capabilities. This is essential to understanding how we are deploying the bridge. For more information, see the introduction to [Hybrid Deployment](README.md).
{% endhint %}

## Deploying with Helm

You can find everything you need to deploy this hybrid architecture in [Gravitee's Helm charts](https://helm.gravitee.io/).

### Before you begin

Before you deploy APIM, ensure the two GCP clusters exist and that Helm is installed on both clusters:

<figure><img src="https://docs.gravitee.io/images/apim/3.x/installation/hybrid/hybrid_k8s_clusters.png" alt=""><figcaption><p>Sample K8 clusters</p></figcaption></figure>

{% hint style="warning" %}
The following examples use the names in the illustration above, but you can name your clusters whatever you like and replace the names with your own.
{% endhint %}

### Deploy the management cluster

1. The first step is to initialize the cluster with some prerequisites:

{% code overflow="wrap" %}
```sh
$ gcloud container clusters get-credentials hybrid-mgmt-eu --zone=europe-west1-b

// Create namespace
$ kubectl create namespace graviteeio

// Nginx ingress controller is required for Gravitee APIM chart
$ helm install --name nginx-ingress --namespace graviteeio stable/nginx-ingress --set rbac.create=true --set controller.publishService.enabled=true

// Add Gravitee Helm repository
$ helm repo add graviteeio https://helm.gravitee.io
```
{% endcode %}

2. Deploy the management APIM instance, which includes components Management Console, Developer Portal, Management API and the bridge Gateway (which will be used as a bridge between the two clusters):

```sh
$ helm install — name graviteeio-apim3 — namespace graviteeio \
 -f values-bridge-http-server.yaml \
 -f values-hybrid-management-eu.yaml \
 graviteeio/apim3
```

The `values-hybrid-management-eu.yaml` file looks like this:

{% code title="values-hybrid-management-eu.yaml" %}
```yaml
mongo:
    uri: mongodb+srv://xxxxxx:xxxxx@demo.xxxxx.gcp.mongodb.net/gio-apim-hybrid?retryWrites=true&w=majority

es:
    endpoints:
        - https://xxxxxxxxx-elasticsearch.services.elasticcloud.com/
    index: demo_hybrid_apim
    security:
        enabled: true
        username: xxxxxx
        password: xxxxxx

api:
    ingress:
        management:
            path: /management
            hosts:
                - demo-hybrid-apim-api.cloud.gravitee.io
            tls:
            -   hosts:
                    - demo-hybrid-apim-api.cloud.gravitee.io
                secretName: cloud-gravitee-cert
        portal:
            path: /portal
            hosts:
                - demo-hybrid-apim-api.cloud.gravitee.io
            tls:
            -   hosts:
                    - demo-hybrid-apim-api.cloud.gravitee.io
                secretName: cloud-gravitee-cert

gateway:
    ingress:
        enabled: false
    services:
        bridge:
            enabled: true
            username: xxxxxxxxx
            password: xxxxxxxxx
            service:
                externalPort: 92
                internalPort: 18092
            ingress:
                enabled: true
                path: /
                hosts:
                    - demo-hybrid-apim-bridge.cloud.gravitee.io
                annotations:
                    kubernetes.io/ingress.class: nginx
                    nginx.ingress.kubernetes.io/ssl-redirect: "false"
                    nginx.ingress.kubernetes.io/enable-rewrite-log: "true"
                    nginx.ingress.kubernetes.io/configuration-snippet: "etag on;\nproxy_pass_header ETag;\nproxy_set_header if-match \"\";\n"
                tls:
                -   secretName: cloud-gravitee-cert
                    hosts:
                        - demo-hybrid-apim-bridge.cloud.gravitee.io

ui:
    ingress:
        path: /
        hosts:
            - demo-hybrid-apim-console.cloud.gravitee.io
        annotations:
            nginx.ingress.kubernetes.io/rewrite-target: /
        tls:
        -   hosts:
                - demo-hybrid-apim-console.cloud.gravitee.io
            secretName: cloud-gravitee-cert

portal:
    ingress:
        path: /
        hosts:
            - demo-hybrid-apim-portal.cloud.gravitee.io
        tls:
        -   hosts:
                - demo-hybrid-apim-portal.cloud.gravitee.io
            secretName: cloud-gravitee-cert
```
{% endcode %}

From this file, we can see that:

* the Gateway is not exposed through the ingress controller (it is not accepting API calls for the bridge gateway)
* we have enabled the bridge service for the Gateway and declared a new ingress to expose it to remote clusters

<figure><img src="https://docs.gravitee.io/images/apim/3.x/installation/hybrid/hybrid_deployment_ingress.png" alt=""><figcaption><p>APIM management cluster</p></figcaption></figure>

### Deploy the Gateway cluster

1. Again, we need to initialize the cluster with some prerequisites:

{% code overflow="wrap" %}
```sh
$ gcloud container clusters get-credentials hybrid-gw-eu --zone=europe-west2-b

// Create namespace
$ kubectl create namespace graviteeio

// Nginx ingress controller is required for Gravitee APIM chart
$ helm install --name nginx-ingress --namespace graviteeio stable/nginx-ingress --set rbac.create=true --set controller.publishService.enabled=true

// Add Gravitee Helm repository
$ helm repo add graviteeio https://helm.gravitee.io
```
{% endcode %}

2. Now we deploy APIM, but only the APIM Gateway component:

```sh
$ helm install — name graviteeio-apim3 — namespace graviteeio \
 -f values-bridge-http-client.yaml \
 -f values-hybrid-gw-eu.yaml \
 graviteeio/apim3
```

The `values-hybrid-management-gw-eu.yaml` file looks like this:

{% code title="values-hybrid-management-gw-eu.yaml" %}
```yaml
mongo:
    uri: mongodb+srv://xxxxxx:xxxxx@demo.xxxxx.gcp.mongodb.net/gio-apim-hybrid?retryWrites=true&w=majority
es:
    endpoints:
        - https://xxxxxxxxx-elasticsearch.services.elasticcloud.com/
    index: demo_hybrid_apim
    security:
        enabled: true
        username: xxxxxx
        password: xxxxxx
management:
    type: http
api:
    enabled: false
gateway:
    management:
        http:
            version: 3.3.1
            url: https://demo-hybrid-apim-bridge.cloud.gravitee.io/
            username: xxxxxxxxx
            password: xxxxxxxxx
    ingress:
        path: /
        hosts:
            - demo-hybrid-apim-gw.cloud.gravitee.io
        tls:
        -   hosts:
                - demo-hybrid-apim-gw.cloud.gravitee.io
            secretName: cloud-gravitee-cert
ui:
    enabled: false
portal:
    enabled: false
```
{% endcode %}

From this file, we can see that:

* All the management components have been disabled to prevent their deployment — management API, Management Console, and Developer Portal
* We have enabled `http` management mode for the gateway, and we use this link to mount all the required information in the Gateway to be able to process API calls

<figure><img src="https://docs.gravitee.io/images/apim/3.x/installation/hybrid/hybrid_deployment_http.png" alt=""><figcaption><p>APIM gatewaye cluster</p></figcaption></figure>

If you have a look at the Gateway pod logs, you will see something like this:

```sh
08:27:29.394 [graviteeio-node] [] INFO  i.g.g.r.p.RepositoryPluginHandler - Register a new repository plugin: repository-bridge-http-client [io.gravitee.repository.bridge.client.HttpBridgeRepository]
08:27:29.402 [graviteeio-node] [] INFO  i.g.g.r.p.RepositoryPluginHandler - Repository [MANAGEMENT] loaded by http
08:27:30.999 [graviteeio-node] [] INFO  i.g.r.b.client.http.WebClientFactory - Validate Bridge Server connection ...
08:27:32.888 [vert.x-eventloop-thread-1] [] INFO  i.g.r.b.client.http.WebClientFactory - Bridge Server connection successful.
```

We can now open up Management Console and see our two gateways running:

<figure><img src="https://docs.gravitee.io/images/apim/3.x/installation/hybrid/hybrid_deployment_gateways.png" alt=""><figcaption><p>Hybrid K8 deployment</p></figcaption></figure>

{% hint style="success" %}
Congratulations! Now that APIM is up and running, check out the [Quickstart Guide](../../quickstart-guide/README.md) for your next steps.
{% endhint %}
