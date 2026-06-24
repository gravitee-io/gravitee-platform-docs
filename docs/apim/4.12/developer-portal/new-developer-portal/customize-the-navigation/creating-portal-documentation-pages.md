# Creating Portal Documentation Pages

## Overview

Portal administrators can create and configure three types of documentation pages in the portal navigation tree: Gravitee Markdown, OpenAPI, and AsyncAPI. OpenAPI pages support configurable viewers (Swagger UI or Redoc) with granular control over display, Try It Out behavior, and server URL resolution. AsyncAPI pages provide a split-pane editor with live preview and interactive documentation rendering. All page types are created and edited in the Console's Portal Navigation settings (`/#!/default/_portal/navigation`) and published to the developer portal for end users. This feature applies only to Next-Gen portal documentation in the Portal Navigation settings screen; legacy API-level documentation screens are not impacted.

## Key Concepts

### Page Types

Portal navigation supports three documentation page types, each optimized for different content formats and use cases.

| Page Type | Content Format | Console Editor | Portal Viewer |
|:----------|:---------------|:---------------|:--------------|
| Gravitee Markdown | Markdown content | Markdown editor | Rendered markdown |
| OpenAPI | OpenAPI specification | Split editor with live preview | Swagger UI or Redoc (configurable) |
| AsyncAPI | AsyncAPI specification | Split YAML editor with live preview | Interactive AsyncAPI documentation viewer |

### OpenAPI Viewer Options

OpenAPI pages can be rendered using Swagger UI or Redoc. Swagger UI is best for interactive documentation with Try It Out, OAuth, and rich display options. Redoc provides a read-focused API reference layout. Viewer selection and configuration apply to both the Console live preview and the published portal page. The Redoc viewer does not support all Swagger UI features; Try It mode is limited to server URL override via **Base URL**. Viewer settings are stored with the page content and survive publish/unpublish and navigation changes. Settings remain compatible with how OpenAPI page configuration worked in earlier releases.

### Existing OpenAPI Page Migration

Existing OpenAPI pages that had no viewer configuration before this feature are treated as Redoc pages, preserving prior portal behavior. The `OpenApiPortalPageContentConfigurationUpgrader` (order 720) runs on startup and automatically sets default configuration `{"viewer":"REDOC"}` for existing OpenAPI pages without configuration.

## Prerequisites

* Access to the Console's Portal Navigation settings (`/#!/default/_portal/navigation`)
* For OpenAPI Try It Out: CORS may need to be configured on the API entrypoint to allow browser-based API calls
* For AsyncAPI pages: The `assets/style/asyncapi-console-preview.css` file must be present in the Console build output
* For Redoc viewer: The `redoc.standalone.js` script must be available in `assets/redoc/`; if the script fails to load, the viewer will not render

## Gateway Configuration

No gateway-level configuration is required for portal documentation pages. All settings are managed through the Console's Portal Navigation interface.

## Creating Documentation Pages

Navigate to the Portal Navigation settings in the Console (`/#!/default/_portal/navigation`). When adding a new page, select the page type from the dialog: **Gravitee Markdown**, **OpenAPI**, or **AsyncAPI**. New AsyncAPI pages are created with a starter AsyncAPI 3.0 template so editing can begin immediately.

For OpenAPI pages, use the split editor to write or paste the specification on the left and preview the rendered documentation on the right. For AsyncAPI pages, edit the YAML specification in the left pane and use the live preview on the right to check the result. The preview is optimized for the Console's side-by-side layout. The AsyncAPI editor implements `ControlValueAccessor` for Angular forms integration and supports disabled state propagation.

Before saving an AsyncAPI page, the Console validates that the content is valid YAML and includes an `asyncapi` version field with a valid semantic version. If validation fails, an error message is displayed and the page is not saved. The Save button is disabled when the content is invalid (`contentControl.invalid === true`) or when the form is pristine (`contentControl.pristine === true`).
