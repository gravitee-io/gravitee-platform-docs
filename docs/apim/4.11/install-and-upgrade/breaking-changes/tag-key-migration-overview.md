# Tag Key Migration Overview

## Overview

Tag Key Migration introduces a new `key` field to the Tag model, separating user-facing identifiers from internal UUIDs. Tags are now referenced by human-readable keys instead of auto-generated IDs. This change affects tag creation, lookup, and all API endpoints that reference tags.

## Key Concepts

### Tag Identifier Model

Tags use a dual-identifier model. The `id` field stores a system-generated UUID for internal use, while the `key` field stores a user-defined identifier for API operations and references. After migration, existing tag IDs become keys, and new UUIDs are assigned as IDs.

| Field | Type | Purpose | Example |
|:------|:-----|:--------|:--------|
| `id` | UUID string | Internal system identifier | `1d114170-466d-4952-9141-70466de95213` |
| `key` | String (max 64 chars) | User-facing identifier for API operations | `products` |
| `name` | String (max 64 chars) | Display name | `Products` |

### Tag Lookup Behavior

All tag lookup operations use the `key` field instead of `id`. Repository methods query by `key` and `reference` combinations. Tag validation checks for key existence and throws `TagNotFoundException` with an array of missing keys if validation fails.

### Tag Entity Schema

The Tag entity includes three representations:

**TagEntity** (response model) returns `id`, `key`, `name`, `description`, and `restrictedGroups`.

**NewTagEntity** (create request) requires `key` and `name` fields with size constraints (min 1, max 64 characters).

**UpdateTagEntity** (update request) requires only `name` and optional `description` and `restrictedGroups`. The key is provided as a path parameter and can't be changed.

## Prerequisites

* Gravitee API Management platform with tag support
* Database schema version supporting the `tags.key` column (added via Liquibase changelog `09_add_tags_key_column.yml`)
* Completion of `TagKeyUpgrader` migration (execution order 715) before using key-based operations

## Gateway Configuration

### Database Schema

The `tags` table includes a new column to store tag keys.

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `tags.key` | `nvarchar(64)` | `null` | Unique identifier for tag, used in API operations and references |

## Creating Tags

To create a tag, send a POST request to `/tags` with a JSON body containing `key`, `name`, and optional `description` and `restrictedGroups` fields. The `key` must be unique, between 1 and 64 characters, and will be used for all subsequent operations.

