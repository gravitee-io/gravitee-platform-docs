# Portal Navigation Templating Restrictions and Technical Requirements

## Restrictions

- Template validation occurs only when a portal navigation page is linked to the content; orphaned content is not validated.
- The FreeMarker template model depends on navigation hierarchy: pages under an API node receive `${api.*}` model, root-level pages receive `${metadata.*}` model.
- Template rendering failures during read operations (e.g., portal API GET) are surfaced as technical errors, not validation errors.
- All implementations of `PortalPageContentValidator` must update their `validate` method signature to accept `PortalPageContent<?> existingContent` as the first parameter.

## Related Changes

The portal navigation items component now suppresses generic error messages when HTTP error responses are received, allowing specific backend validation messages to be displayed. The `PortalPageContentValidator` interface signature has changed to include the existing content as a parameter, requiring updates to all validator implementations (Gravitee Markdown and OpenAPI validators).
