# Custom Resource Definitions

## Overview

The Gravitee Kubernetes Operator provides several custom resource definitions (CRDs):

* [`ManagementContext`](README.md#managementcontext)
* [`ApiDefinition`](README.md#apidefinition)
* [`ApiResource`](README.md#apiresource)
* [`Application`](README.md#application)

## `ManagementContext`

The `ManagementContext` custom resource represents the configuration for a Management API. For more information:

* The `ManagementContext` CRD code is available on [GitHub](https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/api/v1alpha1/managementcontext_types.go).
* The `ManagementContext` CRD API reference is documented [here](../../../reference/gravitee-kubernetes-operator-api-reference.md).
* You can learn how to use the `ManagementContext` CRD in [this section](managementcontext.md).

The `ManagementContext` resource refers to a remote Management API. You can have any number of `ManagementContext` resources, but you need to reference the appropriate `ManagementContext` in the API definition to indicate to the GKO where the API should be published.

### Examples

A basic example of a `ManagementContext` resource is shown below:

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

The next example shows the same resource, but with a Personal Token:

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

You can then refer to the `ManagementContext` resource from the API:

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

The `APIDefinition` custom resource represents the configuration for a single proxied API and its versions. It is similar to a YAML representation of an API Definition in JSON format. For more information:

* The `ApiDefinition` CRD code is available on [GitHub](https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/api/v1alpha1/apidefinition\_types.go).
* The `ApiDefinition` CRD API reference is documented [here](../../../reference/gravitee-kubernetes-operator-api-reference.md).
* You can learn how to use the `ApiDefinition` resource in [this section](apidefinition.md).

### Workflow

The following workflow is applied when a new `ApiDefinition` resource is added to the cluster:

1. The GKO listens for `ApiDefinition` resources.
2. The GKO performs required changes, such as automatically computing IDs or CrossIDs (for APIs or plans).
3. The GKO converts the definition to JSON format.
4. The GKO compares the definition to the existing definition. If something has changed, the GKO pushes the definition to the Management API (if a `ManagementContext` resource is provided).
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

Here is the same API with support for plans:

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

You can use the GKO to create reusable [API resources](../../api-configuration/resources.md) by applying the `ApiResource` custom resource definition.

The `ApiResource` custom resource allows you to define resources (cache, authentication providers, etc.) a single time and maintain them in a single place, then reuse these resources in multiple APIs. Any additional updates to the resource will be automatically propagated to all APIs that reference that resource.

{% hint style="info" %}
Read more about the`ApiResource`[here.](apiresource.md)
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

This reusable resource can be subsequently referenced in any `ApiDefinition` resource via its namespace and name in the `resources` field:

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

The `Application` custom resource represents the configuration for an application. It is similar to a YAML representation of an application in JSON format. For more information:

* The `Application` CRD code is available on [GitHub](https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/api/v1alpha1/application_types.go).
* The `Application` CRD API reference is documented [here](../../../reference/gravitee-kubernetes-operator-api-reference.md).
* You can learn how to use the `Application` resource in [this section.](application.md)

### Workflow

The following workflow is applied when a new `Application` resource is added to the cluster:

1. The GKO listens for `Application` resources.
2. The GKO resolves any references to external sources such as ConfigMaps or Secrets.
3. The GKO performs required changes, such as adding default settings.
4. The GKO converts the data to JSON format.
5. The GKO compares the definition to the existing definition. If something has changed, the GKO pushes the definition to the Management API (if a `ManagementContext` resource is provided).

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

Here is the same `Application` resource with support for application metadata:

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

## Resource deletion

The potential dependency of an `ApiDefinition` resource on a `ManagementContext` resource places restrictions on resource deletion. First, a check must be performed to determine whether there is an API associated with the particular `ManagementContext` resource. This check is conducted via [Finalizers](https://kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/).

## CRD samples

Sample CRDs are available in the [GKO GitHub repository](https://github.com/gravitee-io/gravitee-kubernetes-operator/tree/alpha/config/crd/bases).
