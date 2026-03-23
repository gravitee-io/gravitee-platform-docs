# API Navigation Items Technical Reference

### Publish State Dependencies

Navigation items cannot be published if their parent folder is unpublished or unavailable. The publish action is disabled in the UI with a tooltip explaining the restriction. Root-level items and items with published parents can be published freely. API items cannot be edited after creation, but publish/unpublish actions remain available.

## Prerequisites

- Portal navigation feature enabled in the environment
- At least one published API available for linking
- A folder item in the `TOP_NAVBAR` area to contain API items
- Appropriate permissions to manage portal navigation

## Gateway Configuration

### Database Schema

The `portal_navigation_items` table requires a new nullable column to store API references.

| Property | Type | Description | Example |
|:---------|:-----|:------------|:--------|
| `api_id` | `nvarchar(64)` | Foreign key to API entity; required when `type` is `API` | `"api-1"` |

### Asset Bundling

Redoc documentation renderer is now bundled locally (version 2.4.0) instead of loaded from CDN. Configure Angular build assets to include the Redoc standalone bundle.

| Source Path | Output Path | Purpose |
|:------------|:------------|:--------|
| `node_modules/redoc/bundles/redoc.standalone.js` | `assets/redoc/redoc.standalone.js` | Local OpenAPI documentation renderer |

Update HTML templates to reference `assets/redoc/redoc.standalone.js` instead of `https://cdn.redoc.ly/redoc/v2.1.5/bundles/redoc.standalone.js`.

## End-User Configuration

### API Navigation Item Properties

| Property | Required | Description | Example |
|:---------|:---------|:------------|:--------|
| `type` | Yes | Must be `"API"` | `"API"` |
| `title` | Yes | Display name in navigation | `"Payments API"` |
| `area` | Yes | Must be `"TOP_NAVBAR"` | `"TOP_NAVBAR"` |
| `parentId` | Yes | ID of parent folder item | `"folder-123"` |
| `apiId` | Yes | Unique API identifier | `"api-456"` |
| `visibility` | Yes | `"PUBLIC"` or `"PRIVATE"` (constrained by parent) | `"PUBLIC"` |
| `published` | No | Publish state (defaults to `false`) | `true` |

### Management API

**POST `/environments/{envId}/portal-navigation-items/_bulk`**

Creates multiple navigation items in a single request. All items are validated before any are persisted. Returns `200 OK` with the created items array, or validation errors if any item fails constraints.

## Related Changes

The UI now hides the edit button for API navigation items while preserving publish/unpublish actions. Visibility toggles are disabled with explanatory tooltips when parent folders enforce private visibility. Publish menu items display accessibility-compliant disabled states with tooltips explaining parent-level restrictions. The Redoc documentation renderer is bundled locally (version 2.4.0) instead of loaded from CDN, requiring updates to Angular build configuration and HTML script tags. Validation logic now checks for duplicate API IDs within bulk requests and across the entire navigation structure.
