### Restrictions

API Products are subject to the following constraints and limitations:

#### Licensing and Deployment

API Products require the Enterprise Universe tier. Deployment fails if the organization license tier is not "universe."

#### Supported API Types

Only V4 HTTP Proxy APIs can be added to API Products. The following API types are not supported:

* Message APIs
* Kafka APIs
* LLM APIs
* MCP APIs

#### Plan Type Restrictions

API Products do not support the following plan types:

* Keyless plans
* OAuth plans

Supported plan types include **API Key, JWT, and mTLS**.

#### Naming Requirements

API Product names must be unique within an environment. Name uniqueness is validated before creation or update.

#### API Inclusion Rules

APIs must meet the following criteria to be added to an API Product:

* The `allowedInApiProducts` flag must be set to `true`. APIs with `allowedInApiProducts=false` or `null` cannot be added to products.
* The `allowedInApiProducts` flag cannot be disabled once an API is included in a product. The flag is greyed out in the UI when the API is used in products.
* The `allowedInApiProducts` flag is unavailable for read-only APIs (e.g., Kubernetes-managed APIs).

#### Deprecated Fields

Plans and subscriptions created before version 4.11.0 use the deprecated `api` field. New resources must use `referenceId` and `referenceType` instead. Legacy methods delegate to new reference-based methods for backward compatibility.

#### Policy and Flow Restrictions

API Products cannot include flows or policies at the product level. Policies must be defined at the API or plan level. Customers can use flow conditions to execute product-specific policies by referencing the API Product ID.

#### Plan Tag Handling

Empty tags are automatically set for API Product plans during updates to prevent deployment state inconsistencies.
