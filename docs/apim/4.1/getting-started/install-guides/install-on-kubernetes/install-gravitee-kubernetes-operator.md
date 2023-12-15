---
description: >-
  This article covers how to install and configure the GKO with Gravitee's
  official Helm Chart
---

# Gravitee Kubernetes Operator Helm Install and Configuration

## Overview

A [Kubernetes operator](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/) is an application-specific controller that extends the functionality of the Kubernetes API to create, configure, deploy, and manage application instances using `kubectl` tooling. The Gravitee Kubernetes Operator (GKO) takes advantage of this functionality to allow you to manage your APIs in a fully declarative fashion.

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

An API deployed with Gravitee in a Kubernetes cluster can be described as an API extension of Kubernetes using custom resource definitions (CRDs). These CRDs become the source of truth for your APIs and are synced to the APIM cluster using the ManagementContext CRD. You can learn more in the [GKO guide](../../../guides/gravitee-kubernetes-operator/) after completing the installation.

</details>

The sections below introduce:

* [Architecture overview and possible deployments](install-gravitee-kubernetes-operator.md#architecture-overview)
* [Installation steps](install-gravitee-kubernetes-operator.md#installation)
* [API deployments in Kubernetes](install-gravitee-kubernetes-operator.md#api-deployment-in-a-kubernetes-cluster)

{% hint style="warning" %}
The following sections apply to GKO version 1.x.x. GKO 0.x.x will be deprecated in 2024. Refer to the [GKO 1.x.x changelog](https://github.com/gravitee-io/gravitee-kubernetes-operator/releases/tag/1.0.0-beta.1) to track breaking changes.
{% endhint %}

## Architecture overview

The current functionality of the Gravitee Kubernetes Operator supports two main deployment scenarios, as described below.

{% tabs %}
{% tab title="Cluster Mode" %}
By default, the Gravitee Kubernetes Operator is set up to listen to the custom resources it owns at the cluster level.

In this mode, a single operator must be installed in the cluster to handle resources, regardless of the namespaces they have been created in. For each resource created in a specific namespace, the operator creates a ConfigMap in the same namespace that contains an API definition to be synced with an APIM Gateway.

By default, an APIM Gateway installed using the Helm Chart includes a limited set of permissions, and the Gateway is only able to access ConfigMaps created in its own namespace. However, giving a Gateway the cluster role allows it to access ConfigMaps created by the operator at the cluster level.

An overview of this architecture is described by the diagram below.

<figure><img src="../../../.gitbook/assets/GKO default cluster mode architecture.png" alt=""><figcaption><p>Default Cluster Mode architecture</p></figcaption></figure>
{% endtab %}

{% tab title="Namespaced Mode" %}
The Gravitee Kubernetes Operator can be set up to listen to a single namespace in a Kubernetes cluster. One operator is deployed per namespace, and each listens to the custom resources created in its namespace only.

To achieve this architecture, the `manager.scope.cluster` value must be set to `false` during the Helm install. Role names are computed from the service account name, so each install must set a dedicated service account name for each operator using the `serviceAccount.name` Helm value.

To handle [conversion between resource versions](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definition-versioning/), at least one operator in the cluster must act as a Webhook, meaning it must be installed with the `manager.webhook.enabled` property set to `true` (the default). When all operators use this default setting, the last operator installed in the cluster acts as the conversion Webhook.

<img src="../../../.gitbook/assets/file.excalidraw (20).svg" alt="Multiple operators, each listening to its own namespace" class="gitbook-drawing">
{% endtab %}

{% tab title="Multi-Cluster Mode" %}
In a multi-cluster architecture, you can set up Gateways on different Kubernetes clusters or virtual machines, then use an operator to generate an API definition that is accessible from each of these Gateways. This means that:

* An APIM instance is required to act as a source of truth for the Gateways
* The operator will obtain the API definition from APIM instead of creating one in a ConfigMap
* The API definition requires a Management Context
* The `definitionContext` of the API must be set to sync from APIM

The following snippet contains the relevant specification properties for the API definition of a multi-cluster architecture:

```yaml
apiVersion: gravitee.io/v1beta1
kind: ApiDefinition
metadata:
  name: multi-cluster-api
spec:
  contextRef:
    name: apim-ctx
    namespace: gravitee
  definitionContext:
    syncFrom: MANAGEMENT
  # [...]
```

<figure><img src="../../../.gitbook/assets/GKO multi-cluster architecture (2).png" alt=""><figcaption><p>Multi-cluster architecture overview</p></figcaption></figure>
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

### Install steps

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
    * Multiple instances of the operator with the cluster scope disabled can be installed in the same cluster, with each one watching a different namespace. One operator must be given the cluster role and the ability to perform the Webhook conversion between v1alpha1 and v1beta1 CRD references.
    {% endhint %}

## Upgrading the Operator

Assuming that the repository has been aliased as `graviteeio` and that the release name is `graviteeio-gko`:

```bash
$ helm repo update graviteeio
$ helm upgrade --install graviteeio-gko graviteeio/gko
```

## Configuration parameters

The Gravitee Kubernetes Operator Helm Chart supports configuration of the following:

* [RBAC](install-gravitee-kubernetes-operator.md#rbac)
* [RBAC Proxy](install-gravitee-kubernetes-operator.md#rbac-proxy)
* [Controller Manager](install-gravitee-kubernetes-operator.md#controller-manager)
* [Ingress](install-gravitee-kubernetes-operator.md#ingress)

{% tabs %}
{% tab title="RBAC" %}
Required RBAC resources are created by default for all components involved in the release.

<table><thead><tr><th>Name</th><th width="233">Description</th><th>Value</th></tr></thead><tbody><tr><td><code>serviceAccount.create</code></td><td>Specifies if a service account should be created for the manager pod.</td><td><code>true</code></td></tr><tr><td><code>serviceAccount.name</code></td><td><a data-footnote-ref href="#user-content-fn-1">Specifies the service account name to use. </a>If the operator is deployed in multiple namespaces by setting <code>scope.cluster</code> to <code>false</code>, a different service account name must be used for each installation.</td><td><code>gko-controller-manager</code></td></tr><tr><td><code>rbac.create</code></td><td>Specifies if RBAC resources should be created.</td><td><code>true</code></td></tr><tr><td><code>rbac.skipClusterRoles</code></td><td>Specifies if cluster roles should be created when RBAC resources are created.</td><td><code>false</code></td></tr></tbody></table>
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
| `rbacProxy.image.pullPolicy` | Specifies the pull policy to apply to the RBAC proxy image.   | `Always`                         |
{% endtab %}

{% tab title="Controller Manager" %}
Use these parameters to configure the deployment and the ways in which the operator will interact with APIM and custom resources in your cluster.

| Name                                        | Description                                                                                               | Value                            |
| ------------------------------------------- | --------------------------------------------------------------------------------------------------------- | -------------------------------- |
| `manager.image.repository`                  | Specifies the Docker registry and image name to use.                                                      | `graviteeio/kubernetes-operator` |
| `manager.image.tag`                         | Specifies the Docker image tag to use.                                                                    | `latest`                         |
| `manager.image.pullPolicy`                  | Specifies the pull policy to apply to the controller manager image.                                       | `Always`                         |
| `manager.log.format`                        | Specifies log output format. Can be either JSON or console.                                               | `json`                           |
| `manager.log.level`                         | Specifies log level. Can be either debug, info, warn, or error.                                           | `info`                           |
| `manager.log.timestamp.field`               | Specifies the name of the field to use for the timestamp.                                                 | `timestamp`                      |
| `manager.log.timestamp.format`              | Specifies the format to use for the timestamp. Can be iso-8601, epoch-second, epoch-millis or epoch-nano. | `epoch-second`                   |
| `manager.configMap.name`                    | The name of the ConfigMap used to set the manager config from these values.                               | `gko-config`                     |
| `manager.resources.limits.cpu`              | The CPU resource limits for the GKO Manager container.                                                    | `500m`                           |
| `manager.resources.limits.memory`           | The memory resources limits for the GKO Manager container.                                                | `128Mi`                          |
| `manager.resources.requests.cpu`            | The requested CPU for the GKO Manager container.                                                          | `5m`                             |
| `manager.resources.requests.memory`         | The requested memory for the GKO Manager container.                                                       | `64Mi`                           |
| `manager.scope.cluster`                     | Use `false` to listen only in the release namespace.                                                      | `true`                           |
| `manager.metrics.enabled`                   | If true, a metrics server will be created so that metrics can be scraped using Prometheus.                | `true`                           |
| `manager.metrics.port`                      | Which port the metric server will bind to.                                                                | `8080`                           |
| `manager.probe.port`                        | The port the readiness and liveness probes will listen to.                                                | `8081`                           |
| `manager.httpClient.insecureSkipCertVerify` | If true, the manager HTTP client will not verify the certificate used by the Management API.              | `false`                          |
| `manager.httpClient.timeoutSeconds`         | The timeout (in seconds) used when issuing requests to the Management API.                                | `10`                             |
| `manager.webhook.enabled`                   | If true, the manager will register a Webhook server operating on custom resources.                        | `true`                           |
| `manager.webhook.service.name`              | The service used to expose the Webhook server.                                                            | `gko-webhook`                    |
| `manager.webhook.service.port`              | The port the Webhook server will listen to.                                                               | `9443`                           |
| `manager.webhook.cert.create`               | If true, a secret will be created to store the Webhook server certificate.                                | `true`                           |
| `manager.webhook.cert.name`                 | The name of the cert-manager certificate used by the Webhook server.                                      | `gko-webhook-cert`               |
| `manager.webhook.cert.secret.name`          | The name of the secret storing the Webhook server certificate.                                            | `gko-webhook-cert`               |
{% endtab %}

{% tab title="Ingress" %}
Use the following parameters to configure the behavior of the ingress controller.

When storing templates in ConfigMaps, the ConfigMap should contain a `content` key and a `contentType` key, for example:

```yaml
content: '{ "message": "Not Found" }'
contentType: application/json
```

<table><thead><tr><th width="229">Name</th><th width="271">Description</th><th>Value</th></tr></thead><tbody><tr><td><code>ingress.templates.404.name</code></td><td>Name of the ConfigMap storing the HTTP 404 ingress response template.</td><td><code>""</code></td></tr><tr><td><code>ingress.templates.404.namespace</code></td><td>Namespace of the ConfigMap storing the HTTP 404 ingress response template.</td><td><code>""</code></td></tr></tbody></table>
{% endtab %}
{% endtabs %}

## Next steps

Visit our [GKO guide](../../../guides/gravitee-kubernetes-operator/) to:

* Learn how to use the GKO to define, deploy, and publish APIs to your API Portal and API Gateway
* Manage custom resource definitions (CRDs)

[^1]: I forgot to add a precision here. Something like: "If you are deploying the operator in several namespaces ny setting \`scope.cluster\` to \`false\`, a different service account name \*must\* be used on each installation.
