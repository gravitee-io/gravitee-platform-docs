# Troubleshooting Portal Page Template Validation Errors

## Managing Portal Page Validation Errors

When a portal navigation page save operation fails due to template validation errors, the Console displays backend-specific error messages instead of generic failure notifications. HTTP errors (status 400, 500, etc.) are handled by the HTTP error interceptor, which surfaces the exact validation failure reason returned by the backend. Non-HTTP errors still trigger a generic `"Failed to update page content"` message.

Template validation errors include:

* **FreeMarker evaluation failures**: Occur when a variable is missing from the model. Example error message: `"Invalid expression or value is missing for <expression>"`
* **Parse failures**: Occur when the template contains syntax errors. Example error message: `"Invalid template: <message>"`

These messages help identify whether the issue is a missing model property, incorrect expression syntax, or a mismatch between the page's navigation context and the template's expectations.

## Restrictions

* Template validation occurs only when a navigation page is linked to content. Orphaned content is not validated.
* The FreeMarker model is context-dependent: pages under an API node receive the `api` object; root-level pages receive the `metadata` object.
* Template rendering failures during validation do not provide line or column numbers from FreeMarker diagnostics.
* Implementations of `PortalPageContentValidator` must update the `validate` method signature to accept both `PortalPageContent<?> existingContent` and `UpdatePortalPageContent updateContent` parameters.

## Related Changes

The portal navigation items component in the Console now suppresses generic error snackbars for HTTP errors during page save operations, allowing the HTTP error interceptor to display backend-specific validation messages. The `PortalPageContentValidator` interface signature has changed to accept the existing content alongside the update payload, enabling context-aware validation. Two new exception types (`InvalidPortalPageContentTemplateException` and `PortalPageContentTemplateException`) provide structured error reporting for template validation failures.
