# Publishing APIs with Portal Listings

## Publishing APIs

### Creating a Portal Listing

To publish APIs to a portal, send a PUT request to `/organizations/{orgId}/environments/{envId}/portals/{portalHrid}/listings` with a `PortalListingSpec` payload. The request body must include an `hrid` and an `apis` array. Each entry in the `apis` array specifies:

* `apiHrid`: The API's human-readable identifier
* `location`: The path in the portal's navigation where the API should appear
* `order` (optional): Display sequence relative to sibling APIs at the same location

The `location` must match a path defined in the portal's `navigation` for the API to be visible. If the location does not exist, the API entry is created but remains invisible until the portal's navigation is updated to include the path. When multiple listings place APIs at the same location, the `order` field disambiguates their display order.

On PUT, the listing specification is persisted and synchronized into the live navigation tree. The platform creates or updates `PortalNavigationApi` rows at deterministic IDs under the resolved parent folder, removes APIs dropped from the listing, and reconciles the API's internal documentation folder tree from the API's `portalNavigation` field. API documentation pages are backfilled under the published API entries.

**Example Request:**

```http
PUT /organizations/org-1/environments/env-1/portals/default-portal/listings
Content-Type: application/json

{
  "hrid": "alpha-apis",
  "apis": [
    { "apiHrid": "pets-api", "location": "/projects/alpha", "order": 1 },
    { "apiHrid": "orders-api", "location": "/projects/alpha", "order": 2 }
  ]
}
```

**Response:**

```json
{
  "hrid": "alpha-apis",
  "apis": [
    { "apiHrid": "pets-api", "location": "/projects/alpha", "order": 1 },
    { "apiHrid": "orders-api", "location": "/projects/alpha", "order": 2 }
  ],
  "id": "e5f6g7h8-...",
  "portalHrid": "default-portal",
  "organizationId": "org-1",
  "environmentId": "env-1"
}
```

To retrieve a listing's current state, send a GET request to `/organizations/{orgId}/environments/{envId}/portals/{portalHrid}/listings/{hrid}`.

To delete a listing, send a DELETE request to `/organizations/{orgId}/environments/{envId}/portals/{portalHrid}/listings/{hrid}`. The operation dematerializes all API navigation entries owned by the listing.

### Kubernetes CRD

For Kubernetes deployments, use the `PortalListing` custom resource:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: PortalListing
metadata:
  name: alpha-apis
spec:
  portalRef:
    name: default-portal
  apis:
    - ref:
        name: pets-api
      location: /projects/alpha
      order: 1
    - ref:
        name: orders-api
      location: /projects/alpha
      order: 2
```

The `portalRef` field is required and immutable after creation. All listed APIs must be of kind `ApiV4Definition`. All APIs must have a management context (`spec.contextRef`) and must share the same management context as the portal.

### Configuring API Internal Documentation

To define an API's internal documentation folder tree, include a `portalNavigation` array in the API definition. This field uses the same `NavigationPath` structure as the portal's top-level navigation. The API's documentation folders are materialized under every published instance of the API.

**Example API Definition Extension:**

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiV4Definition
metadata:
  name: pets-api
spec:
  # ... existing API fields
  portalNavigation:
    - path: /getting-started
      displayName: Getting Started
      order: 1
    - path: /getting-started/quickstart
    - path: /reference
```

The `portalNavigation` field is persisted on the API record and included in Automation API GET/PUT round-trips. It is not propagated to the gateway definition — it is portal-only metadata. When a Portal Listing publishes the API, the platform reconciles the declared folder hierarchy under each `PortalNavigationApi` row.
