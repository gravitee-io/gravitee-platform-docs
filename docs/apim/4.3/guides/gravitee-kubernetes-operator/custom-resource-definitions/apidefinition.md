# ApiDefinition

## How to use the API Definition (`ApiDefinition`) custom resource

The `ApiDefinition` custom resource represents the configuration for a single proxied API and its versions. It is similar to a YAML representation of an API definition in JSON format.

The example below shows a simple `ApiDefinition` custom resource definition:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiDefinition
metadata:
  name: basic-api-example
spec:
  name: "GKO Basic"
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

### API deployment in a Kubernetes Cluster

You can deploy an API on Gravitee Gateways deployed in different Kubernetes clusters. The Management API will be deployed in the same cluster as the GKO. The following reference diagram is the basis for both the single and multi-Gateway deployment options discussed below.

<figure><img src="../../../../4.1/.gitbook/assets/image (45).png" alt=""><figcaption><p>Gateways in different Kubernetes Clusters</p></figcaption></figure>

{% tabs %}
{% tab title="Single Gateway" %}
To deploy an API on a single Gateway, apply the following configuration on the Gateway 1 cluster:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiDefinition
metadata:
  name: local-api-example
spec:
  name: "GKO Basic"
  version: "1.1"
  description: "Basic api managed by Gravitee Kubernetes Operator"
  proxy:
    virtual_hosts:
      - path: "/k8s-basic"
    groups:
      - endpoints:
          - name: "Default"
            target: "https://api.gravitee.io/echo"
  local: true
```

The `local` field is optional and is set to `true` by default to indicate that the API will be deployed only in the cluster where the custom resource is applied. Run the following command to verify that the API ConfigMap has been created in the Gateway 1 cluster:

```sh
kubectl get cm -n gateway-1-cluster
```

```
NAMESPACE            NAME                DATA    AGE
gateway-1-namespace  local-api-example   1       1m
```
{% endtab %}

{% tab title="Multiple clusters" %}
To deploy an API on multiple Gateways, use a custom resource that can be applied to any cluster. As long as the Management API is available, the `ApiDefinition` refers to a `ManagementContext` and the `local` field is set to `false`.

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiDefinition
metadata:
  name: global-api-example
spec:
  name: "GKO Basic"
  version: "1.1"
  description: "Basic api managed by Gravitee Kubernetes Operator"
  contextRef:
    name: apim-example-context
    namespace: apim-example
  proxy:
    virtual_hosts:
      - path: "/k8s-basic"
    groups:
      - endpoints:
          - name: "Default"
            target: "https://api.gravitee.io/echo"
  local: false
```

With the above configuration, there should be no `ConfigMap` linked to the `ApiDefinition` in the cluster where the custom resource has been applied because the `ApiDefinition` was deployed using the Management API and the `ApiDefinition` is not local to the cluster.
{% endtab %}
{% endtabs %}

## The `ApiDefinition` lifecycle

The `ApiDefiniton` resource has a `Processing Status` field that makes it possible to view the status of the resource in the cluster. The following `Processing Status` field values are possible:

<table><thead><tr><th width="143.5">Status</th><th>Description</th></tr></thead><tbody><tr><td>[None]</td><td>The API definition has been created but not yet processed.</td></tr><tr><td>Completed</td><td>The API definition has been created or updated successfully.</td></tr><tr><td>Reconciling</td><td>The operator has encountered a recoverable error. A retry will be performed every 5 seconds until the cluster retry limit is reached.</td></tr><tr><td>Failed</td><td>The operator has encountered an unrecoverable error. These are errors that require manual action to correct. No retry will be performed.</td></tr></tbody></table>

Events are added to the resource as part of each action performed by the operator. To view these events, ensure that the CRD creation steps described above are completed, then run the following command:

```sh
kubectl describe -n default apidefinitions.gravitee.io basic-api-example
```

Example output is shown below:

```bash
Name:         basic-api-example
Namespace:    default
[...]
Events:
  Type    Reason          Age   From                      Message
  ----    ------          ----  ----                      -------
  Normal  AddedFinalizer  73s   apidefinition-controller  Added Finalizer for the API definition
  Normal  Creating        73s   apidefinition-controller  Creating API definition
  Normal  Created         72s   apidefinition-controller  Created API definition
```
