---
description: The AuthzPdp custom resource declares a PDP gateway of Authorization Management, with its AuthZEN endpoint, for the Gravitee Kubernetes Operator 4.14. See the key fields.
---

# AuthzPdp

The `AuthzPdp` custom resource declares a PDP gateway of Authorization Management: the engine it runs, the Gateways it runs on, and its AuthZEN endpoint.

## Overview

The platform gives each PDP gateway a routing scope: `<targetPdpId>@<tag>` when the resource sets a sharding tag, and `<targetPdpId>` when it doesn't. A routing scope names one PDP gateway. [`AuthzSchema`](authzschema.md), [`AuthzEntity`](authzentity.md), and [`AuthzPolicy`](authzpolicy.md) resources name the PDP gateway they're published to through `pdpRef`.

GKO checks the resource against the platform before it's admitted, then applies it. The status reports the routing scope and the AuthZEN discovery path of the endpoint. Run `kubectl get authzpdps` to see each PDP gateway's routing scope, endpoint path, and strict mode.

Strict mode is shared by every PDP gateway with the same `targetPdpId`. A new `AuthzPdp` is refused when its `strict` differs from the PDP gateways that `targetPdpId` already has. Changing `strict` on an existing `AuthzPdp` changes it on the others too, with a warning that names each one.

Deleting the resource deletes the PDP gateway and its AuthZEN endpoint. The schema documents, entities, and policies that targeted the PDP gateway stop targeting it. A delete that leaves a policy or an entity with no target is refused. The resource then stays in `Terminating`, and its `Accepted` condition gives the reason, until each of them has another target or is deleted.

## Example

```yaml
apiVersion: gravitee.io/v1alpha1
kind: AuthzPdp
metadata:
  name: orders-eu
spec:
  contextRef:
    name: "apim-context"
  name: Orders PDP (EU)
  targetPdpId: orders
  tag: eu
  strict: true
  endpoint:
    path: /authz/orders-eu
```

The routing scope of this PDP gateway is `orders@eu`.

## Key fields

| Field | Description |
|:------|:------------|
| `spec.contextRef` | Reference to a `ManagementContext` resource |
| `spec.name` | Display name of the PDP gateway |
| `spec.targetPdpId` | The engine the PDP gateway runs. PDP gateways with the same `targetPdpId` share the engine and its strict mode |
| `spec.tag` | Sharding tag of the Gateways that run the PDP gateway (optional). A tag that doesn't exist in the organization yet is created with the PDP gateway |
| `spec.strict` | Strict mode: whether the engine checks policies and entities against its schema document. Defaults to `false` |
| `spec.endpoint` | The AuthZEN endpoint of the PDP gateway (optional), with the context `path` it listens on. Without `endpoint`, the PDP gateway has no AuthZEN endpoint, and an existing one is deleted |

## Validation

* `spec.contextRef` is required, and can't change after the resource is created.
* `spec.targetPdpId` and `spec.tag` can't change after the resource is created.
* A routing scope that another PDP gateway already has is refused.
* `spec.endpoint.path` is refused when another API of the environment uses the path. Write it without a trailing slash, for example `/authz/orders-eu`. It can't be `/`, and it can't be under `/.well-known/authzen-configuration`.
* A sharding tag that exists in the organization, and that the service account isn't allowed to use, is refused when GKO applies the resource, not at admission.
* Give every `AuthzPdp` with the same `targetPdpId` the same `strict` value. Two resources that disagree overwrite each other.
* Deleting an `AuthzPdp` that other resources still name in `pdpRef` is allowed, with a warning that names them. Each of them reports `ResolvedRefs` as `False` until its `pdpRef` changes.
