
# Subscription form field attributes and validation constraints reference


## Key Concepts

### Checkbox Group Field

A checkbox group is a multi-select input component that allows subscribers to choose one or more options from a predefined or dynamically resolved list. Selected values are serialized as comma-separated strings and sorted alphabetically (e.g., `"Option 1,Option 3"`). Checkbox groups support required validation (at least one selection must be made) and option list validation (all selected values must exist in the allowed options).

| Attribute | Type | Description | Example |
|:----------|:-----|:------------|:--------|
| `fieldKey` | string | Unique identifier for the field in form state and metadata | `"features"` |
| `label` | string | Display label rendered as fieldset legend | `"Select Features"` |
| `options` | string | Comma-separated list or EL expression with fallback | `"{#api.metadata['features']}:Auth,Logging"` |
| `required` | boolean | Whether at least one option must be selected | `true` |
| `value` | string | Comma-separated preselected values | `"Auth,Logging"` |
| `disabled` | boolean | Disables all checkboxes and removes field from form state | `false` |

### Dynamic Options Resolution

Options can be populated at runtime using Expression Language (EL) expressions that reference API or environment metadata. Expressions follow the syntax `{#api.metadata['key']}:fallback1,fallback2`, where the fallback list is required and used when no API context is available (e.g., in the Console Form Builder) or when the metadata key is missing.

Invalid EL syntax triggers configuration errors that block form saving:
- Expressions starting with `#{` or `{` without `#` report an `invalidElSyntax` error
- Missing fallback values report a `missingElFallback` error

Configuration errors with severity `error` block form saving. Warnings do not block save.

### Validation Constraints

Subscription form submissions are validated against constraints derived from the form schema. Validation occurs before subscription creation and returns HTTP 400 with field-level error messages when constraints are violated.

Constraints include required field checks, length limits, pattern matching, and option list validation. Checkbox groups enforce **Non-Empty Selection** (at least one value when required) and **Each Of** (every selected value must exist in the allowed options list).

| Constraint | Applies To | Rule | Error Message |
|:-----------|:-----------|:-----|:--------------|
| Required | Text fields | Value must not be blank | `"Field '{fieldKey}' is required"` |
| Must Be True | Checkbox | Value must equal `"true"` | `"Field '{fieldKey}' is required"` |
| Non-Empty Selection | Checkbox group | At least one value in CSV | `"Field '{fieldKey}' is required"` |
| Each Of | Checkbox group | Every CSV value in allowed list | `"Field '{fieldKey}': value '{item}' is not among the allowed options"` |
| Min Length | Input, Textarea | Length ≥ min (skipped when empty) | `"Field '{fieldKey}' must be at least {min} characters long"` |
| Max Length | Input, Textarea | Length ≤ max (skipped when empty) | `"Field '{fieldKey}' must be at most {max} characters long"` |
| Matches Pattern | Input | Value matches regex (skipped when empty) | `"Field '{fieldKey}' does not match the required pattern"` |
| One Of | Select, Radio | Single value in allowed list | `"Field '{fieldKey}': value '{value}' is not among the allowed options"` |
| Read Only | Any field with readonly value | Value must equal preset reference | `"Field '{fieldKey}': read-only field cannot be modified"` |

Hard length limits are enforced for input and textarea fields:
- **Input fields**: 256 characters maximum. User-defined `maxLength` values are clamped to 256. When omitted, 256 is used.
- **Textarea fields**: 1024 characters maximum. User-defined `maxLength` values are clamped to 1024. When omitted, 1024 is used.

## Prerequisites

- Gravitee API Management 4.11.0 or later
- Subscription form enabled for the environment
- For dynamic options: API metadata keys referenced in EL expressions must exist or fallback values will be used
