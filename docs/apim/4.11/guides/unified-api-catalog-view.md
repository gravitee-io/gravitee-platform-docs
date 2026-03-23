# Unified API Catalog View

## Overview

This release consolidates the API catalog interface, improves subscription workflow clarity, and enhances pagination controls across the developer portal. Category-based navigation has been removed in favor of a unified catalog view. The subscription flow now includes descriptive step headers, and pagination controls offer configurable page sizes with improved accessibility.

## Key Concepts

### Unified Catalog View

The catalog presents all APIs in a single view at `/catalog` with grid or list display modes. Category-based navigation has been removed. Users search and filter APIs directly from the main catalog page.

**View Modes:**
- **Grid mode**: 4-column layout that adjusts to 2 columns on narrow screens and 1 column on mobile devices
- **List mode**: Table view with columns for name, labels, version, and MCP status. On mobile devices, the labels column is omitted.

**Legacy Route Redirects:**

The following routes redirect to `/catalog` for backward compatibility:
- `/categories`
- `/categories/catalog`
- `/catalog/all`
- `/catalog/categories`
- `/catalog/categories/:categoryId`

**Search and Filtering:**

A search bar allows users to filter APIs by keyword. The catalog displays context-specific empty state messages:
- When a search returns no results: "Your search didn't return any APIs. Please try again with different keywords."
- When no APIs are published: "Our API catalog is currently being updated. More APIs will be available soon."

**Removed Components:**

The following components have been removed:
- `CategoriesViewComponent`
- `CategoryApisComponent`
- `TabsViewComponent`
- `ApisListComponent`
- `CatalogBannerComponent`

The `portalNext.banner.enabled` configuration property is no longer supported.


