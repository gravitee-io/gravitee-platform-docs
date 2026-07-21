---
hidden: false
noIndex: false
---

# Custom policies overview

Custom policies govern resources that are not routed through MCP, API, Agent, AI Model, or Event categories — internal applications, data assets, and bespoke resources.

## How custom policies differ

| Aspect | Service policies (MCP, API, etc.) | Custom policies |
|--------|----------------------------------|-----------------|
| **Target** | Bound to a specific catalog entry | No target — applies globally |
| **Resource groups** | Pre-defined (for example, MCPServer, MCPTool) | User-defined or any entity type |
| **Policy type** | Derived from entity kind prefix | `CUSTOM` (catch-all) |
| **Entity ID resolution** | Prefix maps to a service type | Null entity ID or non-service prefix falls back to `CUSTOM` |

## When to use custom policies

Use custom policies for:

- **Internal applications** — Resources with custom type prefixes (for example, `app.payroll-portal`)
- **Data assets** — Resources like `Asset::"customer-db"` or `Resource::"s3-bucket-prod"`
- **Cross-cutting rules** — Global policies that apply regardless of service type
- **Domain-specific resources** — Any entity type you define in your schema that is not MCP, API, Agent, Model, or Event

## Custom Policies page

Navigate to **Policy Management → Custom Policies**. The page provides:

- A policy list table with search and status filters
- **Create Custom Policy** button
- No target picker (custom policies are untargeted)

## Available condition snippets

| Condition | GAPL |
|-----------|------|
| **Corporate IP range** | `context.source.ip.in_cidr("10.0.0.0/8")` |
| **MFA required** | `context.auth.mfa == true` |
| **Business hours** | `context.time.hour >= 9 && context.time.hour < 17` |
| **Owner only** | `resource.owner == principal` |

## Policy type resolution

The entity-kind registry determines whether a policy is routed to a service page or the Custom page:

- If an entity ID has a prefix registered in the kind registry (for example, `mcp.`, `model.`, `api.`), the policy appears on the corresponding service page
- If the entity ID has no registered prefix or the prefix is unknown, the policy appears on the **Custom Policies** page
- Policies with a null entity ID are always classified as `CUSTOM`

## Next steps

* [Create a custom policy](create-a-custom-policy.md) — Step-by-step guide
* [Create, update, and delete policies](../create-update-delete-policies.md) — Full editor reference
