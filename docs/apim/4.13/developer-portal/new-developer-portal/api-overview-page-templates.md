---
description: API Overview page templates for the New Developer Portal.
---

# API Overview Page Templates


## Overview

API Overview Page Templates provide pre-configured Gravitee Markdown content for API pages in the New Developer Portal. When you add an API to the portal navigation in the Console, Gravitee automatically creates an unpublished **Overview** child page (unless the API navigation item already has a child page). The page uses FreeMarker templating to render API metadata, subscription guidance, and integration instructions. Two templates are available: a standard template for general APIs and an MCP proxy template for Model Context Protocol servers.

For step-by-step instructions, see [Customize the Navigation](customize-the-navigation.md#api). For Gravitee Markdown component reference, see [Gravitee Markdown components](gravitee-markdown-components.md). For the `<gmd-install-mcp>` install widget used in the MCP proxy template, see [MCP Server Installation Widget for Portal Pages](../../mcp-server-installation-widget-for-portal-pages.md).

## Key Concepts

### Portal API Types

The New Developer Portal supports six API types: `NATIVE`, `MESSAGE`, `PROXY`, `A2A_PROXY`, `LLM_PROXY`, and `MCP_PROXY`. Only `MCP_PROXY` APIs receive the MCP-specific Overview page template with an embedded `<gmd-install-mcp>` component. All other types receive the generic Overview template.

### Standard API Template

The standard template presents API information in a card-based layout with three primary sections: API metadata (version, visibility, owner, deployment date), a three-column **Get started** guide covering subscription, documentation exploration, and integration steps, and customization guidance for API publishers. The template uses styled cards with primary color theming and a 12px border radius for visual consistency.

### MCP Proxy Template

The MCP proxy template is tailored for Model Context Protocol servers published through the Gravitee gateway. It includes the same API metadata card as the standard template, an **Install in your AI client** section with a `<gmd-install-mcp>` component for one-click configuration in Cursor, VS Code, and Claude Desktop, and a **What you can do** section with action cards emphasizing MCP-specific workflows: discovering tools and resources, understanding secure gateway routing, and subscribing for credentials.

### Template Components

| Component | Purpose | Attributes |
|:----------|:--------|:-----------|
| `<gmd-card>` | Styled container for API information and guidance sections | `class="overview-info"` for metadata, `class="overview-card"` for action cards |
| `<gmd-grid>` | Three-column layout for action cards | `columns="3"` |
| `<gmd-install-mcp>` | One-click MCP server configuration generator (MCP template only) | `name`, `transport="http"`, `url` (gateway endpoint + MCP path) |

## Prerequisites

* Enable the New Developer Portal. For more information, see [Configure the New Portal](configure-the-new-portal.md).
* Add the API to the New Developer Portal navigation in the Console. For more information, see [Customize the Navigation](customize-the-navigation.md#api).
* For the MCP proxy template: the API type must be **MCP Proxy**, with a gateway entrypoint and `api.mcp.mcpPath` configured so the `<gmd-install-mcp>` component can build a valid URL.

## Creating API Overview Pages

When you add APIs to the portal navigation in the Console, Gravitee automatically seeds a default **Overview** page under each API navigation item that does not already have a child page. Existing child pages are not overwritten.

The seeded page is created **unpublished**. Publish the Overview page—or publish the parent API navigation item, which cascades to child pages—to make it visible on the New Developer Portal.

Gravitee selects the Overview template based on API type:

* **`MCP_PROXY`**: The MCP proxy template is applied. It includes an embedded `<gmd-install-mcp>` component pre-configured with `transport="http"` and a URL constructed from the first gateway entrypoint and the MCP path (`${api.entrypoints[0]}${api.mcp.mcpPath}`).
* **All other types** (`PROXY`, `MESSAGE`, `NATIVE`, `A2A_PROXY`, `LLM_PROXY`): The generic Overview template is applied without the MCP installation widget.

The page header displays the API name as the title and includes a descriptive subtitle explaining the API's purpose and access model. An API information card presents the version, visibility level, owner display name (if available), and last deployment date (formatted as `yyyy-MM-dd`, if available).

Below the metadata, a three-column grid of action cards guides consumers through subscription, documentation exploration, and integration workflows. For MCP proxy APIs, an **Install in your AI client** section embeds `<gmd-install-mcp>` to generate client configuration from the gateway endpoint and MCP path, followed by action cards focused on MCP-specific tasks.

A customization section at the bottom encourages API publishers to enhance the overview with quick start guides, use case descriptions, and links to changelogs.

## Customizing Templates

API publishers can edit the generated Overview page in the Console to add context-specific content:

1. Go to **Portal → Navigation**.
2. In the navigation tree, select the **Overview** child page under the API navigation item.
3. Edit the Gravitee Markdown content in the editor, then click **Save**.
4. Publish the page—or publish the parent API navigation item—to make changes visible in the New Developer Portal.

The standard template suggests adding a quick start section, highlighting key use cases, and linking to external guides or changelogs. The MCP proxy template recommends listing available MCP tools, documenting authentication requirements, and describing expected use cases. If your MCP proxy requires OAuth2, see [Secure MCP Proxy with OAuth2](../../ai-agent-management/secure-mcp-proxy-with-oauth2.md).

Both templates include a link to Gravitee documentation: the standard template links to the [Developer Portal overview](README.md), while the MCP proxy template links to the [OAuth2 security guide for MCP proxies](../../ai-agent-management/secure-mcp-proxy-with-oauth2.md).

## Restrictions

* The **Type** and **Identifier** fields previously displayed in API information sections are no longer included in the new templates.
* The **Owner** field is displayed only if `api.primaryOwner.displayName` is present.
* The **Last deployed** field is displayed only if `api.deployedAt` is available.
* The `<gmd-install-mcp>` component is available only in the MCP proxy template and requires `api.entrypoints[0]` and `api.mcp.mcpPath` to be defined.

## Related Changes

The API overview page format has migrated from plain markdown lists to styled card components. Information cards now use an 8% primary color background with a 24% primary color border and 12px border radius, while action cards use a surface container background with a 12% primary color mixed border and 10px border radius. Card titles apply the `--gio-app-primary-main-color` CSS variable (default: `#32329f`).

The page subtitle text is now tailored to the API type, with standard APIs emphasizing subscription and secure gateway access, and MCP proxy APIs highlighting Model Context Protocol integration and AI client connectivity.

## Related Documentation

* [MCP Server Installation Widget for Portal Pages](../../mcp-server-installation-widget-for-portal-pages.md)
* [Secure MCP Proxy with OAuth2](../../ai-agent-management/secure-mcp-proxy-with-oauth2.md)
* [APIM 4.12 release notes](../../release-information/release-notes/apim-4.12.md)
