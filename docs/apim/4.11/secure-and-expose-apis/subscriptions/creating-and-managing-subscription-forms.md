# Creating and Managing Subscription Forms

## Navigation Menu Configuration

The Subscription Form menu item appears in Portal Settings navigation.

| Property | Value | Description |
|:---------|:------|:------------|
| `displayName` | `'Subscription Form'` | Menu item label |
| `routerLink` | `'subscription-form'` | Route path |
| `icon` | `'gio:list-check'` | Icon identifier |
| `permissions` | `['environment-metadata-r', 'environment-metadata-u']` | Required permissions to view menu item |

## Route Configuration

| Property | Value | Description |
|:---------|:------|:------------|
| `path` | `'subscription-form'` | Route path |
| `component` | `SubscriptionFormComponent` | Component to render |
| `canDeactivate` | `[HasUnsavedChangesGuard]` | Navigation guard for unsaved changes |
| `permissions.anyOf` | `['environment-metadata-r', 'environment-metadata-u']` | Required permissions |

## Creating a Subscription Form

1. Navigate to Portal Settings → Subscription Form in the Management Console.
    
    The editor loads with default boilerplate content containing example form components organized in sections (Applicant Information, Usage Details, Quick Access).

2. Edit the GMD content to define custom form fields using `<gmd-input>`, `<gmd-textarea>`, `<gmd-select>`, `<gmd-radio>`, or `<gmd-checkbox>` components.

3. Set the `fieldKey` attribute on each input component to define the metadata key.
    
    Use `<gmd-grid columns="2">` to create multi-column layouts and `<gmd-card>` to group related fields.

4. Click Save to persist changes.
    
    The Save button is disabled when content is empty, unchanged, or contains configuration errors.

5. Toggle the Enabled switch to make the form visible to API consumers in the Portal.
    
    The Enable toggle is disabled when configuration errors exist or the user lacks `environment-metadata-u` permission.


