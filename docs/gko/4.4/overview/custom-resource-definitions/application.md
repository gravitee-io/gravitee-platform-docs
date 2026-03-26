---
description: Overview of Application.
---

# Application

The `Application` custom resource represents the configuration for a Gravitee application. To access Gravitee APIs, consumers must register an application and subscribe to a published API plan. Applications act on behalf of the user to request tokens, provide user identity information, and consume APIs.

{% hint style="danger" %}
The Application CRD is expected to undergo many changes, including breaking changes, between GKO 4.4 and 4.5. We are making this exceptional decision given the initial feedback we have received on the Application CRD in its first iteration. From GKO 4.5 onwards, we expect this CRD to become highly stable and respect the versioning policy more strictly.
{% endhint %}

## Create an `Application`

The example below shows a simple `Application` custom resource definition:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: Application
metadata:
  name: basic-application
  namespace: gravitee
spec:
  contextRef:
    name: "dev-ctx"
    namespace: "gravitee"
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

## The `Application` lifecycle

The following workflow is applied when a new `Application` resource is added to the cluster:

1. The GKO listens for `Application` resources.
2. The GKO resolves any references to external sources such as ConfigMaps or Secrets.
3. The GKO performs required changes, such as adding default settings.
4. The GKO converts the data to JSON format.
5. The GKO compares the definition to the existing definition. If something has changed, the GKO pushes the definition to the Management API (if a `ManagementContext` resource is provided).

The `Application` resource has a `Processing Status` field that makes it possible to view the status of the resource in the cluster. The following `Processing Status` field values are possible:

| Status      | Description                                                                                                                              |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| \[None]     | The application has been created but not processed yet.                                                                                  |
| Completed   | The application has been created or updated successfully.                                                                                |
| Reconciling | The operator has encountered a recoverable error. A retry will be performed every 5 seconds until the cluster retry limit is reached.    |
| Failed      | The operator has encountered an unrecoverable error. These are errors that require manual action to correct. No retry will be performed. |

Events are added to the resource as part of each action performed by the operator. To view these events, ensure that the CRD creation steps described above are completed, then run the following command:

```sh
kubectl describe -n gravitee application.gravitee.io basic-application
```

Example output is shown below:

```bash
Name:         basic-application
Namespace:    gravitee
[...]
Events:
  Type    Reason          Age   From                      Message
  ----    ------          ----  ----                      -------
  Normal  AddedFinalizer  73s   application-controller  Added Finalizer for the Application
  Normal  Creating        73s   application-controller  Creating Application
  Normal  Created         72s   application-controller  Created Application
```

For more information:

* The `Application` CRD code is available on [GitHub](https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/api/v1alpha1/application_types.go).
* The `Application` CRD API reference is documented [here](../../reference/api-reference.md).
