# Gravitee Kubernetes Operator Deployment

## Overview

A [Kubernetes operator](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/) is an application-specific controller that extends the functionality of the Kubernetes API to create, configure, deploy, and manage application instances using `kubectl` tooling.

### Context for introducing an operator

Gravitee is able to deploy the following components:

* APIs and associated applications
* The API Gateway and the Management Console

An increasing number of Gravitee users are implementing infrastructure-as-code (IAC). To support IAC-based use cases, Gravitee enables platform deployment “as code” by performing the actions below without the use of a UI:

* Push/deploy APIs to the API Gateway
* Test the APIs
* Promote the APIs across different environments (test, UAT, dev, prod, etc.)

Historically, Gravitee customers have deployed APIs using the following:

* **Gravitee Management Console:** Gravitee includes an easy-to-use, self-serve UI. The Console is often used as a development tool and is connected to a backend service that is part of the Gravitee web application.
* **Gravitee management API:** Every action in the Gravitee Management Console represents a REST API with a JSON payload that is documented using an API spec. Consequently, every UI action can be performed via REST API calls backed by JSON files. A Gravitee API definition is also a JSON file that explains endpoints, protections, etc.

While the REST API method is compatible with IaC, customer feedback favors a Kubernetes-native deployment of APIs, the Gravitee APIM Gateway and the Console via [Custom Resource Definitions (CRDs)](../../../guides/gravitee-kubernetes-operator/page-1/). The introduction of the Gravitee Kubernetes Operator (GKO) makes this possible.

### How it works

An API deployed in a Kubernetes cluster can be described as an API extension of Kubernetes using CRDs. This approach relies on the Management Console or the Management API to use the GKO and the Kubernetes API to deploy the API to your API Gateway.

## Architecture overview

The current functionality of the Gravitee Kubernetes Operator supports three main deployment scenarios, as described below.

### Standard deployment

In a standard deployment, the Management API and the API Gateway are deployed in the same Kubernetes cluster.

With this workflow, the GKO listens for CRDs. For each custom resource, an API is pushed to the Management API using the import endpoint and the API Gateway deploys the APIs accordingly.

The following diagram illustrates the standard deployment architectural approach:

<figure><img src="https://docs.gravitee.io/images/apim/3.x/kubernetes/gko-architecture-1-standard.png" alt=""><figcaption><p>Standard deployment architecture</p></figcaption></figure>

### Deployment on multiple clusters

This scenario assumes the following:

1. The user manages multiple Kubernetes clusters using a different set of APIs for each cluster
2. All APIs are managed using a single API Console
3. GKO is installed on all required clusters

The following diagram illustrates the multi-cluster deployment architectural approach:

<figure><img src="https://docs.gravitee.io/images/apim/3.x/kubernetes/gko-architecture-2-multi-cluster.png" alt=""><figcaption><p>Multi-cluster deployment architecture</p></figcaption></figure>

### Deployment on multiple environments

In this scenario, a single GKO is deployed that can publish APIs to different environments (logical or physical). This is managed directly from the [ApiDefinition custom resource](../../../guides/gravitee-kubernetes-operator/page-1/apidefinition-crd.md), which refers to a [ManagementContext custom resource](../../../guides/gravitee-kubernetes-operator/page-1/managementcontext-resource.md).

{% hint style="info" %}
Different APIs are published on each of the environments because although APIs use the `ManagementContext` CRD, which can reference any Management API, an `ApiDefinition` CRD can only have one Management Context.
{% endhint %}

The following diagram illustrates the multi-environment deployment architectural approach:

<figure><img src="https://docs.gravitee.io/images/apim/3.x/kubernetes/gko-architecture-3-multi-env.png" alt=""><figcaption><p>Multi-environment deployment architecture</p></figcaption></figure>

## Installation

The steps to install the GKO on an existing Kubernetes cluster are described below.

{% hint style="info" %}
If your architecture requires the management of multiple Kubernetes clusters, each with a different set of APIs, you should deploy the GKO separately on each cluster. Follow the deployment process for each cluster deployment.
{% endhint %}

### Prerequisites

* [Kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl) and [Helm v3](https://helm.sh/docs/intro/install/), installed and running locally.
* An APIM instance running on your cluster, installed per our [installation guide](./).
* Set `gateway.services.sync.kubernetes.enabled=true` in your APIM configuration to enable the Gateway to synchronize with the operator resources.

{% hint style="info" %}
**Namespaces**

By default, the Kubernetes synchronizer is configured to watch for API definitions in the API Gateway namespace. To watch all namespaces, set`gateway.services.sync.kubernetes.namespaces=all` in the Gateway configuration. Alternatively, you can provide a specific list of namespaces to watch. This requires that the Gateway service account has the `list` permissions for ConfigMaps at the cluster level or that the`gateway.services.sync.kubernetes.namespaces` property defines the list of namespaces.&#x20;
{% endhint %}

### Install using Helm

1. Add the Gravitee Helm Chart repo:

```sh
helm repo add graviteeio https://helm.gravitee.io
```

2.  Install the chart with the release name `graviteeio-gko`:

    * For all deployments other than DB-less:&#x20;

    ```bash
    helm install graviteeio-gko graviteeio/gko
    ```

    * For a DB-less deployment:

    ```bash
    helm upgrade --install --create-namespace -n dbless-gko graviteeio-gko graviteeio/gko
    ```
3. **(Optional)** By default, the operator listens to resources created anywhere in the cluster. To restrict the operator to the release namespace, set `manager.scope.cluster=false`:

{% code overflow="wrap" %}
```sh
helm install --set manager.scope.cluster=false -n ${RELEASE_NAMESPACE} graviteeio-gko graviteeio/gko
```
{% endcode %}

{% hint style="info" %}
**Cluster scope**

If you are installing the operator with the cluster scope enabled (the default), it is recommended to install one instance of the operator per cluster. If you are installing the operator with the cluster scope disabled, you can install multiple instances of the operator in the same cluster, with each one watching a different namespace.
{% endhint %}

## API deployment in a Kubernetes Cluster

You can deploy an API on Gravitee Gateways deployed in different Kubernetes clusters. The Management API will be deployed in the same cluster as the GKO.

<figure><img src="../../../.gitbook/assets/image (45).png" alt=""><figcaption><p>Gateways in different Kubernetes Clusters</p></figcaption></figure>

### Deploy on a single Gateway

To deploy an API on a single Gateway, apply the following configuration on the Gateway 1 cluster:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiDefinition
metadata:
  name: local-api-example
spec:
  name: "GKO Basic"
  version: "1.1"
  description: "Basic api managed by Gravitee Kubernetes Operator"
  proxy:
    virtual_hosts:
      - path: "/k8s-basic"
    groups:
      - endpoints:
          - name: "Default"
            target: "https://api.gravitee.io/echo"
  local: true
```

The `local` field is optional and is set to `true` by default to indicate that the API will be deployed only in the cluster where the custom resource is applied. Run the following command to verify that the API ConfigMap has been created in the Gateway 1 cluster:

```sh
kubectl get cm -n gateway-1-cluster
```

```
NAMESPACE            NAME                DATA    AGE
gateway-1-namespace  local-api-example   1       1m
```

### Deploy on multiple clusters

To deploy an API on multiple Gateways, use a custom resource that can be applied to any cluster. As long as the Management API is available, the `ApiDefinition` refers to a `ManagementContext` and the `local` field is set to `false`.

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiDefinition
metadata:
  name: global-api-example
spec:
  name: "GKO Basic"
  version: "1.1"
  description: "Basic api managed by Gravitee Kubernetes Operator"
  contextRef:
    name: apim-example-context
    namespace: apim-example
  proxy:
    virtual_hosts:
      - path: "/k8s-basic"
    groups:
      - endpoints:
          - name: "Default"
            target: "https://api.gravitee.io/echo"
  local: false
```

With the above configuration, there should be no `ConfigMap` linked to the `ApiDefinition` in the cluster where the custom resource has been applied because the `ApiDefinition` was deployed using the Management API and the `ApiDefinition` is not local to the cluster.

## Next steps

Visit our [GKO guide](../../../guides/gravitee-kubernetes-operator/) to:

* Learn how to use the GKO to define, deploy, and publish APIs to your API Portal and API Gateway
* Manage custom resource definitions (CRDs)
