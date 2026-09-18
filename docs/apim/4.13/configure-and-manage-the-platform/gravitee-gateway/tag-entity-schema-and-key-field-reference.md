---
hidden: true
noIndex: true
description: Each API Management 4.13 tag has a key field separating the human-readable name from the identifier. Browse the schema reference.
---

# Tag entity schema and key field reference

## Overview

Starting in APIM 4.12, each tag has a dedicated `key` field that separates the human-readable tag identifier from the internal `id`. This affects how tags are referenced in REST API endpoints and how new tags are created.

For existing tags, the migration preserves the current `id` value and copies it into the new `key` field. This means existing API clients continue to work without changes. Only new tags created after migration receive a UUID as their `id`.

## Tag fields

| Field | Format | Purpose | Example |
|:------|:-------|:--------|:--------|
| `id` | String | Internal database reference. For existing tags, this retains the original value. For new tags, this is a UUID. | `70237305-6f68-450e-a373-056f68750e50` |
| `key` | String (max 64 chars) | User-facing identifier used in API operations and path parameters | `international` |
| `name` | String (max 64 chars) | Display name (unique within the reference scope) | `International` |
| `description` | String | Optional tag description | — |
| `restrictedGroups` | Array of strings | Optional list of groups with access to this tag | — |

When creating a tag, provide both `key` and `name` (each 1–64 characters). The `key` field is immutable after creation.

### Key validation rules

The `key` field is sanitized on creation using the following rules:

- Lowercase alphanumeric characters and hyphens (`-`) only
- Leading and trailing hyphens are stripped
- Any character that isn't `a-z`, `0-9`, or `-` is replaced with a hyphen
- Consecutive hyphens are collapsed into a single hyphen

For example, `My Tag Name!` becomes `my-tag-name`.

## Tenant key differences

Tenant keys follow the same validation rules as tag keys, with the following differences:

| Property | Tag | Tenant |
|:---------|:----|:-------|
| Key maximum length | 64 characters | 64 characters |
| Name maximum length | 64 characters | 40 characters |
| Key immutable after creation | Yes — the update DTO doesn't include a `key` field | The update DTO includes a `key` field, but the Console UI disables editing. Treat as effectively immutable. |
| Used in | `gravitee.yml` `tags` config, API path parameters | `gravitee.yml` `tenant` config, API endpoint tenant assignment |

## REST API endpoints

All tag management endpoints use the tag `key` in path parameters.

| Endpoint | Method | Path | Notes |
|:---------|:-------|:-----|:------|
| List tags | GET | `/tags` | Returns all tags |
| Get tag | GET | `/tags/{tagKey}` | Retrieve a single tag by key |
| Create tag | POST | `/tags` | Include `key` and `name` in the request body |
| Update tag | PUT | `/tags/{tagKey}` | Accepts `name`, `description`, and `restrictedGroups` only |
| Delete tag | DELETE | `/tags/{tagKey}` | Delete a tag by key |

### Create a tag

Send a POST request to `/tags` with the following fields:

- `key` (required, 1–64 characters): immutable tag identifier
- `name` (required, 1–64 characters): display name, unique within the reference scope
- `description` (optional)
- `restrictedGroups` (optional array)

The system generates a UUID for the internal `id` field. If a tag with the same `key` already exists, the request fails.

### Update a tag

Send a PUT request to `/tags/{tagKey}` with `name`, `description`, and `restrictedGroups`. The request body doesn't accept `id` or `key` fields.

### Delete a tag

Send a DELETE request to `/tags/{tagKey}`.

## Behavior for existing vs. new tags

{% hint style="info" %}
For **existing tags**, the migration preserves the original `id` value and sets `key` to the same value. Existing API clients that reference tags by their current ID in path parameters continue to work, because the `key` matches the old `id`.

For **new tags** created after migration, the `id` is a generated UUID. API clients interact with new tags using the `key` field in path parameters, not the UUID.
{% endhint %}

## Restrictions

- Tag keys are immutable after creation (max 64 characters).
- Tenant keys are effectively immutable after creation (max 64 characters).
- Tenant names are limited to 40 characters.
- Tag and tenant names are unique within the same reference scope.
- Keys accept only lowercase alphanumeric characters and hyphens.

## Related

- [Tag key migration upgrade procedure](../../upgrade-guides/tag-key-migration-upgrade-procedure.md)
