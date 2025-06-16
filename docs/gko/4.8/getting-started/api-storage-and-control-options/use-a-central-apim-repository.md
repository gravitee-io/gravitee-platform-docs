# Use a central APIM repository

The Gravitee platform can use the APIM repository (e.g., MongoDB database) to configure both GKO and the Gateway. In this setup, GKO sends APIs and deployment events (start/stop) to the repository, and the API Gateway loads APIs and deployment events from the repository.

A central control plane like this enables flexible architectures. For example, multiple data planes can run Gateways on different Kubernetes clusters, cloud platforms, or virtual machines, with all of them loading their configurations from this central repository.

To achieve this requires that:

* An APIM instance acts as the source of truth for the Gateways.
* The operator synchronizes the API definitions that it manages with APIM, rather than creating local API definitions in ConfigMaps. This is achieved by setting the `local` flag of the API definition to `false` (default is `true`).
* The API definition and application CRDs reference a management context that points to the APIM instance.

An example of the architecture enabled by these settings is illustrated by the diagram below.

<figure><img src="../../.gitbook/assets/image (3).png" alt=""><figcaption><p>One operator, multiple clusters/regions</p></figcaption></figure>

Below are some detailed examples that illustrate what API definition resources should look like to support this deployment style.

## ApiV4Definition example

For `ApiV4Definitions`, the required settings are shown in the snippet below:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiV4Definition
metadata:
  name: api-v4-with-context-sync-management
spec:
  name: api-v4-with-context-sync-management
  description: Updated V4 API managed by Gravitee Kubernetes Operator
  version: 1.0
  contextRef:
    name: dev-ctx
    namespace: gravitee
  definitionContext:
    origin: KUBERNETES
    syncFrom: MANAGEMENT
  # [...]
```

The `contextRef` attribute points to a `ManagementContext` so that GKO knows with which APIM instance to synchronize.

The `definitionContext.syncFrom` attribute is set to `MANAGEMENT` (default is `KUBERNETES`), which tells GKO that this API will be entirely synced with the central APIM repository (both for API configuration as well as deployment events), and that the API should not be stored in a local ConfigMap.

## ApiDefinition example

For `ApiDefinitions`, the required settings are shown in the snippet below:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiDefinition
metadata:
  name: multi-cluster-api
spec:
  contextRef:
    name: dev-ctx
    namespace: gravitee
  local: false
  # [...]
```

Like with `ApiV4Definitions`, the `contextRef` attribute points to a `ManagementContext` so that GKO knows with which APIM instance to synchronize.

However, the `ApiDefinition` syntax for telling GKO whether or not to store APIs and deployment events in local ConfigMaps uses a boolean attribute called `local`. When set to `false` (default is `true`), it tells GKO not to use local ConfigMaps, and to instead sync this API entirely with the APIM instance referenced from the `ManagementContext`.
