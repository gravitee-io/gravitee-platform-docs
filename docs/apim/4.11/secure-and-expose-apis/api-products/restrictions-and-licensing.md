# API Products restrictions and licensing

## Licensing

API Products require the Enterprise Universe tier. Deployment fails if the organization license tier isn't "universe."

## Supported API types

Only V4 HTTP Proxy APIs can be added to API Products. The following API types aren't supported:

- Message APIs
- Kafka APIs
- LLM APIs
- MCP APIs

## Plan type restrictions

API Products support the following plan types:

- **API Key**
- **JWT**
- **mTLS**

Keyless and OAuth plans aren't supported. The Console UI only displays API Key, JWT, and mTLS as available plan types when creating a plan for an API Product. The Management API rejects Keyless plans with a `400 Bad Request` error: "Plan Security Type KeyLess is not allowed."

## Naming requirements

API Product names are unique within an environment. Name comparison is case-sensitive — for example, "Product A" and "product a" are treated as different names. The name is trimmed of leading and trailing whitespace before validation.

If a duplicate name is submitted, the system rejects it with the error: "API Product name must be unique."

## API inclusion rules

APIs added to an API Product have the following requirements:

- The **Allow in API Products** toggle on the API's General Info page is set to enabled. APIs with this toggle disabled or not set can't be added to products.
- The **Allow in API Products** toggle can't be disabled once an API is included in a product. The toggle is greyed out in the Console when the API is used in products.
- The **Allow in API Products** toggle is unavailable for read-only APIs (for example, Kubernetes-managed APIs).

APIs within a product retain their own plans and subscriptions. Consumers can subscribe to an individual API's plans independently of the product.

## Policy and flow restrictions

API Products can't include flows or policies at the product level. Define policies at the API or plan level. To execute product-specific policies, use flow conditions that reference the API Product ID via the `apiProductId` Expression Language attribute.

## Gateway subscription validation order

The gateway validates subscriptions in the following priority order:

1. The gateway checks the request against the API Product plan subscription first.
2. If no valid API Product subscription exists, the gateway falls back to validating against the individual API plan.

API Product plans take priority, but access through API-level plans is still possible when no product-level subscription applies.
