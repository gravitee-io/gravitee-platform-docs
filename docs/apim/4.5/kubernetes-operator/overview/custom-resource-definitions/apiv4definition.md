---
description: Overview of ApiV4Definition.
---

# ApiV4Definition

The `ApiV4Definition` custom resource represents the configuration for a v4 API on the Gravitee gateway. V4 APIs are the latest version of the Gravitee API definition which supports both synchronous and asynchronous APIs. GKO also supports the previous [v2 API definition](apidefinition.md) with a dedicated CRD.

## Create an `ApiV4Definition`

The example below shows a simple `ApiV4Definition` custom resource definition:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiV4Definition
metadata:
  name: api-v4
  namespace: gravitee
spec:
  name: "api-v4"
  description: "API v4 managed by Gravitee Kubernetes Operator"
  version: "1.0"
  type: PROXY
  contextRef: 
    name: "management-context-1"
  definitionContext:
    origin: KUBERNETES
    syncFrom: MANAGEMENT
  listeners:
    - type: HTTP
      paths:
        - path: "/echo-v4"
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

## The `ApiV4Definition` lifecycle

The following workflow is applied when a new `ApiV4Definition` resource is added to the cluster:

1. The GKO listens for `ApiV4Definition` resources.
2. The GKO performs required changes, such as automatically computing IDs or CrossIDs (for APIs or plans).
3. The GKO converts the definition to JSON format.
4. The GKO compares the definition to the existing definition. If something has changed, the GKO pushes the definition to the Management API (if a `ManagementContext` resource is provided).
5. The GKO deploys the API to the API Gateway.

The `ApiV4Definition` resource has a `Processing Status` field that makes it possible to view the status of the resource in the cluster. The following `Processing Status` field values are possible:

<table><thead><tr><th width="143.5">Status</th><th>Description</th></tr></thead><tbody><tr><td>[None]</td><td>The API definition has been created but not yet processed.</td></tr><tr><td>Completed</td><td>The API definition has been created or updated successfully.</td></tr><tr><td>Reconciling</td><td>The operator has encountered a recoverable error. A retry will be performed every 5 seconds until the cluster retry limit is reached.</td></tr><tr><td>Failed</td><td>The operator has encountered an unrecoverable error. These are errors that require manual action to correct. No retry will be performed.</td></tr></tbody></table>

Events are added to the resource as part of each action performed by the operator.

For more information:

* The `ApiV4Definition` and `ApiDefinition` CRDs are available on [GitHub](https://github.com/gravitee-io/gravitee-kubernetes-operator/tree/master/helm/gko/crds).
* The `ApiV4Definition` and `ApiDefinition` CRD API references are documented [here](../../reference/api-reference.md).
