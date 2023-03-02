---
title: How to use the API Definition custom resource
tags:
  - Gravitee Kubernetes Operator
  - GKO
  - Introduced in version 3.19.0
  - BETA release
  - K8s
  - ApiDefinition
---

# How to use the API Definition (`ApiDefinition`) custom resource

## Overview

The `ApiDefinition` custom resource represents the configuration for a single proxied API and its versions. It is similar to a YAML representation of an API Definition in JSON format.

The example below shows a simple `ApiDefinition` custom resource definition:

```
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

## The `ApiDefinition` lifecycle

The `ApiDefiniton` resource has a `Processing Status` field that makes it possible to view the status of the resource in the cluster. The following `Processing Status` field values are possible:

<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Status</p></td>
<td style="text-align: left;"><p>Description</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>[None]</p></td>
<td style="text-align: left;"><p>The API definition has been created but
not processed yet.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>Completed</p></td>
<td style="text-align: left;"><p>The API definition has been created or
updated successfully.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>Reconciling</p></td>
<td style="text-align: left;"><p>The operator has encountered a
recoverable error. A retry will be performed every 5 seconds until the
cluster retry limit is reached.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>Failed</p></td>
<td style="text-align: left;"><p>The operator has encountered an
unrecoverable error. These are errors that require manual action to
correct. No retry will be performed.</p></td>
</tr>
</tbody>
</table>

Events are added to the resource as part of each action performed by the operator. To view these events, ensure that the CRD creation steps described above are completed and then run the following command:

```
>     k describe -n default apidefinitions.gravitee.io basic-api-example
```

## Example

```
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
