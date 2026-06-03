# Creating and Customizing API Overview Pages

## Creating API Overview Pages

When publishing an API to the Developer Portal, the platform automatically selects the appropriate template based on API type. For standard APIs, navigate to the API documentation editor and the system populates the overview page with the standard template. For MCP proxy APIs, the MCP-specific template is applied. Both templates render dynamic content using API metadata variables: `${api.name}` for the page title, `${api.version}` and `${api.visibility}` in the information card, and `${api.primaryOwner.displayName}` and `${api.deployedAt}` when those values are present. The deployment date formats as `yyyy-MM-dd`. For MCP templates, the install component constructs the server URL from `${api.entrypoints[0]}${api.mcp.mcpPath}`.

**API Information Card:**

| Field | Description | Conditional |
|:------|:------------|:------------|
| **Version** | API version identifier | Always displayed |
| **Visibility** | Public or private access level | Always displayed |
| **Owner** | Display name of the primary API owner | Displayed if `primaryOwner.displayName` is present |
| **Last Deployed** | Deployment timestamp formatted as `yyyy-MM-dd` | Displayed if `deployedAt` is present |

## Customizing Templates

API publishers can modify the generated overview page to add context-specific content. The standard template suggests adding a Quick Start section, linking to integration guides, and documenting changelog locations. The MCP template recommends listing available MCP tools, documenting authentication requirements, and specifying environment setup steps. Both templates include links to Gravitee documentation: the standard template links to [Discover the Gravitee Developer Portal](https://documentation.gravitee.io/apim/developer-portal/new-developer-portal), while the MCP template links to [Secure MCP proxy with Gravitee APIM](https://documentation.gravitee.io/apim/ai-agent-management/secure-mcp-proxy-with-oauth2).

## Restrictions

- Template variables require FreeMarker template engine processing and will not render in environments without FreeMarker support
- Custom web components (`gmd-card`, `gmd-grid`, `gmd-install-mcp`) must be defined in the parent application; templates will not render correctly if component definitions are missing
- CSS styling depends on `--gio-app-primary-main-color` and Material Design system tokens being defined in the application stylesheet
- MCP install component URL generation requires both `api.entrypoints[0]` and `api.mcp.mcpPath` to be populated; missing values will break the install configuration

## Related Changes

The templates replace plain bullet-list API information with styled card components and remove the **Type** and **Identifier** fields from the metadata display. Conditional rendering now controls the visibility of **Owner** and **Last Deployed** fields. The generic "Welcome to the documentation" message is replaced with context-specific introductions (Developer Portal for standard APIs, Model Context Protocol for MCP APIs), and unstructured guidance is replaced with three-column feature grids and actionable sections. Custom CSS applies 8% primary color background and 24% primary color border to information cards, with 12px border radius, while feature cards use surface container backgrounds with 10% primary color border blend and 10px border radius.
