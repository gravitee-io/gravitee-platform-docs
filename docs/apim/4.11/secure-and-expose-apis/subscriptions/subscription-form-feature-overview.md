# Subscription Form Feature Overview

## Overview

The Subscription Form feature enables API administrators to create custom forms that collect structured metadata from API consumers during the subscription process. Forms are built using Gravitee Markdown (GMD) components and can be enabled or disabled per environment. Collected metadata is stored with each subscription and visible in both Console and Portal UIs.

## Key Concepts

### Gravitee Markdown (GMD) Forms

GMD forms are declarative, component-based forms written in Gravitee Markdown syntax. Administrators define form structure using GMD components (`<gmd-input>`, `<gmd-textarea>`, `<gmd-select>`, `<gmd-checkbox>`, `<gmd-radio>`) with validation rules. Forms render in the Portal subscription checkout flow and extract field values as subscription metadata. GMD content is validated to ensure it is non-empty and well-formed.

### Subscription Metadata

Metadata is a key-value object collected from subscription form fields and stored with each subscription. Keys correspond to GMD component `name` attributes; values are user-provided strings. Empty or null values are filtered out before submission. Metadata is visible in Console subscription detail views as read-only JSON.

### Form Visibility

Each environment has one subscription form with an `enabled` flag. When enabled, the form appears in Portal subscription flows for all plans except `KEY_LESS` plans. When disabled, the form is hidden from consumers but remains editable in Console. The Management API returns forms regardless of state; the Portal API returns 404 for disabled forms.

### GMD Form Components

GMD forms support six component types:

* `<gmd-input>` — Text input with type, length, and placeholder options
* `<gmd-textarea>` — Multi-line text with length constraints
* `<gmd-select>` — Dropdown with comma-separated options
* `<gmd-checkbox>` — Boolean checkbox
* `<gmd-radio>` — Radio button group with options
* Layout containers — `<gmd-card>` and `<gmd-grid>`

All components support `name`, `label`, `fieldKey`, and `required` attributes.

## Prerequisites

* Environment-level settings permissions (`environment-metadata-r` for read, `environment-metadata-u` for update)
* JDBC repository configured with `subscription_forms` table schema
* Portal API access for consumers to retrieve enabled forms
