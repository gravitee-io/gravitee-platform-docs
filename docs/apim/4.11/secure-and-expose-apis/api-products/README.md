### Overview

API Products enable administrators to bundle multiple V4 HTTP Proxy APIs into a single subscribable package with unified access control. Instead of managing subscriptions to individual APIs, organizations can define product-level plans that grant access to all APIs within the product. This feature is available in the Enterprise Universe tier.

### API Product Structure

An API Product is an environment-level resource that groups V4 HTTP Proxy APIs under a single subscription model. Each product has:

- A unique name within its environment
- A version
- An optional description
- Product-level plans (API Key, JWT, or mTLS)
- Product-level subscriptions

An API can belong to multiple products simultaneously. APIs within a product can maintain their own plans for direct subscription, independent of the product's plans.

### Reference-Based Plans and Subscriptions

Plans and subscriptions support a reference model that distinguishes between API-level and product-level resources. Each plan and subscription includes:

- `referenceType` field: `API` or `API_PRODUCT`
- `referenceId` field: points to the parent resource (API ID or API Product ID)

The legacy `api` field is deprecated as of version 4.11.0. This model enables unified subscription management across both traditional APIs and API Products.

### API Eligibility

Only V4 HTTP Proxy APIs with the `allowedInApiProducts` flag enabled can be added to API Products. This flag:

- Is disabled by default on existing APIs
- Cannot be changed once an API is included in a product
- Is unavailable for read-only APIs (e.g., Kubernetes-managed)
- Is unavailable for non-HTTP Proxy API types

### Prerequisites

- Gravitee APIM Enterprise license with Universe tier
- Environment-level permissions for API Product management (`api_product-definition-*`)
- V4 HTTP Proxy APIs with `allowedInApiProducts=true`
- MongoDB or JDBC repository implementation (NoOp repository available for testing)
