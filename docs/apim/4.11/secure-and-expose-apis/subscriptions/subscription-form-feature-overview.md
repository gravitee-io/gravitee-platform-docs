# Subscription form feature overview

## Overview

The subscription form feature enables API publishers to define a custom form that API consumers complete when subscribing to API plans. Forms are authored in Gravitee Markdown (GMD) and collect structured metadata stored with each subscription. This feature replaces the legacy comment field from the Classic Portal.

Subscription forms support field-level validation constraints and dynamic option lists. Forms are validated at save time (field count, syntax) and at submission time (required fields, length, pattern, allowed values). Dynamic options use Expression Language (EL) to populate select, radio, and checkbox-group fields from API metadata, with fallback values when no API context is available.

## Key concepts

### Gravitee Markdown (GMD) content

GMD is a structured markup language used to define form fields and layout. Form content is authored in the Management Console using a form editor with live preview.

A subscription form is defined using GMD content containing field components. Each field is identified by a `fieldKey` attribute and may include validation attributes and option lists. The schema is parsed at save time to generate validation constraints, which are persisted and enforced when users submit subscription requests.

#### Supported form components

GMD supports the following form components:

<table>
    <thead>
        <tr>
            <th width="180">Component</th>
            <th width="320">Description</th>
            <th>Supported attributes</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>gmd-input</code></td>
            <td>Single-line text input field</td>
            <td><code>fieldKey</code>, <code>name</code>, <code>label</code>, <code>placeholder</code>, <code>value</code>, <code>required</code>, <code>minLength</code>, <code>maxLength</code> (≤256), <code>pattern</code>, <code>readonly</code>, <code>disabled</code></td>
        </tr>
        <tr>
            <td><code>gmd-textarea</code></td>
            <td>Multi-line text input field</td>
            <td><code>fieldKey</code>, <code>name</code>, <code>label</code>, <code>placeholder</code>, <code>value</code>, <code>required</code>, <code>minLength</code>, <code>maxLength</code> (≤1024), <code>pattern</code>, <code>rows</code>, <code>readonly</code>, <code>disabled</code></td>
        </tr>
        <tr>
            <td><code>gmd-select</code></td>
            <td>Dropdown selection field</td>
            <td><code>fieldKey</code>, <code>name</code>, <code>label</code>, <code>value</code>, <code>required</code>, <code>options</code> (static CSV or EL with fallback), <code>readonly</code>, <code>disabled</code></td>
        </tr>
        <tr>
            <td><code>gmd-checkbox</code></td>
            <td>Single checkbox field</td>
            <td><code>fieldKey</code>, <code>name</code>, <code>label</code>, <code>value</code>, <code>required</code>, <code>readonly</code>, <code>disabled</code></td>
        </tr>
        <tr>
            <td><code>gmd-radio</code></td>
            <td>Radio button selection field</td>
            <td><code>fieldKey</code>, <code>name</code>, <code>label</code>, <code>value</code>, <code>required</code>, <code>options</code> (static CSV or EL with fallback), <code>readonly</code>, <code>disabled</code></td>
        </tr>
        <tr>
            <td><code>gmd-checkbox-group</code></td>
            <td>Multiple checkboxes field</td>
            <td><code>fieldKey</code>, <code>name</code>, <code>label</code>, <code>value</code>, <code>required</code>, <code>options</code> (static CSV or EL with fallback), <code>readonly</code>, <code>disabled</code></td>
        </tr>
    </tbody>
</table>

{% hint style="info" %}
`minLength` and `maxLength` validation attributes are only available on `gmd-input` and `gmd-textarea` components. `gmd-select`, `gmd-checkbox`, `gmd-radio`, and `gmd-checkbox-group` don't support length validation.
{% endhint %}

#### Common attributes

All components share these base attributes:

- **`fieldKey`** — Unique identifier for the form field. Used as the metadata key when the subscription is created.
- **`name`** — Name of the form field.
- **`label`** — Display label shown to the API consumer.
- **`value`** — Default value for the field.
- **`required`** — When set, the field is mandatory and the form can't be submitted without a value.
- **`disabled`** — Prevents the consumer from interacting with the field.

#### Validation

`gmd-input` and `gmd-textarea` support the following validation attributes:

- **`minLength`** — Minimum number of characters required.
- **`maxLength`** — Maximum number of characters allowed. Hard cap is 256 for `gmd-input` and 1024 for `gmd-textarea`.
- **`pattern`** — (`gmd-input` and `gmd-textarea`) Regular expression pattern the value is validated against.

Validation errors use the following error codes: `required`, `minLength`, `maxLength`, and `pattern`.

### Validation constraints

Validation constraints are derived from the GMD content and stored as JSON. Constraints include required-field rules, length bounds, regex patterns, and allowed option lists. At submission time, the system validates submitted metadata against these constraints and rejects invalid submissions with detailed error messages. Constraints are automatically regenerated when the form is updated.

### Dynamic options with EL expressions

Option-bearing fields (`gmd-select`, `gmd-radio`, `gmd-checkbox-group`) support EL expressions to populate options from API metadata. Expressions use the syntax `{#api.metadata['key']}:fallback1,fallback2`. When the form is fetched for a specific API, the expression is resolved against that API's metadata. If resolution fails or no API context is available (e.g., in the Console Form Builder), the fallback values are used. Resolved options are returned in the `resolvedOptions` map and merged into the GMD content before display.

### Configuration errors and warnings

Configuration errors are classified by severity. **Critical errors** (`severity: 'error'`) block form save and include invalid EL syntax and missing fallback values. **Warnings** (`severity: 'warning'`) do not block save and include normalized length values (e.g., `maxLength` clamped to hard cap). The Console Form Builder save button is disabled only when critical errors exist.

### Subscription metadata

When an API consumer submits a subscription form, the form field values are stored as key-value pairs in the subscription's `metadata` property. Empty values (null, empty strings, whitespace-only) are filtered before storage.

{% hint style="info" %}
Metadata belongs to the subscription, not to the form itself. Each subscription stores its own metadata based on the form field values submitted at subscription time.
{% endhint %}

### Form visibility

Each environment has one subscription form. The **Visible to API consumers** toggle in the Console controls whether the form appears in the Developer Portal. When disabled, the form remains accessible via Management API but returns 404 from the Portal API.

Subscription forms aren't displayed for Keyless plans. In the Portal checkout flow, the form only renders when the selected plan requires authentication (API Key, OAuth2, JWT, or mTLS).

## Prerequisites

- Gravitee API Management 4.11.0 or later
- Subscription form feature enabled for the environment
- `environment-metadata-r` permission to view subscription forms
- `environment-metadata-u` permission to create, update, enable, or disable subscription forms
- Portal authentication required to retrieve subscription forms via Portal API
- For dynamic options: API metadata keys referenced in EL expressions must exist on target APIs
