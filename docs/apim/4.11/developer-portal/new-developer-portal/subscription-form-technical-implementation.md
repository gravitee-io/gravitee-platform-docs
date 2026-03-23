# Subscription form technical implementation

## Portal API

### GET `/subscription-form`

Retrieves the enabled subscription form for the current environment. Returns 404 if the form doesn't exist or is disabled.

**Response:**

```json
{
  "gmdContent": "string"
}
```

**Authentication:** Required

## Subscription metadata properties

| Property | Type | Description |
|:---------|:-----|:------------|
| `metadata` | `Record<string, string>` | Key-value pairs from subscription form fields |

Metadata is included in subscription creation requests and stored in the subscription entity. Empty values are filtered before submission.

## Restrictions

- One subscription form per environment (enforced by unique constraint on `environment_id`)
- GMD content can't be null, empty, or whitespace-only
- Subscription forms aren't displayed for `KEY_LESS` security plans
- Disabled forms return 404 from Portal API but remain accessible via Management API
- Metadata keys conform to validation rules (invalid keys return HTTP 400)
- Comment field from Classic Portal is removed in new Portal — subscription form metadata replaces this functionality

## Related changes

- A new navigation menu item appears in Portal Settings with route `/subscription-form`
- Permissions use `environment-metadata-r/u` (updated from `environment-settings-r/u`)
- The subscription checkout flow in Portal renders the form when GMD content exists and the plan security isn't `KEY_LESS`
- Navigation guards prevent navigation away from unsaved form edits
