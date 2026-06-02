# API Overview Page Template Infrastructure

## Overview

API Overview Page Templates provide pre-built Markdown templates for API documentation pages in the Gravitee Developer Portal. Two templates are available: a standard template for general APIs and an MCP Proxy template for Model Context Protocol servers. These templates use structured cards, styled components, and dynamic variables to present API metadata, subscription guidance, and integration instructions.

## Key Concepts

### Standard API Template

The standard template presents API information in a card-based layout with version, visibility, owner, and deployment details. A three-column "Get started" section guides consumers through subscription, documentation exploration, and integration workflows. The template uses FreeMarker variables to populate API metadata dynamically and includes inline CSS styling with primary color theming.

### Template Variables

Both templates use FreeMarker syntax to inject API properties at render time. Core variables include `${api.name}`, `${api.version}`, `${api.visibility}`, and conditional fields like `${api.primaryOwner.displayName}` and `${api.deployedAt}`. The MCP template adds `${api.entrypoints[0]}` and `${api.mcp.mcpPath}` to construct the gateway endpoint URL for MCP clients.

| Variable | Description | Template |
|:---------|:------------|:---------|
| `${api.name}` | API display name | Both |
| `${api.version}` | API version identifier | Both |
| `${api.visibility}` | API visibility level | Both |
| `${api.primaryOwner.displayName}` | Owner display name (conditional) | Both |
| `${api.deployedAt}` | Last deployment timestamp (conditional, formatted as `yyyy-MM-dd`) | Both |
| `${api.entrypoints[0]}` | First gateway entrypoint URL | MCP only |
| `${api.mcp.mcpPath}` | MCP server path | MCP only |

### Styled Components

Templates use custom elements (`gmd-card`, `gmd-grid`, `gmd-install-mcp`) and CSS classes (`.overview-info`, `.overview-card`) to structure content. Card styling applies primary color theming via `--gio-app-primary-main-color` (default: `#32329f`), with background blends, border colors, and border radius values defined inline. The three-column grid layout organizes feature cards for subscription, documentation, and integration guidance.

## Prerequisites

- FreeMarker template engine must be available for variable substitution.
- Rendering environment must support `gmd-card`, `gmd-grid`, and `gmd-install-mcp` custom elements.
- CSS custom property `--gio-app-primary-main-color` should be defined in the parent context (defaults to `#32329f` if not set).
- For MCP template: `api.entrypoints` array must contain at least one element.
- For conditional fields: `api.deployedAt` must be a valid date object for formatting.

## Gateway Configuration

