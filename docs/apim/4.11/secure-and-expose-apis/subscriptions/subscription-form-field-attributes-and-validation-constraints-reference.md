# Subscription form field attributes and validation constraints reference

This reference documents the attributes supported by the `gmd-checkbox-group` form component, the syntax for dynamic options, and the validation constraints applied to subscription form submissions.

## Checkbox group attributes

A checkbox group is a multi-select form field that lets subscribers choose one or more options from a predefined or dynamically resolved list. Selected values are serialized as a comma-separated string sorted alphabetically (for example, `"Option 1,Option 3"`).

| Attribute | Type | Description | Example |
|:----------|:-----|:------------|:--------|
| `fieldKey` | string | Unique identifier for the field, used as the key in the subscription's `metadata` object | `"features"` |
| `label` | string | Display label rendered as the fieldset legend | `"Select Features"` |
| `options` | string | Comma-separated list, or an EL expression followed by a fallback list | `"{#api.metadata['features']}:Auth,Logging"` |
| `required` | boolean | Set to `true` to require at least one selection | `true` |
| `value` | string | Comma-separated preselected values | `"Auth,Logging"` |
| `disabled` | boolean | Set to `true` to disable all checkboxes | `false` |

## Dynamic options with EL expressions

Options on `gmd-select`, `gmd-radio`, and `gmd-checkbox-group` can be populated at runtime using Expression Language (EL) expressions that reference API or environment metadata. Expressions use the syntax `{#expression}:fallback1,fallback2`, where the fallback list is required.

The fallback list is applied when:

- The Portal is rendering the form but the EL expression's metadata key doesn't exist.
- The form is being previewed in the Console subscription form editor, which doesn't resolve EL against API metadata.

Invalid EL syntax produces configuration errors that block saving:

- Expressions that start with `#{`, or `{` without a following `#`, report an `invalidElSyntax` error.
- Expressions without a fallback list after the `}:` separator report a `missingElFallback` error.

Configuration errors with severity `error` block form saving. Warnings don't block saving.

## Validation constraints

Subscription form submissions are validated against constraints derived from the form schema before the subscription is created. When a constraint fails, the submission is rejected with field-level error messages.

The following constraints are applied at submission time:

| Constraint | Applies to | Rule |
|:-----------|:-----------|:-----|
| Required | `gmd-input`, `gmd-textarea`, `gmd-select`, `gmd-radio` | Value isn't blank |
| Must be true | `gmd-checkbox` | Value equals `"true"` |
| Non-empty selection | `gmd-checkbox-group` | At least one value is selected |
| Each of | `gmd-checkbox-group` | Every selected value is in the allowed options list |
| Min length | `gmd-input`, `gmd-textarea` | Length is at least `minLength` (skipped when the value is empty) |
| Max length | `gmd-input`, `gmd-textarea` | Length is at most `maxLength` (skipped when the value is empty) |
| Matches pattern | `gmd-input` | Value matches the configured regex (skipped when the value is empty) |
| One of | `gmd-select`, `gmd-radio` | Value is in the allowed options list |
| Read only | Any field marked `readonly` with a preset `value` | Value equals the preset reference |

### Hard length limits

The following hard length limits are always enforced regardless of user configuration:

- **Input fields** — 256 characters maximum. User-defined `maxLength` values are clamped to 256, and 256 is applied when `maxLength` is omitted.
- **Textarea fields** — 1024 characters maximum. User-defined `maxLength` values are clamped to 1024, and 1024 is applied when `maxLength` is omitted.

### Field count limit

Subscription forms are limited to a maximum of 25 fields. The form editor enforces this limit at save time and rejects forms that exceed it. Subscription submissions are also capped at 25 metadata entries.
