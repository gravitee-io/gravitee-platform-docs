---
hidden: false
noIndex: false
---

# Create a custom policy

Create an authorization policy for resources that are not routed through MCP, API, Agent, AI Model, or Event categories.

## Prerequisites

* At least one principal and one resource entity exist
* The `ENVIRONMENT_AUTHZ_POLICY[CREATE]` permission

## Steps

### 1. Navigate to Custom Policies

From the Authorization Management sidebar, select **Policy Management → Custom Policies**.

### 2. Create a policy

Click **Create Custom Policy**. The policy editor opens directly — there is no target picker because custom policies are not scoped to a specific catalog entry.

### 3. Name the policy

Enter a **Policy name** (required) and an optional **Description**.

### 4. Build statements

Build one or more `permit` or `forbid` statements using the visual editor:

- **Principals**: Select from all available principal entities
- **Actions**: Select from all defined actions
- **Resources**: Select from all resource entities (no resource group filter)

### 5. Add conditions (optional)

Use pre-built condition snippets or write custom conditions:

```
permit (
  principal == User::"alice",
  action == Action::"read",
  resource == Resource::"customer-db"
)
when {
  context.auth.mfa == true &&
  context.source.ip.in_cidr("10.0.0.0/8")
};
```

### 6. Set target gateways (optional)

Scope the policy to specific PDP gateways.

### 7. Save or deploy

- **Create policy** — saves as `Draft`
- **Create and Deploy policy** — saves and deploys immediately

## Example: Owner-only access to a data asset

```
// Policy: owner-only-data-access

permit (
  principal,
  action == Action::"read",
  resource == Asset::"financial-reports"
)
when {
  resource.owner == principal
};
```

## Example: MFA-required access to internal app

```
// Policy: payroll-mfa-required

permit (
  principal in Group::"hr",
  action in [Action::"read", Action::"update"],
  resource == Application::"payroll-portal"
)
when {
  context.auth.mfa == true
};
```

## Difference from service policies

Custom policies use the same editor as service policies, with two differences:

1. **No target picker** — the policy applies to any resource referenced in its statements
2. **No resource group filter** — the resource chip picker shows all resource entities

## Next steps

* [Custom policies overview](custom-policies-overview.md) — When to use custom policies
* [Create, update, and delete policies](../create-update-delete-policies.md) — Full editor reference
