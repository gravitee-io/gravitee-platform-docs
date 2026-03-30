---
hidden: true
noIndex: true
---

# Tag key migration upgrade procedure

<!-- DISCREPANCY: This page was placed in 4.11 by the agent, but the feature is merged in APIM 4.12.x only (confirmed by Okhelifi and verified from git history + Liquibase v4_12_0 directory). Move this file to docs/apim/4.12/ once that folder exists. -->

## Overview

When upgrading to APIM 4.12, an automated migration adds a `key` field to all existing tags. This migration runs once during the platform upgrade and doesn't require manual intervention.

## What the migration does

The migration runs automatically during startup (execution order 716). For each existing tag, it:

1. Reads the current `id` value.
2. Copies that `id` value into the new `key` field.
3. Saves the updated tag.

Existing tag IDs aren't changed. This preserves backward compatibility and allows rollback to a previous APIM version without database conflicts.

<!-- Verified from TagKeyUpgrader.java: tag.setKey(tag.getId()) — the ID is preserved, not regenerated as a UUID. Confirmed by Okhelifi: "to allow customer to rollback to a previous APIM version, during the migration the existing tags will keep the same ids." -->

**Example:**

```text
Before migration:
Tag { id: "international", key: null, name: "International" }

After migration:
Tag { id: "international", key: "international", name: "International" }
```

Only new tags created after migration receive a UUID as their `id`.

## Prerequisites

- The database schema includes the `tags.key` column, added automatically via Liquibase migration (`v4_12_0/00_add_tags_key_column.yml`).

<!-- Verified: Liquibase changelog is at gravitee-apim-repository-jdbc/src/main/resources/liquibase/changelogs/v4_12_0/00_add_tags_key_column.yml. Agent draft incorrectly referenced "09_add_tags_key_column.yml". -->

## Post-migration changes

After migration:

- All tag REST API endpoints use the tag `key` in path parameters instead of the `id`. For existing tags, the `key` equals the old `id`, so existing API calls continue to work.
- New tags created via the API require a `key` field in the request body.
- API clients that create new tags and store the `id` for later reference need to use the `key` for subsequent operations (GET, PUT, DELETE), not the UUID `id`.

For the full list of affected endpoints, see [Tag entity schema and key field reference](../reference/data-model/tag-entity-schema-and-key-field-reference.md#rest-api-endpoints).

{% hint style="info" %}
If the migration encounters an error, it logs a failure message and the platform continues to start. Check the application logs for details and contact support if tag operations don't work as expected after upgrade.
{% endhint %}
