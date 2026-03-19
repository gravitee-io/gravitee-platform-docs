# Subscription Form Database Schema

## Prerequisites

Before configuring subscription forms, ensure the following requirements are met:

* User must have `environment-metadata-r` permission to view subscription forms
* User must have `environment-metadata-u` permission to edit or enable/disable subscription forms
* Database schema migration `08_add_subscription_forms_table.yml` must be applied
* Portal API authentication must be configured for consumer access

## Database Schema

The subscription forms table stores one form per environment.

| Column | Type | Constraints | Description |
|:-------|:-----|:------------|:------------|
| `id` | `nvarchar(64)` | NOT NULL, PRIMARY KEY | Unique identifier |
| `environment_id` | `nvarchar(64)` | NOT NULL, UNIQUE | Environment identifier |
| `gmd_content` | `nclob` | NOT NULL | Gravitee Markdown form content |
| `enabled` | `boolean` | NOT NULL | Whether form is visible to consumers |

**Table name**: `${gravitee_prefix}subscription_forms`

**Constraints**:
* Primary key: `pk_${gravitee_prefix}subscription_forms` on `id`
* Unique constraint: `uc_${gravitee_prefix}subscription_forms_environment_id` on `environment_id`

## Navigation Menu Configuration

The Subscription Form menu item appears in the Portal Settings section.

| Property | Value | Description |
|:---------|:------|:------------|
| `displayName` | `'Subscription Form'` | Menu item label |
| `routerLink` | `'subscription-form'` | Angular route path |
| `icon` | `'gio:list-check'` | Icon identifier |
| `permissions` | `['environment-metadata-r', 'environment-metadata-u']` | Required permissions |

## Managing Form State

The form editor validates content in real-time and displays configuration errors such as `emptyFieldKey` (severity: error).

### Form Visibility Rules

The subscription form appears in the subscription flow only when three conditions are met: the form exists with non-empty `gmdContent`, the form is enabled, and the selected plan's security type is not `KEY_LESS`. When these conditions are not met, the subscription proceeds without collecting metadata.

### Metadata Display

Subscription metadata is displayed in both the API publisher console and application owner console as read-only JSON.
