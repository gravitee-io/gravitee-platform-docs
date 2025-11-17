---
description: Connect GKO to your APIM installation
---

# ManagementContext

## Overview

The `ManagementContext` custom resource is used to provide GKO with a way to phone home to Gravitee API Management via its management API. GKO uses the ManagementContext's parameters and credentials to communicate with a specific organization and environment in APIM. GKO can then use this connection in a number of ways, such as:

* To push API definitions managed by GKO to APIM for display in the API management console
* To push API definitions managed by GKO to APIM to be deployed on API Gateways that are configured to load their APIs from APIM's central database
* To push API definitions managed by GKO to be published on the Gravitee Developer Portal
* To push Applications managed by GKO to APIM

You can have any number of `ManagementContext` resources each pointing to different Gravitee API Management organizations and environments.

ManagementContexts are referenced by name from `ApiV4Definitions`, `ApiDefinitions`, and `Applications`. This is how GKO knows with which APIM environment each of these resources should be synchronized.

The key parts of an management context are:

* **baseURL:** this is the APIM management API's location
* **environmentId**: the ID of the target environment
* **organizationId**: the ID of the target organization
* **auth**: the credentials GKO should use to authentication with the APIM management API

## Management context authentication

In order for GKO to connect to your APIM control plane, it will need to authenticate itself against the APIM management API.

A Management Context custom resource can authenticate to your Management API instance in a few different ways: &#x20;

* using a service account token (recommended)
* using a user token
* basic authentication with a user's personal credentials (username & password)

Head to [this guide](../../guides/define-an-apim-service-account-for-gko.md) to learn how to create a dedicated service account and token for GKO.

{% hint style="info" %}
If both credentials and a bearer token are defined in your custom resource, the bearer token will take precedence.
{% endhint %}

Authentication credentials may either be added inline in the Management Context CRD or referenced from a Kubernetes Secret.

## Create a Management Context

The custom resource created in the example below refers to a Management API instance exposed at `https://gravitee-api.acme.com`. It targets the `dev` environment of the `acme` organization using the `admin` account and basic authentication credentials defined in a Kubernetes Secret. To achieve this:

Create a Secret to store the credentials:

```sh
kubectl create secret generic management-context-credentials \
  --from-literal=username=admin \
  --from-literal=password=admin \
  --namespace gravitee
```

Define a Management Context custom resource referencing the Secret:

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

If no namespace has been specified for the Secret reference, the Management Context resource namespace will be used to resolve the Secret.

{% hint style="info" %}
To target another environment on the same API instance, add and configure another Management Context resource.
{% endhint %}

Although Kubernetes Secrets should be the preferred way to store credentials, you can also add credentials inline in the Management Context custom resource definition:

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

The example below uses a `bearerToken` to authenticate the requests. Note that the token must have been generated for the account beforehand, as described [here](../../guides/define-an-apim-service-account-for-gko.md):

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

Alternatively, here is how to use a Kubernetes secret to store the token:

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

## Reference a Management Context from an API or Application

`ApiV4Definition`, `ApiDefinition`, and `Application` CRDs use the same syntax to reference a ManagementContext, which is to include a contextRef attribute at the root of the spec:

```yaml
spec:
  contextRef:
    name: dev-ctx
    namespace: gravitee
```

Below is a complete example of an ApiV4Definition that references a ManagementContext called `dev-ctx`.

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

Alternatively, you can configure the [Helm Chart](../../getting-started/installation/README.md) to use a cluster role.
{% endhint %}

For more information:

* The `ManagementContext` CRD code is available on [GitHub](https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/api/v1alpha1/managementcontext\_types.go).
* The `ManagementContext` CRD API reference is documented [here](../../reference/api-reference.md).
