---
description: Declare a client secret of an Access Management application with a custom resource of the Gravitee Kubernetes Operator 4.14. See where its value comes from and how to rotate it.
---

# `AMClientSecret`

The `AMClientSecret` custom resource declares a client secret of an application in Gravitee Access Management (AM). It names the [`AMApplication`](amapplication.md) it belongs to and a Kubernetes Secret that holds its value, and GKO creates and deletes the client secret in AM, through the `AMContext` of the application's security domain.

## Overview

The `applicationRef` is required, can't change, and must name an `AMApplication` in the same namespace as the client secret. In AM, the key of the client secret is the namespace and the name of the resource joined with a hyphen. It's made of lowercase letters, digits, and hyphens, and is at most 64 characters, so a longer namespace and name are rejected.

The `secretRef` is required and can't change. It names a Secret of the same namespace with `name`, and the entry of that Secret that holds the value with `key`. GKO reads the value from the Secret and sends it to AM. The value never appears in the status of the resource, and AM never returns it. AM requires a value of at least 43 characters. For the other rules AM applies to a client secret, see [Automation API](https://documentation.gravitee.io/am/guides/automation-api) in the Access Management documentation.

You can apply the client secret before its application or its Secret. It's stored with a warning, its `ResolvedRefs` condition stays `False` until AM has created the application and the Secret entry exists with a value, and GKO then creates the client secret. The application owns the client secret: deleting the `AMApplication` deletes the application in AM with its client secrets, and removes the `AMClientSecret` resource.

A client secret can't change. When the value in the referenced Secret changes, AM rejects it, and the `Accepted` condition of the resource shows the message from AM and asks you to rotate the client secret.

When you apply the resource, GKO checks it with AM before Kubernetes accepts it. AM validates the resource in a dry run, without creating or changing anything in AM:

- If AM reports an error, Kubernetes rejects the resource.
- If AM can't be reached, Kubernetes rejects the resource.

GKO skips this check when the `AMApplication` hasn't been created in AM yet, or when the Secret entry doesn't exist or is empty. Kubernetes accepts the resource with a warning, and GKO creates the client secret in AM once they exist.
See [Admission validation](../admission-validation.md) and [Drift detection](../drift-detection.md).

Deleting the resource deletes the client secret in AM, even when it's the last client secret of the application. A client secret already deleted in AM doesn't block the deletion. GKO never deletes the referenced Secret.

## Rotate a client secret

To rotate a client secret, complete the following steps:

1. Create a Secret with a new value, and an `AMClientSecret` that references it. The application then has both client secrets, and clients can authenticate with either one.
2. Move your clients to the new value.
3. Delete the previous `AMClientSecret`, then its Secret.

## Example

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mobile-app-secret-2026-11
  namespace: production
type: Opaque
stringData:
  client-secret: <value of at least 43 characters>
---
apiVersion: gravitee.io/v1alpha1
kind: AMClientSecret
metadata:
  name: mobile-app-2026-11
  namespace: production
spec:
  applicationRef:
    name: mobile-app
  secretRef:
    name: mobile-app-secret-2026-11
    key: client-secret
```

## Key fields

| Field | Description |
|:------|:------------|
| `spec.applicationRef` | `name` of the `AMApplication`, in the same namespace. Required, and can't change |
| `spec.secretRef` | `name` of a Secret in the same namespace, and `key` of the entry that holds the value. Required, and can't change |
| `status.expiresAt` | When the client secret expires, as AM reports it. Absent when the client secret doesn't expire |

## Validation

* `spec.applicationRef` is required, can't change, and names an application in the same namespace.
* `spec.secretRef` is required and can't change.
* The namespace and name of the resource give a key of lowercase letters, digits, and hyphens, up to 64 characters.
* An application that doesn't exist, or that AM hasn't created yet, gives a warning. So does a Secret or an entry that doesn't exist, or an empty entry. The client secret is created once they exist.
* An error reported by AM rejects the resource. An AM that can't be reached rejects it too.

## Verification

List the client secrets of a namespace:

```sh
kubectl get amclientsecrets -n production
```

Next to each resource, the output shows its application, the Secret that holds its value, and when it expires.
