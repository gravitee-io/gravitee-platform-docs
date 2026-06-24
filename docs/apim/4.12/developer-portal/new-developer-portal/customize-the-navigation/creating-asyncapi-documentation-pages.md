# Creating AsyncAPI Documentation Pages

## AsyncAPI pages

AsyncAPI pages use a single interactive documentation viewer. When creating a new AsyncAPI page, the Console loads a starter AsyncAPI 3.0 template. The Console validates that content is valid YAML with a properly formatted `asyncapi` version field (semantic version format like `3.0.0`) before saving.

## Prerequisites

Before configuring OpenAPI viewer settings, ensure you have the following:

* `ENVIRONMENT_DOCUMENTATION[update]` permission
* For Try It Out functionality: CORS may need to be configured on the API entrypoint
* For OAuth with PKCE: OAuth provider must support PKCE flows

## Creating Documentation Pages

1. Navigate to **Portal → Navigation** in the Console.
2. To add a new documentation page, select the page type from the type selector:
   * **Gravitee Markdown**: For markdown content
   * **OpenAPI**: For OpenAPI specifications with configurable viewers
   * **AsyncAPI**: For AsyncAPI specifications

When creating an AsyncAPI page, the Console loads a starter AsyncAPI 3.0 template with a sample channel and operation. Edit the specification in the YAML editor on the left; the live preview on the right updates as you type.

Before saving, the Console validates that the content is valid YAML and includes a properly formatted `asyncapi` version field. If validation fails, an error message appears and the page is not saved.

For OpenAPI pages, the editor displays a split layout with the specification on one side and a live preview on the other. The preview matches the selected viewer (Swagger UI or Redoc) and reflects configuration changes during the editing session without requiring a separate save.

## Viewing Documentation in the Portal

Published OpenAPI pages render according to the saved viewer configuration. Swagger UI honors all configured options, including Try It Out (authenticated and optionally anonymous), OAuth with PKCE, custom or entrypoint-derived server URLs, and display settings. When entrypoint or context-path options are enabled, the platform resolves the enclosing API and serves a specification with the correct server URLs applied so Try It Out targets the live API gateway.

Redoc shows the page with the Redoc viewer; an optional base URL can be supplied where relevant.

Try It Out is available when **Enable Try It Out mode** is enabled and the user is authenticated. If **Enable Try It Out mode for anonymous users** is also enabled, Try It Out is available for users who are not logged in.

Published AsyncAPI pages render using an interactive AsyncAPI documentation viewer. Visitors can browse channels, messages, and other specification details.
