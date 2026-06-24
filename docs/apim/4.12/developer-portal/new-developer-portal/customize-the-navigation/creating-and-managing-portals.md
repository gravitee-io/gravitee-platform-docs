# Creating and Managing Portals

## Creating a Portal

To create or update a portal, send a PUT request to `/organizations/{orgId}/environments/{envId}/portals` with a `PortalSpec` payload. The request body must include an `hrid` (human-readable identifier) and `name` (display name). Optionally, include a `navigation` array to define the portal's folder hierarchy.

If a portal with the specified HRID already exists in the environment, the operation updates the existing portal. If the HRID is new, a new portal is created with a deterministic UUID derived from the organization, environment, and HRID.

The `navigation` array is a flat list of `NavigationPath` objects. Each path is a slash-separated string (e.g., `/projects/alpha/docs`). Intermediate folders are created implicitly; for example, declaring `/projects/alpha/docs` automatically creates `/projects` and `/projects/alpha` if they do not exist. To attach a custom display name or sibling order to a folder, list its path explicitly with `displayName` and/or `order` fields. Paths are processed in the order they appear in the list.

The navigation array is stored as `portalNavigation` JSON on the `portals` table, not derived on GET from the folder tree. This ensures GET returns exactly what was PUT. Sync only removes folders that appeared in the **previous** persisted navigation list, leaving console-managed folders untouched. Folders that exist in the tree but are not in the `previouslyPersisted` list are preserved (not deleted) during sync. When the desired list is empty, all TOP_NAVBAR folders are deleted.

Folder deletes from Portal PUT only affect folders previously declared in automation-managed navigation. APIs, pages, and folders created through the web console are not removed by automation sync unless they conflict on path/segment.

Cascade delete rules apply when removing folders:

* Deletes all child folders recursively
* Deletes non-folder descendants (Page, Link, Api)
* Deletes associated `PortalPageContent` for Page descendants
* Throws `IllegalStateException` if nesting exceeds `MAX_CASCADE_DEPTH = 50`

When `automation.portal.allowMultiplePortalPerEnv` is `false` and the environment already contains a portal with a different ID, the request fails with a validation error: `"hrid does not match the established portal for this environment"`. When the property is `true`, multiple portals are allowed, but only the first-created portal's navigation tree is materialized. When the portal is not the default portal for the environment, navigation sync and documentation materialization are skipped.

Include the `dryRun=true` query parameter to validate the request without persisting changes. This is used by GKO admission webhooks to reject invalid CRDs before apply.

**Example Request:**

```http
PUT /organizations/org-1/environments/env-1/portals
Content-Type: application/json

{
  "hrid": "default-portal",
  "name": "Default Portal",
  "navigation": [
    { "path": "/projects/alpha", "displayName": "Alpha", "order": 1 },
    { "path": "/projects/alpha/docs" },
    { "path": "/projects/beta" }
  ]
}
```

**Response:**

```json
{
  "hrid": "default-portal",
  "name": "Default Portal",
  "navigation": [
    { "path": "/projects/alpha", "displayName": "Alpha", "order": 1 },
    { "path": "/projects/alpha/docs" },
    { "path": "/projects/beta" }
  ],
  "id": "a1b2c3d4-...",
  "organizationId": "org-1",
  "environmentId": "env-1"
}
```

To retrieve a portal's current state, send a GET request to `/organizations/{orgId}/environments/{envId}/portals/{hrid}`. The response includes the stored `navigation` array exactly as last written (not reconstructed from the live folder tree).

To delete a portal, send a DELETE request to `/organizations/{orgId}/environments/{envId}/portals/{hrid}`. The portal cannot be deleted if any Portal Listings or Documentation resources reference it; the operation fails with an error message indicating the number of dependent resources. Portal listings and related automation data participate in environment deletion cascade handlers.

If a portal is not found, the operation throws `PortalNotFoundException` with the message format: `"Portal [ {portalId} ] not found"`.

### Kubernetes CRD

For Kubernetes deployments, use the `Portal` custom resource:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: Portal
metadata:
  name: default-portal
spec:
  contextRef:
    name: "dev-ctx"
  name: "Default Portal"
  navigation:
    - path: /projects/alpha
      displayName: Alpha
      order: 1
    - path: /projects/alpha/docs
    - path: /projects/beta
```

The `contextRef` field is required and must reference a valid management context. The GKO controller reconciles the desired state by calling the Automation API. Admission webhooks validate the CRD using the `dryRun` endpoint before apply. The portal cannot be deleted while dependent PortalListing or Documentation resources exist.

## Viewing Portal Documentation in the Console

To view portal-scoped documentation pages in the APIM Console:

1. Navigate to **APIs** in the main navigation.
2. Search for your API by name or HRID in the search field.
3. Select the API from the results list.
4. Navigate to **Documentation** in the API's left sidebar.

The Documentation section displays all pages attached to the API. If no homepage is configured, the main content area displays "No homepage set" with the message "You haven't set up a homepage yet."

Portal-scoped documentation pages are managed separately from API-scoped documentation. To view portal-level documentation in the Developer Portal, navigate to the portal's public URL and browse the navigation tree defined in the portal's `navigation` array.
