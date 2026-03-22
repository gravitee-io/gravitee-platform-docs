# Subscription Form Technical Implementation

## Portal API

### GET `/subscription-form`

Retrieves the enabled subscription form for the current environment. Returns 404 if the form does not exist or is disabled.

**Response:**

```json
{
  "gmdContent": "string"
}
```

**Authentication:** Required

## Subscription Metadata Properties

| Property | Type | Description |
|:---------|:-----|:------------|
| `metadata` | `Record<string, string>` | Key-value pairs from subscription form fields |

Metadata is included in subscription creation requests and stored in the subscription entity. Empty values are filtered before submission.

## Restrictions

- One subscription form per environment (enforced by unique constraint on `environment_id`)
- GMD content must not be null, empty, or whitespace-only
- Subscription forms are not displayed for `KEY_LESS` security plans
- Disabled forms return 404 from Portal API but remain accessible via Management API
- Metadata keys must conform to validation rules (invalid keys trigger HTTP 400)
- Comment field from Classic Portal is removed in new Portal — subscription form metadata replaces this functionality

## Related Changes

The subscription form feature introduces a new navigation menu item in Portal Settings with route `/subscription-form` and icon `gio:list-check`. Permissions were updated from `environment-settings-r/u` to `environment-metadata-r/u`. The JDBC repository schema adds a `subscription_forms` table with columns `id`, `environment_id`, `gmd_content`, and `enabled`. Portal page content validation now delegates to validation via interface. The subscription checkout flow in Portal renders the form when subscription form GMD content exists and the plan security is not `KEY_LESS`. Form state is managed with signals for field values, validity, and configuration errors. Navigation guards prevent navigation away from unsaved form edits.
