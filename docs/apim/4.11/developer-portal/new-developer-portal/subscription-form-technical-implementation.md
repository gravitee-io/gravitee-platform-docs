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

## Subscription metadata

When an API consumer subscribes to an API plan, the form field values are included in the subscription creation request as a `metadata` field containing key-value pairs. Empty values (null, empty strings, whitespace-only) are filtered before submission.

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

Each component's `fieldKey` attribute maps to the key in the subscription's `metadata` object. Validation error codes: `required`, `minLength`, `maxLength`, `pattern`.

## Restrictions

- One subscription form per environment
- GMD content can't be null, empty, or whitespace-only
- Subscription forms aren't displayed for Keyless plans — the form only renders when the selected plan requires authentication
- Disabled forms return 404 from Portal API but remain accessible via Management API
- Comment field from Classic Portal is removed in the new Portal — subscription form metadata replaces this functionality

## Console integration

- A **Subscription Form** menu item appears under Portal Settings with route `/subscription-form`
- The toggle label is **Visible to API consumers** (not "Enabled")
- Permissions use `environment-metadata-r/u`
- Navigation guards prevent navigation away from unsaved form edits
- The save button is disabled when content is empty, has configuration errors, or has no unsaved changes
