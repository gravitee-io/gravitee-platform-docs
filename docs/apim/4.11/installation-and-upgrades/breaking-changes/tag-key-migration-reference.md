# Tag Key Migration Reference

## Overview

Tag Key Migration introduces a dedicated `key` field to the Tag model, decoupling user-facing tag identifiers from internal UUIDs. Tags are now referenced by human-readable keys instead of auto-generated IDs, improving API usability and OpenAPI import workflows. This change applies to all tag operations in the Management API and requires a one-time data migration.

## Key Concepts

### Tag Identifier Model

Tags now use two distinct identifiers: an internal UUID `id` for database relationships and a user-defined `key` for API operations. The `key` field stores the original tag identifier (previously stored in `id`), while `id` is regenerated as a UUID during migration. All Management API endpoints now accept tag keys in path parameters instead of IDs.

| Field | Type | Constraints | Purpose |
|:------|:-----|:------------|:--------|
| `id` | string (UUID) | Auto-generated | Internal database identifier |
| `key` | string | 1–64 characters, unique per reference | User-facing identifier for API operations |
| `name` | string | 1–64 characters | Display name |
| `description` | string | Optional | Tag description |
| `restrictedGroups` | array | Optional | Group-based access control |

### Tag Lookup Behavior

All tag lookup operations now use keys instead of IDs. The `findByKeyAndReference()` and `findByKeysAndReference()` repository methods replace ID-based lookups. Tag existence validation checks keys and throws `TagNotFoundException` with the missing key values. User tag filtering returns both the internal ID and key for each accessible tag to support legacy integrations during transition.

### OpenAPI Import Mapping

OpenAPI import now maps tag names from OpenAPI specifications to tag keys (previously mapped to IDs). The `findTagKeyByName()` method resolves tag names to keys, and API definitions store tag keys in the `tags` field. This ensures imported APIs reference tags using stable, human-readable identifiers.

## Prerequisites

- Gravitee API Management platform with existing tag data
- Database schema version supporting the `tags.key` column (Liquibase changelog `09_add_tags_key_column.yml` applied)
- Completion of the `TagKeyUpgrader` migration (execution order 715) before using key-based tag operations

## Creating Tags

Create a tag by submitting a `NewTagEntity` to `POST /tags` with a required `key` field (1–64 characters), `name` (1–64 characters), optional `description`, and optional `restrictedGroups` array. The system generates a UUID for the internal `id` and derives a normalized key identifier from the provided `key` value using `IdGenerator.generate()`. Duplicate tag names are rejected with `DuplicateTagNameException`. The response returns a `TagEntity` containing both the generated `id` and the user-provided `key`.

## Managing Tags

Update a tag by sending a `PUT /tags/{tag}` request where `{tag}` is the tag key (not the ID). The request body (`UpdateTagEntity`) includes `name`, `description`, and `restrictedGroups` but excludes the `id` field. The system looks up the tag by key, updates the specified fields, and preserves the existing `id` and `key` values. Delete a tag using `DELETE /tags/{tag}` with the tag key; the system resolves the key to the internal ID, deletes the tag record, and removes all tag references from associated APIs via `apiTagService.deleteTagFromAPIs()`.

## End-User Configuration

### Management API Endpoints

| Endpoint | Method | Path Parameter | Request Body | Response |
|:---------|:-------|:---------------|:-------------|:---------|
| Get Tag | `GET /tags/{tag}` | `{tag}` = tag key | N/A | `TagEntity` |
| Update Tag | `PUT /tags/{tag}` | `{tag}` = tag key | `UpdateTagEntity` | `UpdateTagEntity` |
| Delete Tag | `DELETE /tags/{tag}` | `{tag}` = tag key | N/A | N/A |

### Tag Entity Properties

| Property | Type | Constraints | Description |
|:---------|:-----|:------------|:------------|
| `key` | string | Required on create; 1–64 characters | User-facing tag identifier |
| `name` | string | Required; 1–64 characters | Tag display name |
| `description` | string | Optional | Tag description |
| `restrictedGroups` | array | Optional | Group IDs with access to this tag |

## Restrictions

- Tag keys must be unique within a reference scope (environment or organization)
- The `key` field cannot be modified after tag creation (updates use the key as a lookup parameter)
- Migration is one-way; rollback to ID-based tags is not supported
- Tag existence validation now throws `TagNotFoundException` with key values instead of IDs
- User tag filtering no longer bypasses group restrictions for environment administrators; all users are subject to `restrictedGroups` filtering
- SQL implementations must escape the `key` column name as it is a reserved word in some databases

## Related Changes

The database schema adds a `tags.key` column (nvarchar(64), nullable). The `TagKeyUpgrader` migration (order 715) iterates all existing tags, copies the old `id` to the `key` field, generates a new UUID for `id`, and replaces the tag record. Repository implementations (JDBC and MongoDB) replace `findByIdAndReference()` and `findByIdsAndReference()` methods with `findByKeyAndReference()` and `findByKeysAndReference()`. Error messages in `TechnicalManagementException` change from "by id" to "by key" phrasing. Test fixtures update all tag records to include UUID-based `id` and string-based `key` fields. The OpenAPI import converter switches from `findTagIdByName()` to `findTagKeyByName()` for tag resolution.
