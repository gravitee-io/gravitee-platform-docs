---
hidden: false
noIndex: true
---

# API policy examples

Practical examples of authorization policies for API proxies, endpoints, and data fields.

## API policy structure

API policies target a specific API and govern access at three levels:

| Resource group | Description |
|---------------|-------------|
| **API** | The API proxy itself |
| **Endpoints** | Individual API endpoints |
| **Data Fields** | Specific fields in API responses |

## Example 1: Allow a group to access an entire API

```
// Policy: engineering-orders-api
// Target: orders-service

permit (
  principal in Group::"engineering",
  action == Action::"read",
  resource in API::"orders-service"
);
```

The `in` match mode covers the API and all child endpoints and data fields.

## Example 2: Restrict access by OAuth scope

```
// Policy: require-orders-read-scope
// Target: orders-service

permit (
  principal,
  action == Action::"read",
  resource == API::"orders-service"
)
when {
  context.auth.scopes.contains("orders:read")
};
```

This policy permits any principal to read the orders API, but only if their OAuth token includes the `orders:read` scope.

## Example 3: Rate limit per principal

```
// Policy: rate-limit-orders
// Target: orders-service

forbid (
  principal,
  action,
  resource in API::"orders-service"
)
when {
  context.rate.per_minute(principal) >= 100
};
```

This policy denies access when a principal exceeds 100 requests per minute.

## Example 4: Tenant isolation

```
// Policy: tenant-isolation
// Target: orders-service

permit (
  principal,
  action == Action::"read",
  resource in API::"orders-service"
)
when {
  context.request.header.x_tenant == principal.tenant
};
```

This policy ensures principals can only access data for their own tenant.

## Example 5: IP-restricted admin access

```
// Policy: admin-corporate-only
// Target: orders-service

permit (
  principal in Group::"api-admins",
  action in [Action::"create", Action::"update", Action::"delete"],
  resource in API::"orders-service"
)
when {
  context.source.ip.in_cidr("10.0.0.0/8")
};
```

## Available condition snippets

| Condition | GAPL |
|-----------|------|
| **Corporate IP range** | `context.source.ip.in_cidr("10.0.0.0/8")` |
| **Scope present** | `context.auth.scopes.contains("orders:read")` |
| **Rate < 100/min** | `context.rate.per_minute(principal) < 100` |
| **Tenant match** | `context.request.header.x_tenant == principal.tenant` |

## Next steps

* [AI policy example](ai-policy-example.md) — Token budget and cost ceiling policies
* [MCP policy examples](mcp-policy-examples.md) — MCP access control patterns
* [Create, update, and delete policies](create-update-delete-policies.md) — Full editor reference
