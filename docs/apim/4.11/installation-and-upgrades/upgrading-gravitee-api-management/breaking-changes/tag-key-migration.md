
# Tag Key Migration: Integration and Repository Changes

This article documents the technical changes required to migrate from ID-based to key-based tag references. For migration context and upgrade procedures, see the [Tag Key Migration Upgrade Guide](upgrade-guide-tag-key-migration.md).

## Related Changes


The `TagEntity` response model now includes both `id` (UUID) and `key` (string) fields. The `NewTagEntity` creation request requires a `key` field with 1–64 character validation. The `UpdateTagEntity` request removes the `id` field entirely. Repository interfaces replace `findByIdAndReference()` with `findByKeyAndReference()` and `findByIdsAndReference()` with `findByKeysAndReference()`. JDBC implementations update SQL `WHERE` clauses from `id = ?` to `key = ?` with reserved word escaping. MongoDB implementations rename methods from `findByIdAndReferenceIdAndReferenceType()` to `findByKeyAndReferenceIdAndReferenceType()`. OpenAPI import workflows use `findTagKeyByName()` instead of `findTagIdByName()` to resolve tag references. User access checks return both `id` and `key` values via `findByUser()`. Error messages reference "key" instead of "id" in `TagNotFoundException` and repository failure logs.
