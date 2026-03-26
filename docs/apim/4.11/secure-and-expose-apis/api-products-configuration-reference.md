# API Products configuration reference

## API Product properties

| Property | Type | Required | Description |
|:---------|:-----|:---------|:------------|
| `name` | string | Yes | API Product name. Unique within the environment (case-sensitive comparison). Leading and trailing whitespace is trimmed. |
| `version` | string | Yes | API Product version |
| `description` | string | No | API Product description |
| `apiIds` | string[] | No | List of API IDs included in the API Product. All referenced APIs must exist and have `allowedInApiProducts=true`. |

## API eligibility configuration

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `allowedInApiProducts` | Boolean | `true` for new V4 HTTP Proxy APIs; `false` for existing APIs created before 4.11.0; `null` for non-HTTP Proxy types | Enables API inclusion in API Products. Only applicable to V4 HTTP Proxy APIs. Can't be disabled once the API is included in an API Product. |

## Plan reference model

Plans and subscriptions created for API Products use the following reference fields:

| Property | Type | Description |
|:---------|:-----|:------------|
| `referenceId` | string | ID of the parent API or API Product |
| `referenceType` | enum | `API` or `API_PRODUCT` |

The legacy `api` field on plans is deprecated as of version 4.11.0. Use `referenceId` and `referenceType` for new integrations.

## Supported plan security types

| Security type | Supported | Notes |
|:--------------|:----------|:------|
| `API_KEY` | Yes | - |
| `JWT` | Yes | - |
| `MTLS` | Yes | - |
| `KEY_LESS` | No | Rejected with `400 Bad Request` |
| `OAUTH2` | No | Not available in Console UI or supported for API Products |
