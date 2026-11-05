---
description: Overview of ApiDefinition.
---

# ApiDefinition

The `ApiDefinition` custom resource represents the configuration for a v2 API on the Gravitee gateway. GKO also supports the more recent [v4 API definition](apiv4definition.md) with its own CRD.

## Create an `ApiDefinition`

The example below shows a simple `ApiDefinition` custom resource definition:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiDefinition
metadata:
  name: basic-api-example
  namespace: gravitee
spec:
  name: "GKO Basic"
  version: "1.1"
  description: "Basic api managed by Gravitee Kubernetes Operator"
  contextRef: 
    name: "management-context-1"
  local: false
  proxy:
    virtual_hosts:
      - path: "/k8s-basic"
    groups:
      - endpoints:
          - name: "Default"
            target: "https://api.gravitee.io/echo"
```

Here is the same API with the addition of an OAuth2 plan:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiDefinition
metadata:
  name: apikey-example
spec:
  name: "K8s OAuth2 Example"
  version: "1.0"
  description: "Api managed by Gravitee Kubernetes Operator with OAuth2 plan"
  contextRef: 
    name: "management-context-1"
  local: false
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

## The `ApiDefinition` lifecycle

The following workflow is applied when a new `ApiDefinition` resource is added to the cluster:

1. The GKO listens for `ApiDefinition` resources.
2. The GKO performs required changes, such as automatically computing IDs or CrossIDs (for APIs or plans).
3. The GKO converts the definition to JSON format.
4. The GKO compares the definition to the existing definition. If something has changed, the GKO pushes the definition to the Management API (if a `ManagementContext` resource is provided).
5. The GKO deploys the API to the API Gateway.

The `ApiDefinition` resource has a `Processing Status` field that makes it possible to view the status of the resource in the cluster. The following `Processing Status` field values are possible:

<table><thead><tr><th width="143.5">Status</th><th>Description</th></tr></thead><tbody><tr><td>[None]</td><td>The API definition has been created but not yet processed.</td></tr><tr><td>Completed</td><td>The API definition has been created or updated successfully.</td></tr><tr><td>Reconciling</td><td>The operator has encountered a recoverable error. A retry will be performed every 5 seconds until the cluster retry limit is reached.</td></tr><tr><td>Failed</td><td>The operator has encountered an unrecoverable error. These are errors that require manual action to correct. No retry will be performed.</td></tr></tbody></table>

Events are added to the resource as part of each action performed by the operator. To view these events, ensure that the CRD creation steps described above are completed, then run the following command:

```sh
kubectl describe -n gravitee apidefinitions.gravitee.io basic-api-example
```

Example output is shown below:

```bash
Name:         basic-api-example
Namespace:    gravitee
[...]
Events:
  Type    Reason          Age   From                      Message
  ----    ------          ----  ----                      -------
  Normal  AddedFinalizer  73s   apidefinition-controller  Added Finalizer for the API definition
  Normal  Creating        73s   apidefinition-controller  Creating API definition
  Normal  Created         72s   apidefinition-controller  Created API definition
```

## Deleting your API

The following executes a simple deletion of the API definition:

```sh
kubectl -n gravitee delete apidefinitions.gravitee.io basic-api-example
```

The potential dependency of an `ApiDefinition` resource on a `ManagementContext` resource places restrictions on resource deletion. First, a check must be performed to determine whether there is an API associated with the particular `ManagementContext` resource. This check is conducted via [Finalizers](https://kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/).

For more information:

* The `ApiV4Definition` and `ApiDefinition` CRDs are available on [GitHub](https://github.com/gravitee-io/gravitee-kubernetes-operator/tree/master/helm/gko/crds).
* The `ApiV4Definition` and `ApiDefinition` CRD API references are documented [here](../../reference/api-reference.md).
