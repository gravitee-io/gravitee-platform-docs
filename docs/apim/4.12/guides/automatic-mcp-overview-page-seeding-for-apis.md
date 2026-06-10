# Automatic MCP Overview Page Seeding for APIs

## Automatic Overview Page Seeding

When default portal pages are created via `POST /portal-navigation-items/_default-pages`, the platform seeds an unpublished "Overview" child page for each API navigation item that does not already have child pages. The seeding behavior varies by API type.

To configure the API type:

1. Navigate to **APIs** in the left sidebar.
2. Select the API you want to configure.
3. Click **Configuration** in the API navigation menu.
4. In the **General** tab, locate the API type field.



The seeding logic applies the following templates based on API type:

- **MCP_PROXY APIs**: Receive an MCP-oriented Overview page (`api-overview-mcp-proxy-page-content.md`) that includes API metadata and a pre-configured `<gmd-install-mcp>` widget with HTTP transport. The widget's `url` attribute is constructed from the first entrypoint URL plus the `mcpPath` value from `api.mcp` (when present).
- **All other API types** (PROXY, MESSAGE, NATIVE, LLM_PROXY, A2A_PROXY): Receive the generic Overview template (`api-overview-page-content.md`).

Seeding is skipped entirely if the API navigation item already has at least one child page. This prevents overwriting custom portal content. All seeded pages are unpublished by default.

## Theming

Use the `@gmd.install-mcp-overrides()` SCSS mixin to customize component tokens for the MCP install widget.

