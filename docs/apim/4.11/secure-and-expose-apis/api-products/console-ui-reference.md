# API Products console UI reference

## Navigation

A new "API Products" navigation item appears in the APIM Console side menu with icon `gio:folder`, routing to `./api-products`.

## API Product Detail Tabs

API Product detail pages include the following tabs, each gated by corresponding permissions:

| Tab | Route | Permission |
|:----|:------|:-----------|
| Configuration | `configuration` | `api_product-definition-r` |
| APIs | `apis` | `api_product-definition-r` |
| Consumers → Plans | `consumers/plans` | `api_product-plan-r` |
| Consumers → Subscriptions | `consumers/subscriptions` | `api_product-subscription-r` |

## API List Filtering

The API list view supports filtering by `allowedInApiProducts` flag. When enabled, only APIs allowed in API Products (V4 HTTP Proxy) are displayed.

## Subscription List Display

Subscription lists display "API" or "API Product" labels based on `referenceType`. Status badges use the following colors:

| Status | Display Name | Badge Color |
|:-------|:-------------|:------------|
| `ACCEPTED` | Accepted | success |
| `CLOSED` | Closed | neutral |
| `PAUSED` | Paused | accent |
| `PENDING` | Pending | warning |
| `REJECTED` | Rejected | warning |
| `RESUMED` | Resumed | neutral |

Default subscription filters include `ACCEPTED`, `PAUSED`, and `PENDING` statuses.

## Audit Events

Audit events for API Product subscriptions use `AuditReferenceType.API_PRODUCT` and include `APPLICATION` property.

## System Roles

A new upgrader (order 950) creates the following system roles with `RoleScope.API_PRODUCT`:

* `ROLE_API_PRODUCT_USER`
* `ROLE_API_PRODUCT_OWNER`
* `PRIMARY_OWNER` (with all `ApiProductPermission` values)

