---
hidden: true
noIndex: true
---

# Portal Navigation Templating Concepts

## Key Concepts

### FreeMarker Template Expressions

Gravitee Markdown pages (`.md` content served through the Developer Portal) support FreeMarker template expressions. Embed `${...}` expressions and FreeMarker directives directly inside page content; they are evaluated at render time before the markdown is parsed and returned to the client. Template rendering occurs when the page is requested, not when it is saved.

### Template Context

The data available inside a template depends on whether the page is attached to an API or is a standalone environment page. API pages expose an `api` root variable containing the full API model object. Environment pages (homepage, standalone documentation) expose a `metadata` root variable containing a flat map of environment-level key/value pairs. Only one of these two variables is present in any given render call — they are mutually exclusive.

### Enclosing API Resolution

Portal navigation items resolve their "enclosing API" by walking the `parentId` chain until an API node is found. If no API ancestor exists, the page is scoped to environment metadata only. This resolution determines which template context (API or environment) is used during validation and rendering.

### Environment Metadata

On environment (non-API) pages the root variable is `metadata`, a flat map of environment-level key/value pairs set in the portal configuration. Access entries with bracket notation: `${metadata['portal-name']}`, `${metadata['support-email']}`.
