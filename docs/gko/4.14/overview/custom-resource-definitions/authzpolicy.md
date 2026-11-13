---
description: The AuthzPolicy custom resource declares an Authorization Management policy written in GAPL and deploys it to PDP gateways, for the Gravitee Kubernetes Operator 4.14. See the key fields.
---

# AuthzPolicy

The `AuthzPolicy` custom resource declares a policy of Authorization Management, written in GAPL, and the PDP gateways it's deployed to.

## Overview

Every time GKO applies an `AuthzPolicy`, the platform deploys the policy. A policy disabled in the console stays disabled until GKO applies the resource again, for example after a change to its `spec`. That apply deploys the policy again, with a warning that says so. `status.policyStatus` reads `DEPLOYED` after every apply the platform accepts. It doesn't reflect a policy disabled in the console afterward.

The `policyText` holds one or more `permit` and `forbid` statements. For the syntax, see [Policy statements](https://documentation.gravitee.io/authorization-management/gapl-reference/policy-statements).

The `targets` of an `AuthzPolicy` name the PDP gateways it's deployed to. Each target is one of the following:

* `pdpRef` names an [`AuthzPdp`](authzpdp.md) resource.
* `scope` holds the routing scope of a PDP gateway that no `AuthzPdp` declares, `default`, or `*` for every PDP gateway.

Without targets, the policy is deployed to the default engine on every Gateway. An MCP proxy asks the default engine only, so leave a policy for an MCP server or an MCP tool without targets, or include `default` or `*` in them.

In `policyText`, name an MCP server as `MCPServer::"<id>"` and an MCP tool as `MCPTool::"<id>"`, where `<id>` is the entity ID of the server or the tool in the Catalog without its `mcp-server.` or `mcp-tool.` prefix. A policy that keeps the prefix is accepted with a warning, and doesn't match the requests of an MCP proxy.

GKO checks the resource against the platform before it's admitted, then applies it. An `AuthzPolicy` with a `pdpRef` isn't applied until that `AuthzPdp` has synced. Until then, its `ResolvedRefs` condition is `False`, and GKO tries again later. Run `kubectl get authzpolicies` to see each policy's entity ID and status.

Deleting the resource removes the policy from its PDP gateways and deletes it. The entities it names are kept.

Applying an `AuthzPolicy`, and deleting one that is deployed, takes one more permission than the other Authorization Management resources. See [Limit the permissions of the service account](../../guides/define-an-apim-service-account-for-gko.md#limit-the-permissions-of-the-service-account).

## Example

```yaml
apiVersion: gravitee.io/v1alpha1
kind: AuthzPolicy
metadata:
  name: hotel-booking-read
spec:
  contextRef:
    name: "apim-context"
  entityId: policy.hotel-booking-read
  name: Hotel booking read access
  policyType: API
  policyText: |
    permit(principal in Group::"agents", action == Action::"read", resource == Hotel::"grand-paris");
  targets:
    - pdpRef:
        name: orders-eu
```

A policy for an MCP tool has no targets, and names the tool without the `mcp-tool.` prefix of its entity ID, `mcp-tool.github.create_issue`:

```yaml
  entityId: policy.github.create-issue
  name: Engineering creates GitHub issues
  policyType: MCP
  policyText: |
    permit(
      principal in Group::"engineering",
      action == Action::"github.create_issue",
      resource == MCPTool::"github.create_issue"
    );
```

## Key fields

| Field | Description |
|:------|:------------|
| `spec.contextRef` | Reference to a `ManagementContext` resource |
| `spec.entityId` | ID of the policy: `policy.` followed by one or more segments separated by dots |
| `spec.name` | Display name of the policy in the console |
| `spec.policyType` | `MCP`, `AGENT`, `MODEL`, `API`, or `CUSTOM`. The console lists the policy under **MCP Policies**, **A2A Policies**, **AI Model Policies**, **API Policies**, or **Custom Policies** |
| `spec.policyText` | The GAPL text of the policy, replaced whole on every apply |
| `spec.targets` | The PDP gateways the policy is deployed to, each a `pdpRef` or a `scope` (optional) |

## Validation

* `spec.contextRef` is required, and can't change after the resource is created.
* `spec.entityId` and `spec.policyType` can't change after the resource is created.
* An `entityId` that another policy of the environment already has is refused, and the error names that policy.
* A `policyText` that doesn't parse is refused. So is a policy template, which uses `?principal` or `?resource`.
* Each target sets `pdpRef` or `scope`, not both. A `pdpRef` names an `AuthzPdp` that uses the same `ManagementContext`.
* A policy that doesn't match the schema document of a PDP gateway in strict mode is refused.
