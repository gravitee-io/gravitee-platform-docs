# API Overview Page Templates

## Overview

API Overview Page Templates provide pre-configured Markdown content for API documentation pages in the Gravitee Developer Portal. When an API is published, the portal automatically generates a structured overview page with API metadata, subscription guidance, and integration instructions. Two templates are available: a standard template for general APIs and an MCP proxy template for Model Context Protocol servers.

## Key Concepts

### Standard API Template

The standard template presents API information in a card-based layout with three primary sections: API metadata (version, visibility, owner, deployment date), a three-column "Get started" guide covering subscription, documentation exploration, and integration steps, and customization guidance for API publishers. The template uses styled cards with primary color theming and a 12px border radius for visual consistency.

### MCP Proxy Template

The MCP proxy template is tailored for Model Context Protocol servers published through the Gravitee gateway. It includes the same API metadata card as the standard template but replaces the "Get started" section with "What you can do," emphasizing MCP-specific workflows: discovering tools and resources, understanding secure gateway routing, and subscribing for credentials. The template embeds a `<gmd-install-mcp>` component that generates one-click configuration for AI clients (Cursor, VS Code, Claude Desktop) using the gateway endpoint and MCP path.

### Template Components

| Component | Purpose | Attributes |
|:----------|:--------|:-----------|
| `<gmd-card>` | Styled container for API information and guidance sections | `class="overview-info"` for metadata, `class="overview-card"` for action cards |
| `<gmd-grid>` | Three-column layout for action cards | `columns="3"` |
| `<gmd-install-mcp>` | One-click MCP server configuration generator (MCP template only) | `name`, `transport="http"`, `url` (gateway endpoint + MCP path) |

## Prerequisites

* API must be published to the Gravitee Developer Portal
* For MCP proxy template: API must expose an MCP server endpoint with `api.mcp.mcpPath` configured

## Creating API Overview Pages

When an API is published to the Developer Portal, the system automatically generates an overview page using the appropriate template. The standard template is applied to general APIs, while the MCP proxy template is used for APIs exposing Model Context Protocol servers.

The page header displays the API name as the title and includes a descriptive subtitle explaining the API's purpose and access model. An API information card presents the version, visibility level, owner display name (if available), and last deployment date (formatted as `yyyy-MM-dd`, if available).

Below the metadata, a three-column grid of action cards guides consumers through subscription, documentation exploration, and integration workflows. For MCP proxy APIs, the action cards focus on MCP-specific tasks (tools and resources, secure gateway access, subscription), and an embedded `<gmd-install-mcp>` component generates client configuration using the gateway endpoint and MCP path.

A customization section at the bottom encourages API publishers to enhance the overview with quick start guides, use case descriptions, and links to changelogs.

## Customizing Templates

API publishers can modify the generated overview page to add context-specific content. The standard template suggests adding a quick start section, highlighting key use cases, and linking to external guides or changelogs. The MCP proxy template recommends listing available MCP tools, documenting authentication requirements, and describing expected use cases.

Both templates include a link to Gravitee documentation: the standard template links to the [Developer Portal overview](https://documentation.gravitee.io/apim/developer-portal/new-developer-portal), while the MCP proxy template links to the [OAuth2 security guide for MCP proxies](https://documentation.gravitee.io/apim/ai-agent-management/secure-mcp-proxy-with-oauth2).

## Restrictions

* The **Type** and **Identifier** fields previously displayed in API information sections are no longer included in the new templates.
* The **Owner** field is displayed only if `api.primaryOwner.displayName` is present.
* The **Last deployed** field is displayed only if `api.deployedAt` is available.
* The `<gmd-install-mcp>` component is available only in the MCP proxy template and requires `api.entrypoints[0]` and `api.mcp.mcpPath` to be defined.

## Related Changes

The API overview page format has migrated from plain markdown lists to styled card components. Information cards now use an 8% primary color background with a 24% primary color border and 12px border radius, while action cards use a surface container background with a 12% primary color mixed border and 10px border radius. Card titles apply the `--gio-app-primary-main-color` CSS variable (default: `#32329f`).

The page subtitle text is now tailored to the API type, with standard APIs emphasizing subscription and secure gateway access, and MCP proxy APIs highlighting Model Context Protocol integration and AI client connectivity.
