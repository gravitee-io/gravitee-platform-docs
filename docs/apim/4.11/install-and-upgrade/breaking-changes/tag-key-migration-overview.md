# Tag Key Migration Overview

## Overview

Tag Key Migration introduces a new `key` field to the Tag model, separating human-readable identifiers from internal UUIDs. Tags are now referenced by stable keys instead of auto-generated IDs, improving consistency across import/export workflows and API definitions. This change affects all tag-related API endpoints and requires a one-time data migration.

## Key Concepts

### Tag Identifier Model

Tags now use two distinct identifiers: `id` (internal UUID) and `key` (user-facing identifier). The `key` field stores a unique, human-readable string (max 64 characters) that replaces the previous role of `id` in API references and lookups. The `id` field is now a randomly generated UUID used only for internal database operations. Tag names remain separate and must be unique within an organization or environment scope.

### Tag Entity Structure

The Tag entity exposes both identifiers in API responses. The `key` field is required when creating tags and serves as the path parameter for update and delete operations. The `id` field is read-only and auto-generated. Tag names and descriptions support up to 64 characters, and tags can be restricted to specific user groups via the `restrictedGroups` array.

| Field | Type | Constraints | Purpose |
|:------|:-----|:------------|:--------|
| `id` | string (UUID) | Read-only, auto-generated | Internal database identifier |
| `key` | string | Required, 1-64 chars, unique per reference | User-facing identifier for API references |
| `name` | string | Required, 1-64 chars, unique per reference | Display name |
| `description` | string | Optional | Human-readable description |
| `restrictedGroups` | array | Optional | Group IDs with access to this tag |

### Tag Lookup Behavior

All tag lookup operations now use the `key` field instead of `id`. Repository methods `findByKeyAndReference` and `findByKeysAndReference` replace the previous ID-based queries. Tag existence validation checks keys against the database and throws `TagNotFoundException` if any requested keys are missing. API definitions, import workflows, and user filtering operations all reference tags by key.

## Prerequisites

- Gravitee API Management platform with existing tag data
- Database schema migration applied (Liquibase changelog `09_add_tags_key_column.yml`)
- Completion of `TagKeyUpgrader` data migration (upgrader order 715)
- API clients updated to use tag keys instead of IDs in requests

## Gateway Configuration

### Database Schema

The `tags` table includes a new column to store tag keys. This column is populated during the data migration process.

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `tags.key` | nvarchar(64) | null | Unique identifier for tag lookups and API references |

## Creating Tags

To create a tag, submit a POST request to the tags endpoint with a `NewTagEntity` payload. The request must include a unique `key` (1-64 characters) and a unique `name` (1-64 characters). The system generates a random UUID for the internal `id` field and derives a normalized key identifier from the provided `key` value.

