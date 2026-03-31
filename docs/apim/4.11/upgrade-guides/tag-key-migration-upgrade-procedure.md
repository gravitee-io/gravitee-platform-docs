---
hidden: true
noIndex: true
---

# Tag key migration upgrade procedure

<!-- DISCREPANCY: This page was placed in 4.11 by the agent, but the feature is merged in APIM 4.12.x only (confirmed by Okhelifi and verified from git history + Liquibase v4_12_0 directory). Move this file to docs/apim/4.12/ once that folder exists. -->

## Overview

When upgrading to APIM 4.12, an automated migration adds a `key` field to all existing tags and tenants. This migration runs once during the platform upgrade and doesn't require manual intervention.

Tags and tenants now use a dedicated `key` field for identification and assignment operations, replacing the previous reliance on auto-generated `id` values. This change enables human-readable, stable identifiers for sharding tag selection in plan deployment and tenant assignment to API endpoints. The feature is designed for API platform administrators managing multi-tenant or multi-gateway deployments.

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

## Key concepts

### Tag key field

Tags now include a required `key` field (1-64 characters) that serves as the stable identifier for sharding tag assignment in plan deployment. The key is immutable after creation, automatically sanitized to lowercase alphanumeric characters with hyphens, and must be unique within the organization. The `id` field remains as a UUID for internal references, but user-facing operations (plan sharding tag selection, entrypoint mapping) now use the `key` field.

### Tenant key field

Tenants now include a required `key` field (1-64 characters) that serves as the stable identifier for endpoint tenant assignment. The key is immutable after creation, automatically sanitized to lowercase alphanumeric characters with hyphens, and must be unique within the organization. Gateway configuration files reference tenants by `key` instead of `id`.

### Key sanitization

Keys are automatically sanitized on input and finalized on blur. The sanitization process removes diacritics, converts to lowercase, replaces non-alphanumeric characters (except hyphens) with single hyphens, and removes trailing hyphens.

| Input | Sanitized Output |
|:------|:-----------------|
| `My Tag Key` | `my-tag-key` |
| `Tâg Spécîal @#$ Nàme!` | `tag-special-name` |
| `Tag   With    Multiple---Spaces` | `tag-with-multiple-spaces` |
| `Tag Key---` | `tag-key` |
| `UPPERCASE KEY` | `uppercase-key` |
| `Key 123 Value 456` | `key-123-value-456` |
| `eu east 1! @#$%` | `eu-east-1` |

## Prerequisites

- Gravitee API Management 4.12.0 or later
- The database schema includes the `tags.key` and `tenants.key` columns, added automatically via Liquibase migration (`v4_12_0/00_add_tags_key_column.yml`).

<!-- Verified: Liquibase changelog is at gravitee-apim-repository-jdbc/src/main/resources/liquibase/changelogs/v4_12_0/00_add_tags_key_column.yml. Agent draft incorrectly referenced "09_add_tags_key_column.yml". -->

## Post-migration changes

After migration:

- All tag REST API endpoints use the tag `key` in path parameters instead of the `id`. For existing tags, the `key` equals the old `id`, so existing API calls continue to work.
- New tags created via the API require a `key` field in the request body.
- API clients that create new tags and store the `id` for later reference need to use the `key` for subsequent operations (GET, PUT, DELETE), not the UUID `id`.
- Tenant deletion operations now use the tenant key instead of the ID.

For the full list of affected endpoints, see [Tag entity schema and key field reference](../reference/data-model/tag-entity-schema-and-key-field-reference.md#rest-api-endpoints).

{% hint style="info" %}
If the migration encounters an error, it logs a failure message and the platform continues to start. Check the application logs for details and contact support if tag operations don't work as expected after upgrade.
{% endhint %}

## Gateway configuration

Update gateway configuration files to reference tenants by their `key` value instead of the auto-generated `id`.

## Creating tags and tenants

To create a tag, navigate to **Organization Settings** → **Sharding Tags** → **Add Tag**, provide a name (1-64 characters) and key (1-64 characters), optionally add a description and restricted groups, then save. The key field is auto-sanitized as you type and finalized when you move to the next field. Once created, the key can't be changed.

To create a tenant, navigate to **Organization Settings** → **Tenants** → **Add Tenant**, provide a name (1-40 characters) and key (1-64 characters), optionally add a description (max 160 characters), then save. The key field follows the same sanitization and immutability rules as tags.

## Assigning tags and tenants

To assign a sharding tag to a plan, edit the plan's General settings, navigate to the Deployment section, and select one or more tags from the **Sharding Tags** dropdown using their human-readable names (the underlying value is now the tag `key`, not `id`).

To assign a tenant to an API endpoint, edit the endpoint configuration, navigate to the Tenants section, and select one or more tenants from the dropdown using their human-readable names (the underlying value is now the tenant `key`, not `id`).

## Tag entity API

**NewTagEntity** (POST `/organizations/{orgId}/configuration/tags`):

| Property | Description | Example |
|:---------|:------------|:--------|
| `name` | Tag display name (1-64 characters, required) | `"Production"` |
| `key` | Tag identifier (1-64 characters, required, immutable) | `"production"` |
| `description` | Optional description | `"Production environment tag"` |
| `restricted_groups` | Optional list of group IDs with access | `["group-uuid-1"]` |

**TagEntity** (response):

| Property | Description | Example |
|:---------|:------------|:--------|
| `id` | Auto-generated UUID | `"550e8400-e29b-41d4-a716-446655440000"` |
| `key` | Tag identifier (1-64 characters, immutable) | `"production"` |
| `name` | Tag display name (1-64 characters) | `"Production"` |
| `description` | Optional description | `"Production environment tag"` |
| `restricted_groups` | List of group IDs with access | `["group-uuid-1"]` |

**UpdateTagEntity** (PUT `/organizations/{orgId}/configuration/tags/{tagKey}`):

| Property | Description | Example |
|:---------|:------------|:--------|
| `name` | Tag display name (1-64 characters, required) | `"Production"` |
| `description` | Optional description | `"Production environment tag"` |
| `restricted_groups` | Optional list of group IDs with access | `["group-uuid-1"]` |

## Tenant entity API

**NewTenant** (POST `/organizations/{orgId}/configuration/tenants`):

| Property | Description | Example |
|:---------|:------------|:--------|
| `name` | Tenant display name (1-40 characters, required) | `"EU East 1"` |
| `key` | Tenant identifier (1-64 characters, required, immutable) | `"eu-east-1"` |
| `description` | Optional description (max 160 characters) | `"European datacenter region 1"` |

**Tenant** (response):

| Property | Description | Example |
|:---------|:------------|:--------|
| `id` | Auto-generated UUID | `"550e8400-e29b-41d4-a716-446655440000"` |
| `key` | Tenant identifier (1-64 characters, immutable) | `"eu-east-1"` |
| `name` | Tenant display name (1-40 characters) | `"EU East 1"` |
| `description` | Optional description (max 160 characters) | `"European datacenter region 1"` |

**UpdateTenantEntity** (PUT `/organizations/{orgId}/configuration/tenants/{tenantKey}`):

| Property | Description | Example |
|:---------|:------------|:--------|
| `name` | Tenant display name (1-40 characters, required) | `"EU East 1"` |
| `key` | Tenant identifier (1-64 characters, immutable) | `"eu-east-1"` |
| `description` | Optional description (max 160 characters) | `"European datacenter region 1"` |

## Restrictions

- Tag and tenant keys are immutable after creation (disabled in edit forms)
- Tag and tenant keys must be unique within the organization
- Tag key length: 1-64 characters
- Tenant key length: 1-64 characters
- Key sanitization is client-side only; server-side validation doesn't enforce sanitization rules, and malformed keys may be rejected
- No automatic key generation from name; users must manually provide a key value during creation

## Related changes

The tag management UI now displays a **Key** field in the creation dialog with real-time sanitization and character count validation. The tag edit dialog shows the key as a disabled field. The sharding tags dropdown in plan deployment now uses tag keys instead of IDs for selection. The entrypoint mapping dialog uses tag keys for tag selection.

The tenant management UI now displays a **Key** field in the creation dialog with the same sanitization behavior. The tenant edit dialog shows the key as a disabled field. The tenant table now displays a **Key** column instead of an **ID** column, and the help text instructs users to copy the tenant's key (not ID) to the gateway configuration file. Endpoint tenant selection dropdowns now use tenant keys instead of IDs.

The tag update and delete API endpoints now accept `{tagKey}` as the path parameter instead of `{tagId}`.
