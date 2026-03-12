# Managing API Products via Management API

## Create an API Product

To create an API Product, send a POST request to `/environments/{envId}/api-products` with a JSON body:

```json
{
  "name": "string",          // Required. Unique within environment (case-sensitive)
  "version": "string",       // Required
  "description": "string",   // Optional
  "apiIds": ["string"]       // Optional. List of API IDs
}
```

The system validates that:

- The name is unique within the environment (case-sensitive comparison)
- The name is not empty (leading and trailing whitespace is trimmed)
- All referenced APIs exist
- All referenced APIs have `allowedInApiProducts=true`

To verify name availability before creation, send a POST request to `/environments/{envId}/api-products/_verify` with the name in the request body. The response includes an `ok` boolean and an optional `reason` string if the name is unavailable.

## Update an API Product

Update an API Product by sending a PUT request to `/environments/{envId}/api-products/{id}` with the same JSON structure. The same validation rules apply.

## Deploy an API Product

Deploy an API Product by sending a POST request to `/environments/{envId}/api-products/{id}/deployments`. Deployment requires an active Enterprise Universe tier license.

To verify deployment readiness before deploying, send a GET request to `/environments/{envId}/api-products/{id}/deployments/_verify`. The response includes:

```json
{
  "ok": true,
  "reason": "string"  // Present when ok=false
}
```

## Manage API Product plans

Create a plan for an API Product by sending a POST request to `/environments/{envId}/api-products/{id}/plans` with a JSON body:

```json
{
  "name": "string",
  "description": "string",
  "validation": "MANUAL",
  "security": {
    "type": "API_KEY",
    "configuration": {}
  },
  "flows": []
}
```

Supported values for `security.type`:

- `API_KEY`
- `JWT`
- `MTLS`

Keyless (`KEY_LESS`) plans are rejected with a `400 Bad Request` error. OAuth plans are not supported.

Manage plan lifecycle using these endpoints:

- Publish: POST to `/_publish`
- Deprecate: POST to `/_deprecate`
- Close: POST to `/_close`
- Update: PUT with the full plan definition

## Manage subscriptions

Create a subscription to an API Product plan by sending a POST request to `/environments/{envId}/api-products/{id}/subscriptions`.

Manage subscription lifecycle using these endpoints:

- Accept: POST to `/_accept`
- Reject: POST to `/_reject`
- Close: POST to `/_close`
- Pause: POST to `/_pause`
- Resume: POST to `/_resume`
- Transfer: POST to `/_transfer`

## Plan and subscription reference model

Plans and subscriptions use a reference model to distinguish between API-level and product-level resources:

- `referenceType`: `API` or `API_PRODUCT`
- `referenceId`: The ID of the parent API or API Product

The legacy `api` field on plans is deprecated as of version 4.11.0. Use `referenceId` and `referenceType` for new integrations.
