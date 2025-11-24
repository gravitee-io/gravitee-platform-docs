---
description: Tutorial on Application CRD.
---

# Application CRD

## How to use the Application (`Application`) custom resource

The `Application` custom resource represents the configuration for an application. It is similar to a YAML representation of an application in JSON format.

The example below shows a simple `Application` custom resource definition:

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

## The `Application` lifecycle

The `Application` resource has a `Processing Status` field that makes it possible to view the status of the resource in the cluster. The following `Processing Status` field values are possible:

| Status      | Description                                                                                                                              |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| \[None]     | The application has been created but not processed yet.                                                                                  |
| Completed   | The application has been created or updated successfully.                                                                                |
| Reconciling | The operator has encountered a recoverable error. A retry will be performed every 5 seconds until the cluster retry limit is reached.    |
| Failed      | The operator has encountered an unrecoverable error. These are errors that require manual action to correct. No retry will be performed. |

Events are added to the resource as part of each action performed by the operator. To view these events, ensure that the CRD creation steps described above are completed, then run the following command:

```sh
kubectl describe -n default application.gravitee.io basic-application
```

Example output is shown below:

```bash
Name:         basic-application
Namespace:    default
[...]
Events:
  Type    Reason          Age   From                      Message
  ----    ------          ----  ----                      -------
  Normal  AddedFinalizer  73s   application-controller  Added Finalizer for the Application
  Normal  Creating        73s   application-controller  Creating Application
  Normal  Created         72s   application-controller  Created Application
```
