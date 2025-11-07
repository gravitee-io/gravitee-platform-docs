# Quickstart Guide

## Overview

Following this quickstart guide is the fastest way to start working with the Gravitee Kubernetes Operator (GKO). The sections below describe how to:

* [Deploy the GKO](quick-start.md#deploy-the-gko)
* [Test the deployed GKO](quick-start.md#test-the-deployed-gko)

## Deploy the GKO

{% hint style="info" %}
For comprehensive deployment details, see the [GKO Install Guide](../../getting-started/install-and-upgrade-guides/installing-a-self-hosted-gravitee-api-management-platform/install-on-kubernetes/architecture-overview.md).
{% endhint %}

### Prerequisites

* A running APIM-ready cluster
* User access to the cluster you want to deploy to&#x20;
* Defined the target cluster as your current/active Kubernetes context

### Deploy the GKO on your cluster

The GKO deployment process is the same for both remote and local Kubernetes clusters. To deploy the GKO on the cluster of your current Kubernetes context:

{% code overflow="wrap" %}
```sh
helm repo add graviteeio https://helm.gravitee.io
helm install graviteeio-gko graviteeio/gko
```
{% endcode %}

## Test the deployed GKO

You can test the functionality of a deployed GKO by creating CRDs and sending API calls from the API Gateway:

1. Create a `ManagementContext` CRD
2. Create an `ApiDefinition` CRD to create a new API on the cluster
3. Test the new API by calling it through the APIM Gateway

{% hint style="info" %}
To ensure that the Gateway works with the GKO, set `services.sync.kubernetes=true` in the [`gravitee.yml`](https://github.com/gravitee-io/gravitee-api-management/blob/master/gravitee-apim-gateway/gravitee-apim-gateway-standalone/gravitee-apim-gateway-standalone-distribution/src/main/resources/config/gravitee.yml#L264) file. For more information, see [Test GKO After Deployment](test-gko-after-deployment.md).
{% endhint %}

### 1. Create a `ManagementContext` CRD

The [`ManagementContext` ](custom-resource-definitions/managementcontext.md)CRD represents the configuration for a Management API.

To create a `ManagementContext` CRD requires a YAML file with the correct Management Context configuration. The sample Gravitee YAML file below can be used directly or as a template:

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/examples/management_context/cluster/management-context-with-credentials.yml" %}

Create the `ManagementContext` resource using the Gravitee sample file:

```sh
kubectl apply -f https://raw.githubusercontent.com/gravitee-io/gravitee-kubernetes-operator/master/config/samples/context/k3d/management-context-with-credentials.yml
```

{% hint style="info" %}
See [Create a ManagementContext CRD](test-gko-after-deployment.md#create-a-management-context-custom-resource) for more details.
{% endhint %}

### 2. Create an `ApiDefinition` CRD

The [`ApiDefinition` ](custom-resource-definitions/apidefinition.md)CRD represents the configuration for a single proxied API and its versions. It is similar to a YAML representation of an API definition in JSON format.

To create an `ApiDefinition` CRD requires a YAML file with the correct API Definition configuration. The following sample Gravitee YAML file can be used directly or as a template:

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/examples/apim/api_definition/api-with-context.yml" %}

To create the `ApiDefinition` resource using the Gravitee sample file:

```sh
kubectl apply -f https://raw.githubusercontent.com/gravitee-io/gravitee-kubernetes-operator/master/config/samples/apim/api-with-context.yml
```

{% hint style="info" %}
See [Create an `ApiDefinition` CRD](#2-create-an-apidefinition-custom-resource) for more details.
{% endhint %}

### 3. Test the API by calling it through the APIM Gateway

To test the API, call it using your APIM Gateway URL:

```sh
curl -i http://localhost:9000/gateway/k8s-basic-with-ctx
```

The entrypoint used for the Gateway URL is deployment-dependent. The URL in the example above is typical for a local cluster created through the local cluster installation process.

{% hint style="info" %}
For more details on trying out the GKO functionality after deployment, see [Call the API through the APIM Gateway](#3-call-the-api-through-the-apim-gateway).
{% endhint %}

{% hint style="success" %}
Congratulations, the GKO is deployed! Visit our [GKO guide](./) to:

* Learn how to use the GKO to define, deploy, and publish APIs to your API Portal and API Gateway
* Manage CRDs
{% endhint %}
