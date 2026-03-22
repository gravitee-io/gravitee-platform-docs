# Tag Key Migration: Schema and Database Changes

## Migration Impact

The migration from ID-based to key-based tag references affects the following components:

* **Database schema**: The `tags` table receives a new `key` column via Liquibase changelog `09_add_tags_key_column.yml`
* **Data migration**: TagKeyUpgrader (order 715) executes at startup, copying existing `id` values to the new `key` field and generating new UUIDs for `id`
* **Repository layer**: Query methods transition from `findByIdAndReference` to `findByKeyAndReference` and from `findByIdsAndReference` to `findByKeysAndReference`
* **OpenAPI import**: Tag references in API definitions now store keys instead of IDs
* **Error handling**: `TagNotFoundException` reports missing keys instead of missing IDs
* **API model**: `UpdateTagEntity` no longer includes an `id` field. Updates reference tags via the `key` path parameter


