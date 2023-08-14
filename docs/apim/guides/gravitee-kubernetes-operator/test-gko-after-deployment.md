# Test GKO After Deployment

## Overview

This section describes how to try out the Gravitee Kubernetes Operator (GKO) functionality after deployment by creating CRDs and testing your API via an API call from the API Gateway.

The process involves the following stages:

1. Create a Management Context custom resource.
2. Create an API Definition custom resource - this creates a new API on the cluster.
3. Test the new API by calling it through the APIM Gateway.

## Prerequisites

Before you start:

1. Ensure that the GKO has been successfully [deployed](../../getting-started/install-guides/install-on-kubernetes/install-gravitee-kubernetes-operator.md) on your Kubernetes cluster.
2. Ensure that the `services.sync.kubernetes` property is enabled (set to `true`) in the [`gravitee.yml`](https://github.com/gravitee-io/gravitee-api-management/blob/master/gravitee-apim-gateway/gravitee-apim-gateway-standalone/gravitee-apim-gateway-standalone-distribution/src/main/resources/config/gravitee.yml#L264) file. This setting is disabled by default. This step is required for the Gateway to be enabled to work with a Kubernetes Operator. The configuration depends on how the Gateway is deployed:
   * If your Gateway is deployed via a helm chart, you can enable the Kubernetes Operator option [through helm values.](../../getting-started/install-guides/install-on-kubernetes/configure-helm-chart.md#gravitee-gateway)
   *   For [other deployment strategies](../../getting-started/install-and-upgrade/install-guides/) (for example, deployment via a VM), you can update the configuration directly in the `gravitee.yml` file or by using an environment variable: `GRAVITEE_SERVICES_SYNC_KUBERNETES_ENABLED=true`.

       The `gravitee.yml` file value is listed below:

```
# Enable Kubernetes Synchronization
# This sync service requires to install Gravitee Kubernetes Operator
#    kubernetes:
#      enabled: false
```

See the [Configure APIM Gateway](../../getting-started/configuration/components/the-gravitee-api-gateway.md) section for more information on using environment variables in Gateway configurations.

## Testing the GKO functionality

### Create a `ManagementContext` custom resource

The first step is to create a [`ManagementContext` custom resource](custom-resource-definitions/managementcontext-resource.md) for your APIM instance.

To do so, you need a YAML file with the correct Management Context configuration. You can use the following sample YAML file from Gravitee directly, or as a template to base your configuration on:

\{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/config/samples/context/k3d/management-context-with-credentials.yml" %\}

In your copy, modify the `spec:` section by providing the actual URL of your APIM instance and the user credentials that match the relevant user configuration.

To create the Management Context resource using the Gravitee sample file directly, just run the following command:

{% code overflow="wrap" %}
```sh
kubectl apply -f https://raw.githubusercontent.com/gravitee-io/gravitee-kubernetes-operator/master/config/samples/context/k3d/management-context-with-credentials.yml
```
{% endcode %}

Alternatively, to create the Management Context resource using a modified configuration, run the following command (using the relevant filename):

```sh
kubectl apply -f your_management_context_credentials_config.yaml
```

If the operation is successful, you should see the following line in the command-line output:

```sh
managementcontext.gravitee.io/dev-mgmt-ctx created
```

The Management Context resource has now been created.

### Create an `ApiDefinition` custom resource

The next step is to create an [`ApiDefinition` custom resource.](custom-resource-definitions/apidefinition-crd.md)

To do so, you need a YAML file with the desired API Definition configuration. You can use the following sample YAML file from Gravitee directly, or as a template to base your configuration on:

\{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/config/samples/apim/api-with-context.yml" %\}

To create the API Definition resource using the Gravitee sample file directly, just run the following command:

{% code overflow="wrap" %}
```sh
kubectl apply -f https://raw.githubusercontent.com/gravitee-io/gravitee-kubernetes-operator/master/config/samples/apim/api-with-context.yml
```
{% endcode %}

Alternatively, to create the API Definition resource using a modified configuration, run the following command (using the relevant filename):

```sh
kubectl apply -f your_api_definition_config.yml
```

If the operation is successful, you should see the following line in the command-line output:

```sh
apidefinition.gravitee.io/basic-api-example created
```

The API Definition resource has now been created and a new API has been added in your Console. You can check it out in your Console URL:

`http://<YOUR_CONSOLE_URL>/console/#!/environments/default/`

If you are using a local cluster created through the local cluster installation process, the Console URL would likely be as follows:

`http://localhost:9000/console/#!/environments/default/`

The new API will be listed in the "Number of APIs" section of the Console dashboard:

<figure><img src="../../.gitbook/assets/Screenshot 2023-07-06 at 9.19.26 PM.png" alt=""><figcaption><p>APIM Console dashboard</p></figcaption></figure>

### Call the API through the APIM Gateway

To test the API, you can call it through the APIM Gateway by running the following command using your APIM Gateway URL:

```sh
curl -i http://<YOUR_GATEWAY_URL>/gateway/k8s-basic-with-ctx
```

The entrypoint used in the Gateway URL may differ depending on your deployment. If you are using a local cluster created through the local cluster installation process, the Gateway URL would likely be as shown in the following command:

```sh
curl -i http://localhost:9000/gateway/k8s-basic-with-ctx
```
