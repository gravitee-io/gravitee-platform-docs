# GKO Quick Start Guide

## Overview

The main purpose of the Gravitee Kubernetes Operator (GKO) is to define, deploy, and publish APIs on your API Portal, Gateway, and Console with Custom Resource Definitions (CRDs).

To enable that, you should deploy the GKO on a Kubernetes cluster.

You can deploy the GKO on an existing, APIM-ready cluster. That cluster could be remote (cloud-based), or local (only recommended for testing purposes).

As described in the next section, there are additional steps to perform in case you do not have a suitable existing cluster and you need to [set up a new local cluster](apim-kubernetes-operator-installation-local.md) prior to deployment.

After a successful GKO deployment, you can try out the GKO functionality by creating CRDs and testing your API by calling it from the API Gateway. This process is documented [here](apim-kubernetes-operator-user-guide-play.md).

The GKO only works with APIM version 3.19.0 (and above).

## Deploying the GKO on your cluster

For full details, see the [GKO deployment guide](apim-kubernetes-operator-installation-cluster.md) section.

### STEP 1: Prepare your cluster

As a prerequisite, you should have an APIM-ready cluster up and running before you deploy the GKO. You should have user access to the cluster you want to deploy to, and it should be the one defined as your current/active Kubernetes context.

If you need to set up a local cluster first, follow the steps in the [local cluster installation](apim-kubernetes-operator-installation-local.md) section, and then proceed to the [GKO deployment steps](apim-kubernetes-operator-installation-cluster.md).

### STEP 2: Deploy the GKO on your cluster

The GKO deployment process is simple and is the same for both remote and local Kubernetes clusters.

To deploy the GKO on the cluster of your current Kubernetes context, run the following command in your command-line tool (the working directory does not matter):

```
kubectl apply -f https://github.com/gravitee-io/gravitee-kubernetes-operator/releases/latest/download/bundle.yml
```

As an optional but recommended next step, you should check if the Gravitee CRDs are available on your cluster. To do so, run the following command:

```
kubectl get crd
```

## Trying out the deployed GKO

After GKO deployment, it is time to try out the GKO functionality by creating CRDs and testing your API via and API call from the API Gateway.

Before you start, ensure that the `services.sync.kubernetes` property is enabled (set to `true`) in the [`gravitee.yml`](https://github.com/gravitee-io/gravitee-api-management/blob/master/gravitee-apim-gateway/gravitee-apim-gateway-standalone/gravitee-apim-gateway-standalone-distribution/src/main/resources/config/gravitee.yml#L264) file. For more information, see [How to try out the GKO after deployment](apim-kubernetes-operator-user-guide-play.md#prerequisites).

The process involves the following stages:

1. Create a Management Context custom resource.
2. Create an API Definition custom resource - this creates a new API on the cluster.
3. Test the new API by calling it through the APIM Gateway.

For full details, see [How to try out the GKO after deployment](apim-kubernetes-operator-user-guide-play.md).

### STEP 1: Create a Management Context custom resource

The `ManagementContext` custom resource represents the configuration for a Management API.

Read more about the Management Context custom resource [here](apim-kubernetes-operator-definitions.md) and [here](apim-kubernetes-operator-user-guide-management-context.md).

To create a Management Context custom resource, you need a YAML file with the correct Management Context configuration. You can use the following sample YAML file from Gravitee directly, or as a template to base your configuration on:

[https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/config/samples/context/k3d/managementcontext\_credentials.yaml](https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/config/samples/context/k3d/managementcontext\_credentials.yaml)

To create the Management Context resource using the ready Gravitee sample file, run the following command:

```
kubectl apply -f https://raw.githubusercontent.com/gravitee-io/gravitee-kubernetes-operator/master/config/samples/context/k3d/managementcontext_credentials.yaml
```

For full details on creating a Management Context custom resource, see [STEP 1: Create a Management Context custom resource](apim-kubernetes-operator-user-guide-play.md#step-1-create-a-management-context-custom-resource) in the User Guide section.

### STEP 2: Create an API Definition custom resource

The APIDefinition custom resource represents the configuration for a single proxied API and its versions. It is similar to a YAML representation of an API Definition in JSON format.

Read more about the API Definition custom resource [here](apim-kubernetes-operator-definitions.md) and [here](apim-kubernetes-operator-user-guide-api-definition.md).

To create an API Definition custom resource, you need a YAML file with the desired API Definition configuration. You can use the following sample YAML file from Gravitee directly, or as a template to base your configuration on:

[https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/config/samples/apim/api-with-context.yml](https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/config/samples/apim/api-with-context.yml)

To create the API Definition resource using the ready Gravitee sample file, run the following command:

```
kubectl apply -f https://raw.githubusercontent.com/gravitee-io/gravitee-kubernetes-operator/master/config/samples/apim/api-with-context.yml
```

For full details on creating an API Definition custom resource, see [STEP 2: Create an API Definition custom resource](apim-kubernetes-operator-user-guide-play.md#step-2-create-an-api-definition-custom-resource) in the User Guide section.

### STEP 3: Test the new API by calling it through the APIM Gateway

For the Gateway to work with the GKO, ensure that the `services.sync.kubernetes` property is enabled (set to `true`) in the [`gravitee.yml`](https://github.com/gravitee-io/gravitee-api-management/blob/master/gravitee-apim-gateway/gravitee-apim-gateway-standalone/gravitee-apim-gateway-standalone-distribution/src/main/resources/config/gravitee.yml#L264) file. For more information, see the prerequisites section in [How to try out the GKO after deployment](apim-kubernetes-operator-user-guide-play.md#prerequisites).

To test the API, you can call it through the APIM Gateway by running the following command using your APIM Gateway URL:

```
curl -i http://localhost:9000/gateway/k8s-basic-with-ctx
```

The entrypoint used in the Gateway URL may differ depending on your deployment. The example above shows the typical Gateway URL generated when using a local cluster created through the [local cluster installation](apim-kubernetes-operator-installation-local.md) process.

For full details on trying out the GKO functionality after deployment, see [STEP 3: Call the API through the APIM Gateway](apim-kubernetes-operator-user-guide-play.md#step-3-call-the-api-through-the-apim-gateway) in the User Guide section.
