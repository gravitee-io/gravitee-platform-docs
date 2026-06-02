
# Creating and managing API overview pages

## Creating API overview pages


Navigate to the API's documentation section in the Gravitee Management Console. When publishing an API navigation item, the platform automatically selects the appropriate template based on API type.

For standard APIs, the template displays a three-column grid with **Subscribe**, **Explore documentation**, and **Integrate** cards. For MCP proxy APIs, the template renders an `<gmd-install-mcp>` component with the gateway endpoint URL (`${api.entrypoints[0]}${api.mcp.mcpPath}`) and transport type set to `http`.

The API information card conditionally displays **Owner** and **Last deployed** fields only when `${api.primaryOwner.displayName}` and `${api.deployedAt}` are present. Customize the page by replacing placeholder sections with API-specific content, such as quick start guides, changelog links, or MCP tool descriptions.

## Managing Template Content

{% hint style="info" %}
**Note:** Information about template update mechanisms, file locations, inheritance rules, and custom template override behavior is not yet documented.
{% endhint %}

To modify template content, edit the Markdown files directly or use the Developer Portal's page editor.

The standard template includes a **Customize this page** section with suggestions:
- Add a Quick start section
- Link to guides or changelogs
- Reference the [Gravitee Developer Portal documentation](https://documentation.gravitee.io/apim/developer-portal/new-developer-portal)

The MCP template suggests:
- Document available MCP tools
- Describe authentication requirements and environment setup steps
- Link to [Secure MCP proxy with OAuth2](https://documentation.gravitee.io/apim/ai-agent-management/secure-mcp-proxy-with-oauth2)

Both templates support FreeMarker conditional rendering. Use `<#if api.description??>` to display optional fields.

## Restrictions

- The `${api.deployedAt}` variable is formatted as `yyyy-MM-dd` and displayed only when present
- The `${api.primaryOwner.displayName}` field is conditional and may not appear for all APIs
- The MCP template requires `${api.entrypoints[0]}` and `${api.mcp.mcpPath}` to generate valid installation configurations
- The `<gmd-install-mcp>` component is specific to the MCP template and not available in the standard template
- Template styling relies on CSS custom properties (`--gio-app-primary-main-color`) defined in the Developer Portal theme

## Related Changes

The standard API template replaces the generic **Explore the API** section with structured **Get started** cards and removes the **Type** and **Identifier** fields from the API information card. The **Owner** and **Last deployed** fields are now conditionally displayed.

Both templates introduce styled card components with primary color theming and include a **Customize this page** section with actionable guidance and documentation links.
