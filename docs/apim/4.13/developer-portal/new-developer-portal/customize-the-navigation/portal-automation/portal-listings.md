# Portal listings

## Create a portal listing

Portal listings publish APIs to specific locations in the portal navigation. Each listing specifies the portal HRID and an array of API entries with their target locations and display order.

### Using the Automation API

Send a `PUT` request to `/organizations/{orgId}/environments/{envId}/portals/{portalHrid}/listings` with the listing specification. The request body includes the listing HRID and an array of API entries.

**Example request:**

{% code overflow="wrap" %}
```http
PUT /organizations/{orgId}/environments/{envId}/portals/{portalHrid}/listings?dryRun=false
Content-Type: application/json
Authorization: Bearer {token}

{
  "hrid": "alpha-apis",
  "apis": [
    {
      "apiHrid": "pets-api",
      "location": "/projects/alpha",
      "order": 1
    },
    {
      "apiHrid": "orders-api",
      "location": "/projects/alpha",
      "order": 2
    }
  ]
}
```
{% endcode %}

Retrieve a portal listing by sending a `GET` request to `/organizations/{orgId}/environments/{envId}/portals/{portalHrid}/listings/{hrid}`. Delete a portal listing by sending a `DELETE` request to the same path, which returns HTTP 204 on success.

On `PUT`, the listing spec is persisted and synced into the live navigation tree. APIs are placed at the specified locations, and their internal documentation folder trees (declared via `portalNavigation`) are materialized under each published API entry. On `DELETE`, all navigation entries owned by the listing are removed.

For the full endpoint reference, see [Automation API endpoint reference](README.md#automation-api-endpoint-reference).

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

{% hint style="warning" %}
**Constraints:**

- The `portalRef` field is immutable after creation. A listing cannot be moved to a different portal.
- Only v4 APIs are supported. The `kind` field defaults to `ApiV4Definition` when omitted.
- The GKO admission webhook blocks deletion of portals or APIs that are referenced by active listings.
{% endhint %}

### Automation API vs GKO validation differences

The Automation API and GKO CRDs validate references differently:

- **Automation API:** A listing tolerates references to API HRIDs and portal HRIDs that do not exist yet. No validation errors are raised for missing references. Orphan entries wait for the referenced resource to be created, so apply order does not matter.
- **GKO admission webhooks:** All referenced APIs must resolve to existing `ApiV4Definition` resources in the cluster and must share the portal's management context. The webhook rejects listings that reference APIs that cannot be found.

This difference means the Automation API supports order-independent applies across multiple resources, while GKO requires APIs and portals to exist before a listing references them.