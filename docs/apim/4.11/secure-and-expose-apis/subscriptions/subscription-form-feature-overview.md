# Subscription Form Feature Overview

## Overview

The Subscription Form feature enables API administrators to create custom forms that collect metadata from developers during API subscription. Forms are built using Gravitee Markdown (GMD) components and can be enabled or disabled per environment. Collected metadata is stored with each subscription and displayed in the Management Console.


## Key Concepts

A subscription form is an environment-scoped configuration containing GMD content that defines form fields.
 Each environment has at most one subscription form, identified by a unique constraint on `environment_id` in the database. The form includes an `enabled` flag that controls visibility to API consumers in the Portal.

**Database Schema:**

The `${gravitee_prefix}subscription_forms` table stores subscription form configurations:

| Column | Type | Constraints |
|:-------|:-----|:------------|
| `id` | `nvarchar(64)` | Primary key, not null |
| `environment_id` | `nvarchar(64)` | Not null, unique constraint |
| `gmd_content` | `nclob` | Not null |
| `enabled` | `boolean` | Not null |

**Additional Constraints:**

- Primary key: `pk_${gravitee_prefix}subscription_forms` on `id`
- Unique constraint: `uc_${gravitee_prefix}subscription_forms_environment_id` on `environment_id`

The [database schema migration](../installation-guide/upgrades-and-migrations/database-migrations.md) `08_add_subscription_forms_table.yml` must be applied to enable this feature.

**Subscription Metadata:**

Subscription metadata is a key-value map attached to subscription entities. Metadata keys correspond to `fieldKey` attributes in GMD form components. Values are stored as strings. Empty or whitespace-only values are filtered out before storage.

**Visibility Rules:**

| Condition | Management API Behavior | Portal API Behavior |
|:----------|:------------------------|:--------------------|
| Form exists AND `enabled = true` | Return form content | Return form content |
| Form exists AND `enabled = false` | Return form content | Return `404 Not Found` |
| Form does not exist | Return `404 Not Found` | Return `404 Not Found` |

**Prerequisites:**

- `environment-metadata-r` permission to view subscription forms
- `environment-metadata-u` permission to edit subscription forms
- Portal authentication for Portal API access

**Restrictions:**

- One subscription form per environment (enforced by unique constraint)
- GMD content must not be null, empty, or whitespace-only
- Subscription forms are not displayed for `KEY_LESS` plans
- Portal API returns `404 Not Found` when form is disabled
- Management API returns form regardless of `enabled` state
- Feature does not apply to Classic Portal

### GMD Form Components

GMD (Gravitee Markdown) provides declarative form components embedded in markdown content. Each input component uses a `fieldKey` attribute to map user input to subscription metadata keys.

**Available Components:**

| Component | Purpose | Key Attributes |
|:----------|:--------|:---------------|
| `<gmd-input>` | Single-line text input | `name`, `label`, `fieldKey`, `required`, `type`, `placeholder`, `minLength`, `maxLength` |
| `<gmd-textarea>` | Multi-line text input | `name`, `label`, `fieldKey`, `required`, `minLength`, `maxLength`, `placeholder` |
| `<gmd-select>` | Dropdown selection | `name`, `label`, `fieldKey`, `required`, `options` (comma-separated) |
| `<gmd-radio>` | Radio button group | `name`, `label`, `fieldKey`, `required`, `options` (comma-separated) |
| `<gmd-checkbox>` | Checkbox | `name`, `label`, `fieldKey`, `required` |
| `<gmd-card>` | Container card | `<gmd-card-title>` for title |
| `<gmd-grid>` | Layout grid | `columns` attribute |
| `<gmd-md>` | Markdown content | (content inside tags) |

**Field Key Mapping:**

Form field values are collected using `fieldKey` attributes and stored as a key-value map. For example:

```html
<gmd-input name="email" label="Email" fieldKey="user_email" required="true"></gmd-input>
```

Results in metadata:

```json
{ "user_email": "user@example.com" }
```

**Navigation and Routing:**

The Subscription Form editor is accessible via Portal Settings with the following configuration:

| Property | Value |
|:---------|:------|
| Menu item label | `Subscription Form` |
| Route path | `subscription-form` |
| Icon | `gio:list-check` |
| Required permissions | `environment-metadata-r`, `environment-metadata-u` |
| Navigation guard | `HasUnsavedChangesGuard` |
