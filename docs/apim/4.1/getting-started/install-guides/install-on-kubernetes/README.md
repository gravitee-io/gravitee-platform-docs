---
description: An overview of Helm charts and Kubernetes operators
---

# Install on Kubernetes

{% hint style="info" %}
This guide assumes familiarity with Kubernetes and its terms.
{% endhint %}

Installing Gravitee API Management (APIM) on Kubernetes is made easy with the help of our Helm chart. **This Helm chart supports Gravitee APIM Management (APIM) versions: 3.0.x and higher** and deploys the following:

* APIM Management API
* APIM Management Console
* APIM Developer Portal
* APIM Gateway
* MongoDB replica set or PostgresSQL (optional dependency)
* Elasticsearch Cluster (optional dependency)

## Installation prerequisites

The following command line tools must be installed:

* [Kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)
* [Helm v3](https://helm.sh/docs/intro/install/)

## Installation Steps

1. Add the Gravitee Helm charts repo:

```sh
helm repo add graviteeio https://helm.gravitee.io
```

2. Install the chart from the Helm repo by specifying the desired release. The example below uses `graviteeio-apim4x`.

{% hint style="warning" %}
**Dedicated namespace**

To prevent potential issues, it is best practice to create a separate namespace for your installation and avoid using the default Kubernetes namespace. This is not mandatory, but the installation command below follows this recommendation.
{% endhint %}

{% tabs %}
{% tab title="Dedicated Namespace" %}
To install the Helm Chart using a dedicated namespace (e.g., `gravitee-apim`), run the following command:

{% code overflow="wrap" %}
```sh
helm install graviteeio-apim4x graviteeio/apim --create-namespace --namespace gravitee-apim
```
{% endcode %}
{% endtab %}

{% tab title="Default Namespace" %}
To install the Helm Chart using the default namespace (not recommended), run the following command:

```sh
helm install graviteeio-apim4x graviteeio/apim
```
{% endtab %}
{% endtabs %}

{% hint style="info" %}
**Installation tips**

Specify each parameter using `helm install` and the `--set key=value[,key=value]`.

Alternatively, provide a YAML file that specifies the values for the parameters when installing the chart. For example:

```sh
helm install my-release -f values.yaml gravitee
```

By default, APIM uses the values in the `values.yml` config file during installation. These can be modified via the parameters in the [configuration](configure-helm-chart.md) tables.
{% endhint %}

3. **(Optional)** Alternatively, you can package this chart directory into a chart archive:

```sh
helm package .
```

To install the chart using the chart archive, run:

```sh
helm install apim-4.0.0.tgz
```

## Configure installation

Refer to our [Helm chart reference page](configure-helm-chart.md) to learn how to customize your installation.

## Deployment management

After using Helm to install APIM on Kubernetes, you can manage the deployment by continuing to use Helm, or by installing Gravitee's Kubernetes Operator (GKO).

### Conceptual overview

Helm is a package manager for Kubernetes that simplifies the deployment and management of applications on Kubernetes clusters. Helm packages are called charts, which are collections of YAML templates that describe the different Kubernetes resources needed to run an application (e.g., deployments, services, ConfigMaps, etc).

If you used Helm to install APIM on Kubernetes, you can continue to use it to manage the APIM installation. Helm allows you to install, upgrade, rollback, and delete applications with just a few commands. However, complex services and applications benefit from the advanced automation and management capabilities of a Kubernetes operator.

A Kubernetes operator is a [pattern](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/) for building custom [controllers](https://kubernetes.io/docs/concepts/architecture/controller/). By linking controllers to one or more custom resources, cluster behavior can be extended without modifying the Kubernetes code base. Operators are designed to perform actions based on a low-level understanding of the applications they manage. They can automatically detect and respond to changes in an application or infrastructure and execute tasks that would be difficult to orchestrate manually.

### Choose your deployment manager

<table data-view="cards"><thead><tr><th></th><th></th><th data-hidden></th><th data-hidden data-type="content-ref"></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Helm</strong></td><td></td><td></td><td><a href="configure-helm-chart.md">configure-helm-chart.md</a></td><td><a href="configure-helm-chart.md">configure-helm-chart.md</a></td></tr><tr><td><strong>Gravitee Kubernetes Operator</strong></td><td></td><td></td><td><a href="install-gravitee-kubernetes-operator.md">install-gravitee-kubernetes-operator.md</a></td><td><a href="install-gravitee-kubernetes-operator.md">install-gravitee-kubernetes-operator.md</a></td></tr><tr><td><strong>Hybrid Deployment on Kubernetes</strong></td><td></td><td></td><td></td><td></td></tr></tbody></table>
