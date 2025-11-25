---
description: Guide to testing GKO After Deployment.
---

# Test GKO After Deployment

## Overview

This section describes how to test Gravitee Kubernetes Operator (GKO) functionality after deployment. The process involves the following:

1. Create a `ManagementContext` CRD
2. Create an `ApiDefinition` CRD, which creates a new API on the cluster
3. Test the new API by calling it through the APIM Gateway

## Prerequisites

* Ensure that the GKO has been successfully [deployed](../../getting-started/install-and-upgrade-guides/installing-a-self-hosted-gravitee-api-management-platform/install-on-kubernetes/architecture-overview.md) on your Kubernetes cluster.
* Ensure that `services.sync.kubernetes` is set to `true`. This property is disabled by default, but must be enabled for the Gateway to communicate with a Kubernetes Operator. How the Gateway is deployed determines how the property is configured:
  * If your Gateway is deployed using a Helm Chart, you can enable the Kubernetes Operator option [through Helm values](../../getting-started/install-and-upgrade-guides/installing-a-self-hosted-gravitee-api-management-platform/install-on-kubernetes/apim-helm-install-and-configuration.md#gravitee-gateway).
  * For [other deployment strategies](../../getting-started/install-and-upgrade-guides/) (e.g., deployment using a VM), you can update the configuration:
    * By setting an environment variable: `GRAVITEE_SERVICES_SYNC_KUBERNETES_ENABLED=true`
    *   Directly in the [`gravitee.yml`](https://github.com/gravitee-io/gravitee-api-management/blob/master/gravitee-apim-gateway/gravitee-apim-gateway-standalone/gravitee-apim-gateway-standalone-distribution/src/main/resources/config/gravitee.yml#L264) file:

        \{% code title="gravitee.yml" %\}

        ```yaml
        # Enable Kubernetes Synchronization
        # This sync service requires to install Gravitee Kubernetes Operator
        #    kubernetes:
        #      enabled: false
        ```

        \{% endcode %\}

{% hint style="info" %}
See [Configure APIM Gateway](../../getting-started/configuration/apim-gateway/) for more information on using environment variables in Gateway configurations.
{% endhint %}

## 1. Create a `ManagementContext` CRD

To create a [`ManagementContext` ](custom-resource-definitions/managementcontext.md)CRD for your APIM instance, you need a YAML file with the correct Management Context configuration. The following sample Gravitee YAML file can be used directly or as a template:

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/examples/management_context/cluster/management-context-with-credentials.yml" %}

To create the Management Context resource using the Gravitee sample file directly, modify the `spec:` section by providing the actual URL of your APIM instance and the user credentials that match the user configuration. Next, run the following command:

{% code overflow="wrap" %}
```sh
kubectl apply -f https://raw.githubusercontent.com/gravitee-io/gravitee-kubernetes-operator/master/config/samples/context/k3d/management-context-with-credentials.yml
```
{% endcode %}

Alternatively, to create the Management Context resource using a modified configuration, run the following command (using the appropriate filename):

```sh
kubectl apply -f your_management_context_credentials_config.yaml
```

If the operation is successful, this line will appear in the CLI output:

```sh
managementcontext.gravitee.io/dev-mgmt-ctx created
```

{% hint style="success" %}
The Management Context resource has been created.
{% endhint %}

## 2. Create an `ApiDefinition` custom resource

To create an [`ApiDefinition` ](custom-resource-definitions/apidefinition.md)CRD requires a YAML file with the correct API Definition configuration. The following sample Gravitee YAML file can be used directly or as a template:

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/examples/apim/api_definition/api-with-context.yml" %}

To create the API Definition resource using the Gravitee sample file directly, run the following command:

{% code overflow="wrap" %}
```sh
kubectl apply -f https://raw.githubusercontent.com/gravitee-io/gravitee-kubernetes-operator/master/config/samples/apim/api-with-context.yml
```
{% endcode %}

Alternatively, to create the API Definition resource using a modified configuration, run the following command (using the appropriate filename):

```sh
kubectl apply -f your_api_definition_config.yml
```

If the operation is successful, this line will appear in the CLI output:

```sh
apidefinition.gravitee.io/basic-api-example created
```

{% hint style="success" %}
The API Definition resource has now been created and a new API has been added to your Console.
{% endhint %}

You can view the new API at your Console URL:

`http://<CONSOLE_URL>/console/#!/environments/default/`

The Console URL below is typical for a local cluster created via the local cluster installation process:

`http://localhost:9000/console/#!/environments/default/`

The new API will be listed in the **Number of APIs** section of the Console dashboard:

<figure><img src="../../.gitbook/assets/Screenshot 2023-07-06 at 9.19.26 PM.png" alt=""><figcaption><p>APIM Console dashboard</p></figcaption></figure>

## 3. Call the API through the APIM Gateway

To test the API, you can call it through the APIM Gateway with the following command (after updating the placeholder to use your APIM Gateway URL):

```sh
curl -i http://<YOUR_GATEWAY_URL>/gateway/k8s-basic-with-ctx
```

If you are using a local cluster created through the local cluster installation process, the Gateway URL is likely `http://localhost:9000/gateway/k8s-basic-with-ctx`. However, the entrypoint used for the Gateway URL may differ depending on your deployment.
