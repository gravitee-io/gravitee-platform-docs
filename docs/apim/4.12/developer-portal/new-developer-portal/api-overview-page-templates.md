---
description: API Overview page templates for the New Developer Portal.
---

# API Overview Page Templates


## Overview

API Overview Page Templates provide pre-configured Gravitee Markdown content for API pages in the New Developer Portal. When you add an API to the portal navigation in the Console, Gravitee automatically creates an unpublished **Overview** child page (unless the API navigation item already has a child page). The page uses FreeMarker templating to render API metadata, subscription guidance, and integration instructions. Two templates are available: a standard template for general APIs and an MCP proxy template for Model Context Protocol servers.

For step-by-step instructions, see [Customize the Navigation](customize-the-navigation.md#api). For Gravitee Markdown component reference, see [Gravitee Markdown components](gravitee-markdown-components.md).

## Key Concepts

### Standard API Template

The standard template presents API information in a card-based layout with three primary sections: API metadata (version, visibility, owner, deployment date), a three-column **Get started** guide covering subscription, documentation exploration, and integration steps, and customization guidance for API publishers. The template uses styled cards with primary color theming and a 12px border radius for visual consistency.

### MCP Proxy Template

The MCP proxy template is tailored for Model Context Protocol servers published through the Gravitee gateway. It includes the same API metadata card as the standard template, an **Install in your AI client** section with a `<gmd-install-mcp>` component for one-click configuration in Cursor, VS Code, and Claude Desktop, and a **What you can do** section with action cards emphasizing MCP-specific workflows: discovering tools and resources, understanding secure gateway routing, and subscribing for credentials.

### Template Components

| Component | Purpose | Attributes |
|:----------|:--------|:-----------|
| `<gmd-card>` | Styled container for API information and guidance sections | `class="overview-info"` for metadata, `class="overview-card"` for action cards |
| `<gmd-grid>` | Three-column layout for action cards | `columns="3"` |
| `<gmd-install-mcp>` | One-click MCP server configuration generator for remote (`http`, `sse`) and local (`stdio`) MCP servers | `name`, `transport` (`http`, `sse`, or `stdio`), `url` (for remote), `headers` (optional, for remote), `command` (for stdio), `args` (optional, for stdio), `env` (optional, for stdio), `clients` (optional) |

## Prerequisites

* Enable the New Developer Portal. For more information, see [Configure the New Portal](configure-the-new-portal.md).
* Add the API to the New Developer Portal navigation in the Console. For more information, see [Customize the Navigation](customize-the-navigation.md#api).
* For the MCP proxy template: the API type must be **MCP Proxy**, with a gateway entrypoint and `api.mcp.mcpPath` configured so the `<gmd-install-mcp>` component can build a valid URL.

## Creating API Overview Pages

When you add an API to the portal navigation, the Console calls the Management API to seed a default **Overview** page under that API navigation item. Gravitee skips seeding if the API navigation item already has a child page, so existing pages are not overwritten.

The seeded page is created **unpublished**. Publish the Overview page—or publish the parent API navigation item, which cascades to child pages—to make it visible on the New Developer Portal.

The standard template is applied to general APIs; the MCP proxy template is used when the API type is **MCP Proxy**.

The page header displays the API name as the title and includes a descriptive subtitle explaining the API's purpose and access model. An API information card presents the version, visibility level, owner display name (if available), and last deployment date (formatted as `yyyy-MM-dd`, if available).

Below the metadata, a three-column grid of action cards guides consumers through subscription, documentation exploration, and integration workflows. For MCP proxy APIs, an **Install in your AI client** section embeds `<gmd-install-mcp>` to generate client configuration from the gateway endpoint and MCP path, followed by action cards focused on MCP-specific tasks.

A customization section at the bottom encourages API publishers to enhance the overview with quick start guides, use case descriptions, and links to changelogs.

## Customizing Templates

API publishers can edit the generated Overview page in the Console to add context-specific content. The standard template suggests adding a quick start section, highlighting key use cases, and linking to external guides or changelogs. The MCP proxy template recommends listing available MCP tools, documenting authentication requirements, and describing expected use cases.

Both templates include a link to Gravitee documentation: the standard template links to the [Developer Portal overview](https://documentation.gravitee.io/apim/developer-portal/new-developer-portal), while the MCP proxy template links to the [OAuth2 security guide for MCP proxies](https://documentation.gravitee.io/apim/ai-agent-management/secure-mcp-proxy-with-oauth2).

## Restrictions

* The **Type** and **Identifier** fields previously displayed in API information sections are no longer included in the new templates.
* The **Owner** field is displayed only if `api.primaryOwner.displayName` is present.
* The **Last deployed** field is displayed only if `api.deployedAt` is available.
* The `<gmd-install-mcp>` component is available only in the MCP proxy template and requires `api.entrypoints[0]` and `api.mcp.mcpPath` to be defined.

## Related Changes

The API overview page format has migrated from plain markdown lists to styled card components. Information cards now use an 8% primary color background with a 24% primary color border and 12px border radius, while action cards use a surface container background with a 12% primary color mixed border and 10px border radius. Card titles apply the `--gio-app-primary-main-color` CSS variable (default: `#32329f`).

The page subtitle text is now tailored to the API type, with standard APIs emphasizing subscription and secure gateway access, and MCP proxy APIs highlighting Model Context Protocol integration and AI client connectivity.
