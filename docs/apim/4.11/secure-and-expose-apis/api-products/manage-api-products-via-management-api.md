# Managing API Products via Management API

## Create an API Product

To create an API Product, send a POST request to `/environments/{envId}/api-products` with a JSON body:

```json
{
  "name": "string",          // Required. Must be unique within environment
  "version": "string",       // Required
  "description": "string",   // Optional
  "apiIds": ["string"]       // Optional. List of API IDs
}
```

The system validates that:
* The name is unique within the environment
* All referenced APIs exist
* All referenced APIs have `allowedInApiProducts=true`

Upon successful creation, the product receives a unique ID and timestamps. To verify name availability before creation, send a POST request to `/environments/{envId}/api-products/_verify` with the name in the request body. The response includes an `ok` boolean and an optional `reason` string if the name is unavailable.

Update an API Product by sending a PUT request to `/environments/{envId}/api-products/{id}` with the same JSON structure. The same validation rules apply.

## Deploy an API Product

Deploy an API Product by sending a POST request to `/environments/{envId}/api-products/{id}/deployments`. The system:
1. Checks that the organization license tier is "universe" and blocks deployment if not
2. Registers the product in the gateway's `ApiProductRegistry`
3. Caches the product's plans in `ApiProductPlanDefinitionCache`
4. Emits `DEPLOY` events to refresh security chains in affected APIs

To verify deployment readiness before deploying, send a GET request to `/environments/{envId}/api-products/{id}/deployments/_verify`. The response includes:

```json
{
  "ok": boolean,
  "reason": "string"  // Present when ok=false
}
```

Redeployment occurs automatically when `deployedAt` is newer than the existing deployment or when forced.

## Manage API Product Plans

Create a plan for an API Product by sending a POST request to `/environments/{envId}/api-products/{id}/plans` with a JSON body:

```json
{
  "name": "string",
  "description": "string",
  "validation": "MANUAL" | "AUTO",  // Default: MANUAL
  "security": {
    "type": "API_KEY" | "JWT" | "MTLS",
    "configuration": {}
  },
  "flows": []
}
```

Plans default to `STANDARD` mode and `V4` definition version. The system automatically sets empty tags for API Product plans to prevent false "needs redeploy" indicators. Keyless and OAuth plan types are not supported for API Products.

Manage plan lifecycle using these endpoints:
* Publish: POST to `/_publish`
* Deprecate: POST to `/_deprecate`
* Close: POST to `/_close`
* Update: PUT with the full plan definition

## Manage Subscriptions

Create a subscription to an API Product plan by sending a POST request to `/environments/{envId}/api-products/{id}/subscriptions`. The subscription must specify:
* `referenceType=API_PRODUCT`
* `referenceId` set to the product ID

Manage subscription lifecycle using these endpoints:
* Accept: POST to `/_accept`
* Reject: POST to `/_reject`
* Close: POST to `/_close`
* Pause: POST to `/_pause`
* Resume: POST to `/_resume`
* Transfer: POST to `/_transfer`

The gateway sets the `ATTR_API_PRODUCT` context attribute and exposes `apiProductId` in the Expression Language context for product subscriptions. API key lookup supports both `API` and `API_PRODUCT` reference types via `findByKeyAndReferenceIdAndReferenceType()`.

## Client Configuration

Clients consume APIs within an API Product using the same authentication mechanisms as individual API subscriptions:
* **API Key plans**: Include the key in the `X-Gravitee-Api-Key` header or as a query parameter
* **JWT plans**: Provide the token in the `Authorization: Bearer` header
* **mTLS plans**: Present the client certificate during TLS handshake

The gateway validates subscriptions against the API Product first, then checks API-level plans if no product subscription matches. Flow conditions can reference the API Product ID to execute product-specific policies.
