### Plan Management

API Product plans are created and configured through the API Product's plan management section. Create a new plan and select the desired security type (API Key, OAuth2, JWT, etc.). Configure plan settings (rate limits, quotas, approval mode) and publish the plan. The gateway caches API Product plans in `ApiProductPlanDefinitionCache` and evaluates them before API-level plans during subscription resolution.

### Subscription Workflow

Consumers create subscriptions to API Product plans through the standard subscription workflow. Select the API Product from the catalog, choose an available plan, and submit the subscription request (subject to approval if the plan requires it). Upon approval, the subscription entity is created with `referenceType=API_PRODUCT` and `referenceId` set to the product ID. The gateway populates the subscription's `apiProductId` field and injects it into the execution context as `{#context.attributes['apiProduct']}` for use in policy expressions.

### API Configuration

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `allowedInApiProducts` | boolean | `null` | Indicates whether this API is allowed to be used in API Products. Only applicable for V4 HTTP Proxy APIs. |

### Restrictions

- API Products require a "universe" tier license. Deployment fails with error "The API Product [name] can not be deployed because it is not allowed by the current license (universe tier)" if the license tier is insufficient.
- Only V4 HTTP Proxy APIs can be included in API Products.
- API Product names must be unique within an environment.
- The `allowedInApiProducts` toggle is disabled when the API is already used in one or more API Products.
- The `allowedInApiProducts` toggle is disabled when the API has `isReadOnly=true` (e.g., Kubernetes-managed APIs).
- The `api` field in Plan and Subscription models is deprecated since 4.11.0. Use `referenceId` and `referenceType` instead.
- Default value for `allowedInApiProducts` is `null` (not `true`).

### UI Routes

The UI introduces new routes for API Product management:

- `/api-products` - List view
- `/api-products/new` - Create new API Product
- `/api-products/:apiProductId` - API Product details (redirect to configuration)
- `/api-products/:apiProductId/configuration` - API Product configuration
- `/api-products/:apiProductId/apis` - API Product APIs management

### Role Upgrader

The `ApiProductRolesUpgrader` (execution order 950) creates API_PRODUCT scope roles (USER, OWNER, PRIMARY_OWNER) during platform upgrade.

### Database Migrations

**Plans Table**
- Added `reference_type` column (nvarchar(32), nullable)
- Added `reference_id` column (nvarchar(64), nullable)
- Created index `idx_${gravitee_prefix}plans_reference_type_reference_id`
- Migration SQL: `UPDATE plans SET reference_type = 'API', reference_id = api WHERE api IS NOT NULL AND reference_type IS NULL`

**Subscriptions Table**
- Added `reference_type` column (nvarchar(32), nullable)
- Added `reference_id` column (nvarchar(64), nullable)
- Created index `idx_${gravitee_prefix}subscriptions_reference_type_reference_id`
- Migration SQL: `UPDATE subscriptions SET reference_type = 'API', reference_id = api WHERE api IS NOT NULL AND reference_type IS NULL`

### Audit Events

Audit events now support `API_PRODUCT` as a reference type, logging subscription lifecycle events (accept, close, reject).

### Dependency Updates

| Artifact | Version Change | Purpose |
|:---------|:---------------|:--------|
| `gravitee-gateway-api` | `5.0.0-alpha.1` → `5.0.0-alpha.2` | Add `apiProductId` field to `Subscription` model |

### Repository Method Changes

Repository methods now support querying plans and subscriptions by `referenceId` and `referenceType`. Legacy `findByApi()` methods delegate to the new reference-based queries.
