### Reference Types

Subscriptions and plans support two reference types: `API` (traditional single-API subscriptions) and `API_PRODUCT` (subscriptions to bundled products). The `referenceType` and `referenceId` fields replace the deprecated `api` field, enabling plans and subscriptions to belong to either an API or an API Product.

### Prerequisites

Before configuring API Products, ensure the following requirements are met:

* Universe tier license (required for deployment)
* V4 HTTP Proxy APIs configured and published
* APIs marked with `allowedInApiProducts = true`
* Database schema updated with API Product tables (`api_products`, `api_product_apis`)
* Subscription and plan tables updated with `reference_type` and `reference_id` columns

### Gateway Configuration

#### API Product Entity

| Property | Type | Description | Example |
|:---------|:-----|:------------|:--------|
| `id` | String | Unique identifier for the API Product | `"prod-12345"` |
| `environmentId` | String | Environment where the product exists | `"env-default"` |
| `name` | String | Product name (must be unique within environment) | `"Payment Services Bundle"` |
| `version` | String | Product version | `"1.0.0"` |
| `description` | String (optional) | Product description | `"Unified access to payment APIs"` |
| `apiIds` | List<String> (optional) | List of API IDs included in the product | `["api-001", "api-002"]` |
| `createdAt` | Date | Creation timestamp | `2024-01-15T10:30:00Z` |
| `updatedAt` | Date | Last update timestamp | `2024-01-20T14:45:00Z` |
| `primaryOwner` | PrimaryOwner | Primary owner of the API Product | - |

#### API Configuration

| Property | Type | Description | Example |
|:---------|:-----|:------------|:--------|
| `allowedInApiProducts` | Boolean (optional) | Whether this API can be included in API Products (V4 HTTP Proxy only) | `true` |

#### Subscription Reference

| Property | Type | Description | Example |
|:---------|:-----|:------------|:--------|
| `referenceId` | String | ID of the API or API Product | `"prod-12345"` |
| `referenceType` | SubscriptionReferenceType | Reference type: `API` or `API_PRODUCT` | `"API_PRODUCT"` |
| `apiProductId` | String (optional) | API Product ID (gateway-side field) | `"prod-12345"` |

#### Plan Reference

| Property | Type | Description | Example |
|:---------|:-----|:------------|:--------|
| `referenceId` | String | ID of the API or API Product this plan belongs to | `"prod-12345"` |
| `referenceType` | String | Reference type: `API` or `API_PRODUCT` | `"API_PRODUCT"` |
| `api` | String | **Deprecated.** Use `referenceId` and `referenceType` instead | `"api-001"` |

### Restrictions

* **Universe tier license required**: API Products require a universe tier license to deploy. Deployment is blocked if the license tier is not "universe". Error message: `"The API Product [name] can not be deployed because it is not allowed by the current license (universe tier)"`
* **V4 HTTP Proxy APIs only**: Only V4 HTTP Proxy APIs can be included in API Products.
* **allowedInApiProducts requirement**: APIs must have `allowedInApiProducts = true` to appear in product API selection.
* **Unique name constraint**: API Product names must be unique within an environment. Attempting to create or update an API Product with a duplicate name throws `ApiProductNameAlreadyExistsException`.
* **Read-only toggle behavior**: The `allowedInApiProducts` toggle becomes read-only when an API is actively used in a product.
* **Deprecated api field**: The `api` field in plans is deprecated. Use `referenceId` and `referenceType` instead.
* **Required database migrations**: Database schema updates are required for `api_products`, `api_product_apis` tables, and `reference_type` and `reference_id` columns in subscriptions and plans tables.

