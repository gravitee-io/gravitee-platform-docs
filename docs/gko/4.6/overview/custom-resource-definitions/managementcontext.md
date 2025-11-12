---
description: Connect GKO to your APIM installation
---

# ManagementContext

## Overview

The `ManagementContext` custom resource is used to provide Gravitee Kubernetes Operator (GKO) with a method to connect to Gravitee API Management (APIM) through the Management API. GKO uses the management context's parameters and credentials to communicate with a specific organization and environment in APIM. GKO then uses this connection to complete the following actions:

* Push API definitions managed by GKO to APIM for display in the API Management Console
* Push API definitions managed by GKO to APIM to be deployed on API Gateways or Gateway Bridge servers that are configured to load their APIs from APIM's central database
* Push API definitions managed by GKO to be published on the Gravitee Developer Portal
* Push Applications managed by GKO to APIM

You can have any number of `ManagementContext` resources, each pointing to different Gravitee API Management organizations and environments.

Management contexts are referenced by name from `ApiV4Definitions`, `ApiDefinitions`, and `Applications`. This is how GKO knows with which APIM environment each of these resources should be synchronized.

The key parts of a management context are:

* **baseURL:** The location of the APIM Management API
* **environmentId**: The ID of the target environment
* **organizationId**: The ID of the target organization
* **auth**: The credentials GKO should use to authenticate with the APIM Management API

## Management context authentication

For GKO to connect to your APIM control plane, it needs to authenticate itself against the APIM Management API.

A `ManagementContext` custom resource can authenticate to your Management API instance in a few different ways:

* Using a service account token (recommended)
* Using a user token
* Basic authentication with a user's personal credentials (username & password)
* Using a cloud token

Refer to [this guide](../../guides/define-an-apim-service-account-for-gko.md) to learn how to create a dedicated service account and token for GKO.

{% hint style="info" %}
If both credentials and a bearer token are defined in your custom resource, the bearer token will take precedence.
{% endhint %}

Authentication credentials may either be added inline in the `ManagementContext` CRD or referenced from a Kubernetes Secret.

## Create a `ManagementContext`

The custom resource created in the following example refers to a Management API instance exposed at `https://gravitee-api.acme.com`. It targets the `dev` environment of the `acme` organization, using the `admin` account and basic authentication credentials defined in a Kubernetes Secret. To create this custom resource, complete the following steps:

1.  Create a Secret to store the credentials:\


    ```sh
    kubectl create secret generic management-context-credentials \
      --from-literal=username=admin \
      --from-literal=password=admin \
      --namespace gravitee
    ```


2. Define a `ManagementContext` custom resource using either of the following methods:
   1.  Define a `ManagementContext` custom resource referencing the Secret:\


       ```yaml
       apiVersion: gravitee.io/v1alpha1
       kind: ManagementContext
       metadata:
         name: dev-ctx
         namespace: gravitee
       spec:
         baseUrl: https://gravitee-api.acme.com
         environmentId: dev
         organizationId: acme
         auth:
           secretRef:
             name: management-context-credentials
       ```


   2.  If you are using the cloud token for authentication, you must use the `cloud` property to define the `ManagementContext` custom resource referencing the Secret:\


       ```yaml
       apiVersion: gravitee.io/v1alpha1
       kind: ManagementContext
       metadata:
         name: dev-ctx
       spec:
         cloud:
           secretRef:
             name: apim-context-bearer-token
       ```

If no namespace has been specified for the Secret reference, the `ManagementContext` resource namespace is used to resolve the Secret.

{% hint style="info" %}
To target another environment on the same API instance, add and configure another `ManagementContext` resource.
{% endhint %}

### Storing credentials

Although Kubernetes Secrets are the preferred way to store credentials, you can also add credentials inline in the `ManagementContext` custom resource definition:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ManagementContext
metadata:
  name: dev-ctx
  namespace: gravitee
spec:
  baseUrl: https://gravitee-api.acme.com
  environmentId: dev
  organizationId: acme
  auth:
    credentials:
      username: admin
      password: admin
```

The example below uses a `bearerToken` to authenticate requests. Note that the token must have been generated for the account beforehand, as described [here](../../guides/define-an-apim-service-account-for-gko.md).

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ManagementContext
metadata:
  name: dev-ctx
  namespace: gravitee
spec:
  baseUrl: https://gravitee-api.acme.com
  environmentId: staging
  organizationId: acme
  auth:
    bearerToken: xxxx-yyyy-zzzz
```

Alternatively, here is how to use a Kubernetes Secret to store the token:

```sh
kubectl create secret generic management-context-credentials \
  --from-literal=bearerToken=xxxx-yyyy-zzzz \
  --namespace gravitee
```

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ManagementContext
metadata:
  name: dev-ctx
  namespace: gravitee
spec:
  baseUrl: https://gravitee-api.acme.com
  environmentId: staging
  organizationId: acme
  auth:
    secretRef:
      name: management-context-credentials
```

## Reference a `ManagementContext` from an API or Application

`ApiV4Definition`, `ApiDefinition`, and `Application` CRDs use the same syntax to reference a `ManagementContext`, which includes a `contextRef` attribute at the root of the spec:

```yaml
spec:
  contextRef:
    name: dev-ctx
    namespace: gravitee
```

Below is a complete example of an `ApiV4Definition` that references a `ManagementContext` called `dev-ctx`:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiV4Definition
metadata:
  name: api-v4-with-context
  namespace: gravitee
spec:
  name: "api-v4-with-context"
  description: "V4 API managed by Gravitee Kubernetes Operator"
  version: "1.0"
  contextRef:
    name: "dev-ctx"
    namespace: "default"
  type: PROXY
  state: STARTED
  definitionContext:
    origin: KUBERNETES
    syncFrom: MANAGEMENT
  listeners:
    - type: HTTP
      paths:
        - path: "/echo-v4-context"
      entrypoints:
        - type: http-proxy
          qos: AUTO
  endpointGroups:
    - name: Default HTTP proxy group
      type: http-proxy
      endpoints:
        - name: Default HTTP proxy
          type: http-proxy
          inheritConfiguration: false
          configuration:
            target: https://api.gravitee.io/echo
          secondary: false
  flowExecution:
    mode: DEFAULT
    matchRequired: false
  plans:
    KeyLess:
      name: "Free plan"
      description: "This plan does not require any authentication"
      security:
        type: "KEY_LESS"
```

{% hint style="warning" %}
By default, the service account created for the Gateway does not have a cluster role. Therefore, to sync a CRD with a Management API:

* Your definitions must sit in the same namespace (e.g., `apim-example`)
* The name of the context must match the reference in the API definition

Alternatively, you can configure the [Helm Chart](../../getting-started/installation/) to use a cluster role.
{% endhint %}

{% hint style="info" %}
**For more information**

* The `ManagementContext` CRD code is available on [GitHub](https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/api/v1alpha1/managementcontext_types.go).
* The `ManagementContext` CRD API reference is documented [here](../../reference/api-reference.md).
{% endhint %}
