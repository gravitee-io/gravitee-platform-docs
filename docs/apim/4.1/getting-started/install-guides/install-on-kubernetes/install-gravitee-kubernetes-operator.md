# Gravitee Kubernetes Operator K8s Installation

## Overview

A [Kubernetes operator](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/) is an application-specific controller that extends the functionality of the Kubernetes API to create, configure, deploy, and manage application instances using `kubectl` tooling.

<details>

<summary>Context for introducing an operator</summary>

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

While the REST API method is compatible with IaC, customer feedback favors a Kubernetes-native deployment of APIs, the Gravitee APIM Gateway and the Console via [Custom Resource Definitions (CRDs)](../../../guides/gravitee-kubernetes-operator/custom-resource-definitions/). The introduction of the Gravitee Kubernetes Operator (GKO) makes this possible.

</details>

<details>

<summary>How it works</summary>

An API deployed in a Kubernetes cluster can be described as an API extension of Kubernetes using CRDs. This approach relies on the Management Console or the Management API to use the GKO and the Kubernetes API to deploy the API to your API Gateway.

</details>

The sections below introduce the following:

* [Architecture overview and possible deployments](install-gravitee-kubernetes-operator.md#architecture-overview)
* [Installation steps](install-gravitee-kubernetes-operator.md#installation)
* [API deployments in Kubernetes](install-gravitee-kubernetes-operator.md#api-deployment-in-a-kubernetes-cluster)

## Architecture overview

The current functionality of the Gravitee Kubernetes Operator supports three main deployment scenarios, as described below.

{% tabs %}
{% tab title="Standard" %}
In a standard deployment, the Management API and the API Gateway are deployed in the same Kubernetes cluster.

With this workflow, the GKO listens for CRDs. For each custom resource, an API is pushed to the Management API using the import endpoint and the API Gateway deploys the APIs accordingly.

The following diagram illustrates the standard deployment architectural approach:

<figure><img src="https://docs.gravitee.io/images/apim/3.x/kubernetes/gko-architecture-1-standard.png" alt=""><figcaption><p>Standard deployment architecture</p></figcaption></figure>
{% endtab %}

{% tab title="Multiple clusters" %}
A deployment on multiple clusters assumes the following:

1. The user manages multiple Kubernetes clusters using a different set of APIs for each cluster
2. All APIs are managed using a single API Console
3. GKO is installed on all required clusters

The following diagram illustrates the multi-cluster deployment architectural approach:

<figure><img src="https://docs.gravitee.io/images/apim/3.x/kubernetes/gko-architecture-2-multi-cluster.png" alt=""><figcaption><p>Multi-cluster deployment architecture</p></figcaption></figure>
{% endtab %}

{% tab title="Multiple environments" %}
In a multi-environment deployment, a single GKO is deployed that can publish APIs to different environments (logical or physical). This is managed directly from the [ApiDefinition custom resource](../../../guides/gravitee-kubernetes-operator/custom-resource-definitions/apidefinition-crd.md), which refers to a [ManagementContext custom resource](../../../guides/gravitee-kubernetes-operator/custom-resource-definitions/managementcontext-resource.md).

{% hint style="info" %}
Different APIs are published on each of the environments because although APIs use the `ManagementContext` CRD, which can reference any Management API, an `ApiDefinition` CRD can only have one Management Context.
{% endhint %}

The following diagram illustrates the multi-environment deployment architectural approach:

<figure><img src="https://docs.gravitee.io/images/apim/3.x/kubernetes/gko-architecture-3-multi-env.png" alt=""><figcaption><p>Multi-environment deployment architecture</p></figcaption></figure>
{% endtab %}
{% endtabs %}

## Installation

The steps to install the GKO on an existing Kubernetes cluster are described below.

{% hint style="info" %}
If your architecture requires the management of multiple Kubernetes clusters, each with a different set of APIs, you should deploy the GKO separately on each cluster. Follow the deployment process for each cluster deployment.
{% endhint %}

### Prerequisites

* Kubernetes: `>=1.16.0-0`
* [Kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl) and [Helm v3](https://helm.sh/docs/intro/install/), installed and running locally
* An APIM instance running on your cluster, installed per our [installation guide](./)
* Set `gateway.services.sync.kubernetes.enabled=true` in your APIM configuration to enable the Gateway to synchronize with the operator resources

{% hint style="info" %}
**Namespaces**

By default, the Kubernetes synchronizer is configured to watch for API definitions in the API Gateway namespace. To watch all namespaces, set`gateway.services.sync.kubernetes.namespaces=all` in the Gateway configuration. Alternatively, you can provide a specific list of namespaces to watch. This requires that the Gateway service account has the `list` permissions for ConfigMaps at the cluster level or that the`gateway.services.sync.kubernetes.namespaces` property defines the list of namespaces.
{% endhint %}

### Install using Helm

1.  Add the Gravitee Helm Chart repo:

    ```bash
    helm repo add graviteeio https://helm.gravitee.io
    ```
2.  Install the chart with the release name `graviteeio-gko`:

    * For all deployments other than DB-less:

    ```bash
    helm install graviteeio-gko graviteeio/gko
    ```

    * For a DB-less deployment:

    ```bash
    $ helm repo update graviteeio
    $ helm upgrade --install --create-namespace -n dbless-gko graviteeio-gko graviteeio/gko
    ```
3.  **(Optional)** By default, the operator listens to resources created anywhere in the cluster. To restrict the operator to the release namespace, set `manager.scope.cluster=false`:

    ```bash
    helm install --set manager.scope.cluster=false -n ${RELEASE_NAMESPACE} graviteeio-gko graviteeio/gko
    ```



    {% hint style="info" %}
    **Cluster scope**

    * If you are installing the operator with the cluster scope enabled (the default), it is recommended to install one instance of the operator per cluster.&#x20;
    * If you are installing the operator with the cluster scope disabled, you can install multiple instances of the operator in the same cluster, with each one watching a different namespace.
    {% endhint %}

### Upgrading the Operator

Assuming that the repository as been aliased as `graviteeio` and that the release name is `graviteeio-gko`:

```bash
$ helm repo update graviteeio
$ helm upgrade --install graviteeio-gko graviteeio/gko
```

### Parameters

The Gravitee Kubernetes Operator Helm Chart supports configuration of the following:

* [RBAC](install-gravitee-kubernetes-operator.md#rbac)
* [RBAC Proxy](install-gravitee-kubernetes-operator.md#rbac-proxy)
* [Controller Manager](install-gravitee-kubernetes-operator.md#controller-manager)
* [Ingress](install-gravitee-kubernetes-operator.md#ingress)
* [Cert Manager](install-gravitee-kubernetes-operator.md#cert-manager)
* [HTTP Client](install-gravitee-kubernetes-operator.md#http-client)

{% tabs %}
{% tab title="RBAC" %}
Required RBAC resources are created by default for all components involved in the release.

| Name                    | Description                                                                   | Value                    |
| ----------------------- | ----------------------------------------------------------------------------- | ------------------------ |
| `serviceAccount.create` | Specifies if a service account should be created for the manager pod.         | `true`                   |
| `serviceAccount.name`   | Specifies the service account name to use.                                    | `gko-controller-manager` |
| `rbac.create`           | Specifies if RBAC resources should be created.                                | `true`                   |
| `rbac.skipClusterRoles` | Specifies if cluster roles should be created when RBAC resources are created. | `false`                  |
{% endtab %}

{% tab title="RBAC Proxy" %}
Kube RBAC Proxy is deployed as a sidecar container and restricts access to the Prometheus metrics endpoint.

{% hint style="warning" %}
If this is disabled, the Prometheus metrics endpoint will be exposed with no access control at all.
{% endhint %}

| Name                         | Description                                                   | Value                            |
| ---------------------------- | ------------------------------------------------------------- | -------------------------------- |
| `rbacProxy.enabled`          | Specifies if the `kube-rbac-proxy` sidecar should be enabled. | `true`                           |
| `rbacProxy.image.repository` | Specifies the Docker registry and image name to use.          | `quay.io/brancz/kube-rbac-proxy` |
| `rbacProxy.image.tag`        | Specifies the Docker image tag to use.                        | `v0.14.3`                        |
{% endtab %}

{% tab title="Controller Manager" %}
Use these parameters to configure the deployment itself and the ways in which the operator will interact with APIM and custom resources in your cluster.

| Name                                        | Description                                                                                  | Value                            |
| ------------------------------------------- | -------------------------------------------------------------------------------------------- | -------------------------------- |
| `manager.image.repository`                  | Specifies the Docker registry and image name to use.                                         | `graviteeio/kubernetes-operator` |
| `manager.image.tag`                         | Specifies the Docker image tag to use.                                                       | `latest`                         |
| `manager.logs.json`                         | Whether to output manager logs in JSON format.                                               | `true`                           |
| `manager.configMap.name`                    | The name of the ConfigMap used to set the manager config.                                    | `gko-config`                     |
| `manager.scope.cluster`                     | Use false to listen only in the release namespace.                                           | `true`                           |
| `manager.applyCRDs`                         | If true, the manager will patch custom resource definitions on startup.                      | `true`                           |
| `manager.metrics.enabled`                   | If true, a metrics server will be created so that metrics can be scraped using Prometheus.   | `true`                           |
| `manager.httpClient.insecureSkipCertVerify` | If true, the manager HTTP client will not verify the certificate used by the Management API. | `false`                          |
{% endtab %}

{% tab title="Ingress" %}
Use the following parameters to configure the behavior of the ingress controller.

When storing templates in ConfigMaps, the ConfigMap should contain a `content` key and a `contentType` key, e.g.:

```yaml
content: '{ "message": "Not Found" }'
contentType: application/json
```

| Name                              | Description                                                                | Value |
| --------------------------------- | -------------------------------------------------------------------------- | ----- |
| `ingress.templates.404.name`      | Name of the ConfigMap storing the HTTP 404 ingress response template.      | `""`  |
| `ingress.templates.404.namespace` | Namespace of the ConfigMap storing the HTTP 404 ingress response template. | `""`  |
{% endtab %}

{% tab title="Cert Manager" %}
Use the following parameters to enable and configure the `cert-manager` dependency. The Cert Manager is necessary to enable Webhook conversions and validation required by the operator.

{% hint style="warning" %}
The Cert Manager manages non-namespaced resources in a cluster. **It must be installed exactly once.**&#x20;

Enabling the `cert-manager` dependency ties the lifecycle of `cert-manager` to the operator. This property is intended for testing purposes. In production, we recommend installing `cert-manager` as a separate component.
{% endhint %}

The namespace defined to install `cert-manager` must have been created prior to enabling the `cert-manager` dependency. Learn more [here](https://cert-manager.io/docs/installation/helm).

<table><thead><tr><th width="217">Name</th><th width="233">Description</th><th>Value</th></tr></thead><tbody><tr><td><code>cert-manager.enabled</code></td><td>If true, <code>cert-manager</code> will be installed as a dependency.</td><td><code>false</code></td></tr><tr><td><code>cert-manager.namespace</code></td><td>Defines the namespace where <code>cert-manager</code> will be installed.</td><td><code>cert-manager</code></td></tr></tbody></table>
{% endtab %}

{% tab title="HTTP Client" %}
{% hint style="warning" %}
This section is deprecated and will be removed in version 1.0.0. The `httpClient` property should now be set with the Controller Manager.
{% endhint %}

<table><thead><tr><th width="241">Name</th><th width="200.66666666666666">Description</th><th>Value</th></tr></thead><tbody><tr><td><code>httpClient.insecureSkipCertVerify</code></td><td>If true, the manager HTTP client will not verify the certificate used by the Management API.</td><td><code>false</code></td></tr></tbody></table>
{% endtab %}
{% endtabs %}

## API deployment in a Kubernetes Cluster

You can deploy an API on Gravitee Gateways deployed in different Kubernetes clusters. The Management API will be deployed in the same cluster as the GKO. The following reference diagram is the basis for both the single and multi-Gateway deployment options discussed below.

<figure><img src="../../../.gitbook/assets/image (45).png" alt=""><figcaption><p>Gateways in different Kubernetes Clusters</p></figcaption></figure>

{% tabs %}
{% tab title="Single Gateway" %}
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
{% endtab %}

{% tab title="Multiple clusters" %}
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
{% endtab %}
{% endtabs %}

## Next steps

Visit our [GKO guide](../../../guides/gravitee-kubernetes-operator/) to:

* Learn how to use the GKO to define, deploy, and publish APIs to your API Portal and API Gateway
* Manage custom resource definitions (CRDs)
