---
description: An overview about Quick Start.
---

# Quick Start

## Overview

This quick start guide is the fastest way to start working with the Gravitee Kubernetes Operator (GKO).

## Deploy the GKO

For full details on deployment, see the [GKO Install Guide](../../getting-started/install-and-upgrade-guides/install-on-kubernetes/architecture-overview.md).

### Prerequisites

Before deploying the GKO, you should have:

* A running APIM-ready cluster
* User access to the cluster you want to deploy to
* Defined the target cluster as your current/active Kubernetes context

### Deploy the GKO on your cluster

The GKO deployment process is the same for both remote and local Kubernetes clusters.

To deploy the GKO on the cluster of your current Kubernetes context, run the following commands:

{% code overflow="wrap" %}
```sh
helm repo add graviteeio https://helm.gravitee.io
helm install graviteeio-gko graviteeio/gko
```
{% endcode %}

## Testing the deployed GKO

After GKO deployment, you can test GKO functionality by creating CRDs and sending API calls from the API Gateway.

{% hint style="info" %}
To ensure that the Gateway works with the GKO, enable (set to `true`) the `services.sync.kubernetes` property in the [`gravitee.yml`](https://github.com/gravitee-io/gravitee-api-management/blob/master/gravitee-apim-gateway/gravitee-apim-gateway-standalone/gravitee-apim-gateway-standalone-distribution/src/main/resources/config/gravitee.yml#L264) file. For more information, see [Test GKO After Deployment](test-gko-after-deployment.md).
{% endhint %}

The process involves the following stages:

1. Create a `ManagementContext` custom resource.
2. Create an `ApiDefinition` custom resource. This creates a new API on the cluster.
3. Test the new API by calling it through the APIM Gateway.

### Create a `ManagementContext` custom resource

The [`ManagementContext` custom resource](custom-resource-definitions/managementcontext-resource.md) represents the configuration for a Management API.

To create a `ManagementContext` custom resource requires a YAML file with the correct Management Context configuration. The following sample Gravitee YAML file can be used directly or as a template:

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/config/samples/context/k3d/management-context-with-credentials.yml" %}

To create the `ManagementContext` resource using the Gravitee sample file, run the following command:

{% code overflow="wrap" %}
```sh
kubectl apply -f https://raw.githubusercontent.com/gravitee-io/gravitee-kubernetes-operator/master/config/samples/context/k3d/management-context-with-credentials.yml
```
{% endcode %}

{% hint style="info" %}
For full details on creating a `ManagementContext` custom resource, see [Create a ManagementContext custom resource](test-gko-after-deployment.md#create-a-management-context-custom-resource).
{% endhint %}

### Create an `ApiDefinition` custom resource

The [`ApiDefinition` custom resource](custom-resource-definitions/apidefinition-crd.md) represents the configuration for a single proxied API and its versions. It is similar to a YAML representation of an API definition in JSON format.

To create an `ApiDefinition` custom resource requires a YAML file with the desired API Definition configuration. The following sample Gravitee YAML file can be used directly or as a template:

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/config/samples/apim/api-with-context.yml" %}

To create the `ApiDefinition` resource using the Gravitee sample file, run the following command:

{% code overflow="wrap" %}
```sh
kubectl apply -f https://raw.githubusercontent.com/gravitee-io/gravitee-kubernetes-operator/master/config/samples/apim/api-with-context.yml
```
{% endcode %}

{% hint style="info" %}
For full details on creating an `ApiDefinition` custom resource, see [Create an `ApiDefinition` custom resource](test-gko-after-deployment.md#create-an-apidefinition-custom-resource).
{% endhint %}

### Test the new API by calling it through the APIM Gateway

To test the API, you can call it through the APIM Gateway by running the following command using your APIM Gateway URL:

```sh
curl -i http://localhost:9000/gateway/k8s-basic-with-ctx
```

The entrypoint used in the Gateway URL may differ depending on your deployment. The example above shows the typical Gateway URL generated when using a local cluster created through the local cluster installation process.

{% hint style="info" %}
For full details on trying out the GKO functionality after deployment, see [Call the API through the APIM Gateway](test-gko-after-deployment.md#step-3-call-the-api-through-the-apim-gateway).
{% endhint %}

## Next steps

Visit our [GKO guide](README.md) to:

* Learn how to use the GKO to define, deploy, and publish APIs to your API Portal and API Gateway
* Manage custom resource definitions (CRDs)
