# Tag Key Migration Guide

## Overview

Tag Key Migration introduces a new `key` field to the Tag model, separating human-readable identifiers from internal database IDs. Existing tags are automatically migrated from ID-based to key-based lookups during upgrade. This change affects API administrators managing tags and developers integrating with tag-related endpoints.

## Key Concepts

### Tag Identifier Model

Tags now use two distinct identifiers: a UUID-based `id` for internal database operations and a human-readable `key` for API references and lookups. The `key` field stores the original tag identifier (up to 64 characters), while the `id` field contains a generated UUID. All tag lookups in REST API endpoints and service methods now use the `key` field instead of `id`.

### Tag Entity Schema

The Tag entity schema includes three variants for different operations:

| Field | TagEntity (response) | NewTagEntity (create) | UpdateTagEntity (update) |
|:------|:---------------------|:----------------------|:-------------------------|
| `id` | UUID string | — | — |
| `key` | 1-64 chars, unique | 1-64 chars, required | — |
| `name` | 1-64 chars | 1-64 chars, required | 1-64 chars, required |
| `description` | string | string | string |
| `restrictedGroups` | array of strings | array of strings | array of strings |

### Tag Lookup Operations

Tag lookup operations have been updated to use key-based queries:

| Operation | Method | Lookup Field |
|:----------|:-------|:-------------|
| Find single tag | `findByKeyAndReference(key, ...)` | `key` |
| Find multiple tags | `findByKeysAndReference(keys, ...)` | `key` |
| Delete tag | `delete(key)` | `key` (resolves to ID internally) |
| Update tag | `update(tagKey, UpdateTagEntity)` | `key` |

## Prerequisites

- Gravitee API Management platform with existing tag data
- Database schema migration support (Liquibase or MongoDB)
- Administrative access to execute upgrader tasks

## Gateway Configuration

### Database Schema

The migration adds a new column to the `tags` table:

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `tags.key` | `nvarchar(64)` | `null` | Stores the tag key; populated during migration with original tag ID values |

## Creating Tags

To create a tag, submit a `NewTagEntity` request with a unique `key` (1-64 characters), a `name` (1-64 characters), and optional `description` and `restrictedGroups` fields. The system generates a UUID for the internal `id` field and validates that the `name` does not duplicate an existing tag. If a duplicate name is detected, the request fails with `DuplicateTagNameException`. The `key` is generated using `IdGenerator.generate(tagEntity.getKey())` and must be unique within the reference scope.

## Managing Tags

To update a tag, send a `PUT` request to `/tags/{tagKey}` with an `UpdateTagEntity` payload containing the updated `name`, `description`, and `restrictedGroups`. The `tagKey` path parameter must match an existing tag's `key` field; the request body no longer includes an `id` field. To delete a tag, send a `DELETE` request to `/tags/{tagKey}`, where `tagKey` is the tag's `key` value. The system resolves the key to the internal ID and removes the tag record. Tag validation during API operations checks for the existence of all referenced keys and throws `TagNotFoundException` with an array of missing keys if any are not found.

## End-User Configuration

### Management API Endpoints

**GET `/tags/{tag}`**

Retrieves a single tag by its `key` value. The `tag` path parameter expects a key, not an ID.

**PUT `/tags/{tag}`**

Updates a tag identified by `tagKey`. The request body is an `UpdateTagEntity` without the `id` field. Returns `200 OK` with the updated tag entity.

**DELETE `/tags/{tag}`**

Deletes a tag identified by its `key` value. The `tag` path parameter expects a key.

## Restrictions

- Tag `key` field is limited to 64 characters
- Tag `name` field is limited to 64 characters
- Tag `key` must be unique within the reference scope
- Tag `name` must be unique (duplicate names trigger `DuplicateTagNameException`)
- REST API path parameters for tag operations now require `key` values instead of `id` values
- `UpdateTagEntity` no longer accepts an `id` field in the request body
- Tag validation methods check `keys` instead of `ids`

## Related Changes

The migration introduces a Liquibase changelog (`09_add_tags_key_column.yml`) that adds the `key` column to the `tags` table. A data upgrader (`TagKeyUpgrader`, execution order 715) automatically migrates existing tags by copying the old `id` value to the new `key` field and generating a new UUID for the `id` field. JDBC and MongoDB repository implementations have been updated to support key-based queries, with JDBC using `escapeReservedWord("key")` to handle reserved SQL keywords. Test data fixtures now include UUID-format `id` values and human-readable `key` values. Error messages in repository methods have been updated from "by id" to "by key" to reflect the new lookup mechanism.
