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

### Create a Management Context custom resource

The `ManagementContext` custom resource represents the configuration for a Management API.

|   | Read more about the Management Context custom resource [here](https://docs.gravitee.io/apim/3.x/apim\_kubernetes\_operator\_definitions.html) and [here](https://docs.gravitee.io/apim/3.x/apim\_kubernetes\_operator\_user\_guide\_management\_context.html). |
| - | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

To create a Management Context custom resource, you need a YAML file with the correct Management Context configuration. You can use the following sample YAML file from Gravitee directly, or as a template to base your configuration on:

[https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/config/samples/context/k3d/management-context-with-credentials.yml](https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/config/samples/context/k3d/management-context-with-credentials.yml)

To create the Management Context resource using the ready Gravitee sample file, run the following command:

```
kubectl apply -f https://raw.githubusercontent.com/gravitee-io/gravitee-kubernetes-operator/master/config/samples/context/k3d/management-context-with-credentials.yml
```

For full details on creating a Management Context custom resource, see [STEP 1: Create a Management Context custom resource](https://docs.gravitee.io/apim/3.x/apim\_kubernetes\_operator\_user\_guide\_play.html#step\_1\_create\_a\_management\_context\_custom\_resource) in the User Guide section.

### Create an API Definition custom resource

The APIDefinition custom resource represents the configuration for a single proxied API and its versions. It is similar to a YAML representation of an API Definition in JSON format.

|   | Read more about the API Definition custom resource [here](https://docs.gravitee.io/apim/3.x/apim\_kubernetes\_operator\_definitions.html) and [here](https://docs.gravitee.io/apim/3.x/apim\_kubernetes\_operator\_user\_guide\_api\_definition.html). |
| - | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |

To create an API Definition custom resource, you need a YAML file with the desired API Definition configuration. You can use the following sample YAML file from Gravitee directly, or as a template to base your configuration on:

[https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/config/samples/apim/api-with-context.yml](https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/config/samples/apim/api-with-context.yml)

To create the API Definition resource using the ready Gravitee sample file, run the following command:

```
kubectl apply -f https://raw.githubusercontent.com/gravitee-io/gravitee-kubernetes-operator/master/config/samples/apim/api-with-context.yml
```

For full details on creating an API Definition custom resource, see [STEP 2: Create an API Definition custom resource](https://docs.gravitee.io/apim/3.x/apim\_kubernetes\_operator\_user\_guide\_play.html#step\_2\_create\_an\_api\_definition\_custom\_resource) in the User Guide section.

### Test the new API by calling it through the APIM Gateway

|   | For the Gateway to work with the GKO, ensure that the `services.sync.kubernetes` property is enabled (set to `true`) in the [`gravitee.yml`](https://github.com/gravitee-io/gravitee-api-management/blob/master/gravitee-apim-gateway/gravitee-apim-gateway-standalone/gravitee-apim-gateway-standalone-distribution/src/main/resources/config/gravitee.yml#L264) file. For more information, see the prerequisites section in [How to try out the GKO after deployment](https://docs.gravitee.io/apim/3.x/apim\_kubernetes\_operator\_user\_guide\_play.html#prerequisites). |
| - | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

To test the API, you can call it through the APIM Gateway by running the following command using your APIM Gateway URL:

```
curl -i http://localhost:9000/gateway/k8s-basic-with-ctx
```

|   | The entrypoint used in the Gateway URL may differ depending on your deployment. The example above shows the typical Gateway URL generated when using a local cluster created through the [local cluster installation](https://docs.gravitee.io/apim/3.x/apim\_kubernetes\_operator\_installation\_local.html) process. |
| - | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

For full details on trying out the GKO functionality after deployment, see [STEP 3: Call the API through the APIM Gateway](https://docs.gravitee.io/apim/3.x/apim\_kubernetes\_operator\_user\_guide\_play.html#step\_3\_call\_the\_api\_through\_the\_apim\_gateway) in the User Guide section.

\
