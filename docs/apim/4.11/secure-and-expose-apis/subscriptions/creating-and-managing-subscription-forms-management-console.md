# Creating and Managing Subscription Forms (Management Console)

## Navigation and Access

### Navigation Menu

The Subscription Form menu item appears in the Management Console under Portal Settings.

| Property | Value | Description |
|:---------|:------|:------------|
| `displayName` | `'Subscription Form'` | Menu item label |
| `routerLink` | `'subscription-form'` | Angular route path |
| `icon` | `'gio:list-check'` | Icon identifier |
| `permissions` | `['environment-metadata-r', 'environment-metadata-u']` | Required permissions |

### Route Configuration

```typescript
{
  path: 'subscription-form',
  component: SubscriptionFormComponent,
  canDeactivate: [HasUnsavedChangesGuard],
  data: {
    permissions: {
      anyOf: ['environment-metadata-r', 'environment-metadata-u']
    }
  }
}
```

## Managing Subscription Forms

### Updating Form Content

To modify the form:

1. Edit the GMD content in the Management Console editor.
2. Click **Save**.

The `PUT /v2/environments/{envId}/subscription-forms/{formId}` endpoint accepts an `UpdateSubscriptionForm` request with a `gmdContent` field. Content is validated to ensure it is not null, empty, or whitespace-only. Violations throw `GraviteeMarkdownContentEmptyException` with the message "Content must not be null or empty."

### Enabling and Disabling Forms

Use the **Enable** toggle in the Management Console or call the Management API v2 endpoints:

- `POST /v2/environments/{envId}/subscription-forms/{formId}/_enable` sets `enabled: true`, making the form visible in the Developer Portal.
- `POST /v2/environments/{envId}/subscription-forms/{formId}/_disable` sets `enabled: false`, hiding the form from API consumers.

### Viewing Collected Metadata

Subscription metadata is displayed in the Management Console subscription details view using a Monaco editor component. Each key-value pair from the subscription's `metadata` field is shown in JSON format.

