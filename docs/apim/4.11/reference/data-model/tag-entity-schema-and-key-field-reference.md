# Tag Entity Schema and Key Field Reference

## Key Concepts

### Tag Identifiers

Tags use two distinct identifiers: an internal UUID (`id`) for database references and a human-readable key (`key`) for API operations. The `key` field stores the original tag identifier (previously stored in `id`), while `id` is regenerated as a UUID during migration. All REST endpoints now accept tag keys instead of IDs in path parameters.

| Field | Format | Purpose | Example |
|:------|:-------|:--------|:--------|
| `id` | UUID | Internal database reference | `70237305-6f68-450e-a373-056f68750e50` |
| `key` | String (max 64 chars) | User-facing identifier for API operations | `international` |
| `name` | String (max 64 chars) | Display name | `International` |

### Tag Entity Schema

The Tag entity includes `id`, `key`, `name`, `description`, and `restrictedGroups`. When creating a tag, both `key` and `name` are required and must be 1-64 characters. The `key` field is immutable after creation — update operations no longer accept an `id` field in the request body. Tag lookups and filtering now use the `key` field for all repository queries.

#### Tag Entity Properties

| Property | Type | Required | Constraints | Description |
|:---------|:-----|:---------|:------------|:------------|
| `id` | String (UUID) | Yes | Auto-generated | Internal database reference |
| `key` | String | Yes | 1-64 characters, immutable | User-facing identifier for API operations |
| `name` | String | Yes | 1-64 characters, unique within reference scope | Display name |
| `description` | String | No | — | Tag description |
| `restrictedGroups` | Array of Strings | No | — | Groups with access to this tag |

#### Tag Creation and Validation

During tag creation, the `key` field is processed using `IdGenerator.generate(tagEntity.getKey())`. The `name` field must be unique within the same reference scope — duplicate names trigger a `DuplicateTagNameException`.

### Tag Lookup Behavior

All tag repository operations now use key-based queries instead of ID-based queries. Single tag lookups call `findByKeyAndReference(key, ...)`, and bulk operations use `findByKeysAndReference(Set<String> keys, ...)`. Tag validation accepts a set of tag keys and throws `TagNotFoundException` with an array of missing keys if any key is not found. Empty input sets return immediately without querying the repository.

## Prerequisites

Database schema must include the `tags.key` column before tag operations can use key-based lookups. This column is added via Liquibase changelog `09_add_tags_key_column.yml` and is nullable during migration but required after the `TagKeyUpgrader` runs.
