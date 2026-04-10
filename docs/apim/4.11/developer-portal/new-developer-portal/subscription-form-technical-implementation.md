# Subscription form technical implementation

## Portal API

### GET `/subscription-form`

Retrieves the enabled subscription form for the current environment. Returns 404 if the form doesn't exist or is disabled. The Portal API response only includes `gmdContent` — it doesn't expose the form `id` or `enabled` flag to consumers.

**Response:**

```json
{
  "gmdContent": "string"
}
```

**Authentication:** Required (Portal auth)

{% hint style="warning" %}
This environment-level portal endpoint does not support EL option resolution and is marked for removal after frontend migration to the API-scoped endpoint.
{% endhint %}

### GET `/apis/{apiId}/subscription-form`

Retrieves the subscription form for a specific API with resolved dynamic options. Returns 404 when no subscription form exists, the form is disabled, or the API is not visible to the user.

**Response:**

| Property | Type | Description |
|:---------|:-----|:------------|
| `gmdContent` | string | Gravitee Markdown content defining the form |
| `resolvedOptions` | object | Map of field keys to effective option lists (resolved from API metadata or fallback values). Present only when at least one field has dynamic options. |

**Behavior:**
- EL expressions are resolved against the API's metadata
- If resolution fails, fallback values are returned
- Enforces portal navigation visibility; if the API is not visible to the user, the endpoint returns 404

**Authentication:** Required (Portal auth)

## Management Console API

### GET `/environments/{envId}/subscription-forms`

Retrieves the subscription form for Console Form Builder editing. Returns the form whether enabled or disabled.

**Response:**

| Property | Type | Description |
|:---------|:-----|:------------|
| `id` | string | Subscription form UUID |
| `gmdContent` | string | Gravitee Markdown content defining the form |
| `enabled` | boolean | Whether the form is enabled |
| `resolvedOptions` | object | Map of field keys to fallback option lists (no API context available). Present only when at least one field has dynamic options. |

**Behavior:**
- EL expressions are resolved without API metadata and fall back to configured options
- Available for Console Form Builder editing regardless of enabled state

## Subscription metadata

When an API consumer subscribes to an API plan, the form field values are included in the subscription creation request as a `metadata` field containing key-value pairs. Empty values (null, empty strings, whitespace-only) are filtered before submission.

| Property | Type | Description |
|:---------|:-----|:------------|
| `metadata` | `Record<string, string>` | Key-value pairs from subscription form fields, submitted with the subscription creation request |

Checkbox-group selected values are serialized as a sorted, comma-separated string (e.g., `"Option 1,Option 3"`); empty selection is serialized as `""`.

## GMD form components

The following GMD components are available for subscription forms:

| Component | Description | Validation |
|:----------|:------------|:-----------|
| `gmd-input` | Single-line text input | `required`, `minLength`, `maxLength`, `pattern` |
| `gmd-textarea` | Multi-line text input | `required`, `minLength`, `maxLength` |
| `gmd-select` | Dropdown selection | `required` |
| `gmd-checkbox` | Checkbox | `required` |
| `gmd-checkbox-group` | Checkbox group selection | `required` |
| `gmd-radio` | Radio button selection | `required` |

Each component's `fieldKey` attribute maps to the key in the subscription's `metadata` object. Validation error codes: `required`, `minLength`, `maxLength`, `pattern`.

## Validation limits

| Property | Value | Description |
|:---------|:------|:------------|
| **Max Fields** | 25 | Maximum number of metadata fields allowed in a subscription form |
| **Max Metadata Entries** | 25 | Maximum number of metadata entries accepted in a subscription form submission |
| **Input Max Length** | 256 | Backend-enforced maximum length for `gmd-input` fields |
| **Textarea Max Length** | 1024 | Backend-enforced maximum length for `gmd-textarea` fields |

Author-defined `maxLength` values above these caps are silently clamped.

## Restrictions

- One subscription form per environment
- GMD content can't be null, empty, or whitespace-only
- Subscription forms aren't displayed for Keyless plans — the form only renders when the selected plan requires authentication
- Disabled forms return 404 from Portal API but remain accessible via Management API
- Comment field from Classic Portal is removed in the new Portal — subscription form metadata replaces this functionality
- Subscription forms are limited to 25 fields; exceeding this limit throws `SubscriptionFormDefinitionValidationException` at save time
- Subscription submissions are limited to 25 metadata entries; exceeding this limit throws `SubscriptionFormValidationException` at submit time
- Input fields are capped at 256 characters; textarea fields at 1024 characters
- EL expressions must use `{#...}` syntax; `#{...}` or `{...}` (without `#`) trigger `invalidElSyntax` config error
- EL expressions in options must include a fallback list (e.g., `{#api.metadata['key']}:option1,option2`); omitting the fallback triggers `missingElFallback` config error
- JSON array syntax for options (e.g., `options='["Option 1","Option 2"]'`) is no longer supported; use comma-separated strings or EL expressions with fallback

## Console integration

- A **Subscription Form** menu item appears under Portal Settings with route `/subscription-form`
- The toggle label is **Visible to API consumers** (not "Enabled")
- Permissions use `environment-metadata-r/u`
- Navigation guards prevent navigation away from unsaved form edits
- The save button is disabled when content is empty, has configuration errors, or has no unsaved changes
- The save button is disabled only when critical config errors exist; warnings (e.g., normalized lengths) do not block save

## Portal integration

- The portal subscription form display merges resolved options into GMD content by matching `fieldkey` attributes before rendering
- Form field spacing has been reduced from `margin-bottom: 1rem` to `margin-block: 0.5rem`

## Data migration

A MongoDB upgrader (`SubscriptionFormValidationConstraintsMongoUpgrader`) backfills the `validationConstraints` field with `"{}"` for existing documents, and a subsequent upgrader (`SubscriptionFormConstraintsUpgrader`) replaces `"{}"` with actual constraints derived from GMD content.
