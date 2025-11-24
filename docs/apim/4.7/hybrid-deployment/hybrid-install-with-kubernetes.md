---
description: Tutorial on hybrid install with kubernetes.
---

# Hybrid Install with Kubernetes

To install a Gravitee Gateway on Kubernetes, complete the following steps:

{% hint style="info" %}
You must be familiar with the following topics:

* Google Cloud Platform (GCP)
* Kubernetes (K8s)
* Helm
{% endhint %}

## Target architecture

In this example, we demonstrate how to deploy a Gravitee Gateway (APIM) in two different GCP regions. Also, we demonstrate how to deploy Gravitee APIM in the follow two different K8s clusters:

* A **Management cluster** that runs the following components:
  * The management API
  * The two APIM UI components
  * A bridge gateway
* A **Gateway cluster** that runs the APIM gateway.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/installation/hybrid/hybrid_deployment_k8s.png" alt=""><figcaption><p>Kubernetes hybrid deployment architecture diagram</p></figcaption></figure>

In this example, the deployment consists of the following components:

* MongoDB. MongoDB manages all the management data. For example, API definitions, subscriptions, and API keys.
* ElasticSearch. ElasticSearch is deployed in the Management cluster.
* Redis. Redis manages the rate limits and quota counters within the Gateway cluster.

## Deploy a Hybrid architecture with Helm

* To deploy a Hybrid architecture with Kubernetes, go to [Gravitee's Helm charts](https://helm.gravitee.io/).

### Before you begin

* Ensure the two GCP clusters exist.
* Ensure that Helm is installed on the GCP clusters.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/installation/hybrid/hybrid_k8s_clusters.png" alt=""><figcaption><p>Sample K8 clusters</p></figcaption></figure>

{% hint style="warning" %}
The following Hybrid architecture example use the following names:

* hybrid-gw-eu
* hybrid-mgmt-eu

You can replace these names with the name of your clusters.
{% endhint %}

### Deploying the management cluster

1. Initialize the cluster with some prerequisites using the following commands:

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

2. Deploy the management APIM instance using the following command. The management APIM contains the follow components:
   * The Management Console
   * The Developer Portal
   * Management API
   * The Bridge Gateway

```sh
$ helm install — name graviteeio-apim3 — namespace graviteeio \
 -f values-bridge-http-server.yaml \
 -f values-hybrid-management-eu.yaml \
 graviteeio/apim3
```

When you install the `values-hybrid-management-eu.yaml`, the file looks like this example:

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
            authentication:
                type: basic
                basic:
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

The file shows the following elements:

* The Gateway is not exposed through the ingress controller.
* You enabled the bridge service for the Gateway.
* Declared a new ingress to expose it to remote clusters.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/installation/hybrid/hybrid_deployment_ingress.png" alt=""><figcaption><p>APIM management cluster</p></figcaption></figure>

### Deploy the Gateway cluster

1. Initialize the cluster with some prerequisites using the following commands:

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

2. Deploy only the APIM Gateway component using the following command:

```sh
$ helm install — name graviteeio-apim3 — namespace graviteeio \
 -f values-bridge-http-client.yaml \
 -f values-hybrid-gw-eu.yaml \
 graviteeio/apim3
```

When you deploy the Gravitee APIM Gateway, the `values-hybrid-management-gw-eu.yaml` file looks like the following example:

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
            url: https://demo-hybrid-apim-bridge.cloud.gravitee.io/
            authentication:
                type: basic
                basic:
                    username: xxxxxxxxx
                    password: xxxxxxxxx
            ssl:
                ### beware: since 4.4 default is false
                trustAll: false
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

`values-hybrid-management-gw-eu.yaml` shows the following elements:

* You have disabled all the management components to prevent their deployment.
* You have enabled `http` management mode for the gateway, and you use this link to mount all the required information in the Gateway to process API calls.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/installation/hybrid/hybrid_deployment_http.png" alt=""><figcaption><p>APIM gatewaye cluster</p></figcaption></figure>

### Verification

To verify that you deployed this architecture correctly, complete the following steps:

#### Examine the Gateway pod logs

Examine the Gateway pod logs. You should see an output like this example:

```sh
08:27:29.394 [graviteeio-node] [] INFO  i.g.g.r.p.RepositoryPluginHandler - Register a new repository plugin: repository-bridge-http-client [io.gravitee.repository.bridge.client.HttpBridgeRepository]
08:27:29.402 [graviteeio-node] [] INFO  i.g.g.r.p.RepositoryPluginHandler - Repository [MANAGEMENT] loaded by http
08:27:30.999 [graviteeio-node] [] INFO  i.g.r.b.client.http.WebClientFactory - Validate Bridge Server connection ...
08:27:32.888 [vert.x-eventloop-thread-1] [] INFO  i.g.r.b.client.http.WebClientFactory - Bridge Server connection successful.
```

#### Check the Management Gateway

Open the Management Console. You should see two gateways.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/installation/hybrid/hybrid_deployment_gateways.png" alt=""><figcaption><p>Hybrid K8 deployment</p></figcaption></figure>

{% hint style="info" %}
**Additional assets**

* [Gravitee Helm charts](https://artifacthub.io/packages/helm/graviteeio/apim3)
{% endhint %}

### **Configuring the connection between the SaaS Control-Plane and the Bridge Gateway**

{% code title="values.yaml" lineNumbers="true" %}
```yaml
management:
  type: http
gateway:
  management:
    http:
      url: https://bridge-gateway-url:bridge-gateway-port
      # the following still works but is deprecated 
      # username: kubernetes://<namespace>/secrets/<my-secret-name>/<my-secret-key>
      # password: kubernetes://<namespace>/secrets/<my-secret-name>/<my-secret-key>
      authentication:
        type: basic
        basic:
          username: secret://kubernetes/<my-secret-name>:<my-secret-key>
          password: secret://kubernetes/<my-secret-name>:<my-secret-key>
      # ssl:
      #   ### beware: since 4.4 default is false (see upgrade guide) 
      #   trustall: true
      #   verifyHostname: true
      #   keystore:
      #     type: jks # Supports jks, pem, pkcs12
      #     path: ${gravitee.home}/security/keystore.jks
      #     password: secret
      #   truststore:
      #     type: jks # Supports jks, pem, pkcs12
      #     path: ${gravitee.home}/security/truststore.jks
      #     password: secret
      # proxy:
      #   host:
      #   port:
      #   type: http
      #   username:
      #   password:
```
{% endcode %}

### **An example of a Self-Hosted Gateway configuration**

{% code title="values.yaml" lineNumbers="true" %}
```yaml
management:
  type: http
gateway:
  management:
    http:
      url: https://bridge-gateway-url:bridge-gateway-port
      authentication:
        type: basic
        basic:
          username: secrets://kubernetes/<my-secret-name>:<my-secret-key>
          password: secrets://kubernetes/<my-secret-name>:<my-secret-key>
  reporters:
    elasticsearch:
      enabled: false
    tcp:
      enabled: true
      host: logstash
      port: 8379
      output: elasticsearch
alerts:
  enabled: true
  endpoints:
    - https://alert-engine-url:alert-engine-port
  security:
    enabled: true
    username: secrets://kubernetes/<my-secret-name>:<my-secret-key>
    password: secrets://kubernetes/<my-secret-name>:<my-secret-key>
```
{% endcode %}
