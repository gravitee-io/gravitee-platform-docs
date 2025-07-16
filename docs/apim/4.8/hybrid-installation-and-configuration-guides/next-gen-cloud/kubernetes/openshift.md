# OpenShift

## Overview

This guide explains how to install and connect a Hybrid Gateway to Gravitee Cloud using OpenShift.

## Prerequisites

Before you install a Hybrid Gateway, complete the following steps:

* [#prepare-your-installation](../#prepare-your-installation "mention").

## Install the Gateway

{% hint style="info" %}
To deploy APIM with OpenShift, you must be running **OpenShift version 3.10 or later**. This is required because the Gravitee Helm Chart only supports Ingress standard objects. It does not support the specific OpenShift Routes.
{% endhint %}

When deploying APIM within OpenShift, you must:&#x20;

* Use the full host domain instead of paths for all components. Ingress paths are not sufficiently supported by OpenShift.
* Override the security context to let OpenShift automatically define the `user-id` and `group-id` with which to run containers.
* Set the `ingressClassName` to "none" for OpenShift to automatically create Routes from Ingress.

Below is a standard `values.yaml` to deploy the Gravitee APIM Gateway into OpenShift:

```yaml
openshift:
  enabled: true
  
gateway:
  replicaCount: 1
  image:
    repository: graviteeio/apim-gateway
    tag: 4.8.1
    pullPolicy: IfNotPresent
  autoscaling:
    enabled: false
  podAnnotations:
    prometheus.io/path: /_node/metrics/prometheus
    prometheus.io/port: "18082"
    prometheus.io/scrape: "true"
  env:
    - name: gravitee_cloud_token
      value: "${your-cloud-token}"
  services:
    metrics:
      enabled: true
      prometheus:
        enabled: true
    core:
      http:
          enabled: true
    sync:
      kubernetes:
        enabled: false
    bridge:
      enabled: false
  resources:
    limits:
      cpu: 500m
      memory: 1024Mi
    requests:
      cpu: 200m
      memory: 1024Mi
  ingress:
    ingressClassName: none
    path: /
    hosts:
      - ${gateway_hostname}.xxxx.xx.openshiftapps.com
    annotations:
      route.openshift.io/termination: edge
  securityContext: null
  deployment:
    securityContext:
      runAsUser: null
      runAsGroup: null
      runAsNonRoot: true
      allowPrivilegeEscalation: false
      capabilities:
        drop: ["ALL"]
      seccompProfile:
        type: RuntimeDefault
  reporters:
    file:
      enabled: false
  terminationGracePeriod: 50
  gracefulShutdown:
    delay: 20
    unit: SECONDS

api:
    enabled: false

ratelimit:
    type: none

portal:
    enabled: false

ui:
    enabled: false

alerts:
    enabled: false

es:
    enabled: false

license:
    key: "${your-license-key}"
```

* Replace `${your-cloud-token}` with your Cloud Token from Gravitee Cloud
* Replace `${gateway_hostname}` with your specific hostname for the Gravitee Gateway
* Replace `${your-license-key}` with your Gravitee License from Gravitee Cloud

## Verification

From the Gravitee Cloud Dashboard, you can see your configured Gateway.

<figure><img src="../../../.gitbook/assets/00 5 copy.png" alt=""><figcaption></figcaption></figure>

To verify that the Gateway is running, make a GET request to the URL on which you have published the Gateway. The output is a default message similar to:

```
No context-path matches the request URI.
```

You can now create and deploy APIs to your hybrid Gateway.
