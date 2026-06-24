# Portal listing management (Next-Gen Developer Portal)

## Create a portal listing

Portal listings publish APIs to specific locations in the portal navigation. Each listing specifies the portal HRID and an array of API entries with their target locations and display order. A listing tolerates references to a parent portal or to API HRIDs that do not exist yet. No validation errors are raised for missing references, and the orphan entries wait for the parent resource to apply.

### Using Kubernetes CRDs

1. Define a `PortalListing` resource with a reference to the parent portal.
2. List the APIs to publish, each with a reference to an `ApiV4Definition` resource, a location path, and an optional order.
3. Apply the manifest with `kubectl apply -f portal-listing.yaml`.

**Example PortalListing custom resource:**

```yaml
apiVersion: gravitee.io/v1alpha1
kind: PortalListing
metadata:
  name: alpha-apis
  namespace: gravitee
spec:
  portalRef:
    name: default-portal
  apis:
    - ref:
        name: pets-api
        kind: ApiV4Definition
      location: /projects/alpha
      order: 1
    - ref:
        name: orders-api
      location: /projects/alpha
      order: 2
```

The `portalRef` field is immutable after creation, so a listing cannot be moved to a different portal. All referenced APIs resolve, have a management context, and share the portal's management context. Only v4 APIs are supported, and the `kind` field defaults to `ApiV4Definition` when omitted. The GKO admission webhook validates the listing before apply and blocks deletion of portals or APIs that are referenced by active listings.

## Automation API endpoints

These endpoints require the `ENVIRONMENT_PORTAL` permission.

| Endpoint | Method | Description |
|:---------|:-------|:------------|
| `/organizations/{orgId}/environments/{envId}/portals/{portalHrid}/listings` | PUT | Create or update a portal listing. Supports the `dryRun` query parameter. |
| `/organizations/{orgId}/environments/{envId}/portals/{portalHrid}/listings/{hrid}` | GET | Retrieve a portal listing by HRID. |
| `/organizations/{orgId}/environments/{envId}/portals/{portalHrid}/listings/{hrid}` | DELETE | Delete a portal listing by HRID. Returns HTTP 204 on success. |
