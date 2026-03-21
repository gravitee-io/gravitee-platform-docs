# Tag Management API Reference

## Managing Tags

Update a tag by sending a PUT request to `/tags/{tag}`, where `{tag}` is the tag's `key` value (not the UUID `id`). The request body (`UpdateTagEntity`) accepts updated `name`, `description`, and `restrictedGroups` values. The `key` and `id` fields are immutable and preserved during updates. Delete a tag by sending a DELETE request to `/tags/{tag}` using the tag's `key`. Deletion removes the tag from all associated APIs via the `apiTagService` and cannot be undone. Retrieve a single tag by key using GET `/tags/{tag}`.

## End-User Configuration

### Tag API Endpoints

All tag management endpoints now use the `key` field as the path parameter instead of the internal `id`.

| Endpoint | Method | Path Parameter | Description |
|:---------|:-------|:---------------|:------------|
| `/tags/{tag}` | GET | `{tag}` = tag key | Retrieve tag by key |
| `/tags/{tag}` | PUT | `{tag}` = tag key | Update tag name, description, or restricted groups |
| `/tags/{tag}` | DELETE | `{tag}` = tag key | Delete tag and remove from all APIs |

### Tag Request Models

**NewTagEntity** (create request):

```json
{
  "key": "string",
  "name": "string",
  "description": "string",
  "restrictedGroups": ["string"]
}
```

**UpdateTagEntity** (update request):

```json
{
  "name": "string",
  "description": "string",
  "restrictedGroups": ["string"]
}
```

**TagEntity** (response):

```json
{
  "id": "string",
  "key": "string",
  "name": "string",
  "description": "string",
  "restrictedGroups": ["string"]
}
```
