# MCP Installation Widget Reference

## Restrictions

* The MCP installation widget requires at least one entrypoint URL; if `api.entrypoints` is empty, the installation URL will be incomplete
* Seeding skips API navigation items that already have a child page; existing Overview pages are not overwritten
* Only `MCP_PROXY` APIs trigger MCP-specific Overview seeding; `LLM_PROXY` and `A2A_PROXY` types use the generic template
* FreeMarker templates must include null and size checks when accessing `api.entrypoints[0]` to avoid rendering errors
* The `<gmd-install-mcp>` component displays a placeholder if required attributes (`name`, `transport`, and transport-specific fields) are missing or invalid
* Values for `api.entrypoints` and `api.mcp` are populated only from V4 API entrypoint configuration with `mcp` or `mcp-proxy` types

## Related Changes

* The Developer Portal now accepts three new API types: `MCP_PROXY`, `LLM_PROXY`, and `A2A_PROXY`
* The HTML sanitizer allowlist has been updated to preserve the `<gmd-install-mcp>` tag and its attributes (`name`, `transport`, `url`, `headers`, `command`, `args`, `env`, `clients`) when storing Gravitee Markdown portal pages
* The FreeMarker template model for V4 APIs now exposes `api.entrypoints` (list of gateway entrypoint URLs) and `api.mcp` (map of MCP-related configuration including `mcpPath`), enabling template authors to construct installation URLs dynamically
* These changes were introduced in APIM-14224 (component, sanitizer, and template model) and APIM-14225 (default page seeding)
