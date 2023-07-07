# Custom Resource Definitions

## Overview

The Gravitee Kubernetes Operator comes with different Custom Resource Definitions (CRDs) - `ManagementContext`, `ApiDefinition`, `Application` and `ApiResource`.

## `ManagementContext`

The `ManagementContext` custom resource represents the configuration for a Management API.

Resources:

* The `ManagementContext` CRD code is available on [GitHub](https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/api/v1alpha1/managementcontext\_types.go).
* The `ManagementContext` CRD API reference is documented [here](../../reference/gravitee-kubernetes-operator-api-reference.md).
* You can learn how to use the `ManagementContext` CRD in [this section](custom-resource-definitions/managementcontext-resource.md).

The `ManagementContext` refers to a remote Management API. You can have as many `ManagementContext` resources as you want; however, you need to reference the relevant `ManagementContext` from the API Definition to indicate to the GKO where the API should be published.

### Examples

A basic example of an `ManagementContext` resource is shown below:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ManagementContext
metadata:
  name: dev-mgmt-ctx
spec:
  baseUrl: http://localhost:8083
  environmentId: DEFAULT
  organizationId: DEFAULT
  auth:
    credentials:
      username: admin
      password: admin
```

The next example shows the same resource but with a Personal Token:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ManagementContext
metadata:
  name: dev-mgmt-ctx
spec:
  baseUrl: http://localhost:8083
  environmentId: DEFAULT
  organizationId: DEFAULT
  auth:
    bearerToken: xxxx-yyyy-zzzz
```

You can then refer to the `ManagementContext` from the API, as shown in the example below:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiDefinition
metadata:
  name: basic-api-example
spec:
  name: "K8s Basic Example"
  contextRef:
    name: "dev-mgmt-ctx"
    namespace: "default"
  version: "1.1"
  description: "Basic api managed by Gravitee Kubernetes Operator"
  proxy:
    virtual_hosts:
      - path: "/k8s-basic"
    groups:
      - endpoints:
          - name: "Default"
            target: "https://api.gravitee.io/echo"
```

## `ApiDefinition`

The `APIDefinition` custom resource represents the configuration for a single proxied API and its versions. It is similar to a YAML representation of an API Definition in JSON format.

Resources:

* The `ApiDefinition` CRD code is available on [GitHub](https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/api/v1alpha1/apidefinition\_types.go).
* The `ApiDefinition` CRD API reference is documented [here](../../reference/gravitee-kubernetes-operator-api-reference.md).
* You can learn how to use the `ApiDefinition` resource in [this section](custom-resource-definitions/apidefinition-crd.md).

### Workflow

The following workflow is applied when a new `ApiDefinition` resource is added to the cluster:

1. The GKO listens for `ApiDefinition` resources.
2. The GKO performs some required changes, such as automatically computing IDs or CrossIDs (for APIs or Plans).
3. The GKO converts the definition to JSON format.
4. The GKO compares the definition to the existing definition. If something has changed, the GKO pushes the definition to the Management API (if a `ManagementContext` is provided).
5. The GKO deploys the API to the API Gateway.

### Examples

A basic example of an `ApiDefinition` resource is shown below:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiDefinition
metadata:
  name: basic-api-example
spec:
  name: "K8s Basic Example"
  version: "1.0"
  description: "Basic api managed by Gravitee Kubernetes Operator"
  proxy:
    virtual_hosts:
      - path: "/k8s-basic"
    groups:
      - endpoints:
          - name: "Default"
            target: "https://api.gravitee.io/echo"
```

The same API with support for plans is shown in the example below:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiDefinition
metadata:
  name: apikey-example
spec:
  name: "K8s OAuth2 Example"
  version: "1.0"
  description: "Api managed by Gravitee Kubernetes Operator with OAuth2 plan"
  resources:
    - name: "am-demo"
      type: oauth2-am-resource
      configuration:
        version: V3_X
        serverURL: "https://am-nightly-gateway.cloud.gravitee.io"
        securityDomain: "test-jh"
        clientId: "localjh"
        clientSecret: "localjh"
  plans:
    - name: "OAuth2"
      description: "Oauth2 plan"
      security: OAUTH2
      securityDefinition: '{"oauthResource":"am-demo"}'
  proxy:
    virtual_hosts:
      - path: "/k8s-oauth2"
    groups:
      - name: default-group
        endpoints:
          - name: "Default"
            target: "https://api.gravitee.io/echo"
```

## `ApiResource`

The `ApiResource` custom resource allows you to use the GKO to create reusable [API resources](https://docs.gravitee.io/apim/3.x/apim\_resources\_overview.html) by applying the `ApiResource` custom resource definition. This enables you to define resources such as cache or authentication providers once only and maintain them in a single place, and then reuse them in multiple APIs - any further updates to such a resource will be automatically propagated to all APIs containing a reference to that resource.

{% hint style="info" %}
Read more about the`ApiResource`[here.](custom-resource-definitions/apiresource-crd.md)
{% endhint %}

### Examples

Here is an example of an `ApiResource` cache resource:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiResource
metadata:
  name: reusable-resource-cache
  namespace: default
spec:
  name: "cache-resource"
  type: "cache"
  enabled: true
  configuration:
      timeToIdleSeconds: 0
      timeToLiveSeconds: 0
      maxEntriesLocalHeap: 1000
```

This reusable resource can then be later referenced in any `ApiDefinition` resource using a reference to its namespaced name in the `resources` field:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiDefinition
metadata:
  name: resource-ref-example
  namespace: default
spec:
  name: "Resource reference example"
  version: "1.0"
  description: "An API with a reference to a reusable resource"
  resources:
    - ref:
        name: reusable-resource-cache
        namespace: default
  proxy:
    virtual_hosts:
      - path: "/resource-ref-sample"
    groups:
      - endpoints:
          - name: "Default"
            target: "https://api.gravitee.io/echo"
```

## `Application`

The `Application` custom resource represents the configuration for an Application. It is similar to a YAML representation of an Application in JSON format.

Resources:

* The `Appication` CRD code is available on [GitHub](https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/api/v1alpha1/application\_types.go).
* The `Application` CRD API reference is documented [here](../../reference/gravitee-kubernetes-operator-api-reference.md).
* You can learn how to use the `Application` resource in [this section.](custom-resource-definitions/application-crd.md)

### Workflow

The following workflow is applied when a new `Application` resource is added to the cluster:

1. The GKO listens for `Application` resources.
2. The GKO resolves any references to external sources such as configmaps or secrets.
3. The GKO performs some required changes, such as adding default settings.
4. The GKO converts the data to JSON format.
5. If something has changed, the GKO pushes the definition to the Management API.

### Examples

A basic example of an `Application` resource is shown below:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: Application
metadata:
  name: basic-application
  namespace: default
spec:
  contextRef:
    name: "dev-ctx"
    namespace: "default"
  name: "K8S-Application"
  type: "WEB"
  domain: "https://example.com"
  description: "K8s Application"
```

The same Application with support for application metadata is shown in the example below:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: Application
metadata:
  name: basic-application
  namespace: default
spec:
  contextRef:
    name: "dev-ctx"
    namespace: "default"
  name: "K8S-Application"
  type: "WEB"
  domain: "https://example.com"
  description: "K8s Application"
  applicationMetaData:
    - name: "test metadata"
      format: "STRING"
    - name: "test metadata 2"
      format: "STRING"
```

## CRD dependencies - resource deletion

Since an `ApiDefinition` can rely on a `ManagementContext`, resource deletion is restricted until a check is performed first whether there is an API associated with the respective `ManagementContext`. This is achieved through the use of [Finalizers](https://kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/).

## CRD samples

Check out some sample CRDs in the [GKO GitHub repository](https://github.com/gravitee-io/gravitee-kubernetes-operator/tree/config/samples/apim).
