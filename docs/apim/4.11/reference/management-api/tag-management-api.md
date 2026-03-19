
# Tag Management REST API Operations

## Creating a Tag


To create a tag, submit a `NewTagEntity` request to the Tags REST API:

1. Provide a unique `key` (1-64 characters) and `name` (1-64 characters).
2. Optionally include a `description` and `restrictedGroups` array.
3. The system generates a UUID for the `id` field and validates that the `name` does not duplicate an existing tag.
4. If the name already exists, the API returns `DuplicateTagNameException`.

**NewTagEntity Schema**:

| Property | Type | Validation | Description |
|:---------|:-----|:-----------|:------------|
| `key` | string | `@NotNull`, `@Size(min=1, max=64)` | Unique identifier for the tag |
| `name` | string | `@NotNull`, `@Size(min=1, max=64)` | Display name |
| `description` | string | — | Optional description |
| `restrictedGroups` | array of strings | — | Groups allowed to use this tag |

## Updating a Tag

To update a tag, send a `PUT` request to `/tags/{tagKey}` with an `UpdateTagEntity` payload:

1. The path parameter `{tagKey}` identifies the tag by its `key` field.
2. The request body includes `name` (1-64 characters), `description`, and `restrictedGroups`.
3. The system validates the tag exists by key and applies the changes.
4. If the key is not found, the API returns `TagNotFoundException`.

**UpdateTagEntity Schema**:

| Property | Type | Validation | Description |
|:---------|:-----|:-----------|:------------|
| `name` | string | `@NotNull`, `@Size(min=1, max=64)` | Display name |
| `description` | string | — | Optional description |
| `restrictedGroups` | array of strings | — | Groups allowed to use this tag |

## Tag Filtering by User

The `findByUser()` method returns both `id` and `key` values for each tag accessible to the user. Users see tags that are unrestricted or belong to their assigned groups.

**Example return value**:

A user with access to two tags receives:

```
Set.of(
  "1d114170-466d-4952-9141-70466de95213",  // tag ID
  "products",                               // tag key
  "70237305-6f68-450e-a373-056f68750e50",  // tag ID
  "international"                           // tag key
)
```

## Restrictions

- Tag `key` field is limited to 64 characters
- Tag `name` field is limited to 64 characters
- Tag `key` must be unique within the reference scope (organization or environment)
- Tag `name` must be unique within the reference scope
- REST API path parameters now require `key` values instead of `id` values
- Migration failure prevents platform upgrade completion
- SQL reserved word `"key"` requires escaping in JDBC queries

