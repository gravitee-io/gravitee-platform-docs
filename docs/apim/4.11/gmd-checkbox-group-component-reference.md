# GMD Checkbox Group Component Reference

### GMD Component Properties

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| **Name** | string | `''` | HTML name attribute for checkbox inputs |
| **Label** | string | — | Display label shown above the group (renders as `<legend>`) |
| **Field Key** | string | — | Key used for form state tracking and data collection |
| **Value** | string | — | Comma-separated preselected values (e.g., `"Option 1,Option 3"`) |
| **Required** | boolean | `false` | Whether at least one option must be selected |
| **Options** | string | `''` | Comma-separated list of options or EL expression with fallback (e.g., `"{#api.metadata['key']}:option1,option2"`) |
| **Disabled** | boolean | `false` | Disables all checkboxes and removes field from form state |

**Value Format:**

- Single selection: `"Option 1"`
- Multiple selections: `"Option 1,Option 3"`
- No selection: `""`

**Options Syntax:**

- **Static options:** Comma-separated list (e.g., `"Authentication,Rate Limiting,Analytics"`)
- **Dynamic options:** EL expression with fallback values (e.g., `"{#api.metadata['key']}:option1,option2"`)

When using dynamic options:
- In preview/editing contexts (Console Form Builder), fallback values are displayed.
- At runtime (Portal subscription flow), the expression is resolved against the API's metadata.
- If resolution fails, fallback values are used.

**Validation:**

When **Required** is `true`, at least one option must be selected. For more information about subscription form validation constraints and error messages, see the [Validation Constraints](subscription-form-feature-overview.md#validation-constraints) section.

**Disabled Behavior:**

When **Disabled** is `true`, all checkboxes are disabled and the field is removed from form state.

**API Integration:**

For how `resolvedOptions` are merged into GMD content at runtime, see the [Portal API Reference](../developer-portal/new-developer-portal/subscription-form-technical-implementation.md#get-apisapiidsubscription-form).

## Restrictions

- A field cannot define both static **Options** and dynamic options. The schema constructor throws `IllegalArgumentException` if both are present.
- EL expressions must start with `{#`. Expressions starting with `#{` or `{` (without `#`) trigger an `invalidElSyntax` config error.
- EL expressions in **Options** must include fallback values after `}:`. If omitted, the component reports a `missingElFallback` config error.
- The `gmd-checkbox-group` component does not support the `readonly` attribute.
