---
hidden: true
noIndex: true
---

# Portal Page Content Validator API Changes

## Related Changes

Portal page content validators now receive the existing page content to determine context (navigation placement, enclosing API) during validation. The validation interface signature changed from `validate(UpdatePortalPageContent updateContent)` to `validate(PortalPageContent<?> existingContent, UpdatePortalPageContent updateContent)`. All implementations of `PortalPageContentValidator` must update their method signatures accordingly.

Gravitee Markdown content validation now performs a dry-run FreeMarker template rendering with the appropriate model (API or environment metadata) and throws `InvalidPortalPageContentTemplateException` if the template is invalid or references missing properties.
