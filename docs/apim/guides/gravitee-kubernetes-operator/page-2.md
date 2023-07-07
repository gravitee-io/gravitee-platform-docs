# Quick Start

## Overview

This quick start guide is the fastest way to get up and running with the Gravitee Kubernetes Operator (GKO). You can deploy the GKO on an existing, APIM-ready cluster. That cluster could be remote (cloud-based), or local (only recommended for testing purposes).

{% hint style="warning" %}
There are [additional steps to perform](../developer-contributions/gravitee-kubernetes-operator-development-environment.md) in case you do not have a suitable existing cluster, and you need to set up a new local cluster prior to deployment.
{% endhint %}

## Deploy the GKO

For full details on deployment, see the [GKO Deployment Guide](../../getting-started/install-guides/install-on-kubernetes/install-gravitee-kubernetes-operator.md).

### Prepare your cluster

As a prerequisite, you should have an APIM-ready cluster up and running before you deploy the GKO. You should have user access to the cluster you want to deploy to, and it should be the one defined as your current/active Kubernetes context.

### Deploy the GKO on your cluster

The GKO deployment process is simple and is the same for both remote and local Kubernetes clusters.

To deploy the GKO on the cluster of your current Kubernetes context, run the following command in your command-line tool (the working directory is irrelevant):

{% code overflow="wrap" %}
```sh
kubectl apply -f https://github.com/gravitee-io/gravitee-kubernetes-operator/releases/latest/download/bundle.yml
```
{% endcode %}

As an optional but recommended next step, you should check if the Gravitee CRDs are available on your cluster. To do so, run the following command:

```sh
kubectl get crd
```

## Testing the deployed GKO

After GKO deployment, you can try out the GKO functionality by creating CRDs and testing your API via an API call from the API Gateway.

{% hint style="info" %}
Before you start, ensure that the `services.sync.kubernetes` property is enabled (set to `true`) in the [`gravitee.yml`](https://github.com/gravitee-io/gravitee-api-management/blob/master/gravitee-apim-gateway/gravitee-apim-gateway-standalone/gravitee-apim-gateway-standalone-distribution/src/main/resources/config/gravitee.yml#L264) file. For more information, see [How to try out the GKO after deployment](https://docs.gravitee.io/apim/3.x/apim\_kubernetes\_operator\_user\_guide\_play.html#prerequisites).
{% endhint %}

The process involves the following stages:

1. Create a Management Context custom resource.
2. Create an API Definition custom resource. This creates a new API on the cluster.
3. Test the new API by calling it through the APIM Gateway.

### Create a `ManagementContext` custom resource

The [`ManagementContext` custom resource](custom-resource-definitions/managementcontext-resource.md) represents the configuration for a Management API.

To create a `ManagementContext` custom resource, you need a YAML file with the correct Management Context configuration. You can use the following sample YAML file from Gravitee directly, or as a template to base your configuration on:

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/config/samples/context/k3d/management-context-with-credentials.yml" %}

To create the `ManagementContext` resource using the ready Gravitee sample file, run the following command:

{% code overflow="wrap" %}
```sh
kubectl apply -f https://raw.githubusercontent.com/gravitee-io/gravitee-kubernetes-operator/master/config/samples/context/k3d/management-context-with-credentials.yml
```
{% endcode %}

{% hint style="info" %}
For full details on creating a `ManagementContext` custom resource, see [Create a ManagementContext custom resource](test-gko-after-deployment.md#create-a-management-context-custom-resource).
{% endhint %}

### Create an `ApiDefinition` custom resource

The [`ApiDefinition` custom resource](custom-resource-definitions/apidefinition-crd.md) represents the configuration for a single proxied API and its versions. It is similar to a YAML representation of an API Definition in JSON format.

To create an `ApiDefinition` custom resource, you need a YAML file with the desired API Definition configuration. You can use the following sample YAML file from Gravitee directly, or as a template to base your configuration on:

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/config/samples/apim/api-with-context.yml" %}

To create the `ApiDefinition` resource using the ready Gravitee sample file, run the following command:

{% code overflow="wrap" %}
```sh
kubectl apply -f https://raw.githubusercontent.com/gravitee-io/gravitee-kubernetes-operator/master/config/samples/apim/api-with-context.yml
```
{% endcode %}

For full details on creating an `ApiDefinition` custom resource, see [Create an `ApiDefinition` custom resource](test-gko-after-deployment.md#create-an-apidefinition-custom-resource) in the User Guide section.

### Test the new API by calling it through the APIM Gateway

{% hint style="info" %}
For the Gateway to work with the GKO, ensure that the `services.sync.kubernetes` property is enabled (set to `true`) in the [`gravitee.yml`](https://github.com/gravitee-io/gravitee-api-management/blob/master/gravitee-apim-gateway/gravitee-apim-gateway-standalone/gravitee-apim-gateway-standalone-distribution/src/main/resources/config/gravitee.yml#L264) file. For more information, see the prerequisites section in [Test GKO After Deployment.](test-gko-after-deployment.md)
{% endhint %}

To test the API, you can call it through the APIM Gateway by running the following command using your APIM Gateway URL:

```sh
curl -i http://localhost:9000/gateway/k8s-basic-with-ctx
```

{% hint style="info" %}
The entrypoint used in the Gateway URL may differ depending on your deployment. The example above shows the typical Gateway URL generated when using a local cluster created through the local cluster installation process.
{% endhint %}

For full details on trying out the GKO functionality after deployment, see [Call the API through the APIM Gateway](test-gko-after-deployment.md#step-3-call-the-api-through-the-apim-gateway) in the User Guide section.
