# Creating API Navigation Items

## Bulk Creating API Items

For adding multiple API items at once, use the bulk create endpoint with a request body containing an `items` array. Each item in the array follows the same validation rules as single creation: `type` must be `API`, `area` must be `TOP_NAVBAR`, `parentId` and `apiId` are required, and each `apiId` must be unique across both the request and existing navigation items (enforced by unique `apiId` [constraint](#api-navigation-item-properties)).

**POST** `/environments/{envId}/portal-navigation-items/_bulk`

**Request Body:**

```json
{
  "items": [
    {
      "title": "API 2",
      "type": "API",
      "area": "TOP_NAVBAR",
      "parentId": "folder-id",
      "visibility": "PUBLIC",
      "apiId": "api-2"
    },
    {
      "title": "API 3",
      "type": "API",
      "area": "TOP_NAVBAR",
      "parentId": "folder-id",
      "visibility": "PUBLIC",
      "apiId": "api-3"
    }
  ]
}
```

The endpoint returns a `200 OK` response with the full array of created items including generated IDs.

**Response:**

```json
{
  "items": [
    { "id": "nav-api-1", "title": "API 2", "type": "API", "apiId": "api-2", ... },
    { "id": "nav-api-2", "title": "API 3", "type": "API", "apiId": "api-3", ... }
  ]
}
```

## Related Changes

The Redoc dependency version `2.4.0` has been added to `package.json` to support local bundling.
