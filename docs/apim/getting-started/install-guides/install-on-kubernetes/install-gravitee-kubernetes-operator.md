# Gravitee Kubernetes Operator

A [Kubernetes operator](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/) is a method of packaging, deploying, and managing a Kubernetes application. A Kubernetes application is both deployed on Kubernetes and managed using the Kubernetes API and `kubectl` tooling.

In this context, a Kubernetes operator is an application-specific controller that extends the functionality of the Kubernetes API to create, configure, and manage application instances.

## Overview

When it comes to Gravitee deployment, there are two main components that can be deployed, as follows:

1. The APIs and applications around those APIs.
2. The actual API Gateway and the Management Console itself.

An increasing number of Gravitee users have already been implementing an Infrastructure-as-code (IAC) practice using Gravitee.

To support IAC-based use cases, Gravitee should enable users to handle Gravitee platform deployment “as code” by performing all the deployment types of actions below without ever having to use an UI:

* Push/deploy APIs to the API Gateway.
* Test the APIs.
* Promote the APIs across different environments - Test, UAT, Dev, Prod, and so on.

Up until now, Gravitee customers have been deploying APIs using the following two main approaches:

1. **Using the Gravitee management UI.** Gravitee comes with an easy-to-use, self-serve UI that is often used for development. This is backed by a backend service that is a part of the Gravitee web application.
2. **Using the Gravitee management API.** Every action in the Gravitee management UI de facto represents a REST API with a JSON payload. This is all documented using an API spec. As a result, everything users can do in the UI can be done via REST API calls backed by JSON files. A lot of users would use tools and systems like GitLab, Jenkins, Bitbucket, or GitHub Actions, for example, to manage everything as JSON files. An API definition in Gravitee is also a JSON file that explains what the endpoints are, what the protections are, and so on.

While the REST API method is compatible with an IAC approach, there has been feedback from many Gravitee users who are going "Kubernetes-native" that they would prefer to be able to deploy APIs and the Gravitee APIM Gateway and Console via \* [Custom Resource Definitions (CRDs)](https://docs.gravitee.io/apim/3.x/apim\_kubernetes\_operator\_definitions.html).

The Gravitee Kubernetes Operator (GKO) makes all this possible.

## How it works

If you deploy APIs in a Kubernetes cluster, you can describe your API as an API extension of Kubernetes using CRDs. This approach removes the need to deploy by relying on the management UI or the management API - when you deploy natively to your K8s cluster, there is an operator there that can deploy the API to your API gateway without relying on a UI or REST API. This is powered by the Kubernetes API and the Gravitee Kubernetes Operator.

## Architecture overview

The current functionality of the Gravitee Kubernetes Operator (GKO) allows for three main deployment scenarios, as described below.

{% hint style="info" %}
To learn how to deploy GKO on a remote cluster, see the [Remote cluster deployment](https://docs.gravitee.io/apim/3.x/apim\_kubernetes\_operator\_installation\_cluster.html) section.
{% endhint %}

### Standard deployment

In the standard deployment scenario, the management API and the API gateway are deployed in the same Kubernetes cluster.

With this workflow, the GKO listens for [Custom Resource Definitions (CRDs)](https://docs.gravitee.io/apim/3.x/apim\_kubernetes\_operator\_definitions.html). For each custom resource, an API is pushed to the management API using the import endpoint. The API gateway deploys the APIs accordingly.

The following diagram illustrates the standard deployment architectural approach:

<figure><img src="https://docs.gravitee.io/images/apim/3.x/kubernetes/gko-architecture-1-standard.png" alt=""><figcaption><p>Standard deployment architecture</p></figcaption></figure>

### Deployment on multiple clusters

In this scenario, the assumption is that both of the following requirements should be met:

1. The user manages multiple Kubernetes clusters with a different set of APIs for each cluster.
2. All APIs are managed using a single API Console.

To make this work with GKO, it should be installed on all the required clusters.

The following diagram illustrates the multi-cluster deployment architectural approach:

<figure><img src="https://docs.gravitee.io/images/apim/3.x/kubernetes/gko-architecture-2-multi-cluster.png" alt=""><figcaption><p>Multi-cluster deployment architecture</p></figcaption></figure>

### Deployment on multiple environments

In this scenario, a single GKO is deployed that can publish APIs to different environments (logical or physical). This is managed directly from the [API Definition](https://docs.gravitee.io/apim/3.x/apim\_kubernetes\_operator\_user\_guide\_api\_definition.html) custom resource, which refers a [Management Context](https://docs.gravitee.io/apim/3.x/apim\_kubernetes\_operator\_user\_guide\_management\_context.html) custom resource.

{% hint style="info" %}
Note that in this case different APIs are published on each of the environments. This is because APIs use the `ManagementContext` CRD, which can reference any Management API, however an `ApiDefinition` CRD can only have one Management Context.
{% endhint %}

The following diagram illustrates the multi-environment deployment architectural approach:

<figure><img src="https://docs.gravitee.io/images/apim/3.x/kubernetes/gko-architecture-3-multi-env.png" alt=""><figcaption><p>Multi-environment deployment architecture</p></figcaption></figure>

## Installation

This section provides steps on how to install  the GKO on an existing Kubernetes cluster.

{% hint style="info" %}
If your architecture requires the management of multiple Kubernetes clusters with a different set of APIs for each cluster, you should deploy the GKO separately on each cluster. Follow the deployment process described below for each cluster deployment.
{% endhint %}

### Prerequisites

Before you start, you need to have the following software set up and running on your machine:

1. [Kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)
2. [Helm v3](https://helm.sh/docs/intro/install/)
3. APIM up and running on your cluster. If you have not installed APIM yet, follow our [installation guide.](./)
4. For the gateway to be able to synchronize with the operator resources, the value of the `gateway.services.sync.kubernetes.enabled` property must be set to `true` in APIM configuration.

{% hint style="info" %}
**Namespaces**

By default the Kubernetes synchronizer is configured to look for API definitions in the API Gateway namespace. To watch all namespaces you must set the property `gateway.services.sync.kubernetes.namespaces` to `all` in the gateway configuration. You can also provide a specific list of namespaces to watch. This requires that the Gateway service account has the `list` permissions for ConfigMaps at the cluster level or on the list of namespaces defined in the `gateway.services.sync.kubernetes.namespaces` property.
{% endhint %}

### Install using Helm

1. If you haven't already, add the Gravitee Helm charts repo using the command below:

```sh
helm repo add graviteeio https://helm.gravitee.io
```

2. To install the chart with the release name `graviteeio-gko`:

```sh
helm install graviteeio-gko graviteeio/gko
```

3. **(Optional)** By default, the operator will listen to resources created in the whole cluster. If you want to restrict the operator to a specific namespace, you must set the `manager.scope.cluster` value to `false`. This way, the operator will be exclusively listening to resources created in the release namespace.

{% code overflow="wrap" %}
```sh
helm install --set manager.scope.cluster=false -n ${RELEASE_NAMESPACE} graviteeio-gko graviteeio/gko
```
{% endcode %}

{% hint style="info" %}
**Cluster scope**

If you are installing the operator with the cluster scope enabled (which is the default), it is recommended to install one instance of the operator per cluster. If you are installing the operator with the cluster scope disabled, you can install multiple instances of the operator in the same cluster, each one watching a different namespace.
{% endhint %}

## Next steps

Learn how to use GKO to define, deploy, and publish APIs to your API Portal and API Gateway and to manage Custom Resource Definitions (CRDs) in our [GKO guide](../../../guides/gravitee-kubernetes-operator/).
