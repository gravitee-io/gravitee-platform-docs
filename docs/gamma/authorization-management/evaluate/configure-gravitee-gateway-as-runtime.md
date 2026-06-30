---
hidden: false
noIndex: false
---

# Configure the Gravitee Gateway as a runtime

Register a Gravitee Gateway instance as a PDP (Policy Decision Point) gateway so the policy engine can evaluate authorization decisions at the wire level.

## How PDP gateways work

A PDP gateway is a registered runtime that executes policy decisions. Each gateway:

- Is identified by a **Target PDP ID** that policies are routed to
- Can be scoped to a **sharding tag** for multi-region or multi-tenant deployments
- Has a **status** (`PENDING` or `PUBLISHED`) indicating whether the engine is provisioned
- Exposes one or more **AuthZEN endpoints** for standards-compliant access evaluation

## Prerequisites

* A Gravitee Gateway instance deployed and connected to the control plane
* The `ENVIRONMENT_AUTHZ_PDP[CREATE]` permission

## Steps

### 1. Navigate to PDP Gateways

From the Authorization Management sidebar, select **PDP Gateways**. The page shows a table of all registered PDP gateways.

### 2. Register a gateway

Click **Register PDP gateway**. A dialog opens with the following fields:

| Field | Required | Description |
|-------|----------|-------------|
| **Name** | Yes | Human-readable name for this gateway (for example, `EU Gateway`) |
| **Target PDP ID** | No | The engine identifier. Leave blank to use the default engine — scoped to this tag's gateways when a tag is set, or every gateway when it is not |
| **Tag** | No | Sharding tag for routing. Leave blank to provision on all gateways |
| **Create AuthZEN endpoint** | No | Checkbox to create an initial AuthZEN endpoint alongside the gateway |

### 3. Set up an AuthZEN endpoint (optional)

If you check **Create AuthZEN endpoint**, an **Endpoint path** field appears. The path auto-derives from the Target PDP ID (for example, Target PDP ID `eu-prod` → path `/eu-prod/`). You can override the path manually.

### 4. Register

Click **Register**. The gateway appears in the table with status `PENDING`. Once the engine provisions, the status transitions to `PUBLISHED`.

## PDP Gateways table

| Column | Description |
|--------|-------------|
| **Name** | Gateway display name |
| **Target PDP ID** | The engine identifier (monospace badge) |
| **Tag** | Optional sharding tag |
| **Status** | `PENDING` (provisioning) or `PUBLISHED` (active) |
| **AuthZEN endpoint** | The endpoint URL for this gateway |
| **Actions** | Endpoint details and delete options |

## Deleting a gateway

1. Click the **⋮** menu on a gateway row → **Delete**
2. The confirmation dialog warns: "The engine is evicted from its gateway and policies/entities targeting it are unbound"
3. If the gateway has AuthZEN endpoints, they are listed in the dialog and will also be deleted
4. Click **Delete** to confirm

{% hint style="warning" %}
Deleting a PDP gateway removes the engine from the specified gateway. Policies and entities that reference this gateway's Target PDP ID are unbound and no longer enforced on that runtime.
{% endhint %}

## Sharding tag patterns

| Pattern | Tag | Target PDP ID | Effect |
|---------|-----|--------------|--------|
| **All gateways** | (blank) | (blank) | Default engine on every gateway |
| **Regional** | `eu` | `eu-prod` | Dedicated engine on EU-tagged gateways only |
| **Multi-tenant** | `tenant-a` | `tenant-a-pdp` | Isolated engine per tenant |

## Next steps

* [Configure a sidecar as runtime](configure-sidecar-as-runtime.md) — Non-gateway deployment pattern
* [Policy syncs](policy-syncs.md) — How policies reach the gateway
* [AuthZEN PDP synchronization](../authz-gateway-sync.md) — Sync protocol details
