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
The environment-scoped endpoint `GET /subscription-form` (no API context) has been removed and replaced by the API-scoped endpoint `GET /apis/{apiId}/subscription-form`.
{% endhint %}

## Subscription metadata

When an API consumer subscribes to an API plan, the form field values are included in the subscription creation request as a `metadata` field containing key-value pairs. Empty values (null, empty strings, whitespace-only) are filtered before submission. The platform enforces a maximum of 25 metadata entries per subscription submission. Exceeding this limit throws `SubscriptionFormValidationException` at validation time.

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
| `gmd-checkbox-group` | Checkbox group with multiple selections | `required`, `eachOf` |

Each component's `fieldKey` attribute maps to the key in the subscription's `metadata` object. Validation error codes: `required`, `minLength`, `maxLength`, `pattern`, `eachOf`.

### Checkbox group behavior

Subscribers select one or more options from each checkbox group. The form serializes selections as comma-separated strings sorted alphabetically (e.g., `"Analytics,Authentication"`).

Validation constraints for checkbox groups:

- **Non-Empty Selection**: At least one value must be selected when the field is required
- **Each Of**: Every selected value must exist in the allowed options list

### Dynamic options resolution

The Portal UI merges resolved options into the GMD content before rendering. This process replaces static or fallback options with values resolved from API and environment metadata. Dynamic options resolution requires API and environment metadata context; fallback values are used in Console Form Builder (no API context available).

## Restrictions

- One subscription form per environment
- Maximum 25 fields per subscription form (enforced at save time)
- Maximum 25 metadata entries per subscription submission (enforced at validation time)
- GMD content can't be null, empty, or whitespace-only
- Input fields: hard maximum length of 256 characters (user-defined `maxLength` clamped to this value; 256 used when omitted)
- Textarea fields: hard maximum length of 1024 characters (user-defined `maxLength` clamped to this value; 1024 used when omitted)
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

## Styling

The following CSS custom properties control the appearance of checkbox group components in subscription forms:

| Property | Description | Default |
|:---------|:------------|:--------|
| `--gmd-checkbox-group-outlined-label-text-size` | Label font size | `0.875rem` |
| `--gmd-checkbox-group-outlined-label-text-weight` | Label font weight | `500` |
| `--gmd-checkbox-group-outlined-label-text-color` | Label text color | `inherit` |
| `--gmd-checkbox-group-error-text-color` | Error message color | (theme error color) |
| `--gmd-checkbox-group-subscript-text-size` | Error message font size | `0.8125rem` |
