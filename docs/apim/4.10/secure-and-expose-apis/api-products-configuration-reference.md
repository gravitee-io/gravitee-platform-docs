### Gateway Configuration



#### API Product Properties

| Property | Description | Example |
|:---------|:------------|:--------|
| `id` | Unique identifier for the API Product | `"prod-12345"` |
| `name` | Product name (must be unique within environment) | `"Payment Gateway Bundle"` |
| `version` | Product version string | `"1.0.0"` |
| `description` | Optional product description | `"Unified payment APIs"` |
| `apiIds` | Array of API identifiers included in the product | `["api-1", "api-2"]` |
| `deploymentState` | Synchronization state: `NEED_REDEPLOY` or `DEPLOYED` | `"DEPLOYED"` |
| `environmentId` | Environment identifier | `"env-prod"` |
| `organizationId` | Organization identifier | `"org-acme"` |

#### API Configuration for Product Inclusion

| Property | Description | Example |
|:---------|:------------|:--------|
| `allowedInApiProducts` | Enables API for inclusion in products (V4 HTTP Proxy only) | `true` |

#### Plan Configuration

| Property | Description | Example |
|:---------|:------------|:--------|
| `referenceId` | ID of the API or API Product | `"prod-12345"` |
| `referenceType` | Reference entity type: `API` or `API_PRODUCT` | `"API_PRODUCT"` |
| `api` | **Deprecated.** Use `referenceId` and `referenceType` | - |
