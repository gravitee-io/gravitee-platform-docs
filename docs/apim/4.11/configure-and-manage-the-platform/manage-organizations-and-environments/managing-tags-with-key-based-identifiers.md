# Managing Tags with Key-Based Identifiers

## Creating Tags

To create a tag, submit a `NewTagEntity` payload with a unique `key` and `name`.

**Example request:**

```json
{
  "key": "products",
  "name": "Products",
  "description": "Product APIs"
}
```

The `key` must be 1-64 characters and serves as the stable identifier for all subsequent operations. After creation, the tag is accessible at `/tags/products`. If a tag with the same name already exists in the reference scope, the request fails.

## Updating and Deleting Tags

Update a tag by sending a `PUT` request to `/tags/{tagKey}` with an `UpdateTagEntity` payload containing the new `name`, `description`, or `restrictedGroups`. The `key` cannot be changed after creation.

Delete a tag by sending a `DELETE` request to `/tags/{tagKey}`.

## End-User Configuration

### Tag Entity Schema

**Response Model (TagEntity):**

```json
{
  "id": "1d114170-466d-4952-9141-70466de95213",
  "key": "products",
  "name": "Products",
  "description": "Product-related APIs",
  "restrictedGroups": ["product-team"]
}
```

**Create Request (NewTagEntity):**

```json
{
  "key": "products",
  "name": "Products",
  "description": "Product-related APIs",
  "restrictedGroups": ["product-team"]
}
```

**Update Request (UpdateTagEntity):**

```json
{
  "name": "Products",
  "description": "Updated description",
  "restrictedGroups": ["product-team"]
}
```

### Management API

| Endpoint | Method | Path Parameter | Description |
|:---------|:-------|:---------------|:------------|
| Get Tag | GET | `/tags/{tag}` | Retrieve tag by key |
| Update Tag | PUT | `/tags/{tag}` | Update tag by key |
| Delete Tag | DELETE | `/tags/{tag}` | Delete tag by key |

Path parameters now accept tag keys instead of IDs. Clients using ID-based references must update to key-based lookups.

## Restrictions

- Tag names must be unique within a reference scope (organization or environment)
- Tag keys must be 1-64 characters and unique within a reference scope
- Tag keys cannot be changed after creation
- Existing API clients using ID-based tag references in URL paths will break after migration
- OpenAPI imports now store tag keys instead of IDs in API definitions
