# Subscription Form Feature Overview

## Overview

The Subscription Form feature enables API administrators to collect custom metadata from API consumers during the subscription process. Administrators define form fields using Gravitee Markdown (GMD) syntax in the Management Console. The form is displayed in the Portal during API subscription checkout. Collected metadata is stored with the subscription and visible in both Management Console and Portal subscription views.

## Key Concepts

### Gravitee Markdown (GMD) Forms

GMD forms use a markdown-based syntax to define interactive form fields. Administrators write GMD content in the Management Console editor, which renders as a live form in the Portal.

Example GMD content:

```markdown
# Subscription Information

<gmd-input name="consumer_company_name" label="Company Name" required="true"/>
<gmd-textarea name="consumer_use_case" label="Use Case" required="true"/>
```

The GMD editor provides live preview and validation. Form configuration errors disable the enable toggle and save button until resolved.

### Subscription Metadata

Metadata is a key-value object submitted with subscription requests. Keys are defined by GMD form field `name` attributes. Values are user-provided strings. Empty string and null values are automatically filtered before submission. Metadata is stored with the subscription entity and displayed in subscription detail views as read-only JSON.

| Property | Type | Description |
|:---------|:-----|:------------|
| `metadata` | `{ [key: string]: string }` | Optional key-value pairs collected from subscription form |

### Form Visibility

The subscription form is displayed during checkout only when the form is enabled AND the selected plan security type is not `KEY_LESS`. When disabled or not found, the form is hidden and metadata is not collected. The enable toggle controls whether API consumers see the form in the Portal.

## Prerequisites

- `environment-metadata-r` permission to view subscription form configuration
- `environment-metadata-u` permission to edit, enable, or disable subscription form
- JDBC repository implementation with database schema migration applied
- GMD form editor library available in Portal

## Gateway configuration

### Database Schema

The subscription forms table stores one form per environment. Apply the migration `08_add_subscription_forms_table.yml` to create the schema.

| Property | Type | Constraints | Description |
|:---------|:-----|:------------|:------------|
| `id` | nvarchar(64) | NOT NULL, PRIMARY KEY | Unique identifier |
| `environment_id` | nvarchar(64) | NOT NULL, UNIQUE | Environment identifier (one form per environment) |
| `gmd_content` | nclob | NOT NULL | Gravitee Markdown form definition |
| `enabled` | boolean | NOT NULL | Whether form is visible to API consumers |

**Table name**: `${gravitee_prefix}subscription_forms`

**Constraints**:
- Primary key: `pk_${gravitee_prefix}subscription_forms` on `id`
- Unique constraint: `uc_${gravitee_prefix}subscription_forms_environment_id` on `environment_id`
