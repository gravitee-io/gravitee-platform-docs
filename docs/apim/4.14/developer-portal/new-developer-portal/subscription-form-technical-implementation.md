---
description: Retrieve a Developer Portal 4.13 subscription form with resolved dynamic options. Learn what the endpoint returns to you.
---

# Subscription form technical implementation

## Portal API

### GET `/apis/{apiId}/subscription-form`

Retrieves the subscription form assigned to a specific API, with resolved dynamic options. Returns 404 when no form is assigned to the API or when the assigned form is hidden. The Portal API response includes `gmdContent` and optionally `resolvedOptions` — it doesn't expose the form `id` or `enabled` flag to consumers.

**Response fields:**

| Field | Type | Required | Description |
|:------|:-----|:---------|:------------|
| `gmdContent` | string | Yes | Gravitee Markdown content defining the form structure |
| `resolvedOptions` | object | No | Map of `fieldKey` to resolved option list for fields with EL expressions. Present only when at least one field has dynamic options. |

**Example response:**

```json
{
  "gmdContent": "<gmd-checkbox-group fieldKey=\"features\" options=\"{#api.metadata['features']}:Authentication,Rate Limiting\"/>",
  "resolvedOptions": {
    "features": ["Authentication", "Rate Limiting", "Analytics"]
  }
}
```

**Authentication:** Anonymous requests are rejected only when the Developer Portal requires users to log in.

## Subscription metadata

When an API consumer subscribes to an API plan, the form field values are included in the subscription creation request as a `metadata` field containing key-value pairs. Empty values (null, empty strings, whitespace-only) are filtered before submission. Subscription submissions are capped at 25 metadata entries.

| Property | Type | Description |
|:---------|:-----|:------------|
| `metadata` | `Record<string, string>` | Key-value pairs from subscription form fields, submitted with the subscription creation request |

## GMD form components

The following GMD components are available for subscription forms:

| Component | Description | Validation |
|:----------|:------------|:-----------|
| `gmd-input` | Single-line text input | `required`, `minLength`, `maxLength`, `pattern` |
| `gmd-textarea` | Multi-line text input | `required`, `minLength`, `maxLength` |
| `gmd-select` | Dropdown selection | `required` |
| `gmd-checkbox` | Checkbox | `required` |
| `gmd-radio` | Radio button selection | `required` |
| `gmd-checkbox-group` | Checkbox group with multiple selections | `required` |

Each component's `fieldKey` attribute maps to the key in the subscription's `metadata` object. Frontend validation error codes: `required`, `minLength`, `maxLength`, `pattern`. The backend additionally rejects checkbox group submissions when a selected value isn't in the allowed options list, and select or radio submissions when the value isn't in the allowed options list.

### Checkbox group behavior

Subscribers select one or more options from each checkbox group. The form serializes selections as a comma-separated string sorted alphabetically (for example, `"Analytics,Authentication"`).

Checkbox groups enforce two backend checks at submission time:

- When the field is required, at least one value must be selected.
- Every selected value must exist in the allowed options list.

### Dynamic options resolution

The Portal UI merges resolved options into the GMD content before rendering, replacing static or fallback options with values resolved from API and environment metadata. In the Console subscription form editor, EL expressions aren't resolved against API metadata — only the fallback values are shown as a preview.

## Restrictions

- Each API is assigned to one subscription form at most
- Form names are unique in the environment, compared without letter case, with a maximum of 255 characters
- Maximum 25 fields per subscription form (enforced at save time)
- Maximum 25 metadata entries per subscription submission (enforced at validation time)
- GMD content can't be null, empty, or whitespace-only
- Input fields: hard maximum length of 256 characters. User-defined `maxLength` values are clamped to 256, and 256 is applied when `maxLength` is omitted.
- Textarea fields: hard maximum length of 1024 characters. User-defined `maxLength` values are clamped to 1024, and 1024 is applied when `maxLength` is omitted.
- EL expressions in options must include fallback values using syntax `{#expression}:fallback1,fallback2` (missing fallback reports `missingElFallback` error with severity `error`)
- EL expressions must start with `{#` (expressions starting with `#{` or `{` alone report `invalidElSyntax` error)
- Subscription forms aren't displayed for Keyless plans — the form only renders when the selected plan requires authentication
- Hidden forms return 404 from Portal API but remain accessible via Management API
- Comment field from Classic Portal is removed in the new Portal — subscription form metadata replaces this functionality

## Console integration

- The **Subscription Form** menu item of the portal settings opens the **Subscription Forms** list, where each form has a **Visible** toggle
- Navigation guards prevent navigation away from unsaved form edits
- The **Save** button, labeled **Create** for a new form, is disabled when the name or the content is empty, when the content has configuration errors, or when there are no unsaved changes
