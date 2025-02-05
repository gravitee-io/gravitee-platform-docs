# Store APIs in local ConfigMaps

Gravitee Kubernetes Operator (GKO) allows API definitions and deployment events to reach the Gateway via Kubernetes ConfigMaps that are local to the cluster on which the Gateway is running. As a prerequisite, the Gateway must be [configured to load APIs from local ConfigMaps](configure-the-gateway-to-load-apis-from-local-configmaps.md).

Using this approach has certain benefits:

* It removes or reduces the need for Gateways to load configurations from remote repositories. Instead, Gateways load their configuration locally.
* It removes the need to use a `ManagementContext`, and also enables the [DB-less mode](../../guides/db-less-mode.md).

However, there are disadvantages:

* These APIs will only be deployed to Gateways on the local cluster. They cannot, for instance, be deployed to distributed Gateways on different platforms via sharding tags.
* Unless you're running in [DB-less mode](../../guides/db-less-mode.md), the Gateway will still need to connect to a central repository to manage other aspects of the API lifecycle, such as subscription management.

## `ApiV4Definition` example

The following configuration deploys an `ApiDefinition` on a Gateway using a local ConfigMap:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiV4Definition
metadata:
  name: local-api-example
  namespace: gravitee
spec:
  name: GKO Basic
  version: 1.1
  description: Basic api managed by Gravitee Kubernetes Operator
  definitionContext:
    origin: KUBERNETES
    syncFrom: KUBERNETES
  proxy:
    virtual_hosts:
      - path: /k8s-basic
    groups:
      - endpoints:
          - name: Default
            target: https://api.gravitee.io/echo
```

The `definitionContext.syncFrom` attribute is set to `KUBERNETES` (the default value) to indicate that the API will be deployed only in the cluster where the custom resource is applied, and stored in a local ConfigMap.

Run the following command to verify that the API ConfigMap has been created in the cluster:

```sh
kubectl get configmaps -n gravitee
```

```
NAMESPACE            NAME                DATA    AGE
gravitee             local-api-example   1       1m
```

## `ApiDefinition` example

The following configuration deploys an `ApiDefinition` on a Gateway using a local ConfigMap:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiDefinition
metadata:
  name: local-api-example
  namespace: gravitee
spec:
  name: GKO Basic
  version: 1.1
  description: Basic api managed by Gravitee Kubernetes Operator
  proxy:
    virtual_hosts:
      - path: /k8s-basic
    groups:
      - endpoints:
          - name: Default
            target: https://api.gravitee.io/echo
  local: true
```

The `local` field is optional. By default, it is set to `true` to indicate that the API will be deployed only in the cluster where the custom resource is applied.

Run the following command to verify that the API ConfigMap has been created in the cluster:

```sh
kubectl get configmaps -n gravitee
```

```
NAMESPACE            NAME                DATA    AGE
gravitee             local-api-example   1       1m
```
