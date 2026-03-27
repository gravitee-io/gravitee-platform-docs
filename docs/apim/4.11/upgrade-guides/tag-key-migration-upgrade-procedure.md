# Tag key migration upgrade procedure

## Prerequisites

- Database schema must include the `tags.key` column. This column is added via Liquibase changelog `09_add_tags_key_column.yml`.
- The `tags.key` column is nullable to support incremental migration but becomes required after the upgrader runs.

## Database schema

The `tags` table includes a new `key` column to store tag keys.

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `tags.key` | `nvarchar(64)` | `null` | Tag key for API operations and lookups |

## Migration process

The `TagKeyUpgrader` (execution order 715) performs a one-time automated migration during platform upgrade. The upgrader:

1. Reads all existing tags from the repository.
2. For each tag:
    * Generates a new UUID for the `id` field.
    * Copies the old `id` value to the `key` field.
    * Creates a new tag record with the updated fields.
    * Deletes the old tag record using the old ID.

**Example migration:**

```text
Before migration:
Tag { id: "international", key: null, name: "International" }

After migration:
Tag { id: "international", key: "international", name: "International" }
```

If the migration fails, the upgrader returns `false` and logs an error message.

## Post-migration changes

After migration:

- All tag repository operations use key-based queries instead of ID-based queries.
- Error messages in repository implementations reference "by key" instead of "by id".
- API clients must use tag keys instead of tag IDs in path parameters. For the full list of affected endpoints, see [Tag entity schema and key field reference](../reference/data-model/tag-entity-schema-and-key-field-reference.md#rest-api-endpoints).