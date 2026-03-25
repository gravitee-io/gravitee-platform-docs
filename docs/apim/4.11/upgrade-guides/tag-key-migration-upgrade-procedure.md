# Tag Key Migration Upgrade Procedure

## Gateway Configuration

The `TagKeyUpgrader` performs a one-time automated migration during platform upgrade. The upgrader:

1. Reads all existing tags from the repository.
2. For each tag:
   * Generates a new UUID for the `id` field.
   * Copies the old `id` value to the `key` field.
   * Creates a new tag record with the updated fields.
   * Deletes the old tag record using the old ID.

The `tags.key` column is nullable to support incremental migration. After the upgrader runs, the column becomes required for all new tags.

**Example migration:**

```
Before migration:
Tag { id: "international", key: null, name: "International" }

After migration:
Tag { id: "70237305-6f68-450e-a373-056f68750e50", key: "international", name: "International" }
```

If the migration fails, the upgrader returns `false` and logs an error message.
