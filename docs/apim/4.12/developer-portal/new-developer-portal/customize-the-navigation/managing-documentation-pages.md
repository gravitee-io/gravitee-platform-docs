# Managing Documentation Pages

## Managing Documentation

### Creating Portal Documentation

To create or update a portal-scoped documentation page, send a PUT request to `/organizations/{orgId}/environments/{envId}/portals/{portalHrid}/documentations` with a `DocumentationSpec` payload. The request body must include:

* `hrid` — Human-readable ID for the documentation page
* `name` — Display name of the documentation page
* `type` — One of `GRAVITEE_MARKDOWN`, `OPENAPI`, or `ASYNCAPI`
* `content` — The content of the documentation page

Optionally, include:

* `location` — Path in the portal's navigation where the page should appear
* `order` — Display sequence relative to sibling pages at the same location

On PUT, the content is stored with automation metadata (reference type, reference ID, name, location, order) and a `PortalNavigationPage` navigation item is materialized at the specified `location` under the portal's folder tree. If the location does not exist in the portal's navigation, the page is created but remains invisible until the portal's navigation is updated to include the path. When portal navigation is re-synced, existing automation-managed portal documentation is re-materialized to pick up parent folder changes.

**Example Request:**

```http
PUT /organizations/org-1/environments/env-1/portals/default-portal/documentations
Content-Type: application/json

{
  "hrid": "getting-started",
  "name": "Getting Started",
  "type": "GRAVITEE_MARKDOWN",
  "content": "# Getting Started\nWelcome to the developer portal.",
  "location": "/projects/alpha",
  "order": 1
}
```

**Response:**

```json
{
  "hrid": "getting-started",
  "name": "Getting Started",
  "type": "GRAVITEE_MARKDOWN",
  "content": "# Getting Started\nWelcome to the developer portal.",
  "location": "/projects/alpha",
  "order": 1,
  "id": "i9j0k1l2-...",
  "portalHrid": "default-portal",
  "organizationId": "org-1",
  "environmentId": "env-1"
}
```

To retrieve a documentation page's current state, send a GET request to `/organizations/{orgId}/environments/{envId}/portals/{portalHrid}/documentations/{hrid}`.

To delete a documentation page, send a DELETE request to `/organizations/{orgId}/environments/{envId}/portals/{portalHrid}/documentations/{hrid}`.

### Creating API Documentation

To create or update an API-scoped documentation page, send a PUT request to `/organizations/{orgId}/environments/{envId}/apis/{apiHrid}/documentations` with a `DocumentationSpec` payload. The schema is identical to portal documentation, but the `location` is relative to the API's internal documentation folder tree (defined by the API's `portalNavigation` field).

On PUT, the content is stored with automation metadata referencing the API, and a `PortalNavigationPage` navigation item is materialized under every `PortalNavigationApi` row for that API in the environment (wherever the API is published via Portal Listings). If the API's `portalNavigation` does not yet include the specified `location`, the page is created as an orphan under the API navigation entry and reconnects when the folder appears. When a Portal Listing later publishes the API, documentation pages are backfilled automatically.

**Example Request:**

```http
PUT /organizations/org-1/environments/env-1/apis/pets-api/documentations
Content-Type: application/json

{
  "hrid": "quickstart",
  "name": "Quickstart",
  "type": "GRAVITEE_MARKDOWN",
  "content": "# Quickstart\nGet started with the Pets API in 5 minutes.",
  "location": "/getting-started/quickstart",
  "order": 1
}
```

To retrieve an API documentation page's current state, send a GET request to `/organizations/{orgId}/environments/{envId}/apis/{apiHrid}/documentations/{hrid}`.

To delete an API documentation page, send a DELETE request to `/organizations/{orgId}/environments/{envId}/apis/{apiHrid}/documentations/{hrid}`.

### Kubernetes CRD

For Kubernetes deployments, use the `Documentation` custom resource. Exactly one of `portalRef` or `apiRef` must be set. The parent reference is immutable after creation — a documentation page cannot be reassigned from a portal to an API or vice versa. If `apiRef` is set, it must point to an `ApiV4Definition` (next-gen portal only supports V4 APIs).

**Example Portal-scoped Documentation:**

```yaml
apiVersion: gravitee.io/v1alpha1
kind: Documentation
metadata:
  name: getting-started
spec:
  name: "Getting Started"
  type: GRAVITEE_MARKDOWN
  content: |
    # Getting Started
    Welcome to the developer portal.
  portalRef:
    name: default-portal
  location: /projects/alpha
  order: 1
```

**Example API-scoped Documentation:**

```yaml
apiVersion: gravitee.io/v1alpha1
kind: Documentation
metadata:
  name: api-quickstart
spec:
  name: "Quickstart"
  type: GRAVITEE_MARKDOWN
  content: |
    # Quickstart
    Get started with the Pets API in 5 minutes.
  apiRef:
    name: pets-api
  location: /getting-started/quickstart
  order: 1
```
