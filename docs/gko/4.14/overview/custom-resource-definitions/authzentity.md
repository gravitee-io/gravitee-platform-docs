---
description: The AuthzEntity custom resource declares a principal or a resource of Authorization Management, with its parents and attributes, for the Gravitee Kubernetes Operator 4.14. See the key fields.
---

# AuthzEntity

The `AuthzEntity` custom resource declares a principal or a resource of Authorization Management: its parents, its attributes, and the PDP gateways it's published to.

## Overview

Policies name an entity by its type and its entity ID, for example `Group::"agents"`. An environment holds one entity per entity ID. An `AuthzEntity` whose `entityId` another entity already has is refused, and the error names the source of that entity, for example `local` for an entity created in the console. In the console, the **Source** column shows **automation** for the entities this resource creates.

The `targets` of an `AuthzEntity` name the PDP gateways it's published to. Each target is one of the following:

* `pdpRef` names an [`AuthzPdp`](authzpdp.md) resource.
* `scope` holds the routing scope of a PDP gateway that no `AuthzPdp` declares, `default`, or `*` for every PDP gateway.

Without targets, the entity is published to the default engine on every Gateway.

GKO checks the resource against the platform before it's admitted, then applies it. An `AuthzEntity` whose `pdpRef` names an `AuthzPdp` that hasn't synced yet is admitted with a warning and without that check, and isn't applied until the `AuthzPdp` has synced. Until then, its `ResolvedRefs` condition is `False`, and GKO tries again later.

Every apply replaces the attributes and the parents of the entity with the ones the resource declares. An attribute or a parent removed from the resource is removed from the entity. Run `kubectl get authzentities` to see each entity's entity ID and type.

Deleting the resource deletes the entity. On the platform, the resources that have it as a parent are deleted with it, and the principals that have it as a parent are kept and lose that parent. GKO then applies again each `AuthzEntity` that declares one of those children. A principal goes back to what its resource declares, parents included. A resource is refused while its parent doesn't exist, and its `Accepted` condition gives the reason.

Policies that name a deleted entity are kept. A policy that names it with `==` still applies after the delete, so change or delete the policy to remove access.

A delete that removes or detaches more entities than the platform allows is refused. The resource then stays in `Terminating`, and its `Accepted` condition gives the reason.

## Example

```yaml
apiVersion: gravitee.io/v1alpha1
kind: AuthzEntity
metadata:
  name: agents-group
spec:
  contextRef:
    name: "apim-context"
  entityId: agents
  kind: PRINCIPAL
  entityType: Group
  attributes:
    department: travel
  parents:
    - entityType: Group
      entityId: travel
  targets:
    - pdpRef:
        name: orders-eu
```

A resource published to the default engine names it by scope:

```yaml
  entityId: grand-paris
  kind: RESOURCE
  entityType: Hotel
  attributes:
    city: Paris
  targets:
    - scope: default
```

## Key fields

| Field | Description |
|:------|:------------|
| `spec.contextRef` | Reference to a `ManagementContext` resource |
| `spec.entityId` | ID of the entity in policies, without its type: `agents`, not `Group::"agents"` |
| `spec.kind` | `PRINCIPAL` for an entity that acts, or `RESOURCE` for an entity that's acted on |
| `spec.entityType` | Type of the entity, for example `Group` or `MCPTool` |
| `spec.attributes` | Attributes of the entity (optional) |
| `spec.parents` | The entities this one is a member of, each with an `entityType` and an `entityId` (optional) |
| `spec.active` | Whether the entity is published to the PDP gateways it targets. Defaults to `true` |
| `spec.targets` | The PDP gateways the entity is published to, each a `pdpRef` or a `scope` (optional) |

## Validation

* `spec.contextRef` is required, and can't change after the resource is created.
* `spec.entityId`, `spec.kind`, and `spec.entityType` can't change after the resource is created.
* `spec.entityType` is spelled exactly as policies spell it: `Group`, not `group`. A `kind` that contradicts a built-in type is refused.
* An attribute key that starts with `_` is refused.
* Each parent is declared once, and parents can't form a cycle.
* Declare the parent of a resource before the resource. A resource whose parent doesn't exist is refused.
* An entity of type `Action` takes no targets.
* Each target sets `pdpRef` or `scope`, not both. A `pdpRef` names an `AuthzPdp` that uses the same `ManagementContext`.
* A `scope` that isn't `default`, `*`, or the routing scope of a registered PDP gateway is refused.
* An entity that doesn't match the schema document of a PDP gateway in strict mode is refused.
