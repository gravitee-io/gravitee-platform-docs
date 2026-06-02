
# API Import from Remote URL (REST API Reference)

To update an existing v4 API from a remote URL, use the REST API endpoints described below. The backend fetches the definition server-side and applies the changes to the API. All URL validation and SSRF protection rules apply. The update operation requires `API_DEFINITION[UPDATE]` permission.


### Gravitee Definition

**Endpoint:**

```http
PUT /environments/{envId}/apis/{apiId}/_import/definition-url
```

**Request:**

```http
Content-Type: text/plain

https://example.com/api-definition.json
```

**Response:** `200 OK` with `ApiV4` JSON body

**Description:** Updates an existing v4 API by fetching a Gravitee export from the provided URL. The URL must be permitted by the configured import whitelist.

### OpenAPI Specification

**Endpoint:**

```
PUT /environments/{envId}/apis/{apiId}/_import/swagger
```

**Request:**

```
Content-Type: application/json

{
  "payload": "https://example.com/openapi.yaml",
  "type": "URL",
  "withDocumentation": true,
  "withOASValidationPolicy": false
}
```

**Response:** `200 OK` with `ApiV4` JSON body

**Description:** Updates an existing v4 API by fetching an OpenAPI descriptor from the provided URL. The URL must be permitted by the configured import whitelist.

**ImportSwaggerDescriptor Fields:**

| Field | Type | Required | Description |
|:------|:-----|:---------|:------------|
| `payload` | string | Yes | The URL to fetch the OpenAPI specification from |
| `type` | string | Yes | Must be `URL` for remote imports. Defaults to `INLINE` if omitted |
| `withDocumentation` | boolean | No | Whether to import documentation from the OpenAPI specification |
| `withOASValidationPolicy` | boolean | No | Whether to add an OAS validation policy to the API |
