---
description: The AuthzSchema custom resource declares a schema document of Authorization Management and the PDP gateway that enforces it, for the Gravitee Kubernetes Operator 4.14. See the key fields.
---

# AuthzSchema

The `AuthzSchema` custom resource declares a schema document of Authorization Management and the PDP gateway that enforces it.

## Overview

A schema document is written in the GAPL schema language. For the syntax, see [Schema language](https://documentation.gravitee.io/authorization-management/gapl-reference/schema-language).

The `target` of an `AuthzSchema` names the PDP gateway that enforces the document, in one of two ways:

* `pdpRef` names an [`AuthzPdp`](authzpdp.md) resource.
* `scope` holds the routing scope of a PDP gateway that no `AuthzPdp` declares, such as a PDP gateway registered in the console, or `default`. The console shows `default` as **Bootstrap PDP**.

A PDP gateway holds one schema document: a target that another schema document already has is refused. Without `target`, the document is stored and reaches no PDP gateway.

GKO checks the resource against the platform before it's admitted, then applies it. An `AuthzSchema` whose `pdpRef` names an `AuthzPdp` isn't applied until that `AuthzPdp` has synced. Until then, its `ResolvedRefs` condition is `False`, and GKO tries again later.

The status reports the routing scope the document is published to. Run `kubectl get authzschemas` to see it.

Deleting the resource deletes the schema document. Deleting the `AuthzPdp` that `pdpRef` names leaves the document stored with no target. The `AuthzSchema` then reports `ResolvedRefs` as `False` until its `pdpRef` names another `AuthzPdp`.

## Example

```yaml
apiVersion: gravitee.io/v1alpha1
kind: AuthzSchema
metadata:
  name: travel-schema
spec:
  contextRef:
    name: "apim-context"
  name: Travel schema
  target:
    pdpRef:
      name: orders-eu
  schema: |
    entity User in [Group];
    entity Group in [Group] { department?: String };
    entity Hotel;
    action read appliesTo { principal: [User], resource: [Hotel] };
```

A schema document for a PDP gateway that no `AuthzPdp` declares names it by routing scope:

```yaml
  target:
    scope: default
```

## Key fields

| Field | Description |
|:------|:------------|
| `spec.contextRef` | Reference to a `ManagementContext` resource |
| `spec.name` | Display name of the schema document |
| `spec.target.pdpRef` | The `AuthzPdp` that enforces the document. Its namespace defaults to the namespace of the `AuthzSchema` |
| `spec.target.scope` | Routing scope of a PDP gateway that no `AuthzPdp` declares, or `default` |
| `spec.schema` | The text of the schema document, replaced whole on every apply |

## Validation

* `spec.contextRef` is required, and can't change after the resource is created.
* `spec.target` sets `pdpRef` or `scope`, not both.
* `spec.target.scope` can't be `*`.
* `pdpRef` names an `AuthzPdp` that uses the same `ManagementContext`.
* A schema text that doesn't parse is refused.
* A declaration that conflicts with a schema document composed on the same PDP gateway is refused.
