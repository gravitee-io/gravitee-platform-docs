# Subscription Form Feature Overview

## Overview

The Subscription Form feature enables API administrators to collect custom metadata from developers during API subscription. Administrators configure a single environment-level form using Gravitee Markdown (GMD) syntax, which appears in the Developer Portal subscription flow for all APIs with secured plans. Collected metadata is stored with each subscription and displayed in the Management Console.

## Key Concepts

### Gravitee Markdown (GMD) Form Syntax

Subscription forms are authored using GMD, a markdown-based syntax for defining form fields. Administrators write GMD content in the Management Console editor, which renders as interactive form fields in the Developer Portal.

Example GMD syntax:

The GMD content is stored in the `gmd_content` column and validated to ensure it is not null, empty, or whitespace-only.

### Environment-Level Form Scope

Each environment has exactly one subscription form, identified by a unique `environment_id` constraint in the database. The form applies to all APIs within the environment when enabled. Administrators manage the form via the Management Console under Portal Settings → Subscription Form. The form's visibility to API consumers is controlled by the `enabled` boolean flag.

### Metadata Collection and Storage

When a developer subscribes to an API, form field values are captured as key-value pairs in the subscription's `metadata` field (type: `Record<string, string>`). Empty strings, null values, and whitespace-only values are filtered out before storage. Metadata keys must not contain invalid characters such as spaces; violations trigger a `SubscriptionMetadataInvalidException` with the message "Invalid metadata key."

### Form Display Rules

The subscription form appears in the Developer Portal subscription flow only when:

1. A subscription form exists for the environment
2. The form is enabled (`enabled: true`)
3. The selected plan's security type is NOT `KEY_LESS`

If any condition fails, the form is hidden and no metadata is collected.

## Prerequisites

* `environment-metadata-r` permission to view subscription forms
* `environment-metadata-u` permission to create, update, enable, or disable subscription forms
* Database schema migration `08_add_subscription_forms_table.yml` applied (creates `${gravitee_prefix}subscription_forms` table)
* Gravitee Markdown library (`@gravitee/gravitee-markdown`) available in Console and Portal UI

## Gateway Configuration

### Database Schema

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
