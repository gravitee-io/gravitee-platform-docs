# Subscription Forms Overview

## Overview

The Subscription Form feature allows platform administrators to create custom forms that API consumers must complete when subscribing to API plans. Forms are built using Gravitee Markdown (GMD) components and collect structured metadata such as company name, use case, or contact information. This feature is available for all plan types except KEY_LESS.

## Key Concepts

### Subscription Form Lifecycle

A subscription form is created per environment and can be enabled or disabled to control visibility to API consumers. When enabled, the form appears during the subscription checkout process in the Developer Portal. Form data is captured as subscription metadata and stored with the subscription record. Administrators manage forms through the Management Console, while consumers interact with them in the Portal.

### GMD Form Components

Gravitee Markdown (GMD) provides a set of form components for building subscription forms. Available components include text inputs, textareas, selects, radio buttons, checkboxes, and layout containers (cards, grids). Each input component supports validation attributes such as `required`, `minLength`, `maxLength`, and `type`. Forms are rendered in a live preview editor with split-pane view.

| Component | Purpose | Key Attributes |
|:----------|:--------|:---------------|
| `<gmd-input>` | Single-line text input | `name`, `label`, `fieldKey`, `required`, `type`, `placeholder`, `minLength`, `maxLength` |
| `<gmd-textarea>` | Multi-line text input | `name`, `label`, `fieldKey`, `required`, `minLength`, `maxLength`, `placeholder` |
| `<gmd-select>` | Dropdown selection | `name`, `label`, `fieldKey`, `required`, `options` (comma-separated) |
| `<gmd-radio>` | Radio button group | `name`, `label`, `fieldKey`, `required`, `options` (comma-separated) |
| `<gmd-checkbox>` | Single checkbox | `name`, `label`, `fieldKey`, `required` |
| `<gmd-card>` | Container for grouping fields | N/A |
| `<gmd-card-title>` | Title for card container | N/A |
| `<gmd-grid>` | Grid layout container | `columns` |
| `<gmd-md>` | Markdown content block | N/A |

### Subscription Metadata

Metadata collected from subscription forms is stored as key-value pairs on the subscription entity. Metadata keys are derived from the `fieldKey` attribute of GMD form components and must be alphanumeric with underscores or hyphens. Empty or whitespace-only values are filtered out before submission. Metadata is displayed in read-only JSON format in both API and Application subscription detail views.


## Prerequisites

- Environment-level permissions: `environment-metadata-r` (read) and `environment-metadata-u` (update)
- Database schema migration applied (table `${gravitee_prefix}subscription_forms`)
