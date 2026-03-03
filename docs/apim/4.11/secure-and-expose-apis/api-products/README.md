### Overview

API Products bundle multiple V4 HTTP Proxy APIs into a single consumable product with unified plans and subscriptions. Consumers subscribe to the API Product rather than individual APIs. API Products require a "universe" tier license.

### API Product entity

An API Product is a versioned container that groups one or more V4 HTTP Proxy APIs. Each API Product has a unique name within its environment, a version identifier, and an optional description. API Products maintain their own plans and subscriptions, independent of the constituent APIs.

| Property | Type | Description |
|:---------|:-----|:------------|
| `id` | string | Unique identifier |
| `name` | string | Unique within environment |
| `version` | string | Product version |
| `apiIds` | string[] | List of included API IDs |
| `environmentId` | string | Environment identifier |
| `description` | string | Optional description |
| `createdAt` | Date | Creation timestamp |
| `updatedAt` | Date | Last update timestamp |
| `primaryOwner` | PrimaryOwner | Primary owner of the API Product |

### Plan reference model

Plans support two reference types: `API` (standard API plans) and `API_PRODUCT` (API Product plans). The `referenceId` and `referenceType` fields replace the deprecated `api` field (deprecated since 4.11.0). API Product plans are evaluated before API plans in the gateway security chain.

| Property | Type | Description |
|:---------|:-----|:------------|
| `referenceId` | string | Identifier of the entity this plan belongs to (API ID or API Product ID) |
| `referenceType` | string | Type of the reference entity: `API` or `API_PRODUCT` |
| `api` | string | **Deprecated since 4.11.0.** Use `referenceId` and `referenceType` instead |

### Subscription reference model

Subscriptions track their parent entity using `referenceId` and `referenceType` fields. A subscription to an API Product plan sets `referenceType=API_PRODUCT` and `referenceId` to the product ID. The gateway injects the API Product ID into the execution context as `{#context.attributes['apiProduct']}`.

| Property | Type | Description |
|:---------|:-----|:------------|
| `referenceId` | string | API or API Product ID |
| `referenceType` | string | `API` or `API_PRODUCT` |
| `api` | string | **Deprecated since 4.11.0.** Use `referenceId` and `referenceType` instead |
| `apiProductId` | string | API Product ID (gateway subscription model) |

### Prerequisites

* Gravitee API Management 4.11.0 or later
* "Universe" tier license
* At least one V4 HTTP Proxy API with `allowedInApiProducts=true`
* `API_PRODUCT_DEFINITION` permission (CREATE, READ, UPDATE, DELETE actions)

### License requirements

API Products require a "universe" tier license. Deployment is blocked if the license tier does not match. The system returns the following error message when deployment is attempted without the required license:

```
The API Product [name] can not be deployed because it is not allowed by the current license (universe tier)
```

### API eligibility

Only V4 HTTP Proxy APIs can be included in API Products. The `allowedInApiProducts` flag controls eligibility:

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `allowedInApiProducts` | boolean | `null` | Indicates whether this API is allowed to be used in API Products. Only applicable for V4 HTTP Proxy APIs. |

When `allowedInApiProducts=true`, the API appears in the API Product API selection dialog. When `false` or `null`, the API is excluded.

#### Restrictions

The `allowedInApiProducts` toggle is disabled when:

* The API is already used in one or more API Products
* The API has `isReadOnly=true` (e.g., Kubernetes-managed APIs)

The toggle is only visible for V4 PROXY APIs.

### API Product naming

API Product names must be unique within an environment. This constraint is enforced at the repository level.

### Gateway configuration

### Creating an API Product

1. Navigate to the API Products section in the Console.
2. Click **New API Product**.
3. Enter a unique name and version for the API Product.
4. (Optional) Add a description.
5. Click the API selection dialog to choose one or more V4 HTTP Proxy APIs. Only APIs with `allowedInApiProducts=true` appear in the list.
6. Click **Save**. The system assigns a primary owner and creates the API Product entity.

You can now define plans for this API Product.

### Plan Reference Model

See [Plan Reference Model](#plan-reference-model) above for details.
## Prerequisites

Before you create an API Product, ensure the following requirements are met:

* **Gravitee APIM version:** 4.11.0 or later
* **License tier:** Universe tier license (required for API Product deployment)
* **V4 HTTP Proxy API:** At least one V4 HTTP Proxy API with the `allowedInApiProducts` property set to `true`
* **Permissions:** `API_PRODUCT_DEFINITION` permission with CREATE, READ, UPDATE, and DELETE actions

### Enabling APIs for API Product Inclusion

1. Open the API's general information page in the Console.
2. Locate the **Allowed in API Products** toggle. This toggle is visible only for V4 HTTP Proxy APIs.
3. Enable the toggle to make the API selectable in API Product creation dialogs.
4. Click **Save**.

{% hint style="info" %}
The toggle is disabled if the API is already used in one or more API Products or if the API has `isReadOnly=true` (e.g., Kubernetes-managed APIs). The default value is `null` (not allowed).
{% endhint %}

### Creating Plans for API Products

API Product plans follow the same creation workflow as API plans but reference the API Product ID instead of an API ID.

1. Navigate to the API Product's plan management section in the Console.
2. Click **Create New Plan**.
3. Select the desired security type (API Key, OAuth2, JWT, etc.).
4. Configure plan settings (rate limits, quotas, approval mode).
5. Click **Publish**.

The gateway caches API Product plans in `ApiProductPlanDefinitionCache` and evaluates them before API-level plans during subscription resolution.

### Subscribing to an API Product

Consumers create subscriptions to API Product plans through the standard subscription workflow.

1. Select the API Product from the catalog.
2. Choose an available plan.
3. Submit the subscription request. If the plan requires approval, the request is subject to the approval workflow.
4. Upon approval, the subscription entity is created with `referenceType=API_PRODUCT` and `referenceId` set to the API Product ID.

The gateway populates the subscription's `apiProductId` field and injects it into the execution context as `{#context.attributes['apiProduct']}` for use in policy expressions.

## Restrictions

Be aware of the following restrictions when working with API Products:

* **License requirement:** API Products require a "universe" tier license. Deployment fails with the error "The API Product [name] can not be deployed because it is not allowed by the current license (universe tier)" if the license tier is insufficient.
* **API compatibility:** Only V4 HTTP Proxy APIs can be included in API Products.
* **Naming:** API Product names must be unique within an environment.
* **API reuse:** The `allowedInApiProducts` toggle is disabled when the API is already used in one or more API Products.
* **Read-only APIs:** The `allowedInApiProducts` toggle is disabled when the API has `isReadOnly=true` (e.g., Kubernetes-managed APIs).
* **Deprecated fields:** The `api` field in Plan and Subscription models is deprecated since 4.11.0. Use `referenceId` and `referenceType` instead.
* **Default behavior:** The default value for `allowedInApiProducts` is `null` (not `true`).

## Related Changes

The API Product feature introduces several changes across the platform:

### UI Routes
New routes support API Product management:
* `/api-products` — API Product list view
* `/api-products/new` — API Product creation
* `/api-products/:apiProductId/configuration` — API Product configuration
* `/api-products/:apiProductId/apis` — API Product API management

### Role Management
The `ApiProductRolesUpgrader` (execution order 950) creates API_PRODUCT scope roles during platform upgrade:
* USER
* OWNER
* PRIMARY_OWNER

### Database Schema
Database migrations add the following columns to support API Product references:

**Plans table:**
* `reference_type`
* `reference_id`
* Index: `idx_${gravitee_prefix}plans_reference_type_reference_id`

**Subscriptions table:**
* `reference_type`
* `reference_id`
* Index: `idx_${gravitee_prefix}subscriptions_reference_type_reference_id`

### Audit Events
Audit events now support `API_PRODUCT` as a reference type. Subscription lifecycle events are logged for API Products:
* Accept
* Close
* Reject

### Gateway Dependency
The `gravitee-gateway-api` dependency was updated from `5.0.0-alpha.1` to `5.0.0-alpha.2` to include the `apiProductId` field in the gateway Subscription model.

### Repository Methods
Repository methods now support querying plans and subscriptions by `referenceId` and `referenceType`.

### API Configuration

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `allowedInApiProducts` | boolean | `null` | Indicates whether this API can be included in API Products. Only applicable for V4 HTTP Proxy APIs. |

{% hint style="info" %}
The `allowedInApiProducts` toggle is disabled when the API is already used in one or more API Products or when the API has `isReadOnly=true` (e.g., Kubernetes-managed APIs).
{% endhint %}
