---
description: Overview of APIM.
---

# Use a central APIM repository

The Gravitee platform can be set up such that GKO and the Gateway use the APIM repository (e.g. MongoDB database) as the source of configuration to which GKO sends APIs and deployment events (start/stop), and from which the API Gateway loads APIs and deployment events.

Having a central control plane in this way allows for flexible architectures, such as having multiple data planes running Gateways on different Kubernetes clusters, cloud platforms, or virtual machines, all loading their configuration from this central repository.

The requirements to achieve this are that:

* An APIM instance is required to act as a source of truth for the Gateways
* The operator will synchronize API definitions that it manages with APIM, rather than creating local API definitions in ConfigMaps. This is achieved by setting the `local` flag of the API definition to `false` (default is `true`).
* The API definition and Application CRDs must reference a Management Context that points to the APIM instance

An example of the architecture enabled by these settings is illustrated by the diagram below.

<figure><img src="broken-reference" alt=""><figcaption><p>One operator, multiple clusters/regions</p></figcaption></figure>

Next are some detailed examples that illustrate what API definition resources should look like in order to support this deployment style.

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

The **contextRef** attribute is pointing to a ManagementContext so that GKO knows which APIM instance to synchronize with.

The **definitionContext.syncFrom** attribute is set to `MANAGEMENT` (default is `KUBERNETES`) which tells GKO that this API will be entirely synced with the central APIM repository (both for API configuration as well as deployment events), and that the API should not be stored in a local ConfigMap.

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

Like with `ApiV4Definitions`, the **contextRef** attribute is pointing to a ManagementContext so that GKO knows which APIM instance to synchronize with.

However the syntax for telling GKO whether or not to store APIs and deployment events in local ConfigMaps is different for `ApiDefinition`, which uses a boolean attribute called **local**. When set to `false` (default is `true`), it tells GKO not to use local ConfigMaps and instead to sync this API entirely with the APIM instance referenced from the ManagementContext.
