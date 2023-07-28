---
description: An overview of Helm charts and Kubernetes operators
---

# Install on Kubernetes

To make the most of this guide, you should be familiar with Kubernetes and its terms.

Installing Gravitee API Management (APIM) on Kubernetes is easy with the help of our Helm chart. **This Helm chart supports Gravitee APIM Management (APIM) versions: 3.0.x and higher** and will deploy the following:

* APIM Management API
* APIM Management Console
* APIM Developer Portal
* APIM Gateway
* MongoDB replica set or PostgresSQL (optional dependency)
* Elasticsearch Cluster (optional dependency)

## Installation prerequisites

The following command line tools must be installed before proceeding with installation:

1. [Kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)
2. [Helm v3](https://helm.sh/docs/intro/install/)

## Installation Steps

1. Add the Gravitee Helm charts repo using the command below:

```sh
helm repo add graviteeio https://helm.gravitee.io
```

2. Now, install the chart from the Helm repo by specifying the desired release. For example, you could use `graviteeio-apim4x` as in the example below.

{% hint style="warning" %}
**Dedicated namespace**

To prevent potential issues in the future, it is best practice to create a separate namespace for your installation in order to prevent the use of the default Kubernetes namespace. The installation command provided immediately below assumes that such best practice is followed; however, this is not a mandatory requirement.
{% endhint %}

{% tabs %}
{% tab title="Dedicated Namespace" %}
To install the Helm Chart using a dedicated namespace (we use `gravitee-apim` as an example), run the following command:

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
**Install tips**

Specify each parameter using the `--set key=value[,key=value]` argument to `helm install`.

Alternatively, a YAML file that specifies the values for the parameters can be provided while installing the chart. For example,

```sh
helm install my-release -f values.yaml gravitee
```

When you install APIM, it automatically uses the default values from the `values.yml` config file which can be modified using the parameters in the tables in the [configuration](./#configuration) section.
{% endhint %}

3. **(Optional)** Alternatively, you can also package this chart directory into a chart archive by running:

```sh
helm package .
```

Now, to install the chart using the chart archive, run:

```sh
helm install apim-4.0.0.tgz
```

## Configure installation

Head over to our comprehensive [Helm chart reference page](configure-helm-chart.md) to learn how to customize your installation.

## Deployment management

After using Helm to install APIM on Kubernetes, you can manage the deployment by continuing to use Helm or by installing Gravitee's Kubernetes Operator (GKO).

### Conceptual overview

Helm is a package manager for Kubernetes that simplifies the deployment and management of applications on Kubernetes clusters. Helm packages are called "charts," which are collections of YAML templates that describe the different Kubernetes resources needed to run an application, such as deployments, services, and config maps.

You just used Helm to install APIM on Kubernetes and you can continue to use it to manage the APIM installation. Helm allows you to install, upgrade, rollback, and delete applications with just a few commands. However, Helm is more limited than a Kubernetes operator when it comes to advanced automation and management capabilities for complex applications or services.

Kubernetes operators allow you to automate advanced application management tasks. In Kubernetes, an operator is not an API object itself, but rather a pattern for building custom controllers that automate the management of complex, stateful applications on Kubernetes. Kubernetes' [operator pattern](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/) concept lets you extend the cluster's behavior without modifying the code of Kubernetes itself by linking [controllers](https://kubernetes.io/docs/concepts/architecture/controller/) to one or more custom resources.

Operators are designed to understand the application they manage and can take actions based on that understanding which allows for a higher level of automation and intelligence when managing complex applications. They can automatically detect and respond to changes in the application or infrastructure and can handle intricate management tasks that would be difficult to do manually.

### Choose your deployment manager

<table data-view="cards"><thead><tr><th></th><th></th><th data-hidden></th><th data-hidden data-type="content-ref"></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Helm</strong></td><td></td><td></td><td><a href="configure-helm-chart.md">configure-helm-chart.md</a></td><td><a href="configure-helm-chart.md">configure-helm-chart.md</a></td></tr><tr><td><strong>Gravitee Kubernetes Operator</strong></td><td></td><td></td><td><a href="install-gravitee-kubernetes-operator.md">install-gravitee-kubernetes-operator.md</a></td><td><a href="install-gravitee-kubernetes-operator.md">install-gravitee-kubernetes-operator.md</a></td></tr><tr><td><strong>Hybrid Deployment on Kubernetes</strong></td><td></td><td></td><td></td><td></td></tr></tbody></table>
