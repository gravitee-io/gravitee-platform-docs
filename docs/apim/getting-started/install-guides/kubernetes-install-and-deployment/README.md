---
description: An overview of Helm charts and Kubernetes operators
---

# Kubernetes Install & Deployment

To make the most of this guide, you should be familiar with Kubernetes and its terms.

Installing APIM on Kubernetes is easy with the help of our Helm chart. **This Helm chart supports versions: 3.0.x and higher** and will deploy the following:

* Gravitee management API
* Gravitee management UI
* Gravitee developer portal
* Gravitee gateway
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

2. Now, install the chart from the Helm repo by specifying the desired release. For example, you could use `graviteeio-apim3x` as in the example below.

{% hint style="warning" %}
**Dedicated namespace**

To prevent potential issues in the future, it is best practice to create a separate namespace for your installation in order to prevent the use of the default Kubernetes namespace. The installation command provided immediately below assumes that such best practice is followed; however, this is not a mandatory requirement.
{% endhint %}

{% tabs %}
{% tab title="Dedicated Namespace" %}
To install the Helm Chart using a dedicated namespace (we use `gravitee-apim` as an example), run the following command:

{% code overflow="wrap" %}
```sh
helm install graviteeio-apim3x graviteeio/apim3 --create-namespace --namespace gravitee-apim
```
{% endcode %}
{% endtab %}

{% tab title="Default Namespace" %}
To install the Helm Chart using the default namespace (not recommended), run the following command:

```sh
helm install graviteeio-apim3x graviteeio/apim3
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
helm install apim3-3.0.0.tgz
```

## Configure installation

Head over to our comprehensive [Helm chart reference page](helm-chart-deployment.md) to learn how to customize your installation.

## Deployment management

After using Helm to install APIM on Kubernetes, you can manage the deployment by continuing to use Helm or by installing Gravitee's Kubernetes Operator (GKO).

### Conceptual overview

Helm is a package manager for Kubernetes that simplifies the deployment and management of applications on Kubernetes clusters. Helm packages are called "charts," which are collections of YAML templates that describe the different Kubernetes resources needed to run an application, such as deployments, services, and config maps.&#x20;

You just used Helm to install APIM on Kubernetes and you can continue to use it to manage the APIM installation. Helm allows you to in install, upgrade, rollback, and delete applications with just a few commands. However, Helm more limited than a Kubernetes operator when it comes to advanced automation and management capabilities for complex applications or services.

Kubernetes operators allow you to automate advanced application management tasks. In Kubernetes, an operator is not an API object itself, but rather a pattern for building custom controllers that automate the management of complex, stateful applications on Kubernetes. Kubernetes' [operator pattern](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/) concept lets you extend the cluster's behavior without modifying the code of Kubernetes itself by linking [controllers](https://kubernetes.io/docs/concepts/architecture/controller/) to one or more custom resources.&#x20;

Operators are designed to understand the application they manage and can take actions based on that understanding. For example, an operator for a database might automatically scale the number of database instances based on the workload or perform backups and recovery operations automatically.

One key advantage of Kubernetes operators over Helm is that they provide a higher level of automation and intelligence for managing complex applications. They can automatically detect and respond to changes in the application or infrastructure, and can handle intricate management tasks that would be difficult to do manually.

### Choose your deployment manager

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th></th><th data-hidden></th><th data-hidden data-type="content-ref"></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><p></p><p><strong>Helm</strong> </p></td><td></td><td></td><td><a href="helm-chart-deployment.md">helm-chart-deployment.md</a></td><td><a href="helm-chart-deployment.md">helm-chart-deployment.md</a></td></tr><tr><td><p></p><p><strong>Gravitee Kubernetes Operator</strong></p></td><td></td><td></td><td><a href="kubernetes-operator-deployment.md">kubernetes-operator-deployment.md</a></td><td><a href="kubernetes-operator-deployment.md">kubernetes-operator-deployment.md</a></td></tr></tbody></table>

