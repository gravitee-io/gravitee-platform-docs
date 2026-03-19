
# Tag Management API Operations

## Creating a Tag


Submit a `POST` request to `/tags` with a `NewTagEntity` payload containing the required `key` and `name` fields (both 1–64 characters). Optionally include `description` and `restricted_groups` arrays. The system validates key uniqueness within the reference scope and name uniqueness across all tags. On success, the API returns a `TagEntity` with a generated UUID `id`, the provided `key`, and all submitted metadata.

**Example request body**:

```json
{
  "key": "products",
  "name": "Products",
  "description": "Product APIs"
}
```

## Updating a Tag

Submit a `PUT` request to `/tags/{tagKey}` with an `UpdateTagEntity` payload containing the updated `name` (required, 1–64 characters) and optional `description` or `restricted_groups`. The `key` is passed as a path parameter and cannot be modified. The `id` field is no longer accepted in the request body. The system validates that the tag exists and that the new name does not conflict with other tags.

## Deleting a Tag

Submit a `DELETE` request to `/tags/{tagKey}` where `{tagKey}` is the tag's key value (not the UUID). The system removes the tag record and all associated references. If the key does not exist, the API returns a `TagNotFoundException` with the missing key in the error payload.

## Importing Tags from OpenAPI Definitions

When importing OpenAPI definitions, the system matches tags by `name` and resolves them to `key` values for storage in the API entity. For example, an OpenAPI definition with `tags: ["Products", "International"]` is resolved to keys `["products", "international"]` using the `findTagKeyByName()` method. If a tag name does not match an existing tag, the import process creates a new tag with a generated key or fails validation depending on configuration.

## Restrictions

* Tag keys must be 1–64 characters and are validated at creation time
* Tag names must be 1–64 characters and unique across all tags
* The `key` field cannot be modified after tag creation
* Migration from ID-based to key-based tags is one-way and does not support rollback
