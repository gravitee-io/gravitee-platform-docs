# Tag Key Migration Reference

## Overview

Tag Key Migration introduces a new `key` field to the Tag model, separating the user-facing identifier from the internal UUID. Existing tags are migrated from ID-based lookups to key-based lookups, enabling stable, human-readable tag references across API definitions and imports. This change affects API administrators managing tags and developers integrating with the Management API.

## Key Concepts

### Tag Identifier Model

Tags now use two distinct identifiers: a `key` field for user-facing references (max 64 characters, unique within a reference scope) and an `id` field containing a UUID for internal storage. The `key` field replaces the previous ID-based lookup pattern, where the ID was generated from the tag name. After migration, existing tag IDs become keys, and new UUIDs are assigned to the `id` field.

| Field | Type | Purpose | Example |
|:------|:-----|:--------|:--------|
| `id` | UUID string | Internal database identifier | `1d114170-466d-4952-9141-70466de95213` |
| `key` | String (max 64 chars) | User-facing identifier for API references | `products` |
| `name` | String (max 64 chars) | Display name | `Products` |

### Tag Lookup Operations

All tag resolution operations now use the `key` field instead of `id`. Repository methods `findByKeyAndReference()` and `findByKeysAndReference()` replace the previous `findByIdAndReference()` and `findByIdsAndReference()` methods. Tag validation during API creation or update matches provided keys against the `key` field and throws `TagNotFoundException` with an array of missing keys if validation fails.

### Tag Entity Schema

The Tag entity schema includes three models for different operations:

**TagEntity** (response model):
```json
{
  "id": "1d114170-466d-4952-9141-70466de95213",
  "key": "products",
  "name": "Products",
  "description": "Product APIs",
  "restrictedGroups": ["group-id"]
}
```

**NewTagEntity** (create request):
```json
{
  "key": "products",
  "name": "Products",
  "description": "Product APIs",
  "restrictedGroups": ["group-id"]
}
```

**UpdateTagEntity** (update request):
```json
{
  "name": "Products",
  "description": "Product APIs",
  "restrictedGroups": ["group-id"]
}
```

The `key` field is required in `NewTagEntity`. The `id` field was removed from `UpdateTagEntity`; updates now use the `key` path parameter.


## Gateway Configuration

No gateway-level configuration changes are required for tag key migration.
