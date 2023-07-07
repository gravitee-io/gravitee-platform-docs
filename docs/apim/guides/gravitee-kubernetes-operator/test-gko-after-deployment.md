# Test GKO After Deployment

## Overview

This section describes how to try out the GKO functionality after deployment by creating CRDs and testing your API via and API call from the API Gateway.

The process involves the following stages:

1. Create a Management Context custom resource.
2. Create an API Definition custom resource - this creates a new API on the cluster.
3. Test the new API by calling it through the APIM Gateway.

## Prerequisites

Before you start:

1. Ensure that the GKO has been successfully [deployed](https://docs.gravitee.io/apim/3.x/apim\_kubernetes\_operator\_installation\_cluster.html) on your Kubernetes cluster.
2. Ensure that the `services.sync.kubernetes` property is enabled (set to `true`) in the [`gravitee.yml`](https://github.com/gravitee-io/gravitee-api-management/blob/master/gravitee-apim-gateway/gravitee-apim-gateway-standalone/gravitee-apim-gateway-standalone-distribution/src/main/resources/config/gravitee.yml#L264) file. This setting is disabled by default. This step is required for the Gateway to be enabled to work with a Kubernetes Operator. The configuration depends on how the Gateway is deployed:
   * If your Gateway is deployed via a helm chart, you can enable the kubernetes operator option [through helm values](https://docs.gravitee.io/apim/3.x/apim\_installguide\_kubernetes.html#gravitee\_gateway).
   *   For [other deployment strategies](https://docs.gravitee.io/apim/3.x/apim\_installguide.html) (for example, deployment via a VM), you can update the configuration directly in the `gravitee.yml` file or by using an environment variable: `GRAVITEE_SERVICES_SYNC_KUBERNETES_ENABLED=true`.

       The `gravitee.yml` file value is listed below:

       [https://github.com/gravitee-io/gravitee-api-management/blob/master/gravitee-apim-gateway/gravitee-apim-gateway-standalone/gravitee-apim-gateway-standalone-distribution/src/main/resources/config/gravitee.yml#L264](https://github.com/gravitee-io/gravitee-api-management/blob/master/gravitee-apim-gateway/gravitee-apim-gateway-standalone/gravitee-apim-gateway-standalone-distribution/src/main/resources/config/gravitee.yml#L264)

       ```
       # Enable Kubernetes Synchronization
       # This sync service requires to install Gravitee Kubernetes Operator
       #    kubernetes:
       #      enabled: false
       ```

       See the [Configure APIM Gateway](https://docs.gravitee.io/apim/3.x/apim\_installguide\_gateway\_configuration.html) section for more information on using environment variables in Gateway configurations.

## Testing the GKO functionality

### Create a `ManagementContext` custom resource

The first step is to create a `ManagementContext` custom resource for your APIM instance.

|   | Read more about the Management Context custom resource [here](https://docs.gravitee.io/apim/3.x/apim\_kubernetes\_operator\_definitions.html) and [here](https://docs.gravitee.io/apim/3.x/apim\_kubernetes\_operator\_user\_guide\_management\_context.html). |
| - | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

To do so, you need a YAML file with the correct Management Context configuration. You can use the following sample YAML file from Gravitee directly, or as a template to base your configuration on:

[https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/config/samples/context/k3d/management-context-with-credentials.yml](https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/config/samples/context/k3d/management-context-with-credentials.yml)

The content of this sample file is shown below:

```
apiVersion: gravitee.io/v1alpha1
kind: ManagementContext
metadata:
  name: dev-ctx
  namespace: default
spec:
  baseUrl: http://apim-apim3-api.default.svc:83
  environmentId: DEFAULT
  organizationId: DEFAULT
  auth:
    credentials:
      username: admin
      password: admin
```

In your copy, modify the `spec:` section by providing the actual URL of your APIM instance and the user credentials that match with the relevant user configuration.

To create the Management Context resource using the Gravitee sample file directly, just run the following command:

```
kubectl apply -f https://raw.githubusercontent.com/gravitee-io/gravitee-kubernetes-operator/master/config/samples/context/k3d/management-context-with-credentials.yml
```

Alternatively, to create the Management Context resource using a modified configuration, run the following command (using the relevant filename):

```
kubectl apply -f your_management_context_credentials_config.yaml
```

If the operation is successful, you should see the following line in the command-line output:

```
managementcontext.gravitee.io/dev-mgmt-ctx created
```

The Management Context resource has now been created.

#### Create an `ApiDefinition` custom resource

The next step is to create an `ApiDefinition` custom resource.

|   | Read more about the API Definition custom resource [here](https://docs.gravitee.io/apim/3.x/apim\_kubernetes\_operator\_definitions.html) and [here](https://docs.gravitee.io/apim/3.x/apim\_kubernetes\_operator\_user\_guide\_api\_definition.html). |
| - | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |

To do so, you need a YAML file with the desired API Definition configuration. You can use the following sample YAML file from Gravitee directly, or as a template to base your configuration on:

[https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/config/samples/apim/api-with-context.yml](https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/config/samples/apim/api-with-context.yml)

The content of this sample file is shown below:

```
apiVersion: gravitee.io/v1alpha1
kind: ApiDefinition
metadata:
  name: basic-api-example
  namespace: default
spec:
  name: "K8s Basic Example With Management Context"
  contextRef:
    name: "dev-mgmt-ctx"
    namespace: "default"
  version: "1.1"
  description: "Basic api managed by Gravitee Kubernetes Operator"
  proxy:
    virtual_hosts:
      - path: "/k8s-basic-with-ctx"
    groups:
      - endpoints:
          - name: "Default"
            target: "https://api.gravitee.io/echo"
```

To create the API Definition resource using the Gravitee sample file directly, just run the following command:

```
kubectl apply -f https://raw.githubusercontent.com/gravitee-io/gravitee-kubernetes-operator/master/config/samples/apim/api-with-context.yml
```

Alternatively, to create the API Definition resource using a modified configuration, run the following command (using the relevant filename):

```
kubectl apply -f your_api_definition_config.yml
```

If the operation is successful, you should see the following line in the command-line output:

```
apidefinition.gravitee.io/basic-api-example created
```

The API Definition resource has now been created and a new API has been added in your Console. You can check it out in your Console URL:

[http://\<YOUR\_CONSOLE\_URL>/console/#!/environments/default/](broken-reference)

If you are using a local cluster created through the [local cluster installation](https://docs.gravitee.io/apim/3.x/apim\_kubernetes\_operator\_installation\_local.html) process, the Console URL would likely be as follows:

[http://localhost:9000/console/#!/environments/default/](http://localhost:9000/console/#!/environments/default/)

The new API will be listed in the "Number of APIs" section of the Console dashboard:

![gko deployment cluster console](https://docs.gravitee.io/images/apim/3.x/kubernetes/gko-deployment-cluster-console.png)

### Call the API through the APIM Gateway

To test the API, you can call it through the APIM Gateway by running the following command using your APIM Gateway URL:

```
curl -i http://<YOUR_GATEWAY_URL>/gateway/k8s-basic-with-ctx
```

The entrypoint used in the Gateway URL may differ depending on your deployment. If you are using a local cluster created through the [local cluster installation](https://docs.gravitee.io/apim/3.x/apim\_kubernetes\_operator\_installation\_local.html) process, the Gateway URL would likely be as shown in the following command:

```
curl -i http://localhost:9000/gateway/k8s-basic-with-ctx
```

\
