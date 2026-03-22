# Managing Tags with Key-Based Identifiers

## Prerequisites

Before using key-based tag operations, complete the following steps:

* Complete the database schema migration
* Update existing API definitions that reference tags by ID to use keys
* Verify that OpenAPI import definitions using `x-graviteeio-definition.tags` automatically resolve tag names to keys

## Gateway Configuration

No gateway-level configuration changes are required for tag key migration.

## Creating Tags

To create a tag, submit a `NewTagEntity` to the Management API with the following fields:

* `key` (required): A unique identifier for the tag, limited to 64 characters
* `name` (required): The display name for the tag, limited to 64 characters
* `description` (optional): A description of the tag
* `restrictedGroups` (optional): An array of group identifiers that can access the tag

The system generates a UUID for the internal `id` field and derives the `key` from the provided value using `IdGenerator.generate(tagEntity.getKey())`. The `key` must be unique within the reference scope (organization or environment). If a tag with the same name already exists, the system throws `DuplicateTagNameException`.

## Managing Tags

To update a tag, send a `PUT` request to `/tags/{tagKey}` with an `UpdateTagEntity` payload containing the updated `name`, `description`, and `restrictedGroups`. The `tagKey` path parameter must match an existing tag's `key` field.

To delete a tag, send a `DELETE` request to `/tags/{tagKey}`. The system internally resolves the key to the UUID ID before deletion.

To retrieve a tag, send a `GET` request to `/tags/{tagKey}`.

## End-User Configuration

### Management API Endpoints

| Endpoint | Method | Path Parameter | Description |
|:---------|:-------|:---------------|:------------|
| `/tags/{tag}` | `GET` | `tag` (key) | Retrieve tag by key |
| `/tags/{tag}` | `PUT` | `tag` (key) | Update tag by key |
| `/tags/{tag}` | `DELETE` | `tag` (key) | Delete tag by key |

### Database Schema

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `tags.key` | `nvarchar(64)` | `null` | Tag key column added to `tags` table |

## Restrictions

* The `key` field is limited to 64 characters
* Tag keys must be unique within a reference scope (organization or environment)
* Migration is one-way; rollback is not supported
* After migration, API definitions must reference tags by `key` instead of `id`
* The `id` field in `UpdateTagEntity` was removed; updates require the `key` path parameter
* Tag filtering operations (`findByUser()`) return both UUID IDs and keys for backward compatibility during transition

## Related Changes

The database schema adds a `tags.key` column via Liquibase changelog `09_add_tags_key_column.yml`. Repository implementations (JDBC and MongoDB) add `findByKeyAndReference()` and `findByKeysAndReference()` methods, with JDBC using `escapeReservedWord("key")` for SQL compatibility. The `TagKeyUpgrader` (execution order 715) migrates existing tags by generating new UUIDs for the `id` field and moving old IDs to the `key` field. OpenAPI import logic (`OAIToAPIConverter`) now maps tag names to keys instead of IDs. Test fixtures update tag IDs from name-based strings (e.g., `"international"`) to UUIDs (e.g., `"70237305-6f68-450e-a373-056f68750e50"`), with keys preserving the original identifier.
