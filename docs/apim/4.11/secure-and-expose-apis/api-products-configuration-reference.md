# API Products configuration reference

## Gateway Configuration

### API Product Entity Properties

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `id` | string | (generated) | Unique identifier for the API Product |
| `name` | string | (required) | Product name; must be unique within environment |
| `version` | string | (required) | Product version |
| `description` | string | null | Product description |
| `apiIds` | string[] | [] | List of API IDs included in the product |
| `environmentId` | string | (required) | Environment where product is deployed |
| `organizationId` | string | (required) | Organization owning the product |
| `createdAt` | Date | (auto) | Creation timestamp |
| `updatedAt` | Date | (auto) | Last update timestamp |
| `deployedAt` | Date | null | Last deployment timestamp |
| `primaryOwner` | PrimaryOwner | (required) | Primary owner of the API Product |
| `deploymentState` | enum | null | Deployment sync state: `NEED_REDEPLOY` or `DEPLOYED` |

### API Configuration for Product Eligibility

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `allowedInApiProducts` | boolean | null | Enables API inclusion in API Products; only applicable to V4 HTTP Proxy APIs |

### Plan Configuration

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `referenceId` | string | (required) | ID of the parent API or API Product |
| `referenceType` | enum | (required) | Reference type: `API` or `API_PRODUCT` |
| `api` | string | (deprecated) | **Deprecated since 4.11.0.** Use `referenceId` and `referenceType` |
