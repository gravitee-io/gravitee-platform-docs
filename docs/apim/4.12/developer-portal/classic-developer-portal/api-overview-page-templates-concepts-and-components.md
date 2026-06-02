# API Overview Page Templates: Concepts and Components

## Overview

API Overview Page Templates provide pre-structured Markdown content for API documentation pages in the Gravitee Developer Portal. Two templates are available: a standard template for general APIs and an MCP-specific template for Model Context Protocol proxy APIs. These templates display API metadata, guide consumers through subscription and integration workflows, and support customization through FreeMarker variables.

## Key Concepts

### Standard API Template

The standard template (`api-overview-page-content.md`) introduces general-purpose APIs with a three-column "Get started" section covering subscription, documentation exploration, and integration. It displays API version, visibility, owner, and last deployment date in a styled information card. The template uses FreeMarker variables to populate API metadata dynamically and includes guidance for customizing the overview page.

### MCP Proxy API Template

The MCP proxy template (`api-overview-mcp-proxy-page-content.md`) is tailored for Model Context Protocol servers published through the Gravitee gateway. It includes an `<gmd-install-mcp>` component that generates one-click installation configurations for AI clients (Cursor, VS Code, Claude Desktop). The template highlights MCP-specific capabilities (tools, prompts, resources) and links to OAuth2 security documentation for MCP proxies.

### Template Variables

Both templates use FreeMarker syntax to inject API metadata at render time:

| Variable | Description | Template Availability |
|:---------|:------------|:---------------------|
| `${api.name}` | API display name | Both |
| `${api.version}` | API version identifier | Both |
| `${api.visibility}` | API visibility level | Both |
| `${api.primaryOwner.displayName}` | Owner display name (conditional) | Both |
| `${api.deployedAt}` | Last deployment timestamp, formatted as `yyyy-MM-dd` (conditional) | Both |
| `${api.entrypoints[0]}` | First gateway entrypoint URL | MCP only |
| `${api.mcp.mcpPath}` | MCP server path | MCP only |

### Styled Components

Templates use custom card components with primary color theming:

- **API Information Card** (`.overview-info`): 8% primary color background, 24% primary color border, 12px border radius
- **Get Started / What You Can Do Cards** (`.overview-card`): Surface container background, 12% primary color mixed border, 10px border radius
- Card titles use `--gio-app-primary-main-color` (default: `#32329f`)

## Prerequisites

- Gravitee API Management platform with Developer Portal enabled
- API published to the Developer Portal
- FreeMarker template processing enabled in the portal

## Gateway Configuration

