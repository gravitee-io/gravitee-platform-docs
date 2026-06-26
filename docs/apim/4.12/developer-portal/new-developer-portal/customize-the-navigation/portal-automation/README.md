# Portal automation

## Overview

The Next-Gen Developer Portal supports CI/CD-driven setup of portal structure, published APIs, and documentation through the Automation API. You declare portal configuration, navigation hierarchies, API listings, and documentation pages declaratively with Gravitee Kubernetes Operator (GKO) custom resources or the Terraform provider, and APIM reconciles the desired state into the live portal navigation tree.

The Automation API supports Gravitee Markdown, OpenAPI, and AsyncAPI documentation types. External link navigation items remain a Console concern.

## Automation API access

The Automation API is served at the `/automation` base path on your Management API host. All endpoints in this section use this base path.

| Property | Value |
|:---------|:------|
| Base URL | `https://<your-gravitee-mapi-host>/automation` |
| Authentication | Bearer token (Personal Access Token or Cloud Token) in the `Authorization` header |
| Content type | `application/json` |

For example, the full URL for portal operations is `https://<your-gravitee-mapi-host>/automation/organizations/{orgId}/environments/{envId}/portals`.

For Terraform provider setup, see the [quick start guide](../../../../terraform/quick-start-guide.md). For Kubernetes, see the [GKO quickstart](https://documentation.gravitee.io/gravitee-kubernetes-operator-gko/getting-started/quickstart-guide).

## Concepts

The following concepts describe how the Automation API models a portal and its content.

### Portal instance

A portal is a Next-Gen Developer Portal bound to an environment. Each portal has a human-readable ID (HRID) that you provide, a display name, and a top-level navigation hierarchy. In APIM 4.12, only one portal instance can be created per environment. Use the HRID `default-portal` for all portal operations. The portal is created on the first successful `PUT` request.

{% hint style="info" %}
Multi-portal support (multiple portal instances per environment) is planned for a future release. In 4.12, all portal, listing, and documentation requests must target the HRID `default-portal`. Requests targeting any other HRID are rejected with HTTP 400.
{% endhint %}

The portal's navigation is declared as a flat list of slash-separated paths. Intermediate folders are created implicitly when they are not listed explicitly. The persisted navigation array is returned exactly as written on `GET`.

### Navigation paths

Navigation paths define the portal's folder hierarchy using slash-separated strings, such as `/projects/alpha` or `/projects/alpha/docs`. Each path optionally includes a display name and an order. The sequence in the declaration list is preserved. Navigation sync operates only on the top navigation bar. Other areas, such as the homepage, are untouched.

| Property | Description | Example |
|----------|-------------|---------|
| `path` | Slash-separated navigation hierarchy. Required, and starts with `/`. | `/projects/alpha` |
| `displayName` | Human-friendly label for the node. Optional. | `Alpha` |
| `order` | Display order relative to siblings at the same level. Optional integer. | `1` |

### Portal listing

A portal listing publishes one or more APIs to specific locations in the portal navigation. Each API entry specifies the API's HRID, the navigation path where it appears, and an optional order. Within a single listing, multiple APIs can share the same location, with the `order` field controlling the display sequence. Across listings, validation rejects two different listings that place different APIs at the same location segment.

| Property | Description | Example |
|:---------|:------------|:--------|
| `apiHrid` | Human-readable ID of the API to publish. Required. | `pets-api` |
| `location` | Path in the portal's navigation where the API appears. Required, and matches a declared portal path. | `/projects/alpha` |
| `order` | Display order relative to siblings at the same location. Optional integer. | `1` |

### Documentation pages

Documentation pages attach to either a portal (platform-level guides) or an API (API-specific documentation). Each page has a type (Gravitee Markdown, OpenAPI, or AsyncAPI), content, and a location in the navigation hierarchy. Portal-scoped documentation appears at the specified location in the portal's top-level navigation. API-scoped documentation appears under every published instance of the API, relative to the API's internal documentation folder tree.

| Property | Description | Example |
|:---------|:------------|:--------|
| `hrid` | Human-readable ID of the documentation page. Required. | `getting-started` |
| `name` | Display name of the page. Required. | `Getting Started` |
| `type` | Documentation type. Required: `GRAVITEE_MARKDOWN`, `OPENAPI`, or `ASYNCAPI`. | `GRAVITEE_MARKDOWN` |
| `content` | Content of the documentation page. Required. | `# Getting Started\nWelcome...` |
| `location` | Path in the navigation hierarchy where the page appears. When omitted, the page is placed at the root of the portal or API navigation tree. | `/projects/alpha/docs` |
| `order` | Display order relative to siblings at the same location. Optional integer. | `1` |

### API internal documentation tree

Each API declares its own internal documentation folder hierarchy using the `portalNavigation` field, which uses the same navigation path structure as the portal's top-level navigation. When an API is published through a portal listing, the API's internal folder tree is materialized under each published API entry, and API-scoped documentation pages are placed relative to this tree.

The `portalNavigation` field is portal-only metadata. It is not propagated to the gateway definition, has no effect on the classic portal, and does not apply to v2 APIs.

## Prerequisites

* A Gravitee APIM 4.12+ environment, with its organization and environment IDs
* A bearer token (Personal Access Token or Cloud Token) for the Automation API
* The `ENVIRONMENT_PORTAL` permission for portal, portal listing, and portal documentation operations
* The `API_DOCUMENTATION` permission for API-scoped documentation operations
* For Kubernetes deployments: Gravitee Kubernetes Operator installed

{% hint style="info" %}
Resources can reference each other before all dependencies exist. Documentation pages and portal listings tolerate missing navigation paths, API HRIDs, and parent portals. Orphan entries reconnect when the referenced resource is created, so apply order does not matter.
{% endhint %}

## Multi-portal support

In APIM 4.12, each environment supports a single portal instance. Full multi-portal support (multiple independent portals per environment with separate navigation trees) is planned for a future release.

The `allowMultiplePortalPerEnv` setting controls whether the Automation API accepts portal HRIDs other than `default-portal`. When set to `true`, multiple portal records can be created, but navigation tree materialization (folder sync, listing materialization, and documentation materialization) still runs only for the environment's first-created portal. Setting this flag is primarily useful for forward-compatibility testing.

| Property | Description | Default |
|:---------|:------------|:--------|
| `automation.portal.allowMultiplePortalPerEnv` | When `false`, only `default-portal` is accepted as the HRID. Requests targeting a different HRID are rejected with HTTP 400 and the message `{fieldName} does not match the established portal for this environment`. When `true`, multiple portal records are allowed, but navigation tree materialization runs only for the first-created portal. | `false` |

Configure it in `gravitee.yml`:

```yaml
automation:
  portal:
    allowMultiplePortalPerEnv: false
```

For Kubernetes deployments, set it in the APIM Helm chart values:

```yaml
api:
  automation:
    portal:
      allowMultiplePortalPerEnv: false
```

## Create a portal

### Using the Automation API

Create or update a portal by sending a `PUT` request to `/organizations/{orgId}/environments/{envId}/portals` with the portal specification. The request body includes the portal's HRID, display name, and navigation hierarchy. The `dryRun` query parameter validates the request without persisting changes.

**Request:**

{% code overflow="wrap" %}
```http
PUT /organizations/{orgId}/environments/{envId}/portals?dryRun=false
Content-Type: application/json
Authorization: Bearer {token}

{
  "hrid": "default-portal",
  "name": "Default Portal",
  "navigation": [
    {
      "path": "/projects/alpha",
      "displayName": "Alpha",
      "order": 1
    },
    {
      "path": "/projects/alpha/docs"
    },
    {
      "path": "/projects/beta"
    }
  ]
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
  "navigation": [
    {
      "path": "/projects/alpha",
      "displayName": "Alpha",
      "order": 1
    },
    {
      "path": "/projects/alpha/docs"
    },
    {
      "path": "/projects/beta"
    }
  ],
  "errors": {
    "severe": [],
    "warning": []
  }
}
```

Retrieve a portal by sending a `GET` request to `/organizations/{orgId}/environments/{envId}/portals/{hrid}`. The response returns the persisted navigation array exactly as written. Delete a portal by sending a `DELETE` request to the same path, which returns HTTP 204 on success.

### Using Kubernetes CRDs

1. Create a `ManagementContext` resource that references your APIM instance, if one is not already configured.
2. Define a `Portal` resource with the HRID, display name, and navigation paths.
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
  navigation:
    - path: /projects/alpha
      displayName: Alpha
      order: 1
    - path: /projects/alpha/docs
    - path: /projects/beta
```

The GKO controller reconciles the desired state by calling the Automation API. Admission webhooks validate the resource before apply using the `dryRun` endpoint. The management context must resolve, and the navigation paths must pass validation: paths start with `/`, do not contain `//` or `..`, and do not end with `/` unless the path is root.

### Navigation path normalization

Navigation paths are normalized during processing:

| Input | Normalized output | Notes |
|:------|:------------------|:------|
| `/a/b/` | `/a/b` | Trailing slash stripped, except for root |
| `/Docs/Getting Started` | `/docs/getting-started` | Segments are lowercased, and non-alphanumeric characters are replaced with hyphens |
| `/a` | `/a` | Single segment accepted |

When you provide a path such as `/a/b/c` and do not list `/a` and `/a/b` explicitly, the intermediate ancestor folders are created implicitly.

### Automation and Console coexistence

When you remove a path from the navigation list, folder sync removes only folders that appeared in the previously persisted navigation list. Folders created through the Console that were not in the previous automation list are preserved. When an automation-managed folder is deleted, its child folders, pages, links, and API entries are deleted as well, but only within the scope of items that automation previously created.

## Verification

To verify a portal is configured as expected:

1. Send a `GET` request to `/organizations/{orgId}/environments/{envId}/portals/{hrid}`.
2. Confirm the response returns the portal with the navigation array you declared.
3. Open the Next-Gen Developer Portal and confirm the navigation hierarchy and published APIs appear at the declared locations.

## Automation API endpoint reference

The following endpoints belong to the Automation API, served at the `/automation` base path. The `dryRun` query parameter validates the request and returns validation errors without persisting changes. Validation errors are returned in the response body under the `errors` field, categorized as `severe` (blocking) or `warning` (informational).

### Portal endpoints

These endpoints require the `ENVIRONMENT_PORTAL` permission.

| Endpoint | Method | Description |
|:---------|:-------|:------------|
| `/organizations/{orgId}/environments/{envId}/portals` | PUT | Create or update a portal. Supports `dryRun`. |
| `/organizations/{orgId}/environments/{envId}/portals/{hrid}` | GET | Retrieve a portal by HRID. Returns the persisted navigation array exactly as written. |
| `/organizations/{orgId}/environments/{envId}/portals/{hrid}` | DELETE | Delete a portal by HRID. Returns HTTP 204. |

### Portal listing endpoints

These endpoints require the `ENVIRONMENT_PORTAL` permission.

| Endpoint | Method | Description |
|:---------|:-------|:------------|
| `/organizations/{orgId}/environments/{envId}/portals/{portalHrid}/listings` | PUT | Create or update a portal listing. Supports `dryRun`. |
| `/organizations/{orgId}/environments/{envId}/portals/{portalHrid}/listings/{hrid}` | GET | Retrieve a portal listing by HRID. |
| `/organizations/{orgId}/environments/{envId}/portals/{portalHrid}/listings/{hrid}` | DELETE | Delete a portal listing by HRID. Returns HTTP 204. |

### Portal documentation endpoints

These endpoints require the `ENVIRONMENT_PORTAL` permission.

| Endpoint | Method | Description |
|:---------|:-------|:------------|
| `/organizations/{orgId}/environments/{envId}/portals/{portalHrid}/documentations` | PUT | Create or update portal documentation. Supports `dryRun`. |
| `/organizations/{orgId}/environments/{envId}/portals/{portalHrid}/documentations/{docHrid}` | GET | Retrieve portal documentation by HRID. |
| `/organizations/{orgId}/environments/{envId}/portals/{portalHrid}/documentations/{docHrid}` | DELETE | Delete portal documentation by HRID. Returns HTTP 204. |

### API documentation endpoints

These endpoints require the `API_DOCUMENTATION` permission.

| Endpoint | Method | Description |
|:---------|:-------|:------------|
| `/organizations/{orgId}/environments/{envId}/apis/{apiHrid}/documentations` | PUT | Create or update API-scoped documentation. Supports `dryRun`. |
| `/organizations/{orgId}/environments/{envId}/apis/{apiHrid}/documentations/{docHrid}` | GET | Retrieve API-scoped documentation by HRID. |
| `/organizations/{orgId}/environments/{envId}/apis/{apiHrid}/documentations/{docHrid}` | DELETE | Delete API-scoped documentation by HRID. Returns HTTP 204. |
