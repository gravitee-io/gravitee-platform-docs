---
hidden: true
noIndex: true
---

# Tag entity schema and key field reference

<!-- DISCREPANCY: This page was placed in 4.11 by the agent, but the feature is merged in APIM 4.12.x only (confirmed by Okhelifi and verified from git history + Liquibase v4_12_0 directory). Move this file to docs/apim/4.12/ once that folder exists. -->

## Overview

Starting in APIM 4.12, each tag has a dedicated `key` field that separates the human-readable tag identifier from the internal `id`. This affects how tags are referenced in REST API endpoints and how new tags are created.

For existing tags, the migration preserves the current `id` value and copies it into the new `key` field. This means existing API clients continue to work without changes. Only new tags created after migration receive a UUID as their `id`.

<!-- Verified from TagKeyUpgrader.java: tag.setKey(tag.getId()) — existing IDs are preserved, not regenerated. Confirmed by Okhelifi. -->

## Tag fields

| Field | Format | Purpose | Example |
|:------|:-------|:--------|:--------|
| `id` | String | Internal database reference. For existing tags, this retains the original value. For new tags, this is a UUID. | `70237305-6f68-450e-a373-056f68750e50` |
| `key` | String (max 64 chars) | User-facing identifier used in API operations and path parameters | `international` |
| `name` | String (max 64 chars) | Display name (unique within the reference scope) | `International` |
| `description` | String | Optional tag description | — |
| `restrictedGroups` | Array of strings | Optional list of groups with access to this tag | — |

When creating a tag, provide both `key` and `name` (each 1–64 characters). The `key` field is immutable after creation.

<!-- Verified from UpdateTagEntity.java: no key field exists in the update DTO. TagServiceImpl preserves the key on update via .key(existingTag.getKey()). -->

## REST API endpoints

All tag management endpoints use the tag `key` in path parameters.

| Endpoint | Method | Path | Notes |
|:---------|:-------|:-----|:------|
| List tags | GET | `/tags` | Returns all tags |
| Get tag | GET | `/tags/{tagKey}` | Retrieve a single tag by key |
| Create tag | POST | `/tags` | Include `key` and `name` in the request body |
| Update tag | PUT | `/tags/{tagKey}` | Accepts `name`, `description`, and `restrictedGroups` only |
| Delete tag | DELETE | `/tags/{tagKey}` | Delete a tag by key |

<!-- Verified from TagsResource.java: GET /tags, GET /tags/{tag}, POST /tags, PUT /tags/{tag}, DELETE /tags/{tag}. All path params reference the key. -->

### Create a tag

Send a POST request to `/tags` with the following fields:

- `key` (required, 1–64 characters): immutable tag identifier
- `name` (required, 1–64 characters): display name, unique within the reference scope
- `description` (optional)
- `restrictedGroups` (optional array)

The system generates a UUID for the internal `id` field. If a tag with the same `key` already exists, the request fails.

<!-- Verified: DuplicateTagKeyException is thrown on duplicate key (TagServiceImpl.java line 142). -->

### Update a tag

Send a PUT request to `/tags/{tagKey}` with `name`, `description`, and `restrictedGroups`. The request body doesn't accept `id` or `key` fields.

### Delete a tag

Send a DELETE request to `/tags/{tagKey}`.

## Behavior for existing vs. new tags

{% hint style="info" %}
For **existing tags**, the migration preserves the original `id` value and sets `key` to the same value. Existing API clients that reference tags by their current ID in path parameters continue to work, because the `key` matches the old `id`.

For **new tags** created after migration, the `id` is a generated UUID. API clients interact with new tags using the `key` field in path parameters, not the UUID.
{% endhint %}

<!-- DISCREPANCY: The original agent draft stated "existing API clients using tag IDs will fail" — this is incorrect. Okhelifi confirmed existing IDs are preserved and the key equals the old ID. Only new tags use UUIDs as IDs. -->

## Restrictions

- Tag keys are immutable after creation.
- Tag names are unique within the same reference scope.
- The `key` field is limited to 64 characters.

## Related

- [Tag key migration upgrade procedure](../../upgrade-guides/tag-key-migration-upgrade-procedure.md)
