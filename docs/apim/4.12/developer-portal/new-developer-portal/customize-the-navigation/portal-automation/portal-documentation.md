# Portal documentation

## Create portal documentation

Portal-scoped documentation pages provide platform-level guides and reference material. Each page attaches to a portal and appears at a specified location in the portal's navigation hierarchy.

{% hint style="info" %}
When a documentation page references a `location` that does not exist yet in the portal's navigation, the page is created as an orphan and reconnects when the folder appears. Apply order does not matter.
{% endhint %}

### Using the Automation API

1. Send a `PUT` request to `/organizations/{orgId}/environments/{envId}/portals/{portalHrid}/documentations` with the documentation specification.
2. Specify the page's HRID, display name, type (Gravitee Markdown, OpenAPI, or AsyncAPI), content, location, and optional order.
3. Retrieve a documentation page by sending a `GET` request to `/organizations/{orgId}/environments/{envId}/portals/{portalHrid}/documentations/{docHrid}`.
4. Delete a documentation page by sending a `DELETE` request to the same path.

**Example request:**

{% code overflow="wrap" %}
```http
PUT /organizations/{orgId}/environments/{envId}/portals/{portalHrid}/documentations?dryRun=false
Content-Type: application/json
Authorization: Bearer {token}

{
  "hrid": "getting-started",
  "name": "Getting Started",
  "type": "GRAVITEE_MARKDOWN",
  "content": "# Getting Started\nWelcome to the developer portal.",
  "location": "/projects/alpha",
  "order": 1
}
```
{% endcode %}

When `dryRun` validation fails, the response returns the errors under the `errors` field. The validation messages are:

| Field | Constraint | Validation message |
|:------|:-----------|:-------------------|
| `name` | Required | `name must not be blank` |
| `type` | Required: `GRAVITEE_MARKDOWN`, `OPENAPI`, or `ASYNCAPI` | `type must not be null` |
| `content` | Required | `content must not be null` |

When the portal navigation is re-synced, automation-managed portal documentation is updated to reflect parent folder changes.

For the full endpoint reference, see [Automation API endpoint reference](README.md#automation-api-endpoint-reference).

### Using Kubernetes CRDs

1. Define a `Documentation` resource with a reference to the parent portal.
2. Specify the page's name, type, content, location, and optional order.
3. Apply the manifest with `kubectl apply -f portal-documentation.yaml`.

**Example Documentation custom resource (portal-scoped):**

{% code title="portal-documentation.yaml" %}
```yaml
apiVersion: gravitee.io/v1alpha1
kind: Documentation
metadata:
  name: getting-started
  namespace: gravitee
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
{% endcode %}

{% hint style="warning" %}
**Constraints:**

* The `portalRef` field is immutable after creation. Documentation cannot be moved to a different portal.
* Documentation cannot be reassigned from a portal to an API, or from an API to a portal, after creation.
* The GKO admission webhook validates the documentation before apply.
{% endhint %}
