# Portal Navigation Page Templating Concepts

## Overview

Portal navigation pages in Gravitee Markdown format support FreeMarker templating, allowing dynamic content based on the page's location in the navigation tree. When a page is nested under an API, it can reference API metadata. Root-level pages can reference environment metadata. Template validation occurs at save time, with error handling that surfaces backend-specific validation messages.

## Key Concepts

### FreeMarker Templating in Portal Pages

Portal navigation pages written in Gravitee Markdown can embed FreeMarker expressions to inject dynamic content. The available data model depends on the page's position in the navigation hierarchy. Pages nested under an API node receive an `api` object containing API metadata. Pages at the root level or under non-API nodes receive a `metadata` object containing environment-level metadata. Template expressions are evaluated during content validation to ensure they reference valid model properties.

### Context-Dependent Template Models

| Navigation Context | Available Model Object | Description |
|:-------------------|:-----------------------|:------------|
| Page under API node | `api` | API metadata from the enclosing API ancestor |
| Page at root level or under non-API node | `metadata` | Environment-level metadata |

### Validation Workflow

When a portal navigation page is saved, the system resolves the page's enclosing API by walking the parent navigation chain. If an API ancestor exists, the validator builds a FreeMarker model containing the API's metadata. If no API ancestor is found, the model contains environment metadata. The page content is then dry-rendered with FreeMarker. If the template contains invalid expressions or syntax errors, the save operation fails with a descriptive error message. Template validation occurs only when a navigation page is linked to content; orphaned content is not validated.
