# Tag Key Migration: Conceptual Model

## Overview

The Tag Key Migration introduces a dedicated `key` field to the Tag entity, separating the user-facing identifier from the internal UUID-based `id`. This change affects API administrators managing tags and developers integrating with the Tags REST API. Existing tags are automatically migrated from ID-based to key-based lookups during platform upgrade.

## Key Concepts

### Tag Identifier Structure

Tags now use two distinct identifiers:

| Field | Format | Purpose | Example |
|:------|:-------|:--------|:--------|
| `id` | UUID string | Internal system reference | `1d114170-466d-4952-9141-70466de95213` |
| `key` | String (1-64 chars) | User-facing identifier used in API paths | `products` |
| `name` | String (1-64 chars) | Display name | `Products` |

The `id` field stores a system-generated UUID for internal references. The `key` field stores a user-defined identifier used in REST API paths and tag lookups. After migration, existing tag IDs become keys, and new UUIDs are assigned to the `id` field.

### Tag Lookup Behavior

All tag lookup operations now use the `key` field instead of `id`. REST endpoints accept tag keys in path parameters. Repository methods have changed:

| Operation | Before | After |
|:----------|:-------|:------|
| Find by identifier | `findByIdAndReference(tagId, ...)` | `findByKeyAndReference(key, ...)` |
| Find multiple | `findByIdsAndReference(Set<String> ids, ...)` | `findByKeysAndReference(Set<String> keys, ...)` |
| REST endpoint path | `GET /tags/{tagId}` | `GET /tags/{tagKey}` |
| REST update path | `PUT /tags/{tagId}` | `PUT /tags/{tagKey}` |
| REST delete path | `DELETE /tags/{tagId}` | `DELETE /tags/{tagKey}` |

Tag validation checks for key existence and throws `TagNotFoundException` with an array of missing keys if any are not found.

### Automatic Migration

The `TagKeyUpgrader` runs automatically during platform upgrade with execution order 715. For each existing tag, the upgrader:

1. Generates a new UUID for the `id` field
2. Copies the old `id` value to the `key` field
3. Creates a new tag record
4. Deletes the old record

**Migration Example:**

```java
// Before migration
Tag { id: "products", name: "Products", key: null }

// After migration
Tag { id: "1d114170-466d-4952-9141-70466de95213", key: "products", name: "Products" }
```

If migration fails, the upgrader logs `"Failed to migrate sharding tags"` and returns `false`.
