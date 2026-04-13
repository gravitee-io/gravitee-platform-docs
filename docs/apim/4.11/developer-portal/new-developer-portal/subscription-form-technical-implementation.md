# Subscription form technical implementation

## Portal API

### GET `/apis/{apiId}/subscription-form`

Retrieves the subscription form for a specific API with resolved dynamic options. Returns 404 if the form doesn't exist or is disabled. The Portal API response includes `gmdContent` and optionally `resolvedOptions` — it doesn't expose the form `id` or `enabled` flag to consumers.

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

**Authentication:** Required (Portal auth)

{% hint style="info" %}
The environment-scoped endpoint `GET /subscription-form` is deprecated. Use the API-scoped endpoint `GET /apis/{apiId}/subscription-form` instead, which resolves dynamic options against the API's metadata.
{% endhint %}

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

- One subscription form per environment
- Maximum 25 fields per subscription form (enforced at save time)
- Maximum 25 metadata entries per subscription submission (enforced at validation time)
- GMD content can't be null, empty, or whitespace-only
- Input fields: hard maximum length of 256 characters. User-defined `maxLength` values are clamped to 256, and 256 is applied when `maxLength` is omitted.
- Textarea fields: hard maximum length of 1024 characters. User-defined `maxLength` values are clamped to 1024, and 1024 is applied when `maxLength` is omitted.
- EL expressions in options must include fallback values using syntax `{#expression}:fallback1,fallback2` (missing fallback reports `missingElFallback` error with severity `error`)
- EL expressions must start with `{#` (expressions starting with `#{` or `{` alone report `invalidElSyntax` error)
- Subscription forms aren't displayed for Keyless plans — the form only renders when the selected plan requires authentication
- Disabled forms return 404 from Portal API but remain accessible via Management API
- Comment field from Classic Portal is removed in the new Portal — subscription form metadata replaces this functionality

## Console integration

- A **Subscription Form** menu item appears under Portal Settings with route `/subscription-form`
- The toggle label is **Visible to API consumers** (not "Enabled")
- Permissions use `environment-metadata-r/u`
- Navigation guards prevent navigation away from unsaved form edits
- The save button is disabled when content is empty, has configuration errors, or has no unsaved changes
