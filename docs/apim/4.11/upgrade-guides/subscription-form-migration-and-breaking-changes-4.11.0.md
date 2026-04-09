# Subscription Form Migration and Breaking Changes (4.11.0)

## Related Changes

### Console Form Builder

The Console Form Builder now distinguishes between critical configuration errors (severity `error`) and warnings. Only critical errors block save operations. Warnings (e.g., normalized length values) do not prevent saving the form.

### Deprecated Endpoint Removal

The deprecated endpoint `GET /subscription-form` has been removed. Use `GET /apis/{apiId}/subscription-form` instead. The new endpoint requires an API context and resolves EL expressions against the API's metadata.

### Portal UI Behavior

The Portal UI merges resolved options into GMD content by updating the `options` attribute of matching fields. This merged content must only be rendered by `gmd-viewer`, which sanitizes content before display. Do not bind this output to raw `innerHTML` or other unsanitized sinks.

### Database Schema

A `validation_constraints` column has been added to the `subscription_forms` table with a default value of `'{}'` (empty JSON object).

### MongoDB Upgrader Behavior

MongoDB upgraders backfill the `validationConstraints` field with `"{}"` for documents where the field is `null` or missing. A subsequent upgrader replaces `"{}"` with actual constraints derived from GMD content.

### CSS Spacing

GMD components (`gmd-checkbox-group`, `gmd-checkbox`, `gmd-input`, `gmd-radio`, `gmd-select`) now use `margin-block: 0.5rem` instead of `margin-bottom: 1rem`.

### JSON Array Format Removal

The JSON array format for options (e.g., `options='["Option 1","Option 2"]'`) has been removed. Use comma-separated strings instead (e.g., `options="Option 1,Option 2"`).

