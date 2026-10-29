---
description: Set up the structure, homepage, theme, APIs, documentation, and links of the New Developer Portal as code with the Automation API. Browse the automation guides.
---

# Portal automation

## Overview

The Next-Gen Developer Portal supports CI/CD-driven setup of portal structure, homepage, theme, published APIs, documentation, and links through the Automation API. You declare portal configuration, navigation hierarchies, API listings, documentation pages, links, and themes declaratively with Gravitee Kubernetes Operator (GKO) custom resources. APIM reconciles the desired state into the live portal navigation tree.

The Automation API supports Gravitee Markdown, OpenAPI, and AsyncAPI documentation types. A link opens a URL from the portal navigation or from the documentation of an API.

## Automation API access

{% hint style="warning" %}
On premise Helm Charts users need to configure ingress configuration for `api.ingress.automation`  when using Automation API or GKO.

You need to:

* enable it
* configure `hosts` & `tls`
{% endhint %}

The Automation API is served at the `/automation` base path on your Management API host by default. All endpoints in this section use this base path.&#x20;

{% hint style="info" %}
Gravitee Cloud users must use `/apim/automation` as a base path and have proper access token to Automation/GKO configured.&#x20;
{% endhint %}

| Property       | Value                                                                             |
| -------------- | --------------------------------------------------------------------------------- |
| Base URL       | `https://<your-gravitee-mapi-host>/automation`                                    |
| Authentication | Bearer token (Personal Access Token or Cloud Token) in the `Authorization` header |
| Content type   | `application/json`                                                                |

For example, the full URL for portal operations is `https://<your-gravitee-mapi-host>/automation/organizations/{orgId}/environments/{envId}/portals`.

## Concepts

The following concepts describe how the Automation API models a portal and its content.

### Portal instance

A portal is a Next-Gen Developer Portal bound to an environment. Each portal has a human-readable ID (HRID) that you provide, a display name, a navigation structure, and optionally the theme it uses. By default, an environment holds one portal: a `PUT` whose HRID differs from the portal that already exists in the environment fails with `400` and the message `hrid does not match the established portal for this environment`. The portal is created on the first successful `PUT` request.

The navigation is declared under `structure`, grouped by portal area. `structure.topNavbar` holds the top navigation bar as a flat, ordered list of slash-separated paths. Intermediate folders are created implicitly when they are not listed explicitly. The `GET` response returns `structure` as persisted.

{% hint style="warning" %}
`navigation`, the flat list of paths of earlier versions, is deprecated. A request that sets only `navigation` is accepted and mapped to `structure.topNavbar`. A request that sets both fails with `400` and the message `navigation and structure cannot be used at the same time`. The `GET` response repeats the top navigation bar under `navigation`.
{% endhint %}

### Navigation paths

Navigation paths define the portal's folder hierarchy using slash-separated strings, such as `/projects/alpha` or `/projects/alpha/docs`. Each path optionally includes a display name and a visibility. The sequence in the declaration list sets the display order. Navigation sync operates only on the top navigation bar. The homepage is set with a documentation page, not with a navigation path. For more information, see [Set the portal homepage](portal-documentation.md#set-the-portal-homepage).

| Property      | Description                                                                | Example           |
| ------------- | -------------------------------------------------------------------------- | ----------------- |
| `path`        | Slash-separated navigation hierarchy. Required, and starts with `/`.       | `/projects/alpha` |
| `displayName` | Human-friendly label for the node. Optional.                               | `Alpha`           |
| `visibility`  | `PUBLIC` or `PRIVATE`. Optional. For more information, see [Visibility](#visibility). | `PRIVATE`         |

### Visibility

Navigation paths, listing entries, documentation pages, and links take an optional `visibility` of `PUBLIC` or `PRIVATE`. A private item is shown to consumers who are signed in to the portal. An anonymous visitor who opens a private item gets `404`.

When `visibility` is omitted, the item takes the visibility of its parent folder, and a top-level item is `PUBLIC`. A public item under a private parent is rejected with `400` and the message `Parent item with id <id> must be PUBLIC to create a public child item.`

The resolution runs on every apply. A documentation page or a link that omits `visibility` follows its folder each time it's applied, including a page that was made private in the Console. Declare `visibility: PRIVATE` on every resource whose item stays private.

### Portal listing

A portal listing publishes one or more APIs to specific locations in the portal navigation. Each API entry specifies the API's HRID, the navigation path where it appears, an optional order, and an optional visibility. Within a single listing, multiple APIs can share the same location, with the `order` field controlling the display sequence. Across listings, validation rejects two different listings that place different APIs at the same location segment.

| Property     | Description                                                                                          | Example           |
| ------------ | ---------------------------------------------------------------------------------------------------- | ----------------- |
| `apiHrid`    | Human-readable ID of the API to publish. Required.                                                   | `pets-api`        |
| `location`   | Path in the portal's navigation where the API appears. Required, and matches a declared portal path. | `/projects/alpha` |
| `order`      | Display order relative to siblings at the same location. Optional integer.                           | `1`               |
| `visibility` | `PUBLIC` or `PRIVATE` for the API entry. Optional. For more information, see [Visibility](#visibility). | `PRIVATE`         |

### Documentation pages

Documentation pages attach to either a portal (platform-level guides) or an API (API-specific documentation). Each page has a type (Gravitee Markdown, OpenAPI, or AsyncAPI), content, and a location in the navigation hierarchy. Portal-scoped documentation appears at the specified location in the portal's top-level navigation, or serves as the portal's homepage. API-scoped documentation appears under every published instance of the API, relative to the API's internal documentation folder tree.

| Property     | Description                                                                                                                                 | Example                         |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------- |
| `hrid`       | Human-readable ID of the documentation page. Required.                                                                                      | `getting-started`               |
| `name`       | Display name of the page. Required.                                                                                                         | `Getting Started`               |
| `type`       | Documentation type. Required: `GRAVITEE_MARKDOWN`, `OPENAPI`, or `ASYNCAPI`.                                                                | `GRAVITEE_MARKDOWN`             |
| `content`    | Content of the documentation page. Required.                                                                                                | `# Getting Started\nWelcome...` |
| `location`   | Path in the navigation hierarchy where the page appears. When omitted, the page is placed at the root of the portal or API navigation tree. | `/projects/alpha/docs`          |
| `order`      | Display order relative to siblings at the same location. Optional integer.                                                                  | `1`                             |
| `area`       | Where the page appears. Optional: `TOP_NAVBAR` (default) places the page in the navigation, and `HOMEPAGE` makes a portal page the portal's homepage. | `HOMEPAGE`                      |
| `visibility` | `PUBLIC` or `PRIVATE`. Optional. For more information, see [Visibility](#visibility).                                                      | `PRIVATE`                       |

### API internal documentation tree

Each API declares its own internal documentation folder hierarchy using the `portalNavigation` field, which uses the same navigation path structure as the portal's top-level navigation. When an API is published through a portal listing, the API's internal folder tree is materialized under each published API entry, and API-scoped documentation pages are placed relative to this tree.

The `portalNavigation` field is portal-only metadata. It is not propagated to the gateway definition, has no effect on the classic portal, and does not apply to v2 APIs.

### Links

A link is a navigation entry that opens a URL. A portal link appears in the portal's top navigation bar at its `location`. An API link belongs to an API and appears under the API wherever the API is listed, in every portal. Each link has an HRID, a display name, the URL it points to, and optionally a location, an order, and a visibility. For more information, see [Automate portal and API links](portal-links.md).

### Themes

A theme is the look and feel of the New Developer Portal: its colors, font, custom CSS, logo, favicon, and background image. Themes belong to the environment, and the portal's `activeThemeHrid` selects the theme that consumers see. For more information, see [Automate portal themes](portal-themes.md).

## Prerequisites

* A Gravitee APIM 4.13.0 or later environment, with its organization and environment IDs
* A bearer token (Personal Access Token or Cloud Token) for the Automation API
* The `ENVIRONMENT_PORTAL` permission for portal, portal listing, portal documentation, and portal link operations
* The `ENVIRONMENT_THEME` permission for theme operations, and for changing the active theme of a portal
* The `API_DOCUMENTATION` permission for API-scoped documentation and API link operations
* For Kubernetes deployments: Gravitee Kubernetes Operator 4.13.0 or later installed

{% hint style="info" %}
Resources can reference each other before all dependencies exist. Documentation pages, links, and portal listings tolerate missing navigation paths, API HRIDs, and parent portals. Orphan entries reconnect when the referenced resource is created, so apply order does not matter.
{% endhint %}

## Create a portal

### Using the Automation API

Create or update a portal by sending a `PUT` request to `/organizations/{orgId}/environments/{envId}/portals` with the portal specification. The request body includes the portal's HRID, display name, and navigation structure, and optionally the HRID of the theme it uses. The `dryRun` query parameter validates the request without persisting changes.

**Request:**

{% code overflow="wrap" %}
```http
PUT /organizations/{orgId}/environments/{envId}/portals?dryRun=false
Content-Type: application/json
Authorization: Bearer {token}

{
  "hrid": "default-portal",
  "name": "Default Portal",
  "structure": {
    "topNavbar": [
      {
        "path": "/projects/alpha",
        "displayName": "Alpha"
      },
      {
        "path": "/projects/alpha/docs"
      },
      {
        "path": "/projects/beta",
        "visibility": "PRIVATE"
      }
    ]
  },
  "activeThemeHrid": "brand-theme"
}
```
{% endcode %}

**Response:**

```json
{
  "id": "generated-uuid",
  "environmentId": "env-id",
  "organizationId": "org-id",
  "hrid": "default-portal",
  "name": "Default Portal",
  "structure": {
    "topNavbar": [
      {
        "path": "/projects/alpha",
        "displayName": "Alpha"
      },
      {
        "path": "/projects/alpha/docs"
      },
      {
        "path": "/projects/beta",
        "visibility": "PRIVATE"
      }
    ]
  },
  "navigation": [
    {
      "path": "/projects/alpha",
      "displayName": "Alpha"
    },
    {
      "path": "/projects/alpha/docs"
    },
    {
      "path": "/projects/beta",
      "visibility": "PRIVATE"
    }
  ],
  "activeThemeHrid": "brand-theme",
  "errors": {
    "severe": [],
    "warning": []
  }
}
```

Retrieve a portal by sending a `GET` request to `/organizations/{orgId}/environments/{envId}/portals/{hrid}`. The response returns the persisted navigation structure. Delete a portal by sending a `DELETE` request to the same path, which returns HTTP 204 on success.

Changing `activeThemeHrid` activates or deactivates a theme of the environment, so it requires the `ENVIRONMENT_THEME` update permission in addition to the portal permissions. Without it, the request fails with `403`. For more information, see [Automate portal themes](portal-themes.md).

### Using Kubernetes CRDs

1. Create a `ManagementContext` resource that references your APIM instance, if one is not already configured.
2. Define a `Portal` resource with the HRID, display name, and navigation paths, and optionally a `themeRef` to a `PortalTheme` resource.
3. Apply the manifest with `kubectl apply -f portal.yaml`.

**Example Portal custom resource:**

```yaml
apiVersion: gravitee.io/v1alpha1
kind: Portal
metadata:
  name: default-portal
  namespace: gravitee
spec:
  contextRef:
    name: "apim-context"
  name: "Default Portal"
  structure:
    topNavbar:
      - path: /projects/alpha
        displayName: Alpha
      - path: /projects/alpha/docs
      - path: /projects/beta
        visibility: PRIVATE
  themeRef:
    name: brand-theme
```

The GKO controller reconciles the desired state by calling the Automation API. Admission webhooks validate the resource before apply using the `dryRun` endpoint. The management context must resolve, and the navigation paths must pass validation: paths start with `/`, do not contain `//` or `..`, and do not end with `/` unless the path is root.

{% hint style="warning" %}
`spec.navigation` is deprecated. A resource that sets it is accepted with the warning `spec.navigation is deprecated, use spec.structure.topNavbar instead`. A resource that sets both `spec.navigation` and `spec.structure` is rejected with `navigation and structure cannot be used at the same time`.
{% endhint %}

### Navigation path normalization

Navigation paths are normalized during processing:

| Input                   | Normalized output       | Notes                                                                              |
| ----------------------- | ----------------------- | ---------------------------------------------------------------------------------- |
| `/a/b/`                 | `/a/b`                  | Trailing slash stripped, except for root                                           |
| `/Docs/Getting Started` | `/docs/getting-started` | Segments are converted to lowercase, and non-alphanumeric characters are replaced with hyphens |
| `/a`                    | `/a`                    | Single segment accepted                                                            |

When you provide a path such as `/a/b/c` and do not list `/a` and `/a/b` explicitly, the intermediate ancestor folders are created implicitly.

### Automation and Console coexistence

When you remove a path from the navigation list, folder sync removes only folders that appeared in the previously persisted navigation list. Folders created through the Console that were not in the previous automation list are preserved. When an automation-managed folder is deleted, its child folders, pages, links, and API entries are deleted as well, but only within the scope of items that automation previously created.

## Verification

To verify a portal is configured as expected:

1. Send a `GET` request to `/organizations/{orgId}/environments/{envId}/portals/{hrid}`.
2. Confirm the response returns the portal with the navigation structure you declared.
3. Open the Next-Gen Developer Portal and confirm the navigation hierarchy and published APIs appear at the declared locations.

## Automation API endpoint reference

The following endpoints belong to the Automation API, served at the `/automation` base path. The `dryRun` query parameter validates the request and returns validation errors without persisting changes. Validation errors are returned in the response body under the `errors` field, categorized as `severe` (blocking) or `warning` (informational).

### Portal endpoints

These endpoints require the `ENVIRONMENT_PORTAL` permission.

| Endpoint                                                     | Method | Description                                                                           |
| ------------------------------------------------------------ | ------ | ------------------------------------------------------------------------------------- |
| `/organizations/{orgId}/environments/{envId}/portals`        | PUT    | Create or update a portal. Supports `dryRun`.                                         |
| `/organizations/{orgId}/environments/{envId}/portals/{hrid}` | GET    | Retrieve a portal by HRID. Returns the persisted navigation structure.                |
| `/organizations/{orgId}/environments/{envId}/portals/{hrid}` | DELETE | Delete a portal by HRID. Returns HTTP 204.                                            |

### Portal listing endpoints

These endpoints require the `ENVIRONMENT_PORTAL` permission.

| Endpoint                                                                           | Method | Description                                           |
| ---------------------------------------------------------------------------------- | ------ | ----------------------------------------------------- |
| `/organizations/{orgId}/environments/{envId}/portals/{portalHrid}/listings`        | PUT    | Create or update a portal listing. Supports `dryRun`. |
| `/organizations/{orgId}/environments/{envId}/portals/{portalHrid}/listings/{hrid}` | GET    | Retrieve a portal listing by HRID.                    |
| `/organizations/{orgId}/environments/{envId}/portals/{portalHrid}/listings/{hrid}` | DELETE | Delete a portal listing by HRID. Returns HTTP 204.    |

### Portal documentation endpoints

These endpoints require the `ENVIRONMENT_PORTAL` permission.

| Endpoint                                                                                    | Method | Description                                               |
| ------------------------------------------------------------------------------------------- | ------ | --------------------------------------------------------- |
| `/organizations/{orgId}/environments/{envId}/portals/{portalHrid}/documentations`           | PUT    | Create or update portal documentation. Supports `dryRun`. |
| `/organizations/{orgId}/environments/{envId}/portals/{portalHrid}/documentations/{docHrid}` | GET    | Retrieve portal documentation by HRID.                    |
| `/organizations/{orgId}/environments/{envId}/portals/{portalHrid}/documentations/{docHrid}` | DELETE | Delete portal documentation by HRID. Returns HTTP 204.    |

### Portal link endpoints

These endpoints require the `ENVIRONMENT_PORTAL` permission.

| Endpoint                                                                        | Method | Description                                        |
| ------------------------------------------------------------------------------- | ------ | -------------------------------------------------- |
| `/organizations/{orgId}/environments/{envId}/portals/{portalHrid}/links`        | PUT    | Create or update a portal link. Supports `dryRun`. |
| `/organizations/{orgId}/environments/{envId}/portals/{portalHrid}/links/{hrid}` | GET    | Retrieve a portal link by HRID.                    |
| `/organizations/{orgId}/environments/{envId}/portals/{portalHrid}/links/{hrid}` | DELETE | Delete a portal link by HRID. Returns HTTP 204.    |

### Theme endpoints

These endpoints require the `ENVIRONMENT_THEME` permission.

| Endpoint                                                           | Method | Description                                                                                  |
| ------------------------------------------------------------------ | ------ | -------------------------------------------------------------------------------------------- |
| `/organizations/{orgId}/environments/{envId}/portal-themes`        | PUT    | Create or update a theme. Supports `dryRun`.                                                 |
| `/organizations/{orgId}/environments/{envId}/portal-themes/{hrid}` | GET    | Retrieve a theme by HRID.                                                                    |
| `/organizations/{orgId}/environments/{envId}/portal-themes/{hrid}` | DELETE | Delete a theme by HRID. Returns HTTP 204, or HTTP 400 while a portal uses the theme.         |

### API documentation endpoints

These endpoints require the `API_DOCUMENTATION` permission.

| Endpoint                                                                              | Method | Description                                                   |
| ------------------------------------------------------------------------------------- | ------ | ------------------------------------------------------------- |
| `/organizations/{orgId}/environments/{envId}/apis/{apiHrid}/documentations`           | PUT    | Create or update API-scoped documentation. Supports `dryRun`. |
| `/organizations/{orgId}/environments/{envId}/apis/{apiHrid}/documentations/{docHrid}` | GET    | Retrieve API-scoped documentation by HRID.                    |
| `/organizations/{orgId}/environments/{envId}/apis/{apiHrid}/documentations/{docHrid}` | DELETE | Delete API-scoped documentation by HRID. Returns HTTP 204.    |

### API link endpoints

These endpoints require the `API_DOCUMENTATION` permission.

| Endpoint                                                                    | Method | Description                                     |
| --------------------------------------------------------------------------- | ------ | ----------------------------------------------- |
| `/organizations/{orgId}/environments/{envId}/apis/{apiHrid}/links`          | PUT    | Create or update an API link. Supports `dryRun`. |
| `/organizations/{orgId}/environments/{envId}/apis/{apiHrid}/links/{hrid}`   | GET    | Retrieve an API link by HRID.                   |
| `/organizations/{orgId}/environments/{envId}/apis/{apiHrid}/links/{hrid}`   | DELETE | Delete an API link by HRID. Returns HTTP 204.   |
