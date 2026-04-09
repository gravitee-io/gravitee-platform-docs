# Subscription form feature overview

## Overview

The subscription form feature enables API publishers to define a custom form that API consumers complete when subscribing to API plans. Forms are authored in Gravitee Markdown (GMD) and collect structured metadata stored with each subscription. This feature replaces the legacy comment field from the Classic Portal.

Subscription forms collect metadata from API consumers during subscription creation. Administrators can configure forms with static or API-metadata-driven options; the platform validates submissions against field-level rules before creating subscriptions.

## Key concepts

### Gravitee Markdown (GMD) content

GMD is a structured markup language used to define form fields and layout. Form content is authored in the Management Console using a form editor with live preview.

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
            <td><code>fieldKey</code>, <code>name</code>, <code>label</code>, <code>placeholder</code>, <code>value</code>, <code>required</code>, <code>minLength</code>, <code>maxLength</code>, <code>pattern</code>, <code>readonly</code>, <code>disabled</code></td>
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
            <td><code>gmd-checkbox-group</code></td>
            <td>Checkbox group field allowing multiple selections</td>
            <td><code>fieldKey</code>, <code>name</code>, <code>label</code>, <code>value</code>, <code>required</code>, <code>options</code>, <code>disabled</code></td>
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
- **`maxLength`** — Maximum number of characters allowed.
- **`pattern`** — (`gmd-input` only) Regular expression pattern the value is validated against.

Validation errors use the following error codes: `required`, `minLength`, `maxLength`, and `pattern`.

#### Checkbox group fields

Checkbox group fields allow multiple selections from a list of options. Values are serialized as comma-separated strings (e.g., `"Option 1,Option 3"`). The `gmd-checkbox-group` component supports static options, dynamic options resolved from API metadata, and required validation. When required, at least one option must be selected.

#### Dynamic options resolution

Fields can define options using Expression Language (EL) expressions that reference API metadata. The syntax `{#api.metadata['key']}:fallback1,fallback2` resolves the expression at runtime and falls back to the comma-separated list if resolution fails. Dynamic options are supported in `gmd-select`, `gmd-radio`, and `gmd-checkbox-group` fields. In preview contexts (Console Form Builder), fallback values are displayed; in runtime contexts (Portal subscription flow), the expression is resolved against the API's metadata.

#### Validation constraints

Subscription forms generate validation constraints from field definitions. Constraints include required fields, min/max length, pattern matching, read-only enforcement, and option membership checks. Constraints are persisted alongside the form definition and applied during subscription creation. If validation fails, the platform returns a `SubscriptionFormValidationException` with all constraint violations.

| Constraint Type | Applies To | Behavior |
|:----------------|:-----------|:---------|
| Required | Text fields | Field must not be blank |
| Must Be True | Checkbox | Value must be `"true"` |
| Non-Empty Selection | Checkbox group | At least one value must be selected |
| Read Only | Input, Textarea, Radio, Checkbox | Value must equal the preset read-only reference |
| Min Length | Input, Textarea | Value must be at least `min` characters long (skipped when empty) |
| Max Length | Input, Textarea | Value must be at most `max` characters long (skipped when empty); system caps enforced |
| Matches Pattern | Input | Value must match the given regular expression (skipped when empty) |
| One Of | Select, Radio | Single value must be one of the allowed options (skipped when empty) |
| Each Of | Checkbox group | Every value in a comma-separated string must be one of the allowed options (skipped when empty) |

#### Hard limits

| Limit | Value | Description |
|:------|:------|:------------|
| Maximum fields | 25 | Maximum number of fields allowed in a subscription form |
| Input field length | 256 characters | Maximum length for `gmd-input` fields |
| Textarea field length | 1024 characters | Maximum length for `gmd-textarea` fields |
| Metadata entries | 25 | Maximum number of metadata entries accepted in a subscription form submission |

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
- `environment-metadata-r` permission to view subscription forms
- `environment-metadata-u` permission to create, update, enable, or disable subscription forms
- Portal authentication required to retrieve subscription forms via Portal API
- For dynamic options: API metadata keys referenced in EL expressions must exist

## Creating subscription forms

To create a subscription form, navigate to the environment settings in the Console and define the form using Gravitee Markdown (GMD) syntax. Add fields using GMD components such as `gmd-input`, `gmd-textarea`, `gmd-select`, `gmd-radio`, `gmd-checkbox`, and `gmd-checkbox-group`. For checkbox groups, set the `fieldKey` attribute to identify the field, `label` to display a legend, and `options` to define the available choices (either as a comma-separated list or an EL expression with fallback values). Mark fields as required by setting `required="true"`. When you save the form, the platform parses the GMD content, generates validation constraints, and persists them in the `validation_constraints` column. If the form exceeds 25 fields, the platform rejects the definition with a `SubscriptionFormDefinitionValidationException`.

## Subscribing to APIs with forms

When a user subscribes to an API with an enabled subscription form, the Portal retrieves the form via `GET /apis/{apiId}/subscription-form`. The endpoint resolves EL expressions in dynamic option fields against the API's metadata and returns the form content with a `resolvedOptions` map. The Portal merges resolved options into the GMD content by updating the `options` attribute of matching fields. The user completes the form, and the platform validates the submission against the persisted constraints. If any constraint fails, the platform returns a `SubscriptionFormValidationException` with all error messages. If the submission exceeds 25 metadata entries, the platform rejects it with the message `"Subscription metadata must not exceed 25 entries"`.

### Portal API

**Endpoint:** `GET /apis/{apiId}/subscription-form`

**Response:**

```json
{
  "gmdContent": "string",
  "resolvedOptions": {
    "fieldKey1": ["option1", "option2"],
    "fieldKey2": ["optionA", "optionB"]
  }
}
```

Returns the subscription form content when the form exists and is enabled for the environment. EL expressions in option-bearing fields are resolved against the API's metadata. If resolution fails, fallback values are returned. Returns 404 when no subscription form exists for the environment, when the form is disabled, or when the API is not visible to the user.

### Management API v2

**Endpoint:** `GET /environments/{envId}/subscription-forms`

**Response:**

```json
{
  "id": "uuid",
  "gmdContent": "string",
  "enabled": false,
  "resolvedOptions": {
    "fieldKey": ["option1", "option2"]
  }
}
```

Returns the subscription form for an environment. `resolvedOptions` is present only when at least one field has dynamic options. Keys are field keys; values are the effective option lists (fallback values when no API context is available).
