# API Overview Page Template Components and Variables Reference

### Template Components

Both templates use custom web components and styled cards for visual consistency:

| Component | Purpose | Attributes |
|:----------|:--------|:-----------|
| `gmd-card` | Styled container for API metadata and feature descriptions | `class="overview-info"` or `class="overview-card"` |
| `gmd-grid` | Three-column layout for feature cards | `columns="3"` |
| `gmd-install-mcp` | One-click MCP server configuration generator (MCP template only) | `name`, `transport="http"`, `url` |

### FreeMarker Template Variables

Both templates use FreeMarker variables to populate dynamic content:

| Variable | Purpose | Location |
|:---------|:--------|:---------|
| `${api.name}` | API name | Page title |
| `${api.version}` | API version | Information card |
| `${api.visibility}` | API visibility setting | Information card |
| `${api.primaryOwner.displayName}` | Owner display name | Information card |
| `${api.deployedAt}` | Last deployment timestamp | Information card (conditional, formatted as `yyyy-MM-dd`) |
| `${api.entrypoints[0]}` | Gateway endpoint URL | MCP install component URL construction |
| `${api.mcp.mcpPath}` | MCP server path | MCP install component URL construction |

### API Information Card Fields

The information card displays the following fields:

| Field | Display Condition | Format |
|:------|:------------------|:-------|
| Version | Always displayed | `${api.version}` |
| Visibility | Always displayed | `${api.visibility}` |
| Owner | Displayed when `${api.primaryOwner.displayName}` is present | Display name |
| Last Deployed | Displayed when `${api.deployedAt}` is present | `yyyy-MM-dd` |

### CSS Custom Properties

Template styling relies on the following CSS custom properties defined in the parent application:

| Property | Purpose |
|:---------|:--------|
| `--gio-app-primary-main-color` | Primary color for card titles and borders (default: `#32329f`) |
| Material Design system tokens | Surface container backgrounds and color blending |

### CSS Styling Rules

| Element | Background | Border | Border Radius |
|:--------|:-----------|:-------|:--------------|
| `.overview-info` card | 8% primary color | 24% primary color | 12px |
| `.overview-card` | Surface container | 10% primary color blend | 10px |

## Prerequisites

Before using API overview page templates, ensure the following components are configured:

* Gravitee API Management platform with Developer Portal enabled
* FreeMarker template engine configured for variable substitution
* Web component definitions for `gmd-card`, `gmd-grid`, and `gmd-install-mcp` elements
* CSS custom properties defined in the parent application (`--gio-app-primary-main-color` and Material Design system tokens)

## Gateway Configuration

