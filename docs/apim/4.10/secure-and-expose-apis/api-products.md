### Overview

API Products bundle multiple V4 HTTP Proxy APIs into a single consumable product with unified plans and subscriptions. Consumers subscribe to the product rather than individual APIs, simplifying access management for multi-API workflows.

### Prerequisites

- Gravitee license tier: **universe**
- At least one V4 HTTP Proxy API with `allowedInApiProducts=true`
- Environment-level permissions: `api_product-definition-c`, `api_product-plan-c`, `api_product-subscription-r`

### Create an API Product

1. Send a POST request to `/environments/{envId}/api-products` with the following required fields:

   ```json
   {
     "name": "string",
     "version": "string",
     "description": "string",
     "apiIds": ["string"]
   }
   ```

   - `name`: Must be unique within the environment
   - `version`: Product version string
   - `description`: Optional product description
   - `apiIds`: Optional array of API identifiers

2. Verify name uniqueness by sending a POST request to `/environments/{envId}/api-products/_verify`:

   ```json
   {
     "name": "string"
   }
   ```

   The response indicates whether the name is available:

   ```json
   {
     "ok": false,
     "reason": "An API Product with the same name already exists."
   }
   ```

### Deploy an API Product

1. Ensure your organization has a universe-tier license. Deployment attempts on non-universe tier licenses are blocked with the warning: "The API Product [name] can not be deployed because it is not allowed by the current license (universe tier)."

2. Deploy the API Product. The gateway registers the product and emits `ApiProductChangedEvent` for all included APIs (if `apiIds` is not empty).

3. Verify deployment by sending a request to `/api-products/{productId}/_verify-deploy`:

   ```json
   {
     "ok": true,
     "reason": "string"
   }
   ```

### Create Plans for API Products

API Products support the following plan security types:

- API Key
- JWT
- Mutual TLS

{% hint style="warning" %}
OAuth 2.0, Push, and Keyless plan types are not supported for API Products.
{% endhint %}

1. Navigate to **Consumers → Plans** in the API Product detail view.

2. Create a plan with `referenceId` set to the API Product ID and `referenceType` set to `API_PRODUCT`.

Plans are queried using `findByReferenceIdAndReferenceType()` repository methods.

### Manage Subscriptions

1. Navigate to **Consumers → Subscriptions** in the API Product detail view.

2. Create a subscription with `referenceType` set to `API_PRODUCT` and `referenceId` set to the API Product ID.

The gateway model includes an `apiProductId` field. During subscription processing, the execution context is injected with `ATTR_API_PRODUCT` if `apiProductId` is not null. The template engine populates the subscription variable with `getApiProductId()`.

Subscriptions are queried using `findByReferenceIdAndReferenceType()` repository methods. Audit events use `ApiProductAuditLogEntity` as the reference type.

### Restrictions

- **License requirement**: Universe-tier license is required for deployment.
- **API type restriction**: Only V4 HTTP Proxy APIs can be included. Native and non-proxy APIs cannot be added to products.
- **Product inclusion flag**: APIs must have `allowedInApiProducts=true` to be selectable.
- **Supported plan types**: API Key, JWT, and Mutual TLS only. OAuth 2.0, Push, and Keyless are not supported.
- **Name uniqueness**: Product names must be unique within an environment.

- **Deprecated fields**: The `api` field in Plan and Subscription models is deprecated since 4.11.0. Use `referenceId` and `referenceType` instead.
- **API Key lookup**: The `referenceType` parameter is required when looking up API keys by reference.
