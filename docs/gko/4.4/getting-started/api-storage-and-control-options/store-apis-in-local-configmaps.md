# Store APIs in local configMaps

Gravitee Kubernetes Operator (GKO) provides the option to provide API definitions and deployment events to the Gateway through Kubernetes ConfigMaps that are local to the cluster on which the Gateway is running.

As a pre-requisite, this requires the gateway to be [configured to load APIs from local ConfigMaps](configure-the-gateway-to-load-apis-from-local-configmaps.md).

Using this approach has certain benefits:

* it removes or reduces the need for Gateways to load configuration from remote repositories. Instead, Gateways load their configuration locally.&#x20;
* it removes the need to use a ManagementContext, and also enables the [DB-less mode](../../guides/db-less-mode.md)

On the downside however:

* these APIs will only be deployed to Gateways on the local cluster. They cannot for instance be deployed to distributed gateways on different platforms by means of sharding tags.
* Unless you're running in [DB-less mode](../../guides/db-less-mode.md), the Gateway will still need to connect to a central repository to manage other aspects of the API lifecycle, such a subscription management.

## `ApiV4Definition` example

To deploy an `ApiDefinition` on a Gateway using a local configMap, apply the following configuration on the ApiDefinition:

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

The **definitionContext.syncFrom** attribute is set to `KUBERNETES` (which is the default value) to indicate that the API will be deployed only in the cluster where the custom resource is applied, and stored in a local ConfigMap.&#x20;

Run the following command to verify that the API ConfigMap has been created in the  cluster:

```sh
kubectl get configmaps -n gravitee
```

```
NAMESPACE            NAME                DATA    AGE
gravitee             local-api-example   1       1m
```

## `ApiDefinition` example

To deploy an `ApiDefinition` on a Gateway using a local configMap, apply the following configuration on the ApiDefinition:

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

The `local` field is optional and is set to `true` by default to indicate that the API will be deployed only in the cluster where the custom resource is applied.&#x20;

Run the following command to verify that the API ConfigMap has been created in the  cluster:

```sh
kubectl get configmaps -n gravitee
```

```
NAMESPACE            NAME                DATA    AGE
gravitee             local-api-example   1       1m
```
