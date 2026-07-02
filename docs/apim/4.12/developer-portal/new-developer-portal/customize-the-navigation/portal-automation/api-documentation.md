# API documentation

## Create API documentation

API-scoped documentation pages provide API-specific guides and reference material. Each page attaches to an API and appears under every published instance of that API, relative to the API's internal documentation folder tree. When a listing publishes an API, its documentation pages are backfilled automatically. When a documentation page references a location that does not exist yet in the API's internal tree, the page is created as an orphan under the API navigation row and reconnects when folders appear.

{% hint style="info" %}
Only v4 APIs support API-scoped documentation. The `portalNavigation` field has no effect on the classic portal and does not apply to v2 APIs.
{% endhint %}

### Using the Automation API

1. Send a `PUT` request to `/organizations/{orgId}/environments/{envId}/apis/{apiHrid}/documentations` with the documentation specification.
2. Specify the page's HRID, display name, type, content, location (relative to the API's internal folder tree), and optional order.
3. Retrieve an API documentation page by sending a `GET` request to `/organizations/{orgId}/environments/{envId}/apis/{apiHrid}/documentations/{docHrid}`.
4. Delete an API documentation page by sending a `DELETE` request to the same path.

**Example request:**

{% code overflow="wrap" %}
```http
PUT /organizations/{orgId}/environments/{envId}/apis/pets-api/documentations?dryRun=false
Content-Type: application/json
Authorization: Bearer {token}

{
  "hrid": "api-overview",
  "name": "API Overview",
  "type": "GRAVITEE_MARKDOWN",
  "content": "# Pets API\nThis API manages pet records.",
  "location": "/docs",
  "order": 1
}
```
{% endcode %}

When `dryRun` validation fails, the response returns the errors under the `errors` field. The validation messages are:

| Field     | Constraint                                              | Validation message         |
| --------- | ------------------------------------------------------- | -------------------------- |
| `name`    | Required                                                | `name must not be blank`   |
| `type`    | Required: `GRAVITEE_MARKDOWN`, `OPENAPI`, or `ASYNCAPI` | `type must not be null`    |
| `content` | Required                                                | `content must not be null` |

These endpoints require the `API_DOCUMENTATION` permission. For the full endpoint reference, see [Automation API endpoint reference](./#automation-api-endpoint-reference).

### Using Kubernetes CRDs

1. Define a `Documentation` resource with a reference to the parent API.
2. Specify the page's name, type, content, location (relative to the API's internal folder tree), and optional order.
3. Apply the manifest with `kubectl apply -f api-documentation.yaml`.

**Example Documentation custom resource (API-scoped):**

{% code title="api-documentation.yaml" %}
```yaml
apiVersion: gravitee.io/v1alpha1
kind: Documentation
metadata:
  name: pets-api-overview
  namespace: gravitee
spec:
  name: "API Overview"
  type: GRAVITEE_MARKDOWN
  content: |
    # Pets API
    This API manages pet records.
  apiRef:
    name: pets-api
    kind: ApiV4Definition
  location: /docs
  order: 1
```
{% endcode %}

{% hint style="warning" %}
**Constraints:**

* The `apiRef` field is immutable after creation. Documentation cannot be moved to a different API.
* Documentation cannot be reassigned from a portal to an API, or from an API to a portal, after creation.
* Only v4 APIs are supported. The GKO admission webhook validates the documentation before apply.
* An API referenced by active documentation pages cannot be deleted until those pages are removed.
{% endhint %}

## Configure the API internal documentation tree

Each API declares its own internal documentation folder hierarchy using the `portalNavigation` field, which uses the same navigation path structure as the portal's top-level navigation. The `portalNavigation` field is portal-only metadata and is not propagated to the gateway definition.

### Using the Automation API

Include the `portalNavigation` field in the API specification when you create or update an API through the Automation API:

```json
{
  "hrid": "pets-api",
  "name": "Pets API",
  // ... rest of the API definition
  "portalNavigation": [
    {
      "path": "/docs",
      "displayName": "Documentation",
      "order": 1
    },
    {
      "path": "/docs/guides"
    },
    {
      "path": "/examples"
    }
  ]
}
```

### Using Kubernetes CRDs

Add the `portalNavigation` field to the `ApiV4Definition` resource:

{% code title="api-definition.yaml" %}
```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiV4Definition
metadata:
  name: pets-api
  namespace: gravitee
spec:
  name: "Pets API"
  # ... rest of the API definition
  portalNavigation:
    - path: /docs
      displayName: Documentation
      order: 1
    - path: /docs/guides
    - path: /examples
```
{% endcode %}

When the API is published through a portal listing, the internal folder tree is materialized under each published API entry, and API-scoped documentation pages are placed relative to this tree. When a documentation page references a location that does not exist yet in the API's internal tree, the page is created as an orphan and reconnects when the folder is added.
