---
description: Create and manage OpenAPI documentation pages in the New Developer Portal navigation.
---

# Creating OpenAPI Documentation Pages

## Overview

For each **OpenAPI** page in portal navigation, administrators can choose how the page is rendered in the Console and in the published portal — **Swagger UI** or **Redoc** — and configure viewer behaviour. The same settings apply in the **Console live preview** and when portal users open the page.

## Viewer choice

| Viewer | Best for |
|:-------|:---------|
| **Swagger UI** | Interactive documentation with **Try It Out**, OAuth, and rich display options |
| **Redoc** | Read-focused API reference layout |

Swagger UI exposes the full option set described below. Redoc supports viewer selection and an optional **base URL** override; Swagger-specific options are hidden when Redoc is selected.

## Prerequisites

Before creating OpenAPI documentation pages, ensure you have the following:

* The New Developer Portal enabled. For more information, see [configure-the-new-portal.md](../configure-the-new-portal.md).
* Access to the portal navigation editor in the Management Console.
* For Try It Out functionality: CORS may need to be configured on the API entrypoint. For more information, see [CORS](../../../create-and-configure-apis/configure-v4-apis/cors.md).

## Configure the OpenAPI viewer

When editing an OpenAPI page in portal navigation, click **Configure** to set the viewer and all applicable options.

The dialog includes viewer selection, base URL, entrypoint and context-path options, Try It Out and OAuth options, and display and filtering options. Swagger UI options apply only when Swagger UI is selected.

### Server URL and Try It Out

| Option | What it does |
|:-------|:-------------|
| **Base URL** | Custom server URL used when trying the API. If empty and entrypoints are not used, the server URL from the specification is used. |
| **Use API entrypoints as server URLs** | Replaces specification server URLs with the API's live gateway entrypoints. When enabled, the custom base URL field is not used. |
| **Use API context-path as server URL path** | Applies the API's context-path to the server URL path (can be combined with entrypoints). |
| **Enable Try It Out** | Lets authenticated portal users execute API calls from the documentation page. May require CORS to be configured on the API entrypoint. |
| **Enable Try It Out for anonymous users** | Allows users who are not logged in to use Try It Out on public pages and public APIs. |
| **Use PKCE with OAuth** | Uses PKCE when authenticating with an OAuth authorization-code flow from the documentation page. |

### Display and behaviour

| Option | What it does |
|:-------|:-------------|
| **Expand content on the page** | Controls default expansion: nothing (default), tags only, or tags and operations. |
| **Display operationId** | Shows the `operationId` in the operations list. |
| **Add top bar to filter content** | Adds a filter bar for tags and operations. |
| **Display vendor extensions** | Shows vendor extension (`x-`) fields on operations, parameters, and schemas. |
| **Display extension fields for parameters** | Shows pattern, maxLength, minLength, maximum, and minimum extensions on parameters. |
| **Max number of tagged operations displayed** | Limits how many tagged operations are shown. Use `-1` to show all. |
| **Show URL to download content** | Loads the specification from its download URL instead of inline content. |
| **Disable response body styling for large JSON payloads** | Turns off syntax highlighting on responses to improve performance with large payloads. |

## Console preview

The OpenAPI editor keeps a split layout: specification on one side, live preview on the other. The preview matches the selected viewer:

* **Swagger UI** — reflects Try It Out settings, expansion, filtering, extensions, and other options as they are changed.
* **Redoc** — uses Redoc in preview (new in the Console).

Preview updates during the editing session without requiring a separate save to see changes in the preview pane.

## Viewing in the portal

Published OpenAPI pages render according to the saved viewer configuration.

**Swagger UI** honours all configured options, including Try It Out (authenticated and optionally anonymous), OAuth with PKCE, custom or entrypoint-derived server URLs, and display settings. When entrypoint or context-path options are enabled, the platform resolves the enclosing API and serves a specification with the correct server URLs applied so Try It Out targets the live API gateway.

**Redoc** shows the page with the Redoc viewer; an optional base URL can be supplied where relevant.

## Existing OpenAPI pages

**Existing OpenAPI pages** that had no viewer configuration before this feature are treated as **Redoc** pages, preserving prior portal behaviour. Settings remain compatible with how OpenAPI page configuration worked in earlier releases.

## Typical workflow

1. In the Console, open an OpenAPI page in portal navigation.
2. Choose **Configure OpenAPI Viewer** and select Swagger UI or Redoc.
3. For Swagger UI, enable **Try It Out** and set server URL behaviour (custom base URL, entrypoints, or context-path as needed).
4. Adjust display options (expansion, filtering, extensions, etc.) and check the live preview.
5. Save the configuration and publish the page.
6. Portal users see the same viewer and behaviour when they open the documentation page.

For programmatic configuration, see [Structure the navigation with the Management API](structure-the-navigation-with-the-management-api.md#update-openapi-viewer-configuration).
