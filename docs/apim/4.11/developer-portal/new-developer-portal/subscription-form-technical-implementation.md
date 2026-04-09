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

### GET `/apis/{apiId}/subscription-form`

Retrieves the subscription form content for a specific API when the form exists and is enabled for the environment. EL expressions in option-bearing fields are resolved against the API's metadata. If resolution fails, fallback values are returned. Returns 404 when no subscription form exists for the environment, when the form is disabled, or when the API is not visible to the user.

**Response:**

```json
{
  "gmdContent": "string",
  "resolvedOptions": {
    "fieldKey1": ["option1", "option2"],
    "fieldKey2": ["optionA", "optionB"]
  }
}
```

**Authentication:** Requires `BasicAuth` or `CookieAuth`

## Management API v2

### GET `/environments/{envId}/subscription-forms`

Returns the subscription form for an environment. `resolvedOptions` is present only when at least one field has dynamic options. Keys are field keys; values are the effective option lists (fallback values when no API context is available).

**Response:**

```json
{
  "id": "uuid",
  "gmdContent": "string",
  "enabled": false,
  "resolvedOptions": {
    "fieldKey": ["option1", "option2"]
  }
}
```

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

### GMD checkbox component properties

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| Name | string | `''` | HTML name attribute for checkbox inputs |
| Label | string | — | Display label shown above the group (renders as `<legend>`) |
| Field Key | string | — | Key used for form state tracking and data collection |
| Value | string | — | Comma-separated preselected values (e.g., `"Option 1,Option 3"`) |
| Required | boolean | `false` | Whether at least one option must be selected |
| Options | string | `''` | Comma-separated list of options or EL expression with fallback (e.g., `"{#api.metadata['key']}:option1,option2"`) |
| Disabled | boolean | `false` | Disables all checkboxes and removes field from form state |

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
