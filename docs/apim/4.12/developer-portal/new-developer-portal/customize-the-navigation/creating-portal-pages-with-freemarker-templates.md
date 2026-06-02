# Creating Portal Pages with FreeMarker Templates

## Prerequisites

Before creating portal navigation pages with FreeMarker templates, ensure the following:

* Portal navigation structure is configured
* For API-scoped templates: the page must be nested under an API node in the navigation tree
* For environment-scoped templates: the page must be at root level or under a non-API node

## Creating Portal Navigation Pages with Templates

To create a portal navigation page with FreeMarker templating:

1. Navigate to the portal navigation editor.
2. Add or edit a Gravitee Markdown page.
3. Enter your markdown content with embedded FreeMarker expressions:
   * For API-scoped pages: use `${api.name}` or other API metadata properties
   * For environment-scoped pages: use `${metadata.key}` or other environment metadata properties
4. Position the page in the navigation tree according to the desired template context:
   * Nest the page under an API node to access API metadata
   * Place the page at root level to access environment metadata
5. Save the page.

The system validates the template by dry-rendering it with the appropriate model. If validation succeeds, the page is saved. If the template contains invalid expressions or references missing model properties, the save operation fails and displays an error message describing the issue (e.g., `"Invalid expression or value is missing for <expression>"`).
