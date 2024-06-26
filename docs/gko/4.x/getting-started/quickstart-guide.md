# Quickstart guide

## Overview

Following this quickstart guide is the fastest way to start working with the Gravitee Kubernetes Operator (GKO). The sections below describe how to:

* [Deploy GKO](quickstart-guide.md#deploy-the-gko)
* [Create a Management Context](quickstart-guide.md#create-a-managementcontext)
* [Create an API Definition](quickstart-guide.md#create-an-apidefinition)
* [Invoke the deployed API](quickstart-guide.md#invoke-the-deployed-api-through-the-apim-gateway)

### Prerequisites

* A Kubernetes cluster with Gravitee API Management installed.

## Deploy GKO

{% hint style="info" %}
For comprehensive deployment details, see the [GKO Install Guide](installation/).
{% endhint %}

The GKO deployment process is the same for both remote and local Kubernetes clusters. To deploy the GKO on the cluster of your current Kubernetes context:

{% code overflow="wrap" %}
```sh
$ helm repo add graviteeio https://helm.gravitee.io
$ helm install graviteeio-gko graviteeio/gko
```
{% endcode %}

## Create a ManagementContext

The [`ManagementContext` ](../overview/custom-resource-definitions/managementcontext.md)CRD represents the configuration for a Management API.

To create a `ManagementContext` CRD requires a YAML file with the correct Management Context configuration. The sample Gravitee YAML file below can be used directly or as a template:

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

{% hint style="info" %}
The above example is using the admin account's personal credentials to authenticate GKO to the APIM control plane. Head to the [management context CRD documentation](../overview/custom-resource-definitions/managementcontext.md) to learn about how to use a service account token instead, which is the recommended approach for production.
{% endhint %}

## Create an ApiDefinition

The [`ApiDefinition` ](../overview/custom-resource-definitions/apidefinition.md)CRD represents the configuration for a single proxied API and its versions. It is similar to a YAML representation of an API definition in JSON format.

To create an `ApiDefinition` CRD requires a YAML file with the correct API Definition configuration. The following sample Gravitee YAML file can be used directly or as a template:

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/examples/apim/api_definition/v2/api-with-context.yml" %}

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

{% hint style="info" %}
See [Create an `ApiDefinition` CRD](../overview/custom-resource-definitions/apidefinition.md) for more details.
{% endhint %}

You can view the new API at your Console URL:

`http://<CONSOLE_URL>/console/#!/environments/default/`

The Console URL below is typical for a local cluster created via the local cluster installation process:

`http://localhost:9000/console/#!/environments/default/`

The new API will be listed in the **Number of APIs** section of the Console dashboard:

<figure><img src="../.gitbook/assets/Screenshot 2023-07-06 at 9.19.26 PM.png" alt=""><figcaption><p>APIM Console dashboard</p></figcaption></figure>

## Invoke the deployed API through the APIM Gateway

To test the API, call it using your APIM Gateway URL:

```sh
curl -i http://localhost:9000/gateway/k8s-basic-with-ctx
```

The entrypoint used for the Gateway URL is deployment-dependent. The URL in the example above is typical for a local cluster created through the local cluster installation process.

{% hint style="success" %}
Congratulations, you did it!
{% endhint %}
