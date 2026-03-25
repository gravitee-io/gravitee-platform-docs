# Tag entity schema and key field reference

## Overview

Tag Key Migration introduces a dedicated `key` field to the Tag entity, separating human-readable tag identifiers from internal UUIDs. This change affects all tag management operations and API endpoints that reference tags. Existing tags are automatically migrated from ID-based to key-based lookups during platform upgrade.

## Tag identifiers

Tags use two distinct identifiers: an internal UUID (`id`) for database references and a human-readable key (`key`) for API operations. The `key` field stores the original tag identifier (previously stored in `id`), while `id` is regenerated as a UUID during migration. All REST endpoints accept tag keys instead of IDs in path parameters.

| Field | Format | Purpose | Example |
|:------|:-------|:--------|:--------|
| `id` | UUID | Internal database reference | `70237305-6f68-450e-a373-056f68750e50` |
| `key` | String (max 64 chars) | User-facing identifier for API operations | `international` |
| `name` | String (max 64 chars) | Display name | `International` |

## Tag entity properties

The Tag entity includes `id`, `key`, `name`, `description`, and `restrictedGroups`. When creating a tag, both `key` and `name` are required and must be 1-64 characters. The `key` field is immutable after creation — update operations don't accept an `id` field in the request body. Tag lookups and filtering use the `key` field for all repository queries.

| Property | Type | Required | Constraints | Description |
|:---------|:-----|:---------|:------------|:------------|
| `id` | String (UUID) | Yes | Auto-generated | Internal database reference |
| `key` | String | Yes (create only) | 1-64 characters, immutable | User-facing identifier for API operations |
| `name` | String | Yes | 1-64 characters, unique within reference scope | Display name |
| `description` | String | No | — | Tag description |
| `restrictedGroups` | Array of Strings | No | — | Groups with access to this tag |

## Tag lookup behavior

All tag repository operations use key-based queries instead of ID-based queries. Single tag lookups call `findByKeyAndReference(key, ...)`, and bulk operations use `findByKeysAndReference(Set<String> keys, ...)`. Tag validation accepts a set of tag keys and throws `TagNotFoundException` with an array of missing keys if any key isn't found. Empty input sets return immediately without querying the repository.

## REST API endpoints

All tag management endpoints use tag keys in path parameters instead of UUIDs.

| Endpoint | Method | Path parameter | Request body changes |
|:---------|:-------|:---------------|:---------------------|
| Get tag | GET | `/tags/{tag-key}` | N/A |
| Create tag | POST | `/tags` | Must include `key` field |
| Update tag | PUT | `/tags/{tag-key}` | `id` field removed |
| Delete tag | DELETE | `/tags/{tag-key}` | N/A |

### Create a tag

To create a tag, send a POST request to `/tags` with the following fields:

- `key` (required, 1-64 characters) — immutable tag identifier
- `name` (required, 1-64 characters) — must be unique within the reference scope
- `description` (optional)
- `restrictedGroups` (optional array)

The system generates a UUID for the internal `id` field. If a tag with the same `name` already exists, the operation fails with `DuplicateTagNameException`. The response includes both the generated `id` and the provided `key`.

### Manage tags

To retrieve a tag, send a GET request to `/tags/{tag-key}` using the tag's key (not its UUID).

To update a tag, send a PUT request to `/tags/{tag-key}` with `name`, `description`, and `restrictedGroups`. The `id` field is no longer accepted in update requests.

To delete a tag, send a DELETE request to `/tags/{tag-key}`.

## Repository configuration

JDBC repositories use `escapeReservedWord("key")` in SQL queries because `key` is a reserved word in some databases. MongoDB repositories replace the following methods:

- `findByIdAndReferenceIdAndReferenceType` → `findByKeyAndReferenceIdAndReferenceType`
- `findByIdInAndReferenceIdAndReferenceType` → `findByKeyInAndReferenceIdAndReferenceType`

## Restrictions

- Tag keys are immutable after creation — updates don't accept a `key` field.
- Tag names must be unique within the same reference scope (enforced by `DuplicateTagNameException`).
- The `key` field is limited to 64 characters.
- Path parameters in tag endpoints expect keys, not UUIDs — existing API clients using tag IDs will fail.

{% hint style="warning" %}
This is a breaking change. API clients that reference tags by ID in path parameters must be updated to use tag keys instead.
{% endhint %}

## Prerequisites

- Database schema must include the `tags.key` column (added via Liquibase changelog `09_add_tags_key_column.yml`).
- Existing tags must be migrated using the `TagKeyUpgrader` (execution order 715). For details, see [Tag key migration upgrade procedure](../../upgrade-guides/tag-key-migration-upgrade-procedure.md).
- API clients must be updated to use tag keys instead of tag IDs in path parameters.