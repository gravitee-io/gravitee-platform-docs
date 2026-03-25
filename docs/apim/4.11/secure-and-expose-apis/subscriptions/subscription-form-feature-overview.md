# Subscription form feature overview

## Overview

The subscription form feature enables API publishers to define a custom form that API consumers complete when subscribing to API plans. Forms are authored in Gravitee Markdown (GMD) and collect structured metadata stored with each subscription. This feature replaces the legacy comment field from the Classic Portal.

## Key concepts

### Gravitee Markdown (GMD) content

GMD is a structured markup language used to define form fields and layout. Form content is authored in the Management Console using a split-pane editor with live preview (source on left, rendered form on right). The GMD content is validated and stored in the subscription form entity.

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
            <td><code>fieldKey</code>, <code>name</code>, <code>label</code>, <code>placeholder</code>, <code>value</code>, <code>required</code>, <code>minLength</code>, <code>maxLength</code>, <code>pattern</code>, <code>type</code>, <code>readonly</code>, <code>disabled</code></td>
        </tr>
        <tr>
            <td><code>gmd-textarea</code></td>
            <td>Multi-line text input field</td>
            <td><code>fieldKey</code>, <code>name</code>, <code>label</code>, <code>placeholder</code>, <code>value</code>, <code>required</code>, <code>minLength</code>, <code>maxLength</code>, <code>rows</code>, <code>readonly</code>, <code>disabled</code></td>
        </tr>
        <tr>
            <td><code>gmd-select</code></td>
            <td>Dropdown selection field</td>
            <td><code>fieldKey</code>, <code>name</code>, <code>label</code>, <code>value</code>, <code>required</code>, <code>options</code>, <code>disabled</code></td>
        </tr>
        <tr>
            <td><code>gmd-checkbox</code></td>
            <td>Checkbox field</td>
            <td><code>fieldKey</code>, <code>name</code>, <code>label</code>, <code>value</code>, <code>required</code>, <code>readonly</code>, <code>disabled</code></td>
        </tr>
        <tr>
            <td><code>gmd-radio</code></td>
            <td>Radio button selection field</td>
            <td><code>fieldKey</code>, <code>name</code>, <code>label</code>, <code>value</code>, <code>required</code>, <code>options</code>, <code>readonly</code>, <code>disabled</code></td>
        </tr>
        <tr>
            <td><code>gmd-card</code></td>
            <td>Container for grouping form elements</td>
            <td>Supports nested <code>gmd-card-title</code> and other GMD components</td>
        </tr>
        <tr>
            <td><code>gmd-grid</code></td>
            <td>Layout grid for organizing form elements</td>
            <td><code>columns</code></td>
        </tr>
    </tbody>
</table>

{% hint style="info" %}
`minLength` and `maxLength` validation attributes are only available on `gmd-input` and `gmd-textarea` components. `gmd-select`, `gmd-checkbox`, and `gmd-radio` don't support length validation.
{% endhint %}

#### Common attributes

All form components share these base attributes:

- **`fieldKey`** — Unique identifier for the form field. Used as the metadata key when the subscription is created. If omitted, the field value isn't submitted with the form. Metadata keys must not contain spaces or special characters.
- **`name`** — Name of the form field and HTML id attribute.
- **`label`** — Display label shown to the API consumer.
- **`value`** — Default value for the field.
- **`required`** — When set, the field is mandatory and the form can't be submitted without a value.
- **`disabled`** — Prevents the consumer from interacting with the field.
- **`readonly`** — Makes the field read-only.
- **`placeholder`** — Placeholder text displayed when the field is empty.

#### Input-specific attributes

`gmd-input` supports an additional `type` attribute that accepts the following values: `text`, `email`, `url`, `number`.

`gmd-textarea` supports a `rows` attribute to control the height of the text area.

`gmd-select` and `gmd-radio` require an `options` attribute containing comma-separated values for the available choices.

`gmd-grid` requires a `columns` attribute to define the number of columns in the layout grid.

#### Validation

`gmd-input` and `gmd-textarea` support the following validation attributes:

- **`minLength`** — Minimum number of characters required.
- **`maxLength`** — Maximum number of characters allowed.
- **`pattern`** — (`gmd-input` only) Regular expression pattern the value is validated against.

Validation errors use the following error codes: `required`, `minLength`, `maxLength`, and `pattern`.

### Subscription metadata

When an API consumer submits a subscription form, the form field values are stored as key-value pairs in the subscription's `metadata` property. Empty values (null, empty strings, whitespace-only) are filtered before storage. Metadata is displayed in read-only JSON format in the Console.

{% hint style="info" %}
Metadata belongs to the subscription, not to the form itself. Each subscription stores its own metadata based on the form field values submitted at subscription time.
{% endhint %}

### Form visibility

Each environment has one subscription form. The **Visible to API consumers** toggle in the Console controls whether the form appears in the Developer Portal. When disabled, the form remains accessible via Management API but returns 404 from the Portal API.

Subscription forms aren't displayed for Keyless plans. In the Portal checkout flow, the form only renders when the selected plan requires authentication (API Key, OAuth2, JWT, or mTLS).

## Prerequisites

- `environment-metadata-r` permission to view subscription forms
- `environment-metadata-u` permission to create, update, enable, or disable subscription forms
- Portal authentication required to retrieve subscription forms via Portal API
